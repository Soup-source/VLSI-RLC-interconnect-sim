import math
import matplotlib.pyplot as plt

def solve_rlc_step(R, L, C, Vdd, t_max, num_points=1000):
    omega_0 = 1.0 / math.sqrt(L * C)
    zeta = (R / 2.0) * math.sqrt(C / L)
    
    dt = t_max / num_points
    time_points = [i * dt for i in range(num_points + 1)]
    voltage_points = []
    
    for t in time_points:
        if zeta < 1.0:
            omega_d = omega_0 * math.sqrt(1.0 - zeta**2)
            decay = math.exp(-zeta * omega_0 * t)
            osc = math.cos(omega_d * t) + (zeta / math.sqrt(1.0 - zeta**2)) * math.sin(omega_d * t)
            v = Vdd * (1.0 - decay * osc)
        elif math.isclose(zeta, 1.0, rel_tol=1e-4):
            decay = math.exp(-omega_0 * t)
            v = Vdd * (1.0 - decay * (1.0 + omega_0 * t))
        else:
            s1 = -zeta * omega_0 + omega_0 * math.sqrt(zeta**2 - 1.0)
            s2 = -zeta * omega_0 - omega_0 * math.sqrt(zeta**2 - 1.0)
            v = Vdd * (1.0 - (s2 * math.exp(s1 * t) - s1 * math.exp(s2 * t)) / (s2 - s1))
            
        voltage_points.append(v)
        
    return time_points, voltage_points, zeta

# Physical Interconnect Parameters (Nanoscale regime)
L = 1e-9         # 1.0 nH
C = 100e-15      # 100 fF
Vdd = 1.0        # 1.0 V supply
t_max = 120e-12  # 120 picoseconds

# Three distinct resistance regimes
cases = [
    {"label": "Underdamped (R=50 Ω)", "R": 50.0, "color": "crimson"},
    {"label": "Critically Damped (R=200 Ω)", "R": 200.0, "color": "forestgreen"},
    {"label": "Overdamped (R=500 Ω)", "R": 500.0, "color": "royalblue"}
]

# Set up the plot
plt.figure(figsize=(9, 5), dpi=150)

for case in cases:
    t_vals, v_vals, zeta_val = solve_rlc_step(case["R"], L, C, Vdd, t_max)
    # Convert time to picoseconds (ps) for readability
    t_ps = [t * 1e12 for t in t_vals]
    plt.plot(t_ps, v_vals, label=f'{case["label"]} [ζ={zeta_val:.2f}]', color=case["color"], linewidth=2)

# Styling for academic report
plt.axhline(Vdd, color="black", linestyle="--", linewidth=1, label="Vdd Target (1.0V)")
plt.title("Transient Step Response of Nanoscale RLC Interconnect", fontsize=13, fontweight="bold")
plt.xlabel("Time (picoseconds, ps)", fontsize=11)
plt.ylabel("Voltage at Load (V)", fontsize=11)
plt.grid(True, linestyle=":", alpha=0.6)
plt.legend(loc="lower right", frameon=True)
plt.tight_layout()

# Save the plot automatically for your report and post
plt.savefig("rlc_transient_response.png", dpi=300)
plt.show()

print("Simulation finished. 'rlc_transient_response.png' saved!")