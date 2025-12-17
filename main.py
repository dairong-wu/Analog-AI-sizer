import simulator
import parsers
import optimizer

# --- 1. 定義你的設計目標 ---
TARGET_CURRENT = 1e-3  # 假設我們想要得到 1mA 的電流

# --- 2. 定義 AI 要解決的問題 ---
def objective_function(params):
    w_val = params[0]
    l_val = 0.15  # 固定 Length
    
    # A. 執行模擬
    raw_output = simulator.run_simulation(w_val, l_val)
    
    # B. 解析電流
    current = parsers.parse_dc_current(raw_output)
    
    if current is None:
        return 999  # 如果模擬失敗，給一個很大的懲罰值
    
    # C. 計算誤差 (AI 的目標是讓誤差趨近 0)
    error = abs(TARGET_CURRENT - current)
    
    print(f">> 嘗試 W = {w_val:.2f}um | 電流 = {current*1000:.3f}mA | 誤差 = {error*1000:.3f}mA")
    return error

# --- 3. 執行主程式 ---
if __name__ == "__main__":
    print("=== Analog Circuit Sizer 啟動 ===")
    
    best_w, final_error = optimizer.start_optimization(
        objective_function, 
        w_range=(1.0, 50.0), 
        iterations=15
    )
    
    print("\n=== 優化結果 ===")
    print(f"🎯 最佳 Width: {best_w:.3f} um")
    print(f"📉 最終誤差: {final_error*1000:.6f} mA")