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
        msg = f"❌ Simulation Failed for W={w_val:.2f}u, L={l_val:.2f}u, NF={nf_val}"
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
    w_val, l_val, r_kohm = params
    r_ohm = r_kohm * 1000 
    
    raw_output = simulator.run_diff_pair(w_val, l_val, r_ohm)
    res = parsers.parse_ac_results(raw_output)
    gain = res['gain']
    bw = res['bw']
    
    if gain is None or bw is None:
        msg = f"❌  Simulation Failed for W={w_val:.2f}u, L={l_val:.2f}u, R={r_kohm}"
        print(msg)
        if GUI_CALLBACK: GUI_CALLBACK(msg)
        return 999.0
    
    # 計算 Cost (邏輯不變)
    err_gain = abs(TARGET_GAIN - gain) / TARGET_GAIN if gain < TARGET_GAIN else 0 
    err_bw = abs(TARGET_BW - bw) / TARGET_BW if bw < TARGET_BW else 0
    total_cost = err_gain + err_bw
    
    # --- 修改點：將進度廣播給 GUI ---
    msg = f">> W={w_val:.2f}u, L={l_val:.2f}u, R={r_kohm:.2f}k | Gain={gain:.2f}dB, BW={bw/1e6:.2f}MHz | Cost={total_cost:.4f}"
    print(msg)
    if GUI_CALLBACK:
        GUI_CALLBACK(msg)
    
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

def run_diff_pair_opt(target_gain, target_bw, callback=None): # 增加 callback 參數
    global TARGET_GAIN, TARGET_BW, GUI_CALLBACK
    TARGET_GAIN = target_gain
    TARGET_BW = target_bw
    GUI_CALLBACK = callback # 設定傳聲筒
    
    print("=== Differential Pair Multi-Objective Optimizer ===")
    if GUI_CALLBACK:
        GUI_CALLBACK(f"🎯 Target: Gain >= {target_gain}dB, BW >= {target_bw/1e6}MHz")
    
    space = [(1.0, 100.0), (0.15, 2.0), (1.0, 50.0)]
    
    res = gp_minimize(objective_function_dp, space, n_calls=40, random_state=42)
    
    # 畫圖
    plt.figure()
    plot_convergence(res)
    plt.title("Multi-Objective Convergence (Gain + BW)")
    plt.savefig("convergence_diff_pair.png")
    plt.close() # 記得關閉畫布節省記憶體

    final_msg = f"🎯 AI Found: W={res.x[0]:.2f}u, L={res.x[1]:.2f}u, R={res.x[2]:.2f}k, Cost={res.fun:.4f}"
    print(f"\n=== 最終結果 ===\n{final_msg}")
    if GUI_CALLBACK:
        GUI_CALLBACK(final_msg)

if __name__ == "__main__":
    run_single_mos_opt(1e-3)



