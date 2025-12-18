import re

def parse_dc_current(output_text):
    pattern = r"i\(vds\)\s*=\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)"
    match = re.search(pattern, output_text)
    if match:
        return abs(float(match.group(1)))
    else:
        print("DEBUG: Parser 找不到電流！Ngspice 輸出片段：", output_text[-100:])
        return None

def parse_ac_results(output_text):
    results = {'gain': None, 'bw': None}
    
    # 找 max_gain (注意模板裡改名了)
    gain_match = re.search(r"max_gain\s*=\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)", output_text)
    if gain_match:
        results['gain'] = float(gain_match.group(1))
        
    # 找 bw_hz
    bw_match = re.search(r"bw_hz\s*=\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)", output_text)
    if bw_match:
        results['bw'] = float(bw_match.group(1))
        
    return results

if __name__ == "__main__":
    test_text = "Doing analysis... i(vds) = -5.432100e-05  status = 0"
    result = parse_dc_current(test_text)
    print(f"測試解析結果: {result} A")

