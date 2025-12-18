import customtkinter as ctk
import threading
from PIL import Image
import os
import time

# 引入你的後端邏輯 (這裡假設 main.py 有對應函數，下方會教你怎麼對接)
# import main 

# 設定外觀主題
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class AnalogSizerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- 視窗設定 ---
        self.title("Analog AI Sizer - Jeffy's Portfolio")
        self.geometry("1000x700")

        # --- 佈局配置 (2欄位) ---
        # Column 0: 側邊選單 (Sidebar)
        # Column 1: 主內容區 (Main Area)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ==============================
        # 1. 側邊選單 (Sidebar)
        # ==============================
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Analog AI Sizer", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.pack(padx=20, pady=(20, 10))

        self.mode_label = ctk.CTkLabel(self.sidebar_frame, text="Select Circuit:", anchor="w")
        self.mode_label.pack(padx=20, pady=(10, 0), anchor="w")

        # 電路選擇按鈕 (使用 Segmented Button 看起來更現代)
        self.circuit_selector = ctk.CTkSegmentedButton(
            self.sidebar_frame,
            #values=["Single MOS", "Diff Pair", "Active Load", "Op-Amp"],
            values=["Single MOS", "Diff Pair"],
            command=self.change_circuit_mode
        )
        self.circuit_selector.pack(padx=20, pady=10)
        self.circuit_selector.set("Single MOS") # 預設選取

        # 開始按鈕
        self.run_btn = ctk.CTkButton(self.sidebar_frame, text="🚀 Start Optimization", fg_color="green", hover_color="darkgreen", command=self.start_thread)
        self.run_btn.pack(padx=20, pady=(20, 10), side="bottom")

        # ==============================
        # 2. 主內容區 (Main Area)
        # ==============================
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        # 標題
        self.title_label = ctk.CTkLabel(self.main_frame, text="Single MOSFET Optimization", font=ctk.CTkFont(size=24))
        self.title_label.pack(pady=10, anchor="w")

        # --- 動態規格輸入區 (Dynamic Input Frame) ---
        self.input_frame = ctk.CTkFrame(self.main_frame)
        self.input_frame.pack(fill="x", pady=10)
        
        # 這裡會存放動態生成的輸入框，方便之後取值
        self.entries = {} 
        
        # 初始化預設介面
        self.setup_single_mos_ui()

        # --- Log 顯示區 ---
        self.log_label = ctk.CTkLabel(self.main_frame, text="Optimization Log:", anchor="w")
        self.log_label.pack(anchor="w", pady=(10, 0))
        
        self.log_box = ctk.CTkTextbox(self.main_frame, height=150)
        self.log_box.pack(fill="x", pady=5)

        # --- 結果圖片顯示區 ---
        self.image_frame = ctk.CTkFrame(self.main_frame, height=300)
        self.image_frame.pack(fill="both", expand=True, pady=10)
        
        self.img_label = ctk.CTkLabel(self.image_frame, text="Convergence Plot will appear here...")
        self.img_label.pack(expand=True)

    # ==============================
    # 邏輯控制區
    # ==============================

    def change_circuit_mode(self, value):
        """ 當使用者切換電路模式時觸發 """
        # 1. 清空舊的輸入框
        for widget in self.input_frame.winfo_children():
            widget.destroy()
        self.entries = {} # 清空參照

        # 2. 更新標題與載入新介面
        self.title_label.configure(text=f"{value} Optimization")
        
        if value == "Single MOS":
            self.setup_single_mos_ui()
        elif value == "Diff Pair":
            self.setup_diff_pair_ui()
        #elif value == "Op-Amp":
            #self.setup_opamp_ui()
        #elif value == "Active Load": 
            #self.setup_active_load_ui()

    # --- 介面建構函數 (Builders) ---

    def setup_single_mos_ui(self):
        """ 建立 Single MOS 需要的輸入框 """
        self.add_input_field("Target Current (mA):", "1.0")
        self.add_input_field("Vds (V):", "1.8")

    def setup_diff_pair_ui(self):
        """ 建立 Diff Pair 需要的輸入框 """
        self.add_input_field("Target Gain (dB):", "20.0")
        self.add_input_field("Target Bandwidth (MHz):", "100.0")
        self.add_input_field("Load Resistance (kOhm):", "10.0")

    #def setup_active_load_ui(self):
    #    self.add_input_field("Target Gain (dB):", "40.0") # 主動負載可以挑戰更高的 Gain
    #    self.add_input_field("Target BW (MHz):", "50.0")

    #def setup_opamp_ui(self):
    #    """ 建立 Op-Amp 需要的輸入框 """
    #    self.add_input_field("Open Loop Gain (dB):", "60.0")
    #    self.add_input_field("Phase Margin (deg):", "60.0")
    #    self.add_input_field("GBW (MHz):", "50.0")
    #    ctk.CTkLabel(self.input_frame, text="⚠️ (Phase 3 Under Development)", text_color="orange").pack(pady=5, padx=10, anchor="w")

    def add_input_field(self, label_text, default_value):
        """ 輔助函數：快速產生 標籤+輸入框 """
        row = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        row.pack(fill="x", pady=5, padx=5)
        
        lbl = ctk.CTkLabel(row, text=label_text, width=150, anchor="w")
        lbl.pack(side="left")
        
        entry = ctk.CTkEntry(row, placeholder_text=default_value)
        entry.insert(0, default_value)
        entry.pack(side="left", fill="x", expand=True)
        
        # 將輸入框存入字典，Key 是標籤名稱 (去掉冒號)
        key = label_text.replace(":", "").strip()
        self.entries[key] = entry

    # --- 執行優化邏輯 ---

    def start_thread(self):
        """ 啟動多執行緒，避免介面卡死 """
        self.run_btn.configure(state="disabled", text="Running...")
        self.log_box.delete("1.0", "end")
        threading.Thread(target=self.run_optimization, daemon=True).start()

    def run_optimization(self):
        mode = self.circuit_selector.get()
        self.log(f"=== Starting {mode} Optimization ===")
        try:
            if mode == "Single MOS":
                i_target = float(self.entries["Target Current (mA)"].get()) / 1000.0
                import main
                main.run_single_mos_opt(i_target, callback=self.log_from_thread)
                self.show_image("convergence_multi.png")
                
            elif mode == "Diff Pair":
                # 確保獲取正確的欄位名稱
                gain = float(self.entries["Target Gain (dB)"].get())
                bw = float(self.entries["Target Bandwidth (MHz)"].get()) * 1e6
                
                import main
                # 呼叫已經修改好的 run_diff_pair_opt
                main.run_diff_pair_opt(gain, bw, callback=self.log_from_thread)
                self.show_image("convergence_diff_pair.png")
            elif mode == "Active Load":
                gain = float(self.entries["Target Gain (dB)"].get())
                bw = float(self.entries["Target BW (MHz)"].get()) * 1e6
                import main
                main.run_active_load_opt(gain, bw, callback=self.log_from_thread)
                self.show_image("convergence_active.png")
                
        except Exception as e:
            self.log(f"Error: {str(e)}")
            import traceback
            traceback.print_exc() 
        self.run_btn.configure(state="normal", text="🚀 Start Optimization")
    def log_from_thread(self, message):
        # 因為這是從 AI 線程呼叫的，我們用 .after 確保在主線程更新 UI
        self.after(0, lambda: self.log(message)) 
    def log(self, message):
    # 確保這裡有把文字塞進 Textbox
        self.log_box.insert("end", str(message) + "\n")
        self.log_box.see("end") # 自動捲動到最下面
        '''inputs = {}
        for key, entry in self.entries.items():
            inputs[key] = entry.get()
            self.log(f"  > Set {key} = {inputs[key]}")

        # 2. 模擬呼叫後端 (這裡你需要連接真正的 main.py)
        # 範例：模擬跑動過程
        try:
            for i in range(1, 11):
                time.sleep(0.2) # 假裝在跑 Ngspice
                self.log(f"Iteration {i}: Optimizing W/L...")
            
            self.log("✅ Optimization Finished!")
            self.log(f"🎯 Best Result: W=45.2u, L=0.15u")

            # 3. 顯示圖片 (假設後端生成了 convergence.png)
            # 在真實情況下，呼叫 main.py 後會產生圖片
            self.show_image("convergence_diff_pair.png") # 確保檔名對應

        except Exception as e:
            self.log(f"❌ Error: {str(e)}")

        self.run_btn.configure(state="normal", text="🚀 Start Optimization")'''

    def show_image(self, img_path):
        """ 載入並顯示圖片 """
        if not os.path.exists(img_path):
            self.log(f"⚠️ Image not found yet: {img_path}")
            # 可以設定一個定時器，500ms 後再試一次
            self.after(500, lambda: self.show_image(img_path))
            return
        try:
            img = Image.open(img_path)
            img.load()
            # 調整圖片大小以適應視窗
            img_ratio = img.width / img.height
            display_h = 250
            display_w = int(display_h * img_ratio)
            
            ctk_img = ctk.CTkImage(light_image=img, size=(display_w, display_h))
            self.img_label.configure(image=ctk_img, text="")
        except Exception as e:
            self.log(f"Error loading image: {e}")

if __name__ == "__main__":
    app = AnalogSizerApp()
    app.mainloop()