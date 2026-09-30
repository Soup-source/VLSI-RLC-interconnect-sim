import math

def analyze_metrics(R, L, C, Vdd=1.0, t_max=120e-12, num_points=2000):
    omega_0 = 1.0 / math.sqrt(L * C)
    zeta = (R / 2.0) * math.sqrt(C / L)
    dt = t_max / num_points
    
    t_vals = [i * dt for i in range(num_points + 1)]
    v_vals = []
    
    for t in t_vals:
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
        v_vals.append(v)
        
    v_max = max(v_vals)
    overshoot_pct = max(0.0, ((v_max - Vdd) / Vdd) * 100.0)
    
    # Calculate 10% to 90% rise time
    t_10 = None
    t_90 = None
    for t, v in zip(t_vals, v_vals):
        if t_10 is None and v >= 0.10 * Vdd:
            t_10 = t
        if t_90 is None and v >= 0.90 * Vdd:
            t_90 = t
            break
            
    rise_time_ps = (t_90 - t_10) * 1e12 if (t_10 and t_90) else None
    
    return {
        "R": R,
        "zeta": zeta,
        "V_max (V)": round(v_max, 3),
        "Overshoot (%)": round(overshoot_pct, 2),
        "Rise Time (ps)": round(rise_time_ps, 2) if rise_time_ps else "N/A"
    }

# Run for all three regimes
L = 1e-9
C = 100e-15
regimes = [50.0, 200.0, 500.0]

print(f"{'Regime (R)':<15} | {'Zeta (ζ)':<10} | {'Max V (V)':<10} | {'Overshoot (%)':<15} | {'Rise Time (ps)':<15}")
print("-" * 75)
for R in regimes:
    m = analyze_metrics(R, L, C)
    print(f"{str(m['R']) + ' Ω':<15} | {m['zeta']:<10.3f} | {m['V_max (V)']:<10} | {str(m['Overshoot (%)']) + '%' :<15} | {str(m['Rise Time (ps)']) + ' ps':<15}")