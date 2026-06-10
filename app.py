import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import re
from challenges import CHALLENGES
from latex2mathml.converter import convert as latex_to_mathml

st.set_page_config(page_title="Interactive Polarization Challenges", layout="wide")

# --- 1. SESSION STATE & TUTORIAL ENGINE ---
DEFAULTS = {
    "E_x_amp": 0.707, "phase_relative_pi": 0.0,
    "insert_wp": True, "wp_angle_deg": 45.0, "retardance_pi": 0.5,
    "insert_pol": False, "pol_angle_deg": 90.0,
    "show_combined": True, "show_ex": True, "show_ey": True, "show_axis": True,
    "show_poincare": True,
    "show_hint": False,
    "show_toggles": True  # Controls visibility of insertion and visual toggles
}

for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v


def load_step_setup(challenge_name, step_index):
    step_data = CHALLENGES[challenge_name]["steps"][step_index]
    for k, v in step_data.get("setup", {}).items():
        st.session_state[k] = v


if "tutorial_initialized" not in st.session_state:
    st.session_state.tutorial_initialized = True
    st.session_state.current_challenge = list(CHALLENGES.keys())[0]
    st.session_state.current_step = 0
    load_step_setup(st.session_state.current_challenge, 0)


def reset_challenge():
    st.session_state.current_step = 0
    st.session_state.show_hint = False
    load_step_setup(st.session_state.current_challenge, 0)


def next_step():
    st.session_state.current_step += 1
    st.session_state.show_hint = False
    load_step_setup(st.session_state.current_challenge, st.session_state.current_step)


def toggle_hint():
    st.session_state.show_hint = not st.session_state.show_hint


def solve_challenge():
    """Resets the step to its baseline setup, then applies the solution parameters."""
    challenge_name = st.session_state.current_challenge
    step_index = st.session_state.current_step
    step_data = CHALLENGES[challenge_name]["steps"][step_index]

    # 1. Reset the board to undo any incorrect user meddling
    load_step_setup(challenge_name, step_index)

    # 2. Apply the specific solution over the clean board
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
st.title("Electromagnetic Wave Propagation & State Space")

col_chal, col_step = st.columns([1, 3])
with col_chal:
    st.selectbox("Select Mode / Challenge:", list(CHALLENGES.keys()),
                 key="current_challenge", on_change=reset_challenge)

challenge_data = CHALLENGES[st.session_state.current_challenge]["steps"]
step_data = challenge_data[st.session_state.current_step]
is_last_step = st.session_state.current_step >= len(challenge_data) - 1


def process_math(text):
    """Robustly parses LaTeX. Handles $$ block equations and $ inline equations safely."""
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

    # Extract block math first, then inline math
    text = re.sub(r'\$\$(.*?)\$\$', replace_block, text, flags=re.DOTALL)
    text = re.sub(r'\$(.*?)\$', replace_inline, text, flags=re.DOTALL)
    return text


processed_text = process_math(step_data.get('text', ''))
processed_task = process_math(step_data.get('task', ''))

