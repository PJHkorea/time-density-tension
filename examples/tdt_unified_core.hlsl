// GPU-Accelerated Integrated TDT Cosmological Matrix Execution Pipeline Compute Shader (tdt_unified_core.hlsl)

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
// [First-Principles Geometric Filter Kernels - Branchless Hardware-Optimized Spec]
// ---------------------------------------------------------------------
float GetDebyeFriction(float r)
{
    float r_safe = max(abs(r), 1e-15f);
    float base_scale = (1.0f / c_alpha) * (c_gamma / c_ln2);
    float r_debye = base_scale * (c_ln2 * c_pi);
    float r_scale = 1.0f / (c_alpha * c_ln2 * c_pi);

    float gaussian_decay = exp(-pow(r_safe / r_debye, 2.0f));
    // Leverage the hardware-level transcendent special function unit (SFU) for accelerated tanh execution
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
// [Kinematic Acceleration Kernels - RK4 Integration Framework Binding]
// ---------------------------------------------------------------------
float GetGasAcceleration(float p, float v)
{
    float r = max(abs(p), 1e-15f);
    float debye_f = GetDebyeFriction(r);
    float conformal_braking_scale = (c_c_univ * c_gamma) / (1.0f + c_delta_phase);
    float spatial_projection_factor = sqrt(2.0f * c_pi); // 3D -> 1D Dimensional Cross-Sectional Projection Correction

    float friction_accel = conformal_braking_scale * debye_f * abs(v) * spatial_projection_factor;
    float direction = (v >= 0.0f) ? -1.0f : 1.0f; // Branchless Hardware Condition Sign Switcher
    return direction * friction_accel;
}

float GetTensionAcceleration(float p, float v, float current_z)
{
    float r = max(abs(p), 1e-15f);
    float base_accel = GetTracyWidomTension(r) * (c_alpha * c_pi) * (1.0f / c_alpha) * (sqrt(3.0f) / 2.0f);

    // Intrinsic Hookean Manifold Geometric Masking Operation
    [flatten] // Forces compile-time branch flattening to eliminate Warp Divergence and pipeline latency
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

    // Late-Universe Cosmological Hubble Drag Damping Switch Coupling (Active for z < 8)
    float damping_switch = 0.5f * (1.0f - tanh((current_z - 8.0f) / 1.5f));
    float H0_per_myr = 67.4f * 1.0227e-6f;
    float braking_direction = (v >= 0.0f) ? -1.0f : 1.0f;
    float hubble_friction = braking_direction * (2.0f * H0_per_myr * abs(v));

    return total_accel + (damping_switch * hubble_friction);
}

// ---------------------------------------------------------------------
// [Main Compute Thread Entry Point - Parallel Execution Burst via 64-Thread Warps]
// ---------------------------------------------------------------------
[numthreads(64, 1, 1)]
void CSMain(uint3 dtid : SV_DispatchThreadID)
{
    uint id = dtid.x;
    SimulationNode node = RenderNodes[id];

    float local_dt = 0.01f; // Fixed high-resolution informational grid timestep
    float current_z = node.current_z;

    // ---------------------------------------------------------------------
    // [Compute Shader Level Execution Barrier - Capture Lock Matrix]
    // Upon inner-barrier convergence, gas-phase kinematic integration is halted at the 
    // hardware level to eliminate execution bottlenecks and prevent thread stalling.
    // ---------------------------------------------------------------------
    [branch] // Explicit branch execution path optimization to maximize early rejection efficiency
    if (node.gas_position == 0.0f && abs(node.tension_position) <= c_r_core)
    {
        // --- Post-Capture Phase: Galactic Nucleus Gas Compression & Proto-Starformation Render Layer ---
        // This localized domain is allocated for dynamic virtual texture mapping and vertex color 
        // buffer transformations driven by the derived Star Formation Rate (SFR).
        // e.g., RenderUVLuminosityBuffer[id] = -19.0f - 2.5f * log10(DerivedSFR);
        
        // Execute Runge-Kutta 4th Order (RK4) numerical quadrature strictly for the late-stage 
        // residual oscillations of the coupled spacetime manifold (Tension).
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
        // --- Pre-Capture Phase: Ultra-High-Precision Multi-Body Gas & Lattice RK4 Integration ---
        // Baryonic Gas RK4 Integration Pass
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

        // Spacetime Manifold Lattice RK4 Integration Pass
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

        // Precision Core Attractor Capture Limit Boundary Evaluation
        if ((node.gas_position < 0.0f && gas_pos_next >= -1.0f) || (abs(gas_pos_next) <= c_r_core))
        {
            node.gas_velocity = 0.0f;
            node.gas_position = 0.0f; // Anchor coordinates to core and activate lock trigger
        }
        else
        {
            node.gas_velocity = gas_vel_next;
            node.gas_position = gas_pos_next;
        }
    }

    // --- Cosmological Timeline Decay Integration ---
    // Increments the state-transition lookback timeline. 
    // In production open-world environments, this factor binds directly to the engine's delta frame rate tracker.
    node.current_z = max(node.current_z - 0.0002f, 0.0f);

    // --- Global Graphics Memory Flush & Pipeline Synchronization ---
    // Commits the updated structural kinematic metrics directly back to the VRAM Unordered Access View (UAV) buffer.
    RenderNodes[id] = node;
}

