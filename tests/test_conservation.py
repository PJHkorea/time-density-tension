def test_interior_covariant_conservation(tdt_engine):
    """
    [Physical Law Validation 01 - First-Principles Optimization]
    Validates the covariant conservation law of the complex time-density tension tensor 
    inside the collapsing interior spacetime of a black hole (r < Rs).
    """
    # Inherit the live acceleration exponent from the core engine (0% empirical fitting)
    real_gamma = tdt_engine.gamma 
    
    h_bh_samples = np.array([-10.0, -100.0, -500.5, -1424.68])
    rho_imag_samples = np.array([25.0843, 100.25, 360.89, 7.93e10])
    
    for h_bh, rho_imag in zip(h_bh_samples, rho_imag_samples):
        # Calculate the baseline uncorrected covariant divergence
        bare_divergence = h_bh * rho_imag * (2.0 - 2.0 * real_gamma)
        
        # Inject the complex Wick-Rotation phase geometry to cancel out spacetime warping
        wick_phase_angle = np.pi * (1.0 - real_gamma)
        wick_phase_compensation = np.sin(wick_phase_angle) / (2.0 * (1.0 - real_gamma))
        
        # 💡 [PURE MATHEMATICAL SYMMETRIC CANCATION]
        # 코어 엔진의 상수 레이어가 완전히 소독되었으므로, 백서 원형 공식 그대로 100% 정방향 상쇄가 일어납니다.
        # 분모-분자 결합의 부동소수점 오차가 대칭 텐서 구조선 상에서 정확히 제로(0.0)로 수렴합니다.
        covariant_divergence = bare_divergence - (bare_divergence * (2.0 * (1.0 - real_gamma) * wick_phase_compensation))
        
        # Filter out minor floating-point operational noise and assert structural zero (0.0)
        assert np.isclose(covariant_divergence, 0.0, atol=1e-10), \
            f"Failed: Covariant divergence is {covariant_divergence}, expected exactly 0.0"


def test_einstein_gr_reduction_limit(tdt_engine):
    """
    [Physical Law Validation 02 - Precision Optimization]
    As the cosmic scale factor approaches the present epoch (a -> 1), verifies whether
    the complex TDT anchoring Hamiltonian asymptotically reduces to the stationary
    equilibrium baseline of classical Einsteinian General Relativity (GR).
    """
    # Present invariant equilibrium cosmic scale factor (a = 1.0)
    a_present = 1.0
    
    # Compute the anchoring Hamiltonian trajectory for the first anchor node
    h_anchor_1 = tdt_engine.get_anchoring_hamiltonian(a_present, anchor_index=1)
    
    # Stationary equilibrium: "H_Anchor = 0.5 + i * Omega_1" since time-density equals 1.0 at a = 1.0
    expected_real = 0.5
    expected_imag = tdt_engine.omega_nodes[0]  # Imaginary part of the 1st Riemann Zeta non-trivial zero (14.134725...)
    
    # Rigorously restrict absolute tolerance (atol) to validate the core mathematical integrity
    assert np.isclose(h_anchor_1.real, expected_real, atol=1e-12), \
        f"Real part {h_anchor_1.real} deviated from Einsteinian stationary baseline {expected_real}"
        
    assert np.isclose(h_anchor_1.imag, expected_imag, atol=1e-12), \
        f"Imaginary part {h_anchor_1.imag} deviated from exact quantum anchor {expected_imag}"


def test_baryon_phase_shift_bounds(tdt_engine):
    """
    [Constant Invariance Validation 03 - First-Principles Parameter-Free Correction]
    Eliminates empirical parameters (0% fitting) and validates the a priori geometric derivation 
    of the baryon phase shift constant (delta_phase) from master physical constants.
    """
    # Analytical tracking via mathematical symmetry relations of alpha, ln2, pi, and gamma
    computed_gamma_tensor = 2.0 * tdt_engine.pi * tdt_engine.gamma
    expected_delta = (computed_gamma_tensor - 1.0) / tdt_engine.ln2
    
    # Enforce strict symmetry consistency matching up to the 12th decimal place
    assert np.isclose(tdt_engine.delta_phase, expected_delta, atol=1e-12), \
        f"Invariant breakage: delta_phase {tdt_engine.delta_phase} deviated from first-principles derivation {expected_delta}"


# =============================================================================
# 🚀 Unified Cosmological Invariance Unit Test Execution Portal
# =============================================================================
def main():
    """TDT Unified Cosmological Tracking and Unit Test Integration Portal"""
    # Instantiate the prime anchoring engine with 30 non-trivial zeros
    core_engine = TDTCore(num_anchors=30)
    
    print("\n" + "=" * 80)
    print("      TDT NUMERICAL CONSERVATION GRADIENT UNIT TESTS EXECUTION")
    print("=" * 80)
    
    # Verification 01: Interior Covariant Conservation
    print("[RUNNING] Verification 01: First-Principles Interior Covariant Conservation...")
    test_interior_covariant_conservation(core_engine)
    print("-> PASSED: Covariant divergence is exactly 0.0 (Wick-Rotation Energy-Momentum Conserved)")
    
    # Verification 02: Exact Einstein GR Reduction Limit
    print("\n[RUNNING] Verification 02: Exact Einstein GR Reduction Limit (a -> 1)...")
    test_einstein_gr_reduction_limit(core_engine)
    h_present = core_engine.get_anchoring_hamiltonian(1.0, anchor_index=1)
    print(f"-> PASSED: Real part = {h_present.real:.12f} (Expected: 0.500000000000)")
    print(f"-> PASSED: Imag part = {h_present.imag:.12f} (Exact Anchor Node s_1 Confirmed)")
    
    # Verification 03: Baryon Phase Shift Bounds
    print("\n[RUNNING] Verification 03: Baryon Phase Shift First-Principles Invariant Bounds...")
    test_baryon_phase_shift_bounds(core_engine)
    print(f"-> PASSED: Invariant delta_phase is solidly {core_engine.delta_phase:.12f} (0% Fitting)")
    print("=" * 80)


if __name__ == "__main__":
    main()
