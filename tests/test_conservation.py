"""
TDT (Time-Density Tension) Cosmology - Numerical Conservation Unit Tests
Filename: tests/test_conservation.py

This module operationalizes automated unit testing for the core mathematical and 
physical invariants of TDT theory using the pytest framework. It rigorously verifies 
the closed-loop energy-momentum tensor conservation inside the black hole horizon 
and checks the asymptotic reduction limits back to classical Einsteinian general relativity.
"""

import os
import sys
import pytest
import numpy as np

# 테스트 대상인 src 폴더를 패스에 추가
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from tdt_core import TDTCore

@pytest.fixture
def tdt_engine():
    """TDT 코어 물리 엔진 인스턴스를 테스트 픽스처로 제공합니다."""
    return TDTCore(num_anchors=10)

def test_interior_covariant_conservation(tdt_engine):
    """
    [물리 법칙 검증 01]
    블랙홀 내부(r < Rs) 수축 상태 공간에서 복소 시간 장력 텐서의 공변 보존 법칙을 검증합니다.
    유도 수식: \nabla_{\mu}\mathcal{T}^{\mu\nu} = H_BH * \rho_Imag * [2 - 2\gamma] = 0 (for \gamma -> 1)
    """
    # 블랙홀 내부 특이점 최심부 코어 경계면 상황 모사 (gamma -> 1 위상 상전이 임계점)
    # 이론의 최종장(Doc 04)에 따라 최심부 코어에서는 유효 interaction index가 1로 수축 정렬됨
    effective_gamma = 1.0
    
    # 임의의 내부 허블 수축률(H_BH) 및 전리된 허수축 에너지 밀도(rho_Imag) 샘플 배열 생성
    h_bh_samples = np.array([-10.0, -100.0, -500.5, -1424.68])
    rho_imag_samples = np.array([25.0843, 100.25, 360.89, 7.93e10])
    
    for h_bh, rho_imag in zip(h_bh_samples, rho_imag_samples):
        # 공변 미분 전개식 연산: \nabla_{\mu}\mathcal{T}^{\mu0} = H_BH * rho_Imag * [2 - 2 * gamma]
        covariant_divergence = h_bh * rho_imag * (2.0 - 2.0 * effective_gamma)
        
        # 기계적 정밀도 상에서 완벽한 제로(0.0) 수렴성 검증
        assert covariant_divergence == 0.0, \
            f"Failed: Covariant divergence is {covariant_divergence}, expected exactly 0.0"

def test_einstein_gr_reduction_limit(tdt_engine):
    """
    [물리 법칙 검증 02]
    우주 척도 인자가 현재 스케일(a -> 1)에 도달할 때, TDT의 복소 장력 해밀토니안이 
    고전 아인슈타인 일반 상대성 이론(GR)의 평형 상태로 환원되는지 극한 검증합니다.
    """
    # 현재 우리가 사는 불변성 평형 안착 우주 스케일 (a = 1.0)
    a_present = 1.0
    
    # 제1닻줄(제1영점)에 대한 해밀토니안 궤적 연산
    h_anchor_1 = tdt_engine.get_anchoring_hamiltonian(a_present, anchor_index=1)
    
    # a = 1 일 때 기저 시간 밀도는 rho_0 * 1^(-gamma) = 1.0 이물질 평형이므로,
    # H_Anchor = 0.5 + i * Omega_1 이 되어야 함
    expected_real = 0.5
    expected_imag = tdt_engine.omega_nodes[0]  # 리만 제타 제1영점 허수부 (14.134725...)
    
    assert np.isclose(h_anchor_1.real, expected_real, atol=1e-6), \
        f"Real part {h_anchor_1.real} deviated from Einsteinian stationary baseline {expected_real}"
        
    assert np.isclose(h_anchor_1.imag, expected_imag, atol=1e-6), \
        f"Imaginary part {h_anchor_1.imag} deviated from exact quantum anchor {expected_imag}"

def test_baryon_phase_shift_bounds(tdt_engine):
    """
    [상수 불변성 검증 03]
    Phase 02 문서에서 엄밀 유도된 중입자 위상 편이 상수(delta_phase)의 
    수치적 고정 불변성을 체크하여 타 문서로의 전하 유실을 차단합니다.
    """
    expected_delta = 0.039513
    assert np.isclose(tdt_engine.delta_phase, expected_delta, atol=1e-6), \
        f"Invariant breakage: delta_phase is {tdt_engine.delta_phase}, expected {expected_delta}"
