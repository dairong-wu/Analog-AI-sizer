# Analog-AI-Sizer 🚀

An automated analog circuit sizing framework integrating **AI (Bayesian Optimization)** with the **Open-Source Sky130 PDK**.

## 📖 Overview
Analog circuit sizing is traditionally a manual, iterative process. This project leverages **Machine Learning** to explore the design space and find optimal transistor dimensions ($W/L$) to meet specific performance targets (Specs).

## 📊 Result: Optimization Convergence
The AI successfully found the target current (1mA) within 15 iterations. Below is the error convergence plot:

![Convergence Curve](convergence.png)

## 🛠 Tech Stack
- **PDK:** SkyWater 130nm (Sky130) via Volare
- **Simulator:** Ngspice
- **AI Engine:** Scikit-optimize (Bayesian Optimization)
- **Environment:** Python 3.12 / WSL2 Ubuntu

## 🛤 Future Development Roadmap (Phase 2 & 3)

### 1. Multi-Objective Optimization (MOS Differential Pair)
- **Goal:** Optimize a Differential Pair to achieve target **Gain (Av)** and **Bandwidth (BW)** simultaneously.
- **AI Task:** Use weighted cost functions to balance trade-offs between speed, power, and gain.

### 2. Automated PVT Corner Analysis
- **Goal:** Ensure the design is robust across **Process**, **Voltage**, and **Temperature** variations (e.g., -40°C to 125°C).
- **Benefit:** Mimics real-world industrial reliability testing (Essential for Automotive/Industrial ICs).

### 3. Layout-Aware Optimization (Closing the Loop)
- **Goal:** Integrate with **KLayout** to include parasitic extraction (PEX) effects back into the AI loop.
- **Vision:** Achieving "Layout-Ready" sizing by predicting parasitic capacitance/resistance during the optimization phase.

## 🚀 How to Run
1. `pip install -r requirements.txt`
2. `python3 main.py`