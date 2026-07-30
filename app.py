import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import re
import random
import uuid
import os
import csv
from datetime import datetime
from challenges import CHALLENGES
from latex2mathml.converter import convert as latex_to_mathml

st.set_page_config(page_title="Interactive Polarization Challenges", layout="wide")

# --- 0. LANDING PAGE GATEKEEPER ---
if "show_landing" not in st.session_state:
    st.session_state.show_landing = True

if st.session_state.show_landing:
    st.title("Welcome to this Interactive Polarization Applet")

    st.markdown("""
    Thank you for participating in this study! In this module, you will interactively explore the physics of light polarization. During the study, please do not use any external tools including pen and paper.

    Before we begin, please read how the interface works:
    """)

    st.markdown(
        """
        <div style="background-color: #fff9c4; color: black; padding: 15px; border-radius: 8px; border: 2px solid #fbc02d; margin-bottom: 10px;">
            📖 <b>1. The Setting:</b> Each step begins with an explanation box like this one, introducing the physical concepts.
        </div>

        <div style="background-color: #ffe0b2; color: black; padding: 15px; border-radius: 8px; border: 2px solid #ff9800; margin-bottom: 10px;">
            🎯 <b>2. The Task:</b> You will be given a specific objective. You must adjust the sliders or type the exact values into the number boxes to find the correct optical parameters using the 3D visualizations below.
        </div>

        <div style="background-color: #e8f5e9; color: black; padding: 15px; border-radius: 8px; border: 2px solid #4caf50; margin-bottom: 10px;">
            💡 <b>3. Getting Help:</b> If you don't know how to proceed, you can use the <b>Show Hint</b> button below the applet. If you are entirely stuck, you can reveal the answer using the <b>Show Solution</b> button at the bottom right.
        </div>

        <div style="background-color: #e3f2fd; color: black; padding: 15px; border-radius: 8px; border: 2px solid #2196f3; margin-bottom: 25px;">
            🎓 <b>4. Moving Forward:</b> When your sliders hit the correct values, an explanation box like this one will appear at the bottom. <b>Make sure to read it carefully</b>, and then proceed using the <b>Next Step</b> button.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        if st.button("🚀 I understand, start the tutorial!", use_container_width=True):
            st.session_state.show_landing = False
            st.rerun()

    # Stop the rest of the script from running while the landing page is active
    st.stop()

# --- 1. SESSION STATE, COHORT ASSIGNMENT & LOGGING ENGINE ---

# Capture the Participant ID from the URL right away
if "participant_id" not in st.session_state:
    if "pid" in st.query_params:
        st.session_state.participant_id = st.query_params["pid"]
    else:
        st.session_state.participant_id = "UNKNOWN_ID"

# Capture whether this participant is running with Eye-Tracking (1) or without (0)
if "et_status" not in st.session_state:
    if "et" in st.query_params:
        st.session_state.et_status = st.query_params["et"]
    else:
        st.session_state.et_status = "0"  # Default to 0 if missing

# Randomly assign cohort to Polarization 1 or Polarization 2
if "assigned_journey" not in st.session_state:
    st.session_state.assigned_journey = random.choice(["Polarization 1", "Polarization 2"])

if "current_challenge" not in st.session_state:
    st.session_state.current_challenge = st.session_state.assigned_journey

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

DEFAULTS = {
    "E_x_amp": 0.707, "phase_relative_pi": 0.0,
    "insert_wp": True, "wp_angle_deg": 45.0, "retardance_pi": 0.5,
    "insert_pol": False, "pol_angle_deg": 90.0,
    "show_combined": True, "show_ex": True, "show_ey": True, "show_axis": True,
    "show_poincare": True,
    "show_hint": False,
    "show_toggles": True,
    "disable_keys": []
}

for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v


def log_action(action_name):
    pass


def load_step_setup(challenge_name, step_index):
    step_data = CHALLENGES[challenge_name]["steps"][step_index]
    st.session_state["disable_keys"] = []
    for k, v in step_data.get("setup", {}).items():
        st.session_state[k] = v


if "tutorial_initialized" not in st.session_state:
    st.session_state.tutorial_initialized = True
    st.session_state.current_challenge = st.session_state.assigned_journey
    st.session_state.current_step = 0
    load_step_setup(st.session_state.current_challenge, 0)


def reset_challenge():
    st.session_state.current_step = 0
    st.session_state.show_hint = False
    load_step_setup(st.session_state.current_challenge, 0)
    log_action("Reset Challenge")


def next_step():
    log_action("Clicked Next Step")
    st.session_state.current_step += 1
    st.session_state.show_hint = False
    load_step_setup(st.session_state.current_challenge, st.session_state.current_step)


def toggle_hint():
    st.session_state.show_hint = not st.session_state.show_hint
    action_str = "Showed Hint" if st.session_state.show_hint else "Hid Hint"
    log_action(action_str)


def solve_challenge():
    log_action("Clicked Show Solution")
    challenge_name = st.session_state.current_challenge
    step_index = st.session_state.current_step
    step_data = CHALLENGES[challenge_name]["steps"][step_index]

    load_step_setup(challenge_name, step_index)

    for k, v in step_data.get("solution", {}).items():
        st.session_state[k] = v


# --- 2. PHYSICS EXTRACTION & SIMULATION ---
E_x_amp = st.session_state.E_x_amp
E_y_amp = np.sqrt(1.0 - E_x_amp ** 2)
phase_relative = st.session_state.phase_relative_pi * np.pi

wp_angle = np.deg2rad(st.session_state.wp_angle_deg) if st.session_state.insert_wp else 0.0
retardance = st.session_state.retardance_pi * np.pi if st.session_state.insert_wp else 0.0

pol_angle = np.deg2rad(st.session_state.pol_angle_deg) if st.session_state.insert_pol else 0.0

z_start, z_wp_in, z_wp_out = 0, 10, 15
z_pol = 25
z_end = 35 if st.session_state.insert_pol else 25
resolution = 600
z = np.linspace(z_start, z_end, resolution)
k = 2 * np.pi / 2.0

Ex, Ey, zeros = np.zeros_like(z), np.zeros_like(z), np.zeros_like(z)

cos_t, sin_t = np.cos(wp_angle), np.sin(wp_angle)
cos_p, sin_p = np.cos(pol_angle), np.sin(pol_angle)

J_pol = np.array([[cos_p ** 2, cos_p * sin_p],
                  [cos_p * sin_p, sin_p ** 2]]) if st.session_state.insert_pol else np.eye(2)

E_in_c_origin = np.array([E_x_amp * np.exp(1j * 0), E_y_amp * np.exp(1j * phase_relative)])


def prop_vacuum(E, distance):
    return E * np.exp(1j * k * distance)


def apply_wp(E_in):
    R_minus = np.array([[cos_t, sin_t], [-sin_t, cos_t]])
    R_plus = np.array([[cos_t, -sin_t], [sin_t, cos_t]])
    P_wp = np.array([[np.exp(1j * k * (z_wp_out - z_wp_in)), 0],
                     [0, np.exp(1j * (k * (z_wp_out - z_wp_in) + retardance))]])
    return R_plus @ P_wp @ R_minus @ E_in


E_at_wp_in = prop_vacuum(E_in_c_origin, z_wp_in)
E_at_wp_out = apply_wp(E_at_wp_in)
E_at_pol_in = prop_vacuum(E_at_wp_out, z_pol - z_wp_out)
E_at_pol_out = J_pol @ E_at_pol_in

intensity_percent = (np.abs(E_at_pol_out[0]) ** 2 + np.abs(E_at_pol_out[1]) ** 2) * 100

for i, zi in enumerate(z):
    if zi < z_wp_in:
        Ex[i] = E_x_amp * np.cos(k * zi)
        Ey[i] = E_y_amp * np.cos(k * zi + phase_relative)
    elif z_wp_in <= zi <= z_wp_out:
        E_fs = np.array([[cos_t, sin_t], [-sin_t, cos_t]]) @ prop_vacuum(E_in_c_origin, z_wp_in)
        delta_phase = retardance * ((zi - z_wp_in) / (z_wp_out - z_wp_in))
        delta_z = zi - z_wp_in
        P = np.array([[np.exp(1j * k * delta_z), 0],
                      [0, np.exp(1j * (k * delta_z + delta_phase))]])
        E_xy_out = np.array([[cos_t, -sin_t], [sin_t, cos_t]]) @ (P @ E_fs)
        Ex[i], Ey[i] = np.real(E_xy_out[0]), np.real(E_xy_out[1])
    elif z_wp_out < zi <= z_pol:
        delta_z = zi - z_wp_out
        E_vac = prop_vacuum(E_at_wp_out, delta_z)
        Ex[i] = np.abs(E_vac[0]) * np.cos(np.angle(E_vac[0]))
        Ey[i] = np.abs(E_vac[1]) * np.cos(np.angle(E_vac[1]))
    else:
        delta_z = zi - z_pol
        E_final = prop_vacuum(E_at_pol_out, delta_z)
        Ex[i] = np.abs(E_final[0]) * np.cos(np.angle(E_final[0]))
        Ey[i] = np.abs(E_final[1]) * np.cos(np.angle(E_final[1]))

S_in = np.zeros(3)
S_in[0] = E_x_amp ** 2 - E_y_amp ** 2
S_in[1] = 2 * E_x_amp * E_y_amp * np.cos(phase_relative)
S_in[2] = 2 * E_x_amp * E_y_amp * np.sin(phase_relative)

A_x_wp = np.abs(E_at_wp_out[0])
A_y_wp = np.abs(E_at_wp_out[1])
delta_wp = np.angle(E_at_wp_out[1]) - np.angle(E_at_wp_out[0])

S_out = np.zeros(3)
S_out[0] = A_x_wp ** 2 - A_y_wp ** 2
S_out[1] = 2 * A_x_wp * A_y_wp * np.cos(delta_wp)
S_out[2] = 2 * A_x_wp * A_y_wp * np.sin(delta_wp)

S_pol_axis = np.array([np.cos(2 * pol_angle), np.sin(2 * pol_angle), 0])

if st.session_state.insert_pol:
    S_final = S_pol_axis.tolist()
elif st.session_state.insert_wp:
    S_final = S_out.tolist()
else:
    S_final = S_in.tolist()

# Bundle all calculated states for evaluation
derived_state = {
    "S_in": S_in.tolist(),
    "S_out": S_out.tolist(),
    "S_final": S_final,
    "intensity_percent": intensity_percent
}


def check_target_met(target_dict, derived):
    if not target_dict: return True
    for key, expected in target_dict.items():
        actual = derived.get(key, st.session_state.get(key))

        if actual is None:
            return False

        if isinstance(actual, np.ndarray):
            actual = actual.tolist()

        if isinstance(expected, list):
            if isinstance(actual, list):
                if len(expected) > 0 and isinstance(expected[0], list):
                    if not any(np.allclose(actual, e, atol=0.015) for e in expected): return False
                else:
                    if not np.allclose(actual, expected, atol=0.015): return False
            else:
                if not any(abs(actual - e) < 0.015 for e in expected): return False

        elif type(expected) in (float, int) and type(actual) in (float, int, np.float64, np.float32):
            tol = 1.5 if "percent" in key else 0.015
            if abs(actual - expected) > tol: return False
        else:
            if actual != expected: return False
    return True


# --- 3. UI: HEADER AND TUTORIAL BOX ---
st.title("Polarization of Light")
st.caption(f"Active Module: {st.session_state.assigned_journey}")

challenge_data = CHALLENGES[st.session_state.current_challenge]["steps"]
step_data = challenge_data[st.session_state.current_step]
is_last_step = st.session_state.current_step >= len(challenge_data) - 1


def process_math(text):
    if not text:
        return ""

    def replace_block(match):
        code = match.group(1).strip()
        if not code: return ""
        try:
            mathml = latex_to_mathml(code, display="block")
            return f"<div style='text-align: center; margin: 15px 0; font-size: 110%;'>{mathml}</div>"
        except Exception:
            return f"$$ {code} $$"

    def replace_inline(match):
        code = match.group(1).strip()
        if not code: return ""
        try:
            return latex_to_mathml(code)
        except Exception:
            return f"${code}$"

    text = re.sub(r'\$\$(.*?)\$\$', replace_block, text, flags=re.DOTALL)
    text = re.sub(r'\$(.*?)\$', replace_inline, text, flags=re.DOTALL)
    return text


processed_text = process_math(step_data.get('text', ''))
processed_task = process_math(step_data.get('task', ''))

if processed_text:
    st.markdown(
        f"<div style='background-color: #fff9c4; color: black; padding: 20px; border-radius: 8px; font-size: 16px; border: 2px solid #fbc02d; margin-bottom: 15px;'><div style='line-height: 1.6;'>📖 {processed_text}</div></div>",
        unsafe_allow_html=True)
if processed_task:
    st.markdown(
        f"<div style='background-color: #ffe0b2; color: black; padding: 15px; border-radius: 8px; font-size: 16px; border: 2px solid #ff9800; margin-bottom: 15px;'><div style='line-height: 1.6;'>🎯 <b>Task:</b> {processed_task}</div></div>",
        unsafe_allow_html=True)

target_met = check_target_met(step_data.get("target", {}), derived_state)
if is_last_step and st.session_state.current_challenge != "Free Play":
    st.success("Challenge Completed!")


def create_synced_input(label, min_val, max_val, step_val, base_key):
    slider_key = f"{base_key}_slider"
    num_key = f"{base_key}_num"
    is_disabled = base_key in st.session_state.get("disable_keys", [])

    if (slider_key not in st.session_state) or (st.session_state[slider_key] != st.session_state[base_key]):
        st.session_state[slider_key] = float(st.session_state[base_key])
    if (num_key not in st.session_state) or (st.session_state[num_key] != st.session_state[base_key]):
        st.session_state[num_key] = float(st.session_state[base_key])

    def sync_from_slider():
        st.session_state[base_key] = st.session_state[slider_key]
        st.session_state[num_key] = st.session_state[slider_key]

    def sync_from_num():
        st.session_state[base_key] = st.session_state[num_key]
        st.session_state[slider_key] = st.session_state[num_key]

    st.markdown(label)
    c1, c2 = st.columns([2.5, 1])
    with c1:
        st.slider(label, min_value=float(min_val), max_value=float(max_val), step=float(step_val), key=slider_key,
                  on_change=sync_from_slider, label_visibility="collapsed", disabled=is_disabled)
    with c2:
        st.number_input(label, min_value=float(min_val), max_value=float(max_val), step=float(step_val), key=num_key,
                        on_change=sync_from_num, label_visibility="collapsed", disabled=is_disabled)


col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

with col1:
    st.subheader(r"Incident Wave")
    st.write(r"$\vec{E} = \begin{pmatrix} E_x \\ E_y e^{i\varphi} \end{pmatrix}$")
    create_synced_input(r"Amplitude $E_x$", 0.0, 1.0, 0.01, "E_x_amp")
    st.write(fr"$E_y=$ {np.sqrt(1.0 - st.session_state.E_x_amp ** 2):.3f}")
    create_synced_input(r"Relative Phase $\varphi$ ($\times\pi$ rad)", 0.0, 2.0, 0.125, "phase_relative_pi")

with col2:
    if st.session_state.show_toggles or st.session_state.insert_wp:
        st.subheader("Wave Plate (WP)")
        if st.session_state.show_toggles:
            wp_disabled = "insert_wp" in st.session_state.get("disable_keys", [])
            st.checkbox("Insert Wave Plate", key="insert_wp", disabled=wp_disabled)
        if st.session_state.insert_wp:
            create_synced_input(r"WP Fast Axis Angle $\Delta$ (Degrees)", 0.0, 180.0, 0.5, "wp_angle_deg")
            create_synced_input(r"WP Retardance $\Gamma$ ($\times \pi$ rad)", 0.0, 2.0, 0.125, "retardance_pi")
        elif st.session_state.show_toggles:
            st.write("Removed. Vacuum propagation.")

with col3:
    if st.session_state.show_toggles or st.session_state.insert_pol:
        st.subheader("Linear Polarizer")
        if st.session_state.show_toggles:
            pol_disabled = "insert_pol" in st.session_state.get("disable_keys", [])
            st.checkbox("Insert Polarizer", key="insert_pol", disabled=pol_disabled)
        if st.session_state.insert_pol:
            create_synced_input(r"Transmission Axis $\theta$ (Degrees)", 0.0, 180.0, 1.0, "pol_angle_deg")
        elif st.session_state.show_toggles:
            st.write("Removed. Unobstructed beam.")

with col4:
    if st.session_state.show_toggles:
        st.subheader("Visualization Toggles")
        st.checkbox("Combined Wave (Green)", key="show_combined")
        st.checkbox(r"$E_x$", key="show_ex")
        st.checkbox(r"$E_y$", key="show_ey")
        st.checkbox("Show Optical Axes", key="show_axis")
        st.checkbox("Show Poincaré Sphere(s)", key="show_poincare")

# --- 5. VISUALIZATION ---
spatial_title = f"Spatial Propagation"
has_two_spheres = st.session_state.insert_wp or st.session_state.insert_pol

if st.session_state.show_poincare:
    if has_two_spheres:
        incident_title = "Incident State<br>(with WP Operator)" if st.session_state.insert_wp else "Incident State"
        transmitted_title = f"Transmitted State<br>(with Polarizer Operator)<br>(Intensity: {intensity_percent:.1f}%)" if st.session_state.insert_pol else "Transmitted State"
        fig = make_subplots(
            rows=1, cols=3, specs=[[{"type": "scene"}, {"type": "scene"}, {"type": "scene"}]],
            column_widths=[0.3, 0.40, 0.3], subplot_titles=(incident_title, spatial_title, transmitted_title),
        )
        sphere1_col, spatial_col, sphere2_col = 1, 2, 3
    else:
        fig = make_subplots(
            rows=1, cols=2, specs=[[{"type": "scene"}, {"type": "scene"}]],
            column_widths=[0.4, 0.6], subplot_titles=("Polarization State", spatial_title),
        )
        sphere1_col, spatial_col = 1, 2
else:
    fig = make_subplots(rows=1, cols=1, specs=[[{"type": "scene"}]], subplot_titles=(spatial_title,))
    spatial_col = 1

# GHOST TRACE ARCHITECTURE: Always add traces, inject [None] if condition is false
ex_x, ex_y, ex_z = (z, Ex, zeros) if st.session_state.show_ex else ([None], [None], [None])
fig.add_trace(
    go.Scatter3d(x=ex_x, y=ex_y, z=ex_z, mode='lines', line=dict(color='blue', width=3), name='E<sub>x</sub>'), row=1,
    col=spatial_col)

ey_x, ey_y, ey_z = (z, zeros, Ey) if st.session_state.show_ey else ([None], [None], [None])
fig.add_trace(go.Scatter3d(x=ey_x, y=ey_y, z=ey_z, mode='lines', line=dict(color='red', width=3), name='E<sub>y</sub>'),
              row=1, col=spatial_col)

comb_x, comb_y, comb_z = (z, Ex, Ey) if st.session_state.show_combined else ([None], [None], [None])
fig.add_trace(
    go.Scatter3d(x=comb_x, y=comb_y, z=comb_z, mode='lines', line=dict(color='green', width=4), name='Combined'), row=1,
    col=spatial_col)


def draw_optical_element(z_in, z_out, color, name, is_volume=True):
    transverse = [-1.5, 1.5, 1.5, -1.5, -1.5]
    if is_volume:
        x_vol = [z_in, z_in, z_in, z_in, z_out, z_out, z_out, z_out]
        y_vol = [-1.5, 1.5, 1.5, -1.5, -1.5, 1.5, 1.5, -1.5]
        z_vol = [-1.5, -1.5, 1.5, 1.5, -1.5, -1.5, 1.5, 1.5]
        i_idx, j_idx, k_idx = [0, 0, 4, 4, 0, 0, 3, 3, 0, 0, 1, 1], [1, 2, 5, 6, 1, 5, 2, 6, 3, 7, 2, 6], [2, 3, 6, 7,
                                                                                                           5, 4, 6, 7,
                                                                                                           7, 4, 6, 5]
        fig.add_trace(
            go.Mesh3d(x=x_vol, y=y_vol, z=z_vol, i=i_idx, j=j_idx, k=k_idx, color=color, opacity=0.05, name=name),
            row=1, col=spatial_col)
        fig.add_trace(go.Scatter3d(x=[z_in] * 5, y=transverse,
                                   z=[transverse[1], transverse[1], transverse[0], transverse[0], transverse[1]],
                                   mode='lines', line=dict(color='lightblue', width=2), showlegend=False), row=1,
                      col=spatial_col)
        fig.add_trace(go.Scatter3d(x=[z_out] * 5, y=transverse,
                                   z=[transverse[1], transverse[1], transverse[0], transverse[0], transverse[1]],
                                   mode='lines', line=dict(color='lightblue', width=2), showlegend=False), row=1,
                      col=spatial_col)
    else:
        x_vol, y_vol, z_vol = [z_in] * 4, [-1.5, 1.5, 1.5, -1.5], [-1.5, -1.5, 1.5, 1.5]
        fig.add_trace(
            go.Mesh3d(x=x_vol, y=y_vol, z=z_vol, i=[0, 0], j=[1, 2], k=[2, 3], color=color, opacity=0.2, name=name),
            row=1, col=spatial_col)
        fig.add_trace(go.Scatter3d(x=[z_in] * 5, y=transverse,
                                   z=[transverse[1], transverse[1], transverse[0], transverse[0], transverse[1]],
                                   mode='lines', line=dict(color=color, width=3), showlegend=False), row=1,
                      col=spatial_col)


if st.session_state.insert_wp:
    draw_optical_element(z_wp_in, z_wp_out, 'lightblue', 'Wave Plate', True)

    # WP Fast Axis Line
    fa_x, fa_y = ([-1.5 * np.cos(wp_angle), 1.5 * np.cos(wp_angle)],
                  [-1.5 * np.sin(wp_angle), 1.5 * np.sin(wp_angle)]) if st.session_state.show_axis else ([None, None],
                                                                                                         [None, None])
    fig.add_trace(
        go.Scatter3d(x=[z_wp_in, z_wp_in] if fa_x[0] is not None else [None, None], y=fa_x, z=fa_y, mode='lines',
                     line=dict(color='orange', width=5, dash='dash'), name='Fast Axis'), row=1, col=spatial_col)

    # WP Cone
    c_x, c_y, c_z, c_u, c_v, c_w = ([z_wp_in], [fa_x[1]], [fa_y[1]], [0], [np.cos(wp_angle)],
                                    [np.sin(wp_angle)]) if st.session_state.show_axis else ([None], [None], [None],
                                                                                            [None], [None], [None])
    fig.add_trace(
        go.Cone(x=c_x, y=c_y, z=c_z, u=c_u, v=c_v, w=c_w, colorscale=[[0, 'orange'], [1, 'orange']], showscale=False,
                sizemode="absolute", sizeref=0.3, anchor="tail", hoverinfo='skip', showlegend=False), row=1,
        col=spatial_col)

    # WP Dash Dot Axis
    da_x, da_y, da_z = ([z_wp_in, z_wp_in], [0, 1.5], [0, 0]) if st.session_state.show_axis else ([None, None],
                                                                                                  [None, None],
                                                                                                  [None, None])
    fig.add_trace(go.Scatter3d(x=da_x, y=da_y, z=da_z, mode='lines', line=dict(color='gray', dash='dot', width=2),
                               hoverinfo='skip', showlegend=False), row=1, col=spatial_col)

    # WP physical arc
    arc_cond = wp_angle > 0.01 and st.session_state.show_axis
    arc_t = np.linspace(0, wp_angle, 20) if arc_cond else []
    arc_r = 0.6
    arc_x, arc_y, arc_z = ([z_wp_in] * 20, arc_r * np.cos(arc_t), arc_r * np.sin(arc_t)) if arc_cond else ([None],
                                                                                                           [None],
                                                                                                           [None])
    txt_x, txt_y, txt_z, txt_v = ([z_wp_in], [(arc_r + 0.2) * np.cos(wp_angle / 2)],
                                  [(arc_r + 0.2) * np.sin(wp_angle / 2)], ['Δ']) if arc_cond else ([None], [None],
                                                                                                   [None], [''])
    fig.add_trace(
        go.Scatter3d(x=arc_x, y=arc_y, z=arc_z, mode='lines', line=dict(color='orange', width=2), hoverinfo='skip',
                     showlegend=False), row=1, col=spatial_col)
    fig.add_trace(
        go.Scatter3d(x=txt_x, y=txt_y, z=txt_z, mode='text', text=txt_v, textfont=dict(color='orange', size=15),
                     hoverinfo='skip', showlegend=False), row=1, col=spatial_col)

if st.session_state.insert_pol:
    draw_optical_element(z_pol, z_pol, 'cyan', 'Polarizer', False)

    # Pol Fast Axis Line
    ta_x, ta_y = ([-1.5 * np.cos(pol_angle), 1.5 * np.cos(pol_angle)],
                  [-1.5 * np.sin(pol_angle), 1.5 * np.sin(pol_angle)]) if st.session_state.show_axis else ([None, None],
                                                                                                           [None, None])
    fig.add_trace(go.Scatter3d(x=[z_pol, z_pol] if ta_x[0] is not None else [None, None], y=ta_x, z=ta_y, mode='lines',
                               line=dict(color='cyan', width=5), name='Transmission Axis'), row=1, col=spatial_col)

    # Pol Dash Dot Axis
    da_x, da_y, da_z = ([z_pol, z_pol], [0, 1.5], [0, 0]) if st.session_state.show_axis else ([None, None],
                                                                                              [None, None],
                                                                                              [None, None])
    fig.add_trace(go.Scatter3d(x=da_x, y=da_y, z=da_z, mode='lines', line=dict(color='gray', dash='dot', width=2),
                               hoverinfo='skip', showlegend=False), row=1, col=spatial_col)

    # Pol physical arc
    arc_cond = pol_angle > 0.01 and st.session_state.show_axis
    arc_t = np.linspace(0, pol_angle, 20) if arc_cond else []
    arc_r = 0.6
    arc_x, arc_y, arc_z = ([z_pol] * 20, arc_r * np.cos(arc_t), arc_r * np.sin(arc_t)) if arc_cond else ([None], [None],
                                                                                                         [None])
    txt_x, txt_y, txt_z, txt_v = ([z_pol], [(arc_r + 0.2) * np.cos(pol_angle / 2)],
                                  [(arc_r + 0.2) * np.sin(pol_angle / 2)], ['θ']) if arc_cond else ([None], [None],
                                                                                                    [None], [''])
    fig.add_trace(
        go.Scatter3d(x=arc_x, y=arc_y, z=arc_z, mode='lines', line=dict(color='cyan', width=2), hoverinfo='skip',
                     showlegend=False), row=1, col=spatial_col)
    fig.add_trace(go.Scatter3d(x=txt_x, y=txt_y, z=txt_z, mode='text', text=txt_v, textfont=dict(color='cyan', size=15),
                               hoverinfo='skip', showlegend=False), row=1, col=spatial_col)

# Combined Projection
z_final = z_pol if st.session_state.insert_pol else z_wp_out
comb_x_proj, comb_y_proj, comb_z_proj = ([z_end] * len(z[z >= z_final]), Ex[z >= z_final],
                                         Ey[z >= z_final]) if st.session_state.show_combined else ([None], [None],
                                                                                                   [None])
fig.add_trace(
    go.Scatter3d(x=comb_x_proj, y=comb_y_proj, z=comb_z_proj, mode='lines', line=dict(color='magenta', width=3),
                 name='Projection'), row=1, col=spatial_col)

if st.session_state.show_poincare:
    def add_poincare_sphere(fig, row, col, stokes_vec, name_prefix):
        u, v = np.mgrid[0:2 * np.pi:30j, 0:np.pi:15j]
        fig.add_trace(
            go.Surface(x=np.cos(u) * np.sin(v), y=np.sin(u) * np.sin(v), z=np.cos(v), colorscale='Greys', opacity=0.1,
                       showscale=False, hoverinfo='skip'), row=row, col=col)
        fig.add_trace(go.Scatter3d(x=[-1.15, 1.15, None, 0, 0, None, 0, 0], y=[0, 0, None, -1.15, 1.15, None, 0, 0],
                                   z=[0, 0, None, 0, 0, None, -1.15, 1.15], mode='lines',
                                   line=dict(color='lightgray', width=2, dash='dot'), hoverinfo='skip',
                                   showlegend=False), row=row, col=col)

        cone_args = dict(colorscale=[[0, 'lightgray'], [1, 'lightgray']], showscale=False, sizemode="absolute",
                         sizeref=0.1, anchor="tail", hoverinfo='skip', showlegend=False)
        fig.add_trace(go.Cone(x=[1.15], y=[0], z=[0], u=[1], v=[0], w=[0], **cone_args), row=row, col=col)
        fig.add_trace(go.Cone(x=[0], y=[1.15], z=[0], u=[0], v=[1], w=[0], **cone_args), row=row, col=col)
        fig.add_trace(go.Cone(x=[0], y=[0], z=[1.15], u=[0], v=[0], w=[1], **cone_args), row=row, col=col)

        eq_t = np.linspace(0, 2 * np.pi, 100)
        fig.add_trace(go.Scatter3d(x=np.cos(eq_t), y=np.sin(eq_t), z=np.zeros_like(eq_t), mode='lines',
                                   line=dict(color='gray', width=2, dash='dot'), hoverinfo='skip', showlegend=False),
                      row=row, col=col)

        ref_labels = ['<b>J</b><sub>H</sub> ↔', '<b>J</b><sub>V</sub> ↕', '<b>J</b><sub>D</sub> ⤢',
                      '<b>J</b><sub>A</sub> ⤡', '<b>J</b><sub>R</sub> ↻', '<b>J</b><sub>L</sub> ↺']
        ref_x, ref_y, ref_z = [1.25, -1.25, 0, 0, 0, 0], [0, 0, 1.25, -1.25, 0, 0], [0, 0, 0, 0, 1.25, -1.25]
        fig.add_trace(go.Scatter3d(x=ref_x, y=ref_y, z=ref_z, mode='markers+text', marker=dict(color='gray', size=1),
                                   text=ref_labels, textposition='middle center', textfont=dict(size=14),
                                   hoverinfo='skip', showlegend=False), row=row, col=col)

        fig.add_trace(go.Scatter3d(x=[0, stokes_vec[0]], y=[0, stokes_vec[1]], z=[0, stokes_vec[2]], mode='lines',
                                   line=dict(color='green', width=4), hoverinfo='skip', showlegend=False), row=row,
                      col=col)

        stokes_norm = np.linalg.norm(stokes_vec)
        c_x, c_y, c_z, c_u, c_v, c_w = ([stokes_vec[0]], [stokes_vec[1]], [stokes_vec[2]],
                                        [stokes_vec[0] / stokes_norm], [stokes_vec[1] / stokes_norm],
                                        [stokes_vec[2] / stokes_norm]) if stokes_norm > 1e-4 else ([None], [None],
                                                                                                   [None], [None],
                                                                                                   [None], [None])
        fig.add_trace(
            go.Cone(x=c_x, y=c_y, z=c_z, u=c_u, v=c_v, w=c_w, colorscale=[[0, 'green'], [1, 'green']], showscale=False,
                    sizemode="absolute", sizeref=0.15, anchor="tip", hoverinfo='skip', showlegend=False), row=row,
            col=col)


    if has_two_spheres:
        add_poincare_sphere(fig, row=1, col=sphere1_col, stokes_vec=S_in, name_prefix="Incident")
        add_poincare_sphere(fig, row=1, col=sphere2_col, stokes_vec=S_out, name_prefix="Transmitted")

        if st.session_state.insert_wp:
            n_x, n_y = np.cos(2 * wp_angle), np.sin(2 * wp_angle)
            fig.add_trace(go.Scatter3d(x=[-n_x * 1.15, n_x * 1.15], y=[-n_y * 1.15, n_y * 1.15], z=[0, 0], mode='lines',
                                       line=dict(color='orange', width=4, dash='dash'), hoverinfo='skip',
                                       showlegend=False), row=1, col=sphere1_col)
            fig.add_trace(go.Cone(x=[n_x * 1.15], y=[n_y * 1.15], z=[0], u=[n_x], v=[n_y], w=[0],
                                  colorscale=[[0, 'orange'], [1, 'orange']], showscale=False, sizemode="absolute",
                                  sizeref=0.15, anchor="tail", hoverinfo='skip', showlegend=False), row=1,
                          col=sphere1_col)

            # WP Arc Poincare
            arc_cond = wp_angle > 0.01
            arc_t2 = np.linspace(0, 2 * wp_angle, 30) if arc_cond else []
            arc_r2 = 0.6
            a_x, a_y, a_z = (arc_r2 * np.cos(arc_t2), arc_r2 * np.sin(arc_t2), np.zeros_like(arc_t2)) if arc_cond else (
                [None], [None], [None])
            t_x, t_y, t_z, t_v = ([(arc_r2 + 0.2) * np.cos(wp_angle)], [(arc_r2 + 0.2) * np.sin(wp_angle)], [0],
                                  ['2Δ']) if arc_cond else ([None], [None], [None], [''])
            fig.add_trace(
                go.Scatter3d(x=a_x, y=a_y, z=a_z, mode='lines', line=dict(color='orange', width=3), hoverinfo='skip',
                             showlegend=False), row=1, col=sphere1_col)
            fig.add_trace(
                go.Scatter3d(x=t_x, y=t_y, z=t_z, mode='text', text=t_v, textfont=dict(color='orange', size=15),
                             hoverinfo='skip', showlegend=False), row=1, col=sphere1_col)

            # Retardance Arc Poincare
            ret_cond = retardance > 0
            center = np.array([n_x, n_y, 0]) * 1.15
            e1, e2 = np.array([-n_y, n_x, 0]), np.array([0, 0, 1])
            arc_t = np.linspace(0, retardance, 40) if ret_cond else []
            radius = 0.25
            r_x, r_y, r_z = (center[0] + radius * (np.cos(arc_t) * e1[0] + np.sin(arc_t) * e2[0]),
                             center[1] + radius * (np.cos(arc_t) * e1[1] + np.sin(arc_t) * e2[1]),
                             center[2] + radius * (np.cos(arc_t) * e1[2] + np.sin(arc_t) * e2[2])) if ret_cond else (
                [None], [None], [None])
            u_dir, v_dir, w_dir = (radius * (-np.sin(retardance) * e1[0] + np.cos(retardance) * e2[0]),
                                   radius * (-np.sin(retardance) * e1[1] + np.cos(retardance) * e2[1]), radius * (
                                               -np.sin(retardance) * e1[2] + np.cos(retardance) * e2[
                                           2])) if ret_cond else (0, 0, 0)
            c_x, c_y, c_z, c_u, c_v, c_w = ([r_x[-1]], [r_y[-1]], [r_z[-1]], [u_dir], [v_dir],
                                            [w_dir]) if ret_cond else ([None], [None], [None], [None], [None], [None])
            t_x, t_y, t_z, t_v = ([r_x[-1]], [r_y[-1]], [r_z[-1]],
                                  [f"Γ = {st.session_state.retardance_pi:.2f}π"]) if ret_cond else ([None], [None],
                                                                                                    [None], [''])

            fig.add_trace(go.Scatter3d(x=r_x, y=r_y, z=r_z, mode='lines', line=dict(color='darkorange', width=4),
                                       hoverinfo='skip', showlegend=False), row=1, col=sphere1_col)
            fig.add_trace(
                go.Cone(x=c_x, y=c_y, z=c_z, u=c_u, v=c_v, w=c_w, colorscale=[[0, 'darkorange'], [1, 'darkorange']],
                        showscale=False, sizemode="absolute", sizeref=0.1, anchor="tip", hoverinfo='skip',
                        showlegend=False), row=1, col=sphere1_col)
            fig.add_trace(go.Scatter3d(x=t_x, y=t_y, z=t_z, mode='text', text=t_v, textposition='top right',
                                       textfont=dict(color='darkorange', size=15), hoverinfo='skip', showlegend=False),
                          row=1, col=sphere1_col)

        if st.session_state.insert_pol:
            fig.add_trace(go.Scatter3d(x=[0, S_pol_axis[0]], y=[0, S_pol_axis[1]], z=[0, S_pol_axis[2]], mode='lines',
                                       line=dict(width=4, dash='dashdot'), hoverinfo='skip', showlegend=False), row=1,
                          col=sphere2_col)
            fig.add_trace(go.Scatter3d(x=[S_pol_axis[0]], y=[S_pol_axis[1]], z=[S_pol_axis[2]], mode='text',
                                       text=[f"Pol ({intensity_percent:.0f}%)<br>"], textposition='top center',
                                       textfont=dict(size=15), hoverinfo='skip', showlegend=False), row=1,
                          col=sphere2_col)
            fig.add_trace(
                go.Scatter3d(x=[S_out[0], S_pol_axis[0]], y=[S_out[1], S_pol_axis[1]], z=[S_out[2], S_pol_axis[2]],
                             mode='lines', line=dict(color='rgba(255, 255, 255, 0.4)', width=2, dash='dot'),
                             hoverinfo='skip', showlegend=False), row=1, col=sphere2_col)

            # Pol Arc Poincare
            arc_cond = pol_angle > 0.01
            arc_t2 = np.linspace(0, 2 * pol_angle, 30) if arc_cond else []
            arc_r2 = 0.6
            a_x, a_y, a_z = (arc_r2 * np.cos(arc_t2), arc_r2 * np.sin(arc_t2), np.zeros_like(arc_t2)) if arc_cond else (
                [None], [None], [None])
            t_x, t_y, t_z, t_v = ([(arc_r2 + 0.2) * np.cos(pol_angle)], [(arc_r2 + 0.2) * np.sin(pol_angle)], [0],
                                  ['2θ']) if arc_cond else ([None], [None], [None], [''])
            fig.add_trace(
                go.Scatter3d(x=a_x, y=a_y, z=a_z, mode='lines', line=dict(color='cyan', width=3), hoverinfo='skip',
                             showlegend=False), row=1, col=sphere2_col)
            fig.add_trace(go.Scatter3d(x=t_x, y=t_y, z=t_z, mode='text', text=t_v, textfont=dict(color='cyan', size=15),
                                       hoverinfo='skip', showlegend=False), row=1, col=sphere2_col)

    else:
        add_poincare_sphere(fig, row=1, col=sphere1_col, stokes_vec=S_in, name_prefix="Incident")

# --- Global Layout Formatting ---

# CAMERA GATEKEEPER: Only send the default camera dict when initializing a brand new step!
current_step_id = f"step_{st.session_state.current_step}"
camera_init_key = f"camera_init_{current_step_id}"

scene_spatial_config = dict(
    xaxis=dict(title='Propagation (z)', range=[z_start, z_end]),
    yaxis=dict(title='E<sub>x</sub>', range=[-1.5, 1.5]),
    zaxis=dict(title='E<sub>y</sub>', range=[-1.5, 1.5]),
    aspectratio=dict(x=4 if st.session_state.insert_pol else 3, y=1, z=1),
    uirevision=current_step_id
)

scene_poincare_config = dict(
    xaxis=dict(title='', range=[-1.2, 1.2], showticklabels=False, showgrid=False, zeroline=False),
    yaxis=dict(title='', range=[-1.2, 1.2], showticklabels=False, showgrid=False, zeroline=False),
    zaxis=dict(title='', range=[-1.2, 1.2], showticklabels=False, showgrid=False, zeroline=False),
    aspectratio=dict(x=1, y=1, z=1),
    uirevision=current_step_id
)

# Apply default camera ONLY on the first render of a new step.
if camera_init_key not in st.session_state:
    st.session_state[camera_init_key] = True
    scene_spatial_config['camera'] = dict(eye=dict(x=1.2, y=-3.8, z=1.2))
    scene_poincare_config['camera'] = dict(eye=dict(x=1.5, y=1.5, z=1.5))

for annotation in fig['layout']['annotations']:
    annotation['yshift'] = -100

layout_args = dict(
    height=700 if st.session_state.show_poincare else 500,
    margin=dict(l=10, r=10, b=10, t=40),
    uirevision=current_step_id
)

if st.session_state.show_poincare:
    if has_two_spheres:
        layout_args['scene'] = scene_poincare_config
        layout_args['scene2'] = scene_spatial_config
        layout_args['scene3'] = scene_poincare_config
    else:
        layout_args['scene'] = scene_poincare_config
        layout_args['scene2'] = scene_spatial_config
else:
    layout_args['scene'] = scene_spatial_config

fig.update_layout(**layout_args)

plot_config = {
    'toImageButtonOptions': {'format': 'png', 'filename': 'polarization_state', 'height': 1080, 'width': 1920,
                             'scale': 2},
    'displayModeBar': True,
    'displaylogo': False
}

st.plotly_chart(fig, use_container_width=True, config=plot_config)

# --- 6. NAVIGATION, HINT, & EXPLANATION BOXES (BOTTOM) ---

if st.session_state.show_hint and "hint" in step_data:
    processed_hint = process_math(step_data.get("hint", ""))
    st.markdown(
        f"<div style='background-color: #e8f5e9; color: black; padding: 15px; border-radius: 8px; font-size: 15px; border: 2px solid #4caf50; margin-bottom: 15px;'><b>💡 Hint:</b> {processed_hint}</div>",
        unsafe_allow_html=True)

if target_met and "explanation" in step_data and step_data["explanation"]:
    processed_explanation = process_math(step_data.get("explanation", ""))
    st.markdown(
        f"<div style='background-color: #e3f2fd; color: black; padding: 20px; border-radius: 8px; font-size: 16px; border: 2px solid #2196f3; margin-bottom: 15px;'><div style='line-height: 1.6;'>🎓 <b>Correct! </b> {processed_explanation}</div></div>",
        unsafe_allow_html=True)

# --- ROUTING BUTTON LOGIC ---
if is_last_step and st.session_state.current_challenge != "Free Play":
    st.divider()
    st.markdown("### 🎓 Unit Complete")
    st.markdown("Please click the button below to return to the survey and complete the final questions.")

    limesurvey_domain = "https://your-university-domain.limesurvey.net"
    survey_b_id = "123456"
    pid = st.session_state.participant_id
    journey = st.session_state.assigned_journey
    et = st.session_state.et_status

    return_url = f"{limesurvey_domain}/index.php/{survey_b_id}?pid={pid}&journey={journey}&et={et}"

    st.link_button("🚀 Return to Post-Test Survey", return_url, type="primary", use_container_width=True)

elif not is_last_step:
    st.markdown("<br>", unsafe_allow_html=True)
    col_btn_hint, col_btn_next, _spacer, col_btn_solve = st.columns([1.5, 1.5, 5.5, 1.5])

    with col_btn_hint:
        if "hint" in step_data:
            btn_text = "💡 Hide Hint" if st.session_state.show_hint else "💡 Show Hint"
            st.button(btn_text, on_click=toggle_hint, use_container_width=True)

    with col_btn_next:
        st.button("👣 Next Step ➔", disabled=not target_met, on_click=next_step, use_container_width=True)

    with col_btn_solve:
        if "solution" in step_data:
            st.button("✅ Show Solution", on_click=solve_challenge, use_container_width=True)