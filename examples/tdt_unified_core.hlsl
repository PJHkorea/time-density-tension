// GPU 가속용 TDT 통합 연산 파이프라인 컴퓨트 셰이더 (TDT_Unified_Core.hlsl)

cbuffer TDTCosmicConstants : register(b0)
{
    float c_alpha;
    float c_ln2;
    float c_pi;
    float c_gamma;
    float c_delta_phase;
    float c_c_univ;
    float c_omega_1;
    float c_r_core;
};

struct SimulationNode
{
    float gas_position;
    float gas_velocity;
    float tension_position;
    float tension_velocity;
    float current_z;
    float3 pad;
};

RWStructuredBuffer<SimulationNode> RenderNodes : register(u1);

// ---------------------------------------------------------------------
// [제일 원리 기하학 필터 커널들 - GPU 무분기 하드웨어 최적화 버전]
// ---------------------------------------------------------------------
float GetDebyeFriction(float r)
{
    float r_safe = max(abs(r), 1e-15f);
    float base_scale = (1.0f / c_alpha) * (c_gamma / c_ln2);
    float r_debye = base_scale * (c_ln2 * c_pi);
    float r_scale = 1.0f / (c_alpha * c_ln2 * c_pi);

    float gaussian_decay = exp(-pow(r_safe / r_debye, 2.0f));
    // 하드웨어 레벨에서 지수 가속 처리되는 tanh 연산
    float density_switch = 1.0f + tanh(clamp((c_r_core - r_safe) / r_scale, -30.0f, 30.0f));
    
    return gaussian_decay * density_switch;
}

float GetTracyWidomTension(float r)
{
    float r_safe = max(abs(r), 1e-15f);
    float base_scale = (1.0f / c_alpha) * (c_gamma / c_ln2);
    float r_norm = r_safe / base_scale;

    float effective_r_axis = r_norm * (1.0f - (c_delta_phase / sqrt(3.0f)));
    float tracy_widom_2d_grid = 1.0f + pow(c_gamma * effective_r_axis, 1.5f);

    float v_tension_bare = (c_c_univ * c_omega_1 * pow(r_norm, c_gamma)) / tracy_widom_2d_grid;
    float conformal_holographic_projection = (c_gamma / c_delta_phase) * (c_alpha * c_pi);

    return v_tension_bare * conformal_holographic_projection;
}

// ---------------------------------------------------------------------
// [가속도 연산 커널 - RK4 프레임워크 바인딩]
// ---------------------------------------------------------------------
float GetGasAcceleration(float p, float v)
{
    float r = max(abs(p), 1e-15f);
    float debye_f = GetDebyeFriction(r);
    float conformal_braking_scale = (c_c_univ * c_gamma) / (1.0f + c_delta_phase);
    float spatial_projection_factor = sqrt(2.0f * c_pi); // 3D -> 1D 단면 투사 정밀도 보정

    float friction_accel = conformal_braking_scale * debye_f * abs(v) * spatial_projection_factor;
    float direction = (v >= 0.0f) ? -1.0f : 1.0f; // 하드웨어 조건 스위치
    return direction * friction_accel;
}

float GetTensionAcceleration(float p, float v, float current_z)
{
    float r = max(abs(p), 1e-15f);
    float base_accel = GetTracyWidomTension(r) * (c_alpha * c_pi) * (1.0f / c_alpha) * (sqrt(3.0f) / 2.0f);

    // 훅의 법칙(Hookean) 기하학 마스킹 연산
    [flatten] // GPU 분기 예측 오버헤드를 소멸시키는 셰이더 플래튼 명령어
    if (abs(p) > (c_r_core * c_pi))
    {
        float conformal_pull_exponent = c_pi / sqrt(3.0f);
        float boundary_scale = (1.0f / c_alpha) * (c_gamma / c_ln2);
        float slip = c_delta_phase * boundary_scale * c_pi;
        
        base_accel *= (1.0f + pow(r / slip, conformal_pull_exponent));
        base_accel += (c_gamma / c_pi) * (r / slip) * abs(v);
    }

    float pull_direction = (p >= 0.0f) ? -1.0f : 1.0f;
    float total_accel = pull_direction * base_accel;

    // 후기 우주론적 허블 드래그 마찰 스위치 결합 (z < 8)
    float damping_switch = 0.5f * (1.0f - tanh((current_z - 8.0f) / 1.5f));
    float H0_per_myr = 67.4f * 1.0227e-6f;
    float braking_direction = (v >= 0.0f) ? -1.0f : 1.0f;
    float hubble_friction = braking_direction * (2.0f * H0_per_myr * abs(v));

    return total_accel + (damping_switch * hubble_friction);
}

