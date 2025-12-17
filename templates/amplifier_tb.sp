* AI Sizer Test - Multi-Parameter
.lib "REPLACE_PDK_PATH" tt

* 加入 nf 參數，注意 sky130 的 nf 會影響總體寬度計算
* 這裡我們定義單個 finger 的寬度為 W_total / nf
X1 d g 0 0 sky130_fd_pr__nfet_01v8 W=REPLACE_W L=REPLACE_L nf=REPLACE_NF

Vgs g 0 1.2
Vds d 0 1.8

.op
.control
run
print i(vds)
.endc
.end