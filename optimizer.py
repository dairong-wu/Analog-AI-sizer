from skopt import gp_minimize

def start_optimization(objective_func, w_range=(1.0, 100.0), iterations=20):
    """
    objective_func: 我們定義的目標函數 (從 main.py 傳入)
    w_range: Width 調整範圍 (um)
    iterations: 預計跑幾次模擬
    """
    print(f"--- AI 啟動：尋找最佳尺寸 (範圍: {w_range}um) ---")
    
    # gp_minimize 會嘗試最小化 objective_func 的回傳值
    res = gp_minimize(
        objective_func,                # 目標函數
        [w_range],                     # 參數範圍
        n_calls=iterations,            # 迭代次數
        n_initial_points=5,            # 先隨機抓 5 個點開始
        random_state=42
    )
    
    return res.x[0], res.fun

if __name__ == "__main__":
    # 假裝一個目標函數來測試：假設最佳 W 是 42.5
    def mock_objective(w):
        return abs(w[0] - 42.5)
    
    best_w, min_error = start_optimization(mock_objective)
    print(f"測試完成！AI 找到的最佳 W: {best_w:.2f} (誤差: {min_error:.4f})")