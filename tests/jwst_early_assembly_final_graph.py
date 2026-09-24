import matplotlib.pyplot as plt
import numpy as np

# 논문 및 학술지 스타일 정밀 폰트 및 그리드 환경 설정
plt.figure(figsize=(13, 10), dpi=150)
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')

# ---------------------------------------------------------------------
# Subplot 1: 시공간 장력 소산 조화 진동 및 바리온 가스 포획 궤적 (LSS 역학)
# ---------------------------------------------------------------------
plt.subplot(2, 1, 1)
time_arr = np.array(simulator.time_history)
gas_arr = np.array(simulator.gas_history)
tension_arr = np.array(simulator.tension_history)

# [시각화 고도화 1]: 5만 스텝의 촘촘한 선을 투명하고 얇게 처리하여 내부 밀도 시각화
plt.plot(time_arr, tension_arr, color='#1f77b4', linewidth=0.3, alpha=0.3, label='Soliton Grid Oscillation ($Tension\_Pos$)')

# [시각화 고도화 2]: 진동의 상단/하단 경계(Envelope)를 구해서 깔때기 모양을 선명하게 플롯
# 100개 스텝마다의 로컬 최댓값과 최솟값을 추적하여 포락선을 그립니다.
window = 100
upper_envelope = [max(tension_arr[max(0, i-window):i+1]) for i in range(len(tension_arr))]
lower_envelope = [min(tension_arr[max(0, i-window):i+1]) for i in range(len(tension_arr))]

plt.plot(time_arr, upper_envelope, color='#0b4a75', linewidth=1.5, linestyle='-', label='Tension Boundary (Envelope)')
plt.plot(time_arr, lower_envelope, color='#0b4a75', linewidth=1.5, linestyle='-')

# 바리온 가스는 붉은 대시 선으로 명확히 표현
plt.plot(time_arr, gas_arr, color='#d62728', linewidth=2.5, linestyle='--', label='Baryon Fluid Center ($Gas\_Pos$)')

# 주요 물리적 전이 지점 마킹 (3.43 Myr 포획 록)
plt.axvline(x=3.43, color='darkgreen', linestyle=':', linewidth=1.5, alpha=0.7)
plt.text(5.0, -400, 'Resonant Capture Lock\n(t = 3.43 Myr)', color='darkgreen', fontsize=10, weight='bold')

# z < 8 소산 매니폴드 작동 영역 마킹 (약 380 Myr 지점)
plt.axvline(x=380.0, color='purple', linestyle=':', linewidth=1.5, alpha=0.7)
plt.text(300.0, 200, 'Topological Dissipation\nManifold Active (z < 8)', color='purple', fontsize=10, weight='bold')

plt.title('TDT LSS Soliton Dynamics & Baryon Resonant Capture Profile', fontsize=13, weight='bold', pad=10)
plt.xlabel('Elapsed Cosmic Time (Myr)', fontsize=11)
plt.ylabel('Spatial Coordinate Position (kpc)', fontsize=11)
plt.ylim(-600, 600)
plt.legend(loc='upper right', frameon=True, facecolor='white', edgecolor='none')

# ---------------------------------------------------------------------
# Subplot 2: 우주론적 적색편이 역산 및 JWST 관측 타깃 UV 절대광도 진화 곡선 (기존 유지)
# ---------------------------------------------------------------------
ax1 = plt.subplot(2, 1, 2)
z_arr = simulator.z_history
m_uv_arr = simulator.luminosity_history

color = '#2ca02c'
ax1.set_xlabel('Elapsed Cosmic Time (Myr)', fontsize=11)
ax1.set_ylabel('Cosmological Redshift ($z$ Map)', color=color, fontsize=11)
line1 = ax1.plot(time_arr, z_arr, color=color, linewidth=2.2, label='Analytical FLRW $z$ Map')
ax1.tick_params(axis='y', labelcolor=color)
ax1.set_ylim(6.0, 16.0)

ax2 = ax1.twinx()
color = '#9467bd'
ax2.set_ylabel('Absolute UV Magnitude ($M_{UV}$)', color=color, fontsize=11)

m_uv_masked = [m if m < 0.0 else None for m in m_uv_arr]
line2 = ax2.plot(time_arr, m_uv_masked, color=color, linewidth=2.2, linestyle='-.', label='Projected Magnitude $M_{UV}$')
ax2.tick_params(axis='y', labelcolor=color)
ax2.set_ylim(-14.0, -22.0)
ax2.invert_yaxis()

lines = line1 + line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='upper right', frameon=True, facecolor='white', edgecolor='none')
plt.title('Cosmological Timeline Expansion & Baryon Fluid Core Luminosity Evolution', fontsize=13, weight='bold', pad=10)

plt.tight_layout()
plt.savefig('tdt_jwst_assembly_final_plot_envelope.png', dpi=300, bbox_inches='tight')
plt.show()
