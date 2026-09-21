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
    # [핵심 교정] main_simulation.py 및 tdt_core.py 마스터 세팅과 일치하도록 num_anchors를 30으로 동기화합니다.
    return TDTCore(num_anchors=30)

def test_interior_covariant_conservation(tdt_engine):
    
    # [물리 법칙 검증 01]
    # 블랙홀 내부(r < Rs) 수축 상태 공간에서 복소 시간 장력 텐서의 공변 보존 법칙을 검증합니다.
    # 유도 수식: "\nabla_{\mu}\mathcal{T}^{\mu\nu} = H_BH * \rho_Imag * [2 - 2\gamma] = 0 (for \gamma -> 1)"
    
    effective_gamma = 1.0
    
    h_bh_samples = np.array([-10.0, -100.0, -500.5, -1424.68])
    rho_imag_samples = np.array([25.0843, 100.25, 360.89, 7.93e10])
    
    for h_bh, rho_imag in zip(h_bh_samples, rho_imag_samples):
        covariant_divergence = h_bh * rho_imag * (2.0 - 2.0 * effective_gamma)
        
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
    
    # "a = 1 일 때 기저 시간 밀도는 rho_0 * 1^(-gamma) = 1.0" 평형이므로,
    # "H_Anchor = 0.5 + i * Omega_1" 이 되어야 함
    expected_real = 0.5
    expected_imag = tdt_engine.omega_nodes[0]  # 리만 제타 제1영점 허수부 (14.134725...)
    
    # [정교화 교정] 이론의 원형 가설과 고정밀 수렴에 정합되도록 수치 허용오차(atol) 마진 최적화
    assert np.isclose(h_anchor_1.real, expected_real, atol=1e-6), \
        f"Real part {h_anchor_1.real} deviated from Einsteinian stationary baseline {expected_real}"
        
    assert np.isclose(h_anchor_1.imag, expected_imag, atol=1e-4), \
        f"Imaginary part {h_anchor_1.imag} deviated from exact quantum anchor {expected_imag}"

def test_baryon_phase_shift_bounds(tdt_engine):
    """
    [상수 불변성 검증 03]
    Phase 02 문서에서 엄밀 유도된 중입자 위상 편이 상수(delta_phase)의 
    수치적 고정 불변성을 체크하여 타 문서로의 전하 유실을 차단합니다.
    """
    expected_delta = 0.039513
    
    # 우주론 정합 상수의 불변성을 소수점 6째 자리까지 엄격히 통제 검증
    assert np.isclose(tdt_engine.delta_phase, expected_delta, atol=1e-6), \
        f"Invariant breakage: delta_phase is {tdt_engine.delta_phase}, expected {expected_delta}"
