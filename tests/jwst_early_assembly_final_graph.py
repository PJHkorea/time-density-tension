import matplotlib.pyplot as plt
import numpy as np

# 1. 고해상도 및 넉넉한 캔버스 크기 강제 할당 (하단 잘림 방지)
fig, (ax1, ax2_left) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

# --- 상단 그래프 (Soliton Dynamics) ---
time_arr = np.array(simulator.time_history)
tension_arr = np.array(simulator.tension_history)
gas_arr = np.array(simulator.gas_history)

# linewidth를 0.3으로 얇게 주어 5만 개 고주파 띠를 정밀 사영
ax1.plot(time_arr, tension_arr, color='#4169E1', linewidth=0.3, alpha=0.8, label=r'Soliton Grid Oscillation ($Tension\_Pos$)')
ax1.plot(time_arr, gas_arr, color='#D32F2F', linewidth=2.5, linestyle='--', label=r'Baryon Fluid Center ($Gas\_Pos$)')

# 장력 경계 엔벨로프(Envelope) 라인 추가
r_envelope = np.maximum(abs(tension_arr), 1e-15)
# (여기에 Envelope 상하단 경계 라인 플롯 추가 가능)

ax1.set_ylabel('Spatial Coordinate Position (kpc)', fontsize=12)
ax1.set_title('TDT LSS Soliton Dynamics & Baryon Resonant Capture Profile', fontsize=14, weight='bold', pad=15)
ax1.legend(loc='upper right', frameon=True, facecolor='white', edgecolor='none')
ax1.grid(True, linestyle=':', alpha=0.6)

# --- 하단 그래프 (Cosmological Timeline & Luminosity) ---
z_arr = np.array(simulator.z_history)
muv_arr = np.array(simulator.luminosity_history)

# 왼쪽축: 적색편이 (z Map)
ax2_left.plot(time_arr, z_arr, color='#2E7D32', linewidth=2.2, label=r'Analytical FLRW $z$ Map')
ax2_left.set_xlabel('Elapsed Cosmic Time (Myr)', fontsize=12)
ax2_left.set_ylabel('Cosmological Redshift ($z$ Map)', color='#2E7D32', fontsize=12)
ax2_left.tick_params(axis='y', labelcolor='#2E7D32')
ax2_left.grid(True, linestyle=':', alpha=0.6)

# 오른쪽축 쌍둥이 축 생성: 자외선 절대등급 (M_UV)
ax2_right = ax2_left.twinx()
# 별 형성이 없는 구간(0.0) 필터링 처리 가드
muv_masked = np.where(muv_arr < 0.0, muv_arr, np.nan)

ax2_right.plot(time_arr, muv_masked, color='#8E24AA', linewidth=2.2, linestyle='-.', label=r'Projected Magnitude $M_{UV}$')
ax2_right.set_ylabel('Absolute UV Magnitude ($M_{UV}$)', color='#8E24AA', fontsize=12)
ax2_right.tick_params(axis='y', labelcolor='#8E24AA')

# 등급 특성에 맞는 Y축 범위 반전 고정
ax2_right.set_ylim(-14.0, -22.0) 

# 두 하단 축의 레전드 결합 정합
lines1, labels1 = ax2_left.get_legend_handles_labels()
lines2, labels2 = ax2_right.get_legend_handles_labels()
ax2_left.legend(lines1 + lines2, labels1 + labels2, loc='upper right', frameon=True, facecolor='white', edgecolor='none')

ax2_left.set_title('Cosmological Timeline Expansion & Baryon Fluid Core Luminosity Evolution', fontsize=13, weight='bold', pad=10)

# 2. 레이아웃 충돌 방지 간격 명시적 패딩
plt.subplots_adjust(hspace=0.3)
plt.savefig('tdt_jwst_assembly_perfect_fit.png', dpi=300, bbox_inches='tight')
plt.show()
