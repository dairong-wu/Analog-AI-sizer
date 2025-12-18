* AI Sizer - Active Load Differential Pair
.lib "REPLACE_PDK_PATH" tt

.param wn = REPLACE_WN
.param ln = REPLACE_LN
.param wp = REPLACE_WP
.param lp = REPLACE_LP

* --- 電路網表 (Active Load Diff Pair) ---
* PMOS Current Mirror Load
X3 out_p out_p vdd vdd sky130_fd_pr__pfet_01v8 W={wp} L={lp}
X4 out_n out_p vdd vdd sky130_fd_pr__pfet_01v8 W={wp} L={lp}

* NMOS Input Pair
X1 out_p in_p tail 0 sky130_fd_pr__nfet_01v8 W={wn} L={ln}
X2 out_n in_n tail 0 sky130_fd_pr__nfet_01v8 W={wn} L={ln}

* Iss & Power
Iss tail 0 200u
Vdd vdd 0 1.8
Vin_p in_p 0 dc 0.9 ac 0.5
Vin_n in_n 0 dc 0.9 ac -0.5

.control
  op
  ac dec 10 10 10G
  
  * 印出 DC 工作點供 Python 檢查
  print v(out_n)
  
  meas ac max_gain MAX vdb(out_n)
  let target_3db = max_gain - 3
  meas ac bw_hz WHEN vdb(out_n)=target_3db
  
  echo "RESULTS_START"
  print max_gain
  print bw_hz
  echo "RESULTS_END"
.endc
.end