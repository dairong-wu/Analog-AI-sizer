import subprocess
import os

def run_simulation(w_val, l_val, nf_val):
    lib_path = "/home/jeffy/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/combined/sky130.lib.spice"

    if not os.path.exists(lib_path):
        return f"ERROR: Path not found {lib_path}"
    
    with open("templates/amplifier_tb.sp", "r") as f:
        content = f.read()
    
    content = content.replace("REPLACE_PDK_PATH", lib_path)
    content = content.replace("REPLACE_W", str(w_val))
    content = content.replace("REPLACE_L", str(l_val))
    content = content.replace("REPLACE_NF", str(int(nf_val))) # nf 必須是整數
    
    with open("work/run.sp", "w") as f:
        f.write(content)
    
    result = subprocess.run(["ngspice", "-b", "work/run.sp"], capture_output=True, text=True)
    return result.stdout
    
    with open("work/run.sp", "w") as f:
        f.write(content)
    
    result = subprocess.run(["ngspice", "-b", "work/run.sp"], capture_output=True, text=True)
    return result.stdout

def run_diff_pair(w_val, l_val, r_val):
    lib_path = "/home/jeffy/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/combined/sky130.lib.spice"
    # 1. 讀取新的差動對模板
    with open("templates/diff_pair_tb.sp", "r") as f:
        content = f.read()
    
    # 2. 替換參數 (包含電阻值)
    content = content.replace("REPLACE_PDK_PATH", lib_path)
    content = content.replace("REPLACE_W", str(w_val))
    content = content.replace("REPLACE_L", str(l_val))
    content = content.replace("REPLACE_R", str(r_val))
    
    # 3. 寫入並執行
    with open("work/run_diff.sp", "w") as f:
        f.write(content)
    
    result = subprocess.run(["ngspice", "-b", "work/run_diff.sp"], capture_output=True, text=True)
    return result.stdout

if __name__ == "__main__":
    print("🚀 啟動測試模擬...")
    output = run_simulation(5, 0.15)
    print(output)