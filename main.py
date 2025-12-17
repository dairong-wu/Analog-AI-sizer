import simulator
import parsers
from skopt import gp_minimize
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg') # 強制使用非交互式後端，這就不會觸發 GUI 警告
import matplotlib.pyplot as plt
from skopt.plots import plot_convergence

GUI_CALLBACK = None

# Define Specs
TARGET_CURRENT = 1e-3  # 1mA
TARGET_GAIN = 20.0      # 20 dB 
TARGET_BW   = 100.0e6   # 100 MHz

def objective_function_sm(params):
    w_val, l_val, nf_val = params
    
    raw_output = simulator.run_simulation(w_val, l_val, nf_val)
    current = parsers.parse_dc_current(raw_output)

    if current is None:
        error = 999
        msg = f"❌ Simulation Failed for W={w_val:.2f}u"
    else:
        error = abs(TARGET_CURRENT - current)
        # 建立訊息字串
        msg = f">> Try W={w_val:.2f}u, L={l_val:.2f}u, NF={int(nf_val)} | Err={error*1000:.3f}mA"
    
    # --- 關鍵修改：同時印在 Terminal 和 GUI ---
    print(msg)  # 給 Terminal 看
    if GUI_CALLBACK:
        GUI_CALLBACK(msg)  
    # ---------------------------------------
    return error
    
    #print(f">> Try W={w_val:.2f}u, L={l_val:.2f}u, NF={int(nf_val)} | Current={current*1000:.3f}mA | Error={error*1000:.3f}mA, Error%={error/TARGET_CURRENT*100:.3f}%")
    #return error

def objective_function_dp(params):
    # 參數解包: W (um), L (um), R (kOhm)
    w_val, l_val, r_kohm = params
    
    # 將 R 轉回歐姆傳給 SPICE
    r_ohm = r_kohm * 1000 
    
    # 1. 執行模擬
    raw_output = simulator.run_diff_pair(w_val, l_val, r_ohm)
    
    # 2. 解析結果
    res = parsers.parse_ac_results(raw_output)
    gain = res['gain']
    bw = res['bw']
    
    # 如果模擬失敗 (NaN 或 None)
    if gain is None or bw is None:
        return 999.0
    
    # 3. 計算多目標 Cost (核心演算法)
    # 我們希望 Gain >= Target，BW >= Target
    # 使用相對誤差來平衡量級差異
    
    # Gain 誤差: 如果小於目標，懲罰很大；如果大於目標，獎勵 (誤差為0)
    if gain < TARGET_GAIN:
        err_gain = abs(TARGET_GAIN - gain) / TARGET_GAIN
    else:
        err_gain = 0 

    # BW 誤差: 同理
    if bw < TARGET_BW:
        err_bw = abs(TARGET_BW - bw) / TARGET_BW
    else:
        err_bw = 0
        
    # 總誤差 = Gain誤差 + BW誤差 (權重 1:1)
    total_cost = err_gain + err_bw
    
    print(f">> W={w_val:.2f}u, L={l_val:.2f}u, R={r_kohm:.2f}k | Gain={gain:.2f}dB, BW={bw/1e6:.2f}MHz | Cost={total_cost:.4f}")
    
    return total_cost

def run_single_mos_opt(target_current, callback=None):
    global TARGET_CURRENT, GUI_CALLBACK
    TARGET_CURRENT = target_current
    # 把 GUI 傳進來的函數存起來
    GUI_CALLBACK = callback
    print("=== Analog AI Sizer (Multi-Param) is ON ===")
    print(f"=== Starting Optimization (Target: {target_current*1000:.1f}mA) ===")
    # Define searching range：
    # W: 1.0u to 50.0u
    # L: 0.15u to 2.0u (min length in Sky130 is 0.15)
    # NF: 1 to 10 (int)
    space = [
        (1.0, 50.0),    # W
        (0.15, 2.0),    # L
        (1, 10)         # NF
    ]
    
    res = gp_minimize(
        objective_function_sm, 
        space, 
        n_calls=30,     
        random_state=42
    )
    
    print("\n=== Optimization Results ===")
    print(f"🎯 Final Dimension: W={res.x[0]:.3f}u, L={res.x[1]:.3f}u, NF={int(res.x[2])}")
    print(f"📉 Final Error: {res.fun*1000:.6f} mA = {res.fun/TARGET_CURRENT*100:.3f}%")

    #Plot convergence figures
    plt.figure()
    plot_convergence(res)
    plt.savefig("convergence_multi.png")

    final_msg = f"🎯 AI Found: W={res.x[0]:.3f}u, L={res.x[1]:.3f}u, NF={int(res.x[2])}, Error={res.fun*1000:.6f}mA= {res.fun/TARGET_CURRENT*100:.3f}%"
    #print(final_msg)
    if GUI_CALLBACK:
        GUI_CALLBACK(final_msg)

def run_diff_pair_opt(target_gain, target_bw):
    print("=== Differential Pair Multi-Objective Optimizer ===")
    print(f"🎯 目標: Gain >= {TARGET_GAIN}dB, BW >= {TARGET_BW/1e6}MHz")
    
    # 搜尋空間
    # W: 1u ~ 100u
    # L: 0.15u ~ 2u
    # R: 1k ~ 50k (負載電阻)
    space = [
        (1.0, 100.0), 
        (0.15, 2.0),
        (1.0, 50.0)
    ]
    
    # 開始優化
    res = gp_minimize(objective_function_dp, space, n_calls=40, random_state=42)
    
    print("\n=== 最終結果 ===")
    print(f"最佳參數: W={res.x[0]:.2f}u, L={res.x[1]:.2f}u, R={res.x[2]:.2f}kOhm")
    print(f"最小 Cost: {res.fun:.4f}")

    # 畫圖
    plt.figure()
    plot_convergence(res)
    plt.title("Multi-Objective Convergence (Gain + BW)")
    plt.savefig("convergence_diff_pair.png")

if __name__ == "__main__":
    run_single_mos_opt(1e-3)