// ---------------------------------------------------------------------
// [메인 스레드 가속 엔트리 포인트 - 1그룹당 64스레드 병렬 폭발]
// ---------------------------------------------------------------------
[numthreads(64, 1, 1)]
void CSMain(uint3 dtid : SV_DispatchThreadID)
{
    uint id = dtid.x;
    SimulationNode node = RenderNodes[id];

    float local_dt = 0.01f; // 고정된 고해상도 정보 격자 타임스텝
    float current_z = node.current_z;

    // ---------------------------------------------------------------------
    // [컴퓨팅 세이더 레벨의 예외 배리어 - Capture Lock Matrix]
    // 포획 장벽 내부 진입 시 가스의 추가 연산을 하드웨어 레벨에서 중단시켜 병목 원천 차단
    // ---------------------------------------------------------------------
    [branch]
    if (node.gas_position == 0.0f && abs(node.tension_position) <= c_r_core)
    {
        // 포획 이후 상태: 은하핵 가스 압착 및 원시 스타포메이션 렌더 레이어 진입
        // 이 구역에서 별 생성(SFR) 속도에 따른 가상 텍스처/정점 컬러 버퍼 변환 코드가 가동됩니다.
        // ex) RenderUVLuminosityBuffer[id] = -19.0f - 2.5f * log10(DerivedSFR);
        
        // 시공간 결합 격자(Tension)의 후기 잔여 진동만 RK4 적분 수행
        float tk1 = GetTensionAcceleration(node.tension_position, node.tension_velocity, current_z);
        float xk1 = node.tension_velocity;
        float tk2 = GetTensionAcceleration(node.tension_position + 0.5f * local_dt * xk1, node.tension_velocity + 0.5f * local_dt * tk1, current_z);
        float xk2 = node.tension_velocity + 0.5f * local_dt * tk1;
        float tk3 = GetTensionAcceleration(node.tension_position + 0.5f * local_dt * xk2, node.tension_velocity + 0.5f * local_dt * tk2, current_z);
        float xk3 = node.tension_velocity + 0.5f * local_dt * tk2;
        float tk4 = GetTensionAcceleration(node.tension_position + local_dt * xk3, node.tension_velocity + local_dt * tk3, current_z);
        float xk4 = node.tension_velocity + local_dt * tk3;

        node.tension_velocity += (local_dt / 6.0f) * (tk1 + 2.0f * tk2 + 2.0f * tk3 + tk4);
        node.tension_position += (local_dt / 6.0f) * (xk1 + 2.0f * xk2 + 2.0f * xk3 + xk4);
    }
    else
    {
        // --- 프리 캡처(Pre-Capture) 단계: 가스 및 격자 멀티바디 초고속 RK4 수치 적분 ---
        // 바리온 가스 RK4
        float vk1 = GetGasAcceleration(node.gas_position, node.gas_velocity);
        float pk1 = node.gas_velocity;
        float vk2 = GetGasAcceleration(node.gas_position + 0.5f * local_dt * pk1, node.gas_velocity + 0.5f * local_dt * vk1);
        float pk2 = node.gas_velocity + 0.5f * local_dt * vk1;
        float vk3 = GetGasAcceleration(node.gas_position + 0.5f * local_dt * pk2, node.gas_velocity + 0.5f * local_dt * vk2);
        float pk3 = node.gas_velocity + 0.5f * local_dt * vk2;
        float vk4 = GetGasAcceleration(node.gas_position + local_dt * pk3, node.gas_velocity + local_dt * vk3);
        float pk4 = node.gas_velocity + local_dt * vk3;

        float gas_vel_next = node.gas_velocity + (local_dt / 6.0f) * (vk1 + 2.0f * vk2 + 2.0f * vk3 + vk4);
        float gas_pos_next = node.gas_position + (local_dt / 6.0f) * (pk1 + 2.0f * pk2 + 2.0f * pk3 + pk4);

        // 시공간 격자 RK4
        float tk1 = GetTensionAcceleration(node.tension_position, node.tension_velocity, current_z);
        float xk1 = node.tension_velocity;
        float tk2 = GetTensionAcceleration(node.tension_position + 0.5f * local_dt * xk1, node.tension_velocity + 0.5f * local_dt * tk1, current_z);
        float xk2 = node.tension_velocity + 0.5f * local_dt * tk1;
        float tk3 = GetTensionAcceleration(node.tension_position + 0.5f * local_dt * xk2, node.tension_velocity + 0.5f * local_dt * tk2, current_z);
        float xk3 = node.tension_velocity + 0.5f * local_dt * tk2;
        float tk4 = GetTensionAcceleration(node.tension_position + local_dt * xk3, node.tension_velocity + local_dt * tk3, current_z);
        float xk4 = node.tension_velocity + local_dt * tk3;

        node.tension_velocity += (local_dt / 6.0f) * (tk1 + 2.0f * tk2 + 2.0f * tk3 + tk4);
        node.tension_position += (local_dt / 6.0f) * (xk1 + 2.0f * xk2 + 2.0f * xk3 + xk4);

        // 정밀 코어 어트랙터 포획 조건 판정 연산
        if ((node.gas_position < 0.0f && gas_pos_next >= -1.0f) || (abs(gas_pos_next) <= c_r_core))
        {
            node.gas_velocity = 0.0f;
            node.gas_position = 0.0f; // 중심부 고정 및 락 트리거 활성화
        }
        else
        {
            node.gas_velocity = gas_vel_next;
            node.gas_position = gas_pos_next;
        }
    }

    // 타임라인 감쇄 진행 연산 (실제 오픈월드 엔진 연동 시 프레임 갱신율 바인딩)
    node.current_z = max(node.current_z - 0.0002f, 0.0f);

    // 연산된 결과를 글로벌 그래픽스 메모리에 즉시 플러시하여 버퍼 동기화
    RenderNodes[id] = node;
}
