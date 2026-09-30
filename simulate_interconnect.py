import math
import matplotlib.pyplot as plt

def solve_rlc(R, L, C, Vdd, t_max, steps=1000):
    w0 = 1.0 / math.sqrt(L * C)
    zeta = (R / 2.0) * math.sqrt(C / L)
    
    dt = t_max / steps
    t_vals = [i * dt for i in range(steps + 1)]
    v_vals = []
    
    for t in t_vals:
        if zeta < 1.0:
            wd = w0 * math.sqrt(1.0 - zeta**2)
            decay = math.exp(-zeta * w0 * t)
            osc = math.cos(wd * t) + (zeta / math.sqrt(1.0 - zeta**2)) * math.sin(wd * t)
            v = Vdd * (1.0 - decay * osc)
        elif math.isclose(zeta, 1.0, rel_tol=1e-4):
            decay = math.exp(-w0 * t)
            v = Vdd * (1.0 - decay * (1.0 + w0 * t))
        else:
            s1 = -zeta * w0 + w0 * math.sqrt(zeta**2 - 1.0)
            s2 = -zeta * w0 - w0 * math.sqrt(zeta**2 - 1.0)
            v = Vdd * (1.0 - (s2 * math.exp(s1 * t) - s1 * math.exp(s2 * t)) / (s2 - s1))
        v_vals.append(v)
        
    return t_vals, v_vals, zeta

L = 1e-9
C = 100e-15
Vdd = 1.0
t_max = 120e-12

cases = [
    {"label": "R = 50 Ω (Underdamped)", "R": 50.0, "color": "crimson"},
    {"label": "R = 200 Ω (Critically Damped)", "R": 200.0, "color": "forestgreen"},
    {"label": "R = 500 Ω (Overdamped)", "R": 500.0, "color": "royalblue"}
]

plt.figure(figsize=(9, 5), dpi=150)

for c in cases:
    t, v, zeta = solve_rlc(c["R"], L, C, Vdd, t_max)
    t_ps = [x * 1e12 for x in t]
    plt.plot(t_ps, v, label=f"{c['label']} [ζ={zeta:.2f}]", color=c["color"], linewidth=2)

plt.axhline(Vdd, color="black", linestyle="--", linewidth=1, label="Vdd (1.0V)")
plt.title("Transient Step Response of Nanoscale RLC Interconnect", fontsize=12, fontweight="bold")
plt.xlabel("Time (ps)", fontsize=10)
plt.ylabel("Load Voltage (V)", fontsize=10)
plt.grid(True, linestyle=":", alpha=0.6)
plt.legend(loc="lower right")
plt.tight_layout()

plt.savefig("rlc_transient_response.png", dpi=300)
plt.show()
