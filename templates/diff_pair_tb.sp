* AI Sizer - Differential Pair Optimization
.lib "REPLACE_PDK_PATH" tt

* --- 參數定義 (由 Python 填入) ---
.param w_pair = REPLACE_W
.param l_pair = REPLACE_L
.param r_load = REPLACE_R

* --- 電路網表 (Netlist) ---
* M1, M2: 差動輸入對 (Sky130 NMOS)
X1 out_n in_n tail 0 sky130_fd_pr__nfet_01v8 W={w_pair} L={l_pair}
X2 out_p in_p tail 0 sky130_fd_pr__nfet_01v8 W={w_pair} L={l_pair}

* R1, R2: 負載電阻 (理想電阻，簡化問題)
R1 vdd out_n {r_load}
R2 vdd out_p {r_load}

* Iss: 尾電流源 (理想電流源)
Iss tail 0 200u

* --- 電源與訊號 ---
Vdd vdd 0 1.8
* 共模電壓 0.9V，差模訊號 AC 1
Vin_p in_p 0 dc 0.9 ac 0.5
Vin_n in_n 0 dc 0.9 ac -0.5

* --- 模擬設定 ---
.op
* AC 掃描：從 10Hz 到 10GHz
.ac dec 10 10 10G

* --- 量測指令 (關鍵！) ---
* 1. 測量低頻增益 (Gain in dB)
.meas ac gain_db MAX vdb(out_n)

* 2. 測量 3dB 頻寬 (Bandwidth)
* 找 gain 下降 3dB 的頻率點
.meas ac bw_hz WHEN vdb(out_n)='gain_db-3'

.control
run
* 印出量測結果供 Python 讀取
print gain_db
print bw_hz
.endc
.end