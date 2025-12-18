* AI Sizer - Differential Pair Optimization
.lib "REPLACE_PDK_PATH" tt

.param w_pair = REPLACE_W
.param l_pair = REPLACE_L
.param r_load = REPLACE_R

* --- 電路網表 ---
X1 out_n in_n tail 0 sky130_fd_pr__nfet_01v8 W={w_pair} L={l_pair}
X2 out_p in_p tail 0 sky130_fd_pr__nfet_01v8 W={w_pair} L={l_pair}
R1 vdd out_n {r_load}
R2 vdd out_p {r_load}
Iss tail 0 200u
Vdd vdd 0 1.8
Vin_p in_p 0 dc 0.9 ac 0.5
Vin_n in_n 0 dc 0.9 ac -0.5

.control
  * 執行 AC 模擬
  ac dec 10 10 10G
  
  * 在 control 內部進行量測
  meas ac max_gain MAX vdb(out_n)
  
  * 定義目標值 (下降 3dB)
  let target_3db = max_gain - 3
  
  * 找頻寬 (從低頻往高頻找第一個交叉點)
  meas ac bw_hz WHEN vdb(out_n)=target_3db
  
  * 強制印出結果，讓 Python 的 Regex 抓得到
  echo "RESULTS_START"
  print max_gain
  print bw_hz
  echo "RESULTS_END"
.endc
.end