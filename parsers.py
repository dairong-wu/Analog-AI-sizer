import re

def parse_dc_current(output_text):
    """
    從 Ngspice 的文字輸出中提取 i(vds) 的數值
    """
    # 搜尋格式如: i(vds) = -1.234567e-04
    # Regex 解釋:
    # i\(vds\)  -> 匹配字串 "i(vds)"
    # \s*=\s* -> 匹配等號，前後可以有空格
    # ([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?) -> 匹配科學符號格式的數字
    pattern = r"i\(vds\)\s*=\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)"
    
    match = re.search(pattern, output_text)
    if match:
        return abs(float(match.group(1)))
    else:
        return None

if __name__ == "__main__":
    test_text = "Doing analysis... i(vds) = -5.432100e-05  status = 0"
    result = parse_dc_current(test_text)
    print(f"測試解析結果: {result} A")