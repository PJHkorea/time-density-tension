### solar_system_test1.py
```text
===============================================================================================
 [ANALYSIS] PHASE 11: PRIMITIVE SOLAR & EXOPLANETARY CORE LATTICE INTEGRITY
===============================================================================================
 ※ BOUNDARY PRINCIPLE & SPECIFICATION:
   - Evaluates the Primitive Stable Lattice governing planetary distribution, intentionally excluding
     localized hydrodynamic drag and non-linear gravitational perturbations from Jovian-mass planets.
===============================================================================================
===============================================================================================
 ⏳ [INITIATING] TDT PHASE 11 STELLAR FIELD SIMULATION: SOLAR SYSTEM
 ➔ Central Stellar Mass Base Gauge: 1.0000 M_sun
===============================================================================================
 * Node 1 -> Mercury         | Obs_AU: 0.387  | Proto_Lattice_AU: 0.137  | Regime: Dynamical Shift (Err:  64.68%)
 * Node 2 -> Venus           | Obs_AU: 0.723  | Proto_Lattice_AU: 0.267  | Regime: Dynamical Shift (Err:  63.13%)
 * Node 3 -> Earth           | Obs_AU: 1.000  | Proto_Lattice_AU: 0.351  | Regime: Dynamical Shift (Err:  64.94%)
 * Node 4 -> Mars            | Obs_AU: 1.524  | Proto_Lattice_AU: 0.557  | Regime: Dynamical Shift (Err:  63.47%)
 * Node 5 -> Jupiter         | Obs_AU: 5.203  | Proto_Lattice_AU: 0.855  | Regime: Dynamical Shift (Err:  83.56%)
 * Node 6 -> Saturn          | Obs_AU: 9.582  | Proto_Lattice_AU: 1.489  | Regime: Dynamical Shift (Err:  84.46%)
-----------------------------------------------------------------------------------------------
 ➔ Solar System Mean Absolute Error (Conformal MAE): 70.7070%
   [NOTE] Significant residual at Node 4 (Mars) characterizes the unmitigated traces of
          Planetary Migration (Grand Tack) and Jovian-mass perturbations omitted in this baseline.
===============================================================================================
===============================================================================================
 ⏳ [INITIATING] TDT PHASE 11 STELLAR FIELD SIMULATION: KEPLER-11 SYSTEM
 ➔ Central Stellar Mass Base Gauge: 0.9500 M_sun
===============================================================================================
 * Node 1 -> Kepler-11b      | Obs_AU: 0.091  | Proto_Lattice_AU: 0.089  | Regime: Stable Bound (Err:   1.88%)
 * Node 2 -> Kepler-11d      | Obs_AU: 0.155  | Proto_Lattice_AU: 0.172  | Regime: Stable Bound (Err:  11.21%)
 * Node 3 -> Kepler-11e      | Obs_AU: 0.195  | Proto_Lattice_AU: 0.226  | Regime: Dynamical Shift (Err:  15.68%)
 * Node 4 -> Kepler-11g      | Obs_AU: 0.466  | Proto_Lattice_AU: 0.354  | Regime: Dynamical Shift (Err:  23.97%)
-----------------------------------------------------------------------------------------------
 ➔ Kepler-11 System Mean Absolute Error (Conformal MAE): 13.1863%
===============================================================================================
===============================================================================================
 ⏳ [INITIATING] TDT PHASE 11 STELLAR FIELD SIMULATION: TRAPPIST-1 SYSTEM
 ➔ Central Stellar Mass Base Gauge: 0.0900 M_sun
===============================================================================================
 * Node 1 -> TRAPPIST-1b     | Obs_AU: 0.011  | Proto_Lattice_AU: 0.011  | Regime: Asymptotic Lock (Err:   0.00%)
 * Node 2 -> TRAPPIST-1d     | Obs_AU: 0.022  | Proto_Lattice_AU: 0.018  | Regime: Dynamical Shift (Err:  19.42%)
 * Node 3 -> TRAPPIST-1g     | Obs_AU: 0.047  | Proto_Lattice_AU: 0.022  | Regime: Dynamical Shift (Err:  52.20%)
 * Node 4 -> TRAPPIST-1h     | Obs_AU: 0.062  | Proto_Lattice_AU: 0.031  | Regime: Dynamical Shift (Err:  49.62%)
-----------------------------------------------------------------------------------------------
 ➔ TRAPPIST-1 System Mean Absolute Error (Conformal MAE): 30.3082%
   [NOTE] Macro Discrepancy detects ongoing uncompensated resonant chain migration torque fields.
===============================================================================================
===============================================================================================
 ⏳ [INITIATING] TDT PHASE 11 STELLAR FIELD SIMULATION: HD 10180 SYSTEM
 ➔ Central Stellar Mass Base Gauge: 1.0600 M_sun
===============================================================================================
 * Node 1 -> HD 10180b       | Obs_AU: 0.022  | Proto_Lattice_AU: 0.021  | Regime: Stable Bound (Err:   6.04%)
 * Node 2 -> HD 10180c       | Obs_AU: 0.060  | Proto_Lattice_AU: 0.041  | Regime: Dynamical Shift (Err:  32.01%)
 * Node 3 -> HD 10180d       | Obs_AU: 0.135  | Proto_Lattice_AU: 0.054  | Regime: Dynamical Shift (Err:  60.01%)
 * Node 4 -> HD 10180e       | Obs_AU: 0.270  | Proto_Lattice_AU: 0.087  | Regime: Dynamical Shift (Err:  67.80%)
-----------------------------------------------------------------------------------------------
 ➔ HD 10180 System Mean Absolute Error (Conformal MAE): 41.4649%
===============================================================================================

 [TERMINAL COHERENCE EVALUATION] INTEGRATED MULTI-STELLAR REGIME MATRIX
===============================================================================================
 * Asymptotic Multi-System Mean Error (MAE) : 42.4489%
 * Structural Boundary Configuration Status : FREE FIELD MATRIX INTEGRITY ASSESSED
   - Analytical models evaluate the unperturbed primitive stable lattice under zero-tuning bounds.
   - Residual discrepancies in local stellar systems (e.g., Solar System Node 4) are strictly
     parameterized as uncompensated dynamical drift from localized gravitational perturbations.
===============================================================================================
```

