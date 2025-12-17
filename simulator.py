import subprocess
import os

def run_simulation(w_val, l_val, nf_val):
    # 直接複製你剛剛 find 到的完整路徑
    lib_path = "/home/jeffy/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/combined/sky130.lib.spice"

    # 檢查一下，如果路徑錯了直接報警
    if not os.path.exists(lib_path):
        return f"ERROR: Path not found {lib_path}"
    
    # 2. 讀取模板
    with open("templates/amplifier_tb.sp", "r") as f:
        content = f.read()
    
    # 3. 使用 replace 替換關鍵字 (避免 format 的大括號
    content = content.replace("REPLACE_PDK_PATH", lib_path)
    content = content.replace("REPLACE_W", str(w_val))
    content = content.replace("REPLACE_L", str(l_val))
    content = content.replace("REPLACE_NF", str(int(nf_val))) # nf 必須是整數
    
    with open("work/run.sp", "w") as f:
        f.write(content)
    
    result = subprocess.run(["ngspice", "-b", "work/run.sp"], capture_output=True, text=True)
    return result.stdout
    
    # 4. 寫入執行檔
    with open("work/run.sp", "w") as f:
        f.write(content)
    
    # 5. 執行 Ngspice
    result = subprocess.run(["ngspice", "-b", "work/run.sp"], capture_output=True, text=True)
    return result.stdout

if __name__ == "__main__":
    # 測試
    print("🚀 啟動測試模擬...")
    output = run_simulation(5, 0.15)
    print(output)