# 1. Explanation Box (Yellow)
if processed_text:
    st.markdown(
        f"""
        <div style="background-color: #fff9c4; color: black; padding: 20px; 
                    border-radius: 8px; font-size: 16px; border: 2px solid #fbc02d; margin-bottom: 15px;">
            <div style="line-height: 1.6;">📖 {processed_text}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# 2. Task Box (Darker Orange)
if processed_task:
    st.markdown(
        f"""
        <div style="background-color: #ffe0b2; color: black; padding: 15px; 
                    border-radius: 8px; font-size: 16px; border: 2px solid #ff9800; margin-bottom: 15px;">
            <div style="line-height: 1.6;">🎯 <b>Task:</b> {processed_task}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# 3. Hint Box (Green)
if st.session_state.show_hint and "hint" in step_data:
    processed_hint = process_math(step_data.get("hint", ""))
    st.markdown(
        f"""
        <div style="background-color: #e8f5e9; color: black; padding: 15px; 
                    border-radius: 8px; font-size: 15px; border: 2px solid #4caf50; margin-bottom: 15px;">
            <b>💡 Hint:</b> {processed_hint}
        </div>
        """,
        unsafe_allow_html=True
    )

target_met = check_target_met(step_data.get("target", {}), derived_state)

if not is_last_step:
    # Set up layout for top inline buttons (without the solve button)
    col_btn_hint, col_btn_next, _spacer = st.columns([1.2, 1.8, 7.])

    with col_btn_hint:
        if "hint" in step_data:
            # Keep the emoji on BOTH states so the baseline alignment
            # and button height don't jump when clicked!
            btn_text = "💡 Hide Hint" if st.session_state.show_hint else "💡 Show Hint"

            # use_container_width forces it to center nicely in the column
            st.button(btn_text, on_click=toggle_hint, use_container_width=True)

    with col_btn_next:
        st.button("👣 Next Step ➔", disabled=not target_met, on_click=next_step)

elif st.session_state.current_challenge != "Free Play":
    st.success("Challenge Completed!")

st.divider()

# --- 4. UI: SLIDERS & CONTROLS ---
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

with col1:
    st.subheader(r"Incident Wave")
    st.write(r"$\vec{E} = \begin{pmatrix} E_x \\ E_y e^{i\varphi} \end{pmatrix}$")
    st.slider(r"Amplitude $E_x$", 0.0, 1.0, step=0.01, key="E_x_amp")
    st.write(fr"$E_y=$ {np.sqrt(1.0 - st.session_state.E_x_amp ** 2):.3f}")
    st.slider(r"Relative Phase $\varphi$ ($\times\pi$ rad)", 0.0, 2.0, step=0.125, key="phase_relative_pi")

with col2:
    if st.session_state.show_toggles or st.session_state.insert_wp:
        st.subheader("Wave Plate (WP)")

        if st.session_state.show_toggles:
            st.checkbox("Insert Wave Plate", key="insert_wp")

        if st.session_state.insert_wp:
            st.slider("WP Fast Axis Angle (Degrees)", 0.0, 180.0, step=0.5, key="wp_angle_deg")
            st.slider(r"WP Retardance $\Gamma$ ($\times \pi$ rad)", 0.0, 2.0, step=0.125, key="retardance_pi")
        elif st.session_state.show_toggles:
            st.write("Removed. Vacuum propagation.")

with col3:
    if st.session_state.show_toggles or st.session_state.insert_pol:
        st.subheader("Linear Polarizer")

        if st.session_state.show_toggles:
            st.checkbox("Insert Polarizer", key="insert_pol")

        if st.session_state.insert_pol:
            st.slider("Transmission Axis (Degrees)", 0.0, 180.0, step=1.0, key="pol_angle_deg")
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
spatial_title = f"Spatial Propagation<br>(Intensity: {intensity_percent:.1f}%)" if st.session_state.insert_pol else "Spatial Propagation"

has_two_spheres = st.session_state.insert_wp or st.session_state.insert_pol

if st.session_state.show_poincare:
    if has_two_spheres:
        incident_title = "Incident State<br>(with WP Operator)" if st.session_state.insert_wp else "Incident State"
        transmitted_title = "Transmitted State<br>(with Polarizer Operator)" if st.session_state.insert_pol else "Transmitted State"
        fig = make_subplots(
            rows=1, cols=3,
            specs=[[{"type": "scene"}, {"type": "scene"}, {"type": "scene"}]],
            column_widths=[0.2, 0.60, 0.2],
            subplot_titles=(incident_title, spatial_title, transmitted_title),
        )
        sphere1_col = 1
        spatial_col = 2
        sphere2_col = 3
    else:
        fig = make_subplots(
            rows=1, cols=2,
            specs=[[{"type": "scene"}, {"type": "scene"}]],
            column_widths=[0.2, 0.8],
            subplot_titles=("Incident State", spatial_title),
        )
        sphere1_col = 1
        spatial_col = 2
else:
    fig = make_subplots(
        rows=1, cols=1,
        specs=[[{"type": "scene"}]],
        subplot_titles=(spatial_title,)
    )
    spatial_col = 1

if st.session_state.show_combined:
    fig.add_trace(go.Scatter3d(x=z, y=Ex, z=Ey, mode='lines', line=dict(color='green', width=4), name='Combined Wave'),
                  row=1, col=spatial_col)
if st.session_state.show_ex:
    fig.add_trace(
        go.Scatter3d(x=z, y=Ex, z=zeros, mode='lines', line=dict(color='blue', width=3),
                     name='E<sub>x</sub> Component'),
        row=1, col=spatial_col)
if st.session_state.show_ey:
    fig.add_trace(
        go.Scatter3d(x=z, y=zeros, z=Ey, mode='lines', line=dict(color='red', width=3), name='E<sub>y</sub> Component'),
        row=1, col=spatial_col)


def draw_optical_element(z_in, z_out, color, name, is_volume=True):
    transverse = [-1.5, 1.5, 1.5, -1.5, -1.5]
    if is_volume:
        x_vol = [z_in, z_in, z_in, z_in, z_out, z_out, z_out, z_out]
        y_vol = [-1.5, 1.5, 1.5, -1.5, -1.5, 1.5, 1.5, -1.5]
        z_vol = [-1.5, -1.5, 1.5, 1.5, -1.5, -1.5, 1.5, 1.5]
        i_idx = [0, 0, 4, 4, 0, 0, 3, 3, 0, 0, 1, 1]
        j_idx = [1, 2, 5, 6, 1, 5, 2, 6, 3, 7, 2, 6]
        k_idx = [2, 3, 6, 7, 5, 4, 6, 7, 7, 4, 6, 5]
        fig.add_trace(
            go.Mesh3d(x=x_vol, y=y_vol, z=z_vol, i=i_idx, j=j_idx, k=k_idx, color=color, opacity=0.05, name=name),
            row=1, col=spatial_col)
        fig.add_trace(go.Scatter3d(x=[z_in] * 5, y=transverse,
                                   z=[transverse[1], transverse[1], transverse[0], transverse[0], transverse[1]],
                                   mode='lines', line=dict(color='gray', width=2), showlegend=False), row=1,
                      col=spatial_col)
        fig.add_trace(go.Scatter3d(x=[z_out] * 5, y=transverse,
                                   z=[transverse[1], transverse[1], transverse[0], transverse[0], transverse[1]],
                                   mode='lines', line=dict(color='gray', width=2), showlegend=False), row=1,
                      col=spatial_col)
    else:
        x_vol = [z_in, z_in, z_in, z_in]
        y_vol = [-1.5, 1.5, 1.5, -1.5]
        z_vol = [-1.5, -1.5, 1.5, 1.5]
        fig.add_trace(
            go.Mesh3d(x=x_vol, y=y_vol, z=z_vol, i=[0, 0], j=[1, 2], k=[2, 3], color=color, opacity=0.2, name=name),
            row=1, col=spatial_col)
        fig.add_trace(go.Scatter3d(x=[z_in] * 5, y=transverse,
                                   z=[transverse[1], transverse[1], transverse[0], transverse[0], transverse[1]],
                                   mode='lines', line=dict(color=color, width=3), showlegend=False), row=1,
                      col=spatial_col)


if st.session_state.insert_wp:
    draw_optical_element(z_wp_in, z_wp_out, 'white', 'Wave Plate', True)
    if st.session_state.show_axis:
        fa_x = [-1.5 * np.cos(wp_angle), 1.5 * np.cos(wp_angle)]
        fa_y = [-1.5 * np.sin(wp_angle), 1.5 * np.sin(wp_angle)]
        fig.add_trace(go.Scatter3d(x=[z_wp_in, z_wp_in], y=fa_x, z=fa_y, mode='lines',
                                   line=dict(color='orange', width=5, dash='dash'), name='Fast Axis'), row=1,
                      col=spatial_col)

if st.session_state.insert_pol:
    draw_optical_element(z_pol, z_pol, 'cyan', 'Polarizer', False)
    if st.session_state.show_axis:
        ta_x = [-1.5 * np.cos(pol_angle), 1.5 * np.cos(pol_angle)]
        ta_y = [-1.5 * np.sin(pol_angle), 1.5 * np.sin(pol_angle)]
        fig.add_trace(go.Scatter3d(x=[z_pol, z_pol], y=ta_x, z=ta_y, mode='lines', line=dict(color='cyan', width=5),
                                   name='Transmission Axis'), row=1, col=spatial_col)

if st.session_state.show_combined:
    z_final = z_pol if st.session_state.insert_pol else z_wp_out
    fig.add_trace(go.Scatter3d(x=[z_end] * len(z[z >= z_final]), y=Ex[z >= z_final], z=Ey[z >= z_final], mode='lines',
                               line=dict(color='magenta', width=3), name='Final Polarization'), row=1, col=spatial_col)

if st.session_state.show_poincare:
    def add_poincare_sphere(fig, row, col, stokes_vec, name_prefix):
        u, v = np.mgrid[0:2 * np.pi:30j, 0:np.pi:15j]
        fig.add_trace(
            go.Surface(x=np.cos(u) * np.sin(v), y=np.sin(u) * np.sin(v), z=np.cos(v), colorscale='Greys', opacity=0.1,
                       showscale=False, hoverinfo='skip'), row=row, col=col)

        eq_t = np.linspace(0, 2 * np.pi, 100)
        fig.add_trace(go.Scatter3d(x=np.cos(eq_t), y=np.sin(eq_t), z=np.zeros_like(eq_t), mode='lines',
                                   line=dict(color='gray', width=2, dash='dot'), hoverinfo='skip', showlegend=False),
                      row=row, col=col)

        ref_labels = ['H ↔', 'V ↕', 'D ⤢', 'A ⤡', 'R ↻', 'L ↺']
        ref_x, ref_y, ref_z = [1, -1, 0, 0, 0, 0], [0, 0, 1, -1, 0, 0], [0, 0, 0, 0, 1, -1]
        fig.add_trace(go.Scatter3d(x=ref_x, y=ref_y, z=ref_z, mode='markers+text', marker=dict(color='gray', size=3),
                                   text=ref_labels, textposition='bottom center', textfont=dict(size=13),
                                   hoverinfo='skip', showlegend=False), row=row, col=col)

        fig.add_trace(go.Scatter3d(x=[0, stokes_vec[0]], y=[0, stokes_vec[1]], z=[0, stokes_vec[2]], mode='lines',
                                   line=dict(color='cyan', width=4), hoverinfo='skip', showlegend=False), row=row,
                      col=col)
        fig.add_trace(go.Scatter3d(x=[stokes_vec[0]], y=[stokes_vec[1]], z=[stokes_vec[2]], mode='markers',
                                   marker=dict(color='magenta', size=8), hoverinfo='skip', showlegend=False), row=row,
                      col=col)


    if has_two_spheres:
        add_poincare_sphere(fig, row=1, col=sphere1_col, stokes_vec=S_in, name_prefix="Incident")
        add_poincare_sphere(fig, row=1, col=sphere2_col, stokes_vec=S_out, name_prefix="Transmitted")

        if st.session_state.insert_wp:
            n_x, n_y = np.cos(2 * wp_angle), np.sin(2 * wp_angle)
            fig.add_trace(go.Scatter3d(x=[-n_x * 1.1, n_x * 1.2], y=[-n_y * 1.1, n_y * 1.2], z=[0, 0], mode='lines',
                                       line=dict(color='orange', width=4, dash='dash'), hoverinfo='skip',
                                       showlegend=False),
                          row=1, col=sphere1_col)

            if retardance > 0:
                center = np.array([n_x, n_y, 0]) * 1.15
                e1, e2 = np.array([-n_y, n_x, 0]), np.array([0, 0, 1])
                arc_t = np.linspace(0, retardance, 40)
                radius = 0.25
                arc_x = center[0] + radius * (np.cos(arc_t) * e1[0] + np.sin(arc_t) * e2[0])
                arc_y = center[1] + radius * (np.cos(arc_t) * e1[1] + np.sin(arc_t) * e2[1])
                arc_z = center[2] + radius * (np.cos(arc_t) * e1[2] + np.sin(arc_t) * e2[2])

                fig.add_trace(go.Scatter3d(x=arc_x, y=arc_y, z=arc_z, mode='lines', line=dict(color='gold', width=4),
                                           hoverinfo='skip', showlegend=False), row=1, col=sphere1_col)

                u_dir = radius * (-np.sin(retardance) * e1[0] + np.cos(retardance) * e2[0])
                v_dir = radius * (-np.sin(retardance) * e1[1] + np.cos(retardance) * e2[1])
                w_dir = radius * (-np.sin(retardance) * e1[2] + np.cos(retardance) * e2[2])
                fig.add_trace(go.Cone(x=[arc_x[-1]], y=[arc_y[-1]], z=[arc_z[-1]], u=[u_dir], v=[v_dir], w=[w_dir],
                                      colorscale=[[0, 'gold'], [1, 'gold']], showscale=False, sizemode="absolute",
                                      sizeref=0.1, anchor="tail", hoverinfo='skip', showlegend=False), row=1,
                              col=sphere1_col)
                fig.add_trace(go.Scatter3d(x=[arc_x[-1]], y=[arc_y[-1]], z=[arc_z[-1]], mode='text',
                                           text=[f"Γ = {st.session_state.retardance_pi:.2f}π"],
                                           textposition='top right',
                                           textfont=dict(color='gold', size=12), hoverinfo='skip', showlegend=False),
                              row=1, col=sphere1_col)

        if st.session_state.insert_pol:
            fig.add_trace(go.Scatter3d(x=[0, S_pol_axis[0]], y=[0, S_pol_axis[1]], z=[0, S_pol_axis[2]], mode='lines',
                                       line=dict(color='white', width=4, dash='dashdot'), hoverinfo='skip',
                                       showlegend=False), row=1, col=sphere2_col)
            fig.add_trace(go.Scatter3d(x=[S_pol_axis[0]], y=[S_pol_axis[1]], z=[S_pol_axis[2]], mode='markers+text',
                                       marker=dict(color='white', size=6), text=[f"Pol ({intensity_percent:.0f}%)<br>"],
                                       textposition='top center', textfont=dict(color='white', size=12),
                                       hoverinfo='skip',
                                       showlegend=False), row=1, col=sphere2_col)
            fig.add_trace(
                go.Scatter3d(x=[S_out[0], S_pol_axis[0]], y=[S_out[1], S_pol_axis[1]], z=[S_out[2], S_pol_axis[2]],
                             mode='lines', line=dict(color='rgba(255, 255, 255, 0.4)', width=2, dash='dot'),
                             hoverinfo='skip', showlegend=False), row=1, col=sphere2_col)

    else:
        add_poincare_sphere(fig, row=1, col=sphere1_col, stokes_vec=S_in, name_prefix="Incident")

# --- Global Layout Formatting ---
scene_spatial_config = dict(
    xaxis=dict(title='Propagation (z)', range=[z_start, z_end]),
    yaxis=dict(title='E<sub>x</sub>', range=[-1.5, 1.5]),
    zaxis=dict(title='E<sub>y</sub>', range=[-1.5, 1.5]),
    aspectratio=dict(x=4 if st.session_state.insert_pol else 3, y=1, z=1),
    camera=dict(eye=dict(x=1.2, y=-3.8, z=1.2))
)

scene_poincare_config = dict(
    xaxis=dict(title='', range=[-1.2, 1.2], showticklabels=False, showgrid=False, zeroline=False),
    yaxis=dict(title='', range=[-1.2, 1.2], showticklabels=False, showgrid=False, zeroline=False),
    zaxis=dict(title='', range=[-1.2, 1.2], showticklabels=False, showgrid=False, zeroline=False),
    aspectratio=dict(x=1, y=1, z=1),
    camera=dict(eye=dict(x=2.8, y=2.8, z=2.8))
)

for annotation in fig['layout']['annotations']:
    annotation['yshift'] = -100

layout_args = dict(
    height=700 if st.session_state.show_poincare else 500,
    margin=dict(l=10, r=10, b=10, t=40),
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
    'toImageButtonOptions': {
        'format': 'png',
        'filename': 'polarization_state',
        'height': 1080,
        'width': 1920,
        'scale': 2
    },
    'displayModeBar': True,
    'displaylogo': False
}

st.plotly_chart(fig, use_container_width=True, config=plot_config)

# --- 6. SOLUTION BUTTON (BOTTOM LEFT) ---
if not is_last_step and "solution" in step_data:
    st.markdown("<br>", unsafe_allow_html=True)
    col_bottom_btn, _ = st.columns([1.5, 8.5])
    with col_bottom_btn:
        st.button("✅ Show Solution", on_click=solve_challenge, use_container_width=True)