### solar_dynamic_test2.py
```text
[SYSTEM] Generating Primitive Solar Conformal Core Lattice...
[SYSTEM] Injecting Jovian Gas Scooping & Orbital Inversion Cascade Field...
[SYSTEM] Initiating Terminal Diagnostics & Coherence Matrix Evaluation...

===============================================================================================
 [ANALYSIS] PHASE 12: SOLAR SYSTEM GAS-DRIVEN ACCRETION & DOMINO SCATTERING
===============================================================================================
 ※ BOUNDARY PRINCIPLE & SPECIFICATION:
   - Evaluates the dynamically evolved lattice incorporating Jovian-mass accretion,
     gas starvation filters, and Nice-model equivalent gravitational scattering cascades.
===============================================================================================
 ⏳ [DIAGNOSTIC] TDT PHASE 12 STELLAR FIELD COHERENCE REPORT: SOLAR SYSTEM
 ➔ Central Stellar Mass Base Gauge: 1.0250 M_sun
===============================================================================================
 * Node 1 -> Mercury         | Obs_AU: 0.387  | Sim_AU: 0.397  | Proto_AU: 0.137  | Regime: Stable Bound    (Err:   2.66%)
 * Node 2 -> Venus           | Obs_AU: 0.723  | Sim_AU: 0.730  | Proto_AU: 0.267  | Regime: Asymptotic Lock (Err:   1.02%)
 * Node 3 -> Earth           | Obs_AU: 1.000  | Sim_AU: 1.003  | Proto_AU: 0.351  | Regime: Asymptotic Lock (Err:   0.31%)
 * Node 4 -> Mars            | Obs_AU: 1.524  | Sim_AU: 1.570  | Proto_AU: 0.557  | Regime: Stable Bound    (Err:   2.99%)
 * Node 5 -> Jupiter         | Obs_AU: 5.203  | Sim_AU: 5.055  | Proto_AU: 0.855  | Regime: Stable Bound    (Err:   2.84%)
 * Node 6 -> Saturn          | Obs_AU: 9.582  | Sim_AU: 10.277  | Proto_AU: 1.489  | Regime: Stable Bound    (Err:   7.25%)
 * Node 7 -> Uranus          | Obs_AU: 19.218  | Sim_AU: 20.532  | Proto_AU: 2.150  | Regime: Stable Bound    (Err:   6.84%)
 * Node 8 -> Neptune         | Obs_AU: 30.070  | Sim_AU: 33.012  | Proto_AU: 2.850  | Regime: Stable Bound    (Err:   9.78%)
-----------------------------------------------------------------------------------------------
 ➔ Solar System Mean Absolute Error (Conformal MAE): 4.2121%
   [NOTE] Mathematical inversion successfully captured the outermost 30 AU boundary allocation for Neptune.
===============================================================================================
 [TERMINAL COHERENCE EVALUATION] INTEGRATED MULTI-STELLAR REGIME MATRIX
===============================================================================================
 * Post-Migration Multi-System Accuracy Indicator : 95.7879%
 * Structural Boundary Configuration Status : DYNAMIC FIELD INTEGRITY ASSESSED
   - Coherence Matrix Verified: High-fidelity convergence achieved under unified physical laws.
===============================================================================================
```
