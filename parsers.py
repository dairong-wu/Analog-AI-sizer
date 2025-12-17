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
    """
    從 Ngspice 輸出中抓取 Gain (dB) 和 Bandwidth (Hz)
    """
    results = {}
    
    # 抓取 Gain (例如: gain_db = 2.050000e+01)
    gain_match = re.search(r"gain_db\s*=\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)", output_text)
    if gain_match:
        results['gain'] = float(gain_match.group(1))
    else:
        results['gain'] = None

    # 抓取 Bandwidth (例如: bw_hz = 1.000000e+08)
    bw_match = re.search(r"bw_hz\s*=\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)", output_text)
    if bw_match:
        results['bw'] = float(bw_match.group(1))
    else:
        results['bw'] = None
        
    return results

if __name__ == "__main__":
    test_text = "Doing analysis... i(vds) = -5.432100e-05  status = 0"
    result = parse_dc_current(test_text)
    print(f"測試解析結果: {result} A")

