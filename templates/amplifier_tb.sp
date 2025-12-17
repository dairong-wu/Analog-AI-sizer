* AI Sizer Test
.lib "REPLACE_PDK_PATH" tt

* 使用 sky130 元件
X1 d g 0 0 sky130_fd_pr__nfet_01v8 W=REPLACE_W L=REPLACE_L

Vgs g 0 1.2
Vds d 0 1.8

.op
.control
run
print i(vds)
.endc
.end