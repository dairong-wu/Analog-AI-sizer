import simulator
import parsers
from skopt import gp_minimize
import matplotlib.pyplot as plt
from skopt.plots import plot_convergence

TARGET_CURRENT = 1e-3  # 1mA

def objective_function(params):
    # AI 會傳入一個陣列：[W, L, NF]
    w_val, l_val, nf_val = params
    
    # 執行模擬
    raw_output = simulator.run_simulation(w_val, l_val, nf_val)
    current = parsers.parse_dc_current(raw_output)
    
    if current is None:
        return 999
    
    error = abs(TARGET_CURRENT - current)
    
    print(f">> 嘗試 W={w_val:.2f}u, L={l_val:.2f}u, NF={int(nf_val)} | 電流={current*1000:.3f}mA | 誤差={error*1000:.3f}mA")
    return error

if __name__ == "__main__":
    print("=== Analog AI Sizer (Multi-Param) 啟動 ===")
    
    # 定義搜尋空間：
    # W: 1.0u 到 50.0u
    # L: 0.15u 到 2.0u (Sky130 最小 L 是 0.15)
    # NF: 1 到 10 (整數)
    space = [
        (1.0, 50.0),    # W
        (0.15, 2.0),    # L
        (1, 10)         # NF
    ]
    
    res = gp_minimize(
        objective_function, 
        space, 
        n_calls=30,      # 因為變數變多，建議增加迭代次數
        random_state=42
    )
    
    print("\n=== 優化結果 ===")
    print(f"🎯 最佳尺寸: W={res.x[0]:.3f}u, L={res.x[1]:.3f}u, NF={int(res.x[2])}")
    print(f"📉 最終誤差: {res.fun*1000:.6f} mA")

    # 儲存新的收斂圖
    plt.figure()
    plot_convergence(res)
    plt.savefig("convergence_multi.png")