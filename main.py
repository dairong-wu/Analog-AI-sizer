import simulator
import parsers
from skopt import gp_minimize
import matplotlib.pyplot as plt
from skopt.plots import plot_convergence

TARGET_CURRENT = 1e-3  # 1mA

def objective_function(params):
    w_val, l_val, nf_val = params
    
    raw_output = simulator.run_simulation(w_val, l_val, nf_val)
    current = parsers.parse_dc_current(raw_output)
    
    if current is None:
        return 999
    
    error = abs(TARGET_CURRENT - current)
    
    print(f">> Try W={w_val:.2f}u, L={l_val:.2f}u, NF={int(nf_val)} | Current={current*1000:.3f}mA | Error={error*1000:.3f}mA, Error%={error/TARGET_CURRENT*100:.3f}%")
    return error

if __name__ == "__main__":
    print("=== Analog AI Sizer (Multi-Param) is ON ===")
    
    # Define searching range：
    # W: 1.0u to 50.0u
    # L: 0.15u to 2.0u (min length in Sky130 is 0.15)
    # NF: 1 to 10 (int)
    space = [
        (1.0, 50.0),    # W
        (0.15, 2.0),    # L
        (1, 10)         # NF
    ]
    
    res = gp_minimize(
        objective_function, 
        space, 
        n_calls=30,     
        random_state=42
    )
    
    print("\n=== Optimization Results ===")
    print(f"🎯 Final Dimension: W={res.x[0]:.3f}u, L={res.x[1]:.3f}u, NF={int(res.x[2])}")
    print(f"📉 Final Error: {res.fun*1000:.6f} mA = {res.fun/TARGET_CURRENT*100:.3f}%")

    #Plot convergence figures
    plt.figure()
    plot_convergence(res)
    plt.savefig("convergence_multi.png")