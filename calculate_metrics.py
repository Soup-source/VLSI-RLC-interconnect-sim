import math

def get_metrics(R, L, C, Vdd=1.0, t_max=120e-12, steps=2000):
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
        
    v_max = max(v_vals)
    overshoot = max(0.0, ((v_max - Vdd) / Vdd) * 100.0)
    
    t10 = None
    t90 = None
    for t, v in zip(t_vals, v_vals):
        if t10 is None and v >= 0.10 * Vdd:
            t10 = t
        if t90 is None and v >= 0.90 * Vdd:
            t90 = t
            break
            
    tr_ps = (t90 - t10) * 1e12 if (t10 and t90) else None
    
    return {
        "R": R,
        "zeta": zeta,
        "V_max": round(v_max, 3),
        "overshoot": round(overshoot, 2),
        "rise_time": round(tr_ps, 2) if tr_ps else "N/A"
    }

L = 1e-9
C = 100e-15
test_cases = [50.0, 200.0, 500.0]

print(f"{'Resistance':<15} | {'Zeta (ζ)':<10} | {'V_max (V)':<10} | {'Overshoot (%)':<15} | {'Rise Time (ps)':<15}")
print("-" * 75)
for R in test_cases:
    m = get_metrics(R, L, C)
    print(f"{str(m['R']) + ' Ω':<15} | {m['zeta']:<10.3f} | {m['V_max']:<10} | {str(m['overshoot']) + '%' :<15} | {str(m['rise_time']) + ' ps':<15}")
