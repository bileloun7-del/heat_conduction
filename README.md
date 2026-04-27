# Heat Transfer Simulation (Radial Conduction)

Interactive simulation of transient radial heat conduction in cylindrical systems using Python and Streamlit.

---

##  Overview

This tool models temperature evolution inside a cylindrical product (e.g., food, solid materials) subjected to heating and cooling conditions.

It solves the transient heat diffusion equation using a finite difference method and provides real-time visualization of:

- Temperature distribution (2D cross-section)
- Radial temperature profile (T = f(r))
- Center temperature evolution (critical for process validation)

---

##  Features

- Adjustable geometry (radius)
- Configurable material properties:
  - Density (ρ) [kg/m³]
  - Heat capacity (Cp) [J/kg·K]
  - Thermal conductivity (k) [W/m·K]
- Heating and cooling phases
- Real-time animation
- Scientific visualization with contour plots and isotherms

---

##  Physics Model

The simulation is based on the transient heat conduction equation in cylindrical coordinates:

∂T/∂t = α ( ∂²T/∂r² + (1/r) ∂T/∂r )

where:

α = k / (ρ · Cp)

The equation is solved numerically using an explicit finite difference scheme.

---

##  How to Run

1. Clone the repository:

```bash
https://github.com/bileloun7-del/heat_conduction