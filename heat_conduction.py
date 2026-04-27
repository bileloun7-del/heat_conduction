import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(page_title="Heat Conduction", layout="wide")
st.title("Radial Heat Conduction")


# INPUTS


st.sidebar.markdown("Material Properties")

rho = st.sidebar.number_input("Density ρ (kg/m³)", value=1100.0)
Cp  = st.sidebar.number_input("Heat capacity Cp (J/kg·K)", value=3530.0)
k   = st.sidebar.number_input("Conductivity k (W/m·K)", value=0.412)



col1, col2, col3 = st.columns(3)

with col1:
    R = st.slider("Radius (m)", 0.01, 0.1, 0.056)

with col2:
    T_wall = st.slider("Wall Temperature (°C)", 50.0, 200.0, 143.0)

with col3:
    time_min = st.slider("Simulation Time (min)", 1, 95, 10)


# PARAMETERS

nr = 60
dr = R / (nr - 1)
alpha = k / (rho * Cp)

dt = 0.25 * dr**2 / alpha
tt = time_min * 60
nt = int(tt / dt)

r = np.linspace(0, R, nr)
T = np.ones(nr) * 15

# store snapshots
T_history = []
time_history = []


# SOLVER

for n in range(nt):
    T_new = T.copy()

    for j in range(1, nr - 1):
        d2T = (T[j+1] - 2*T[j] + T[j-1]) / dr**2
        dT = (T[j+1] - T[j-1]) / (2*dr)

        if r[j] != 0:
            radial = d2T + (1 / r[j]) * dT
        else:
            radial = d2T

        T_new[j] = T[j] + alpha * dt * radial

    T_new[-1] = T_wall
    T_new[0] = T_new[1]

    T = T_new.copy()

    # store frames
    if n % 15 == 0:
        T_history.append(T.copy())
        time_history.append(n * dt)


# 2D GRID

r_full = np.concatenate((-r[::-1], r))
X, Y = np.meshgrid(r_full, r_full)
R_disk = np.sqrt(X**2 + Y**2)



#  ANIMATION CONTROLS



start = st.button("▶ Start Animation")

placeholder = st.empty()


# ANIMATION LOOP

if start:
    for i in range(len(T_history)):

        T_current = T_history[i]
        t_current = time_history[i]

        # 2D field
        T_disk = np.interp(R_disk, r, T_current)
        T_disk[R_disk > R] = np.nan

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

        # 1D plot
        ax1.plot(r, T_current, linewidth=2)
        ax1.set_ylim(15, T_wall)
        ax1.set_xlabel("r (m)")
        ax1.set_ylabel("T (°C)")
        ax1.set_title("T = f(r)")
        ax1.grid()

        # 2D plot
        c = ax2.contourf(X, Y, T_disk, levels=100)
        ax2.set_aspect('equal')
        ax2.set_title("Cross-section")
        fig.colorbar(c, ax=ax2)

        # TIME DISPLAY
        time_str = time.strftime('%H:%M:%S', time.gmtime(t_current))

        T_center = T_current[0]

        fig.suptitle(f"Time = {time_str}       Center Temperature = {T_center:.2f} °C", fontsize=14)

        placeholder.pyplot(fig)
        plt.close(fig)
        time.sleep(0.05)
