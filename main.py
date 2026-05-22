import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Wave Plate & Polarizer Applet", layout="wide")
st.title("Electromagnetic Wave Propagation, Wave Plates, & Projection")

# --- UI Controls ---
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

with col1:
    st.subheader("Incident Wave")
    E_x_amp = st.slider("Amplitude (X direction)", 0.0, 1.0, 0.707, step=0.01)
    E_y_amp = np.sqrt(1.0 - E_x_amp ** 2)
    st.write(f"*Calculated Y Amp:* {E_y_amp:.3f}")
    # Displayed as multiple of pi for readability
    phase_relative_pi = st.slider("Relative Phase (×π rad)", 0.0, 2.0, 0.5, step=0.125)
    phase_relative = phase_relative_pi * np.pi

with col2:
    st.subheader("Wave Plate")
    insert_wp = st.checkbox("Insert Wave Plate", value=True)
    if insert_wp:
        # Mechanical angles stay in degrees
        wp_angle_deg = st.slider("WP Fast Axis (Degrees)", 0.0, 180.0, 45.0, step=1.0)
        # Retardance in fractions of pi
        retardance_pi = st.slider("WP Retardance (×π rad)", 0.0, 2.0, 0.5, step=0.125)
        retardance = retardance_pi * np.pi
    else:
        st.write("Removed. Vacuum propagation.")
        wp_angle_deg = 0.0
        retardance = 0.0
        retardance_pi = 0.0
    wp_angle = np.deg2rad(wp_angle_deg)

with col3:
    st.subheader("Linear Polarizer")
    insert_pol = st.checkbox("Insert Polarizer", value=True)
    if insert_pol:
        # Mechanical angles stay in degrees
        pol_angle_deg = st.slider("Transmission Axis (Degrees)", 0.0, 180.0, 90.0, step=1.0)
    else:
        st.write("Removed. Unobstructed beam.")
        pol_angle_deg = 0.0
    pol_angle = np.deg2rad(pol_angle_deg)

with col4:
    st.subheader("Visualization Toggles")
    show_combined = st.checkbox("Combined Wave (Green)", value=True)
    show_ex = st.checkbox("E_x Component (Blue)", value=False)
    show_ey = st.checkbox("E_y Component (Red)", value=False)
    show_axis = st.checkbox("Show Optical Axes", value=True)

# --- Physics Simulation ---
z_start, z_wp_in, z_wp_out = 0, 10, 15
z_pol = 25
z_end = 35 if insert_pol else 25
resolution = 600
z = np.linspace(z_start, z_end, resolution)
k = 2 * np.pi / 2.0

Ex = np.zeros_like(z)
Ey = np.zeros_like(z)
zeros = np.zeros_like(z)

cos_t, sin_t = np.cos(wp_angle), np.sin(wp_angle)
cos_p, sin_p = np.cos(pol_angle), np.sin(pol_angle)

J_pol = np.array([[cos_p ** 2, cos_p * sin_p],
                  [cos_p * sin_p, sin_p ** 2]]) if insert_pol else np.eye(2)

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

# --- Stokes Parameters Calculation ---
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

# --- Dynamic Subplot Layout ---
spatial_title = f"Spatial Propagation (Detector Intensity: {intensity_percent:.1f}%)" if insert_pol else "Spatial Propagation"
transmitted_title = "Transmitted State (with Polarizer Operator)" if insert_pol else "Transmitted State"

fig = make_subplots(
    rows=2, cols=2,
    specs=[[{"colspan": 2, "type": "scene"}, None],
           [{"type": "scene"}, {"type": "scene"}]],
    row_heights=[0.6, 0.4],
    subplot_titles=(spatial_title, "Incident State (with WP Operator)", transmitted_title),
    vertical_spacing=0.1
)

# --- Subplot 1: Spatial Propagation (Row 1) ---
if show_combined:
    fig.add_trace(go.Scatter3d(x=z, y=Ex, z=Ey, mode='lines', line=dict(color='green', width=4), name='Combined Wave'),
                  row=1, col=1)
if show_ex:
    fig.add_trace(
        go.Scatter3d(x=z, y=Ex, z=zeros, mode='lines', line=dict(color='blue', width=3), name='E_x Component'), row=1,
        col=1)
if show_ey:
    fig.add_trace(go.Scatter3d(x=z, y=zeros, z=Ey, mode='lines', line=dict(color='red', width=3), name='E_y Component'),
                  row=1, col=1)


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
            row=1, col=1)
        fig.add_trace(go.Scatter3d(x=[z_in] * 5, y=transverse,
                                   z=[transverse[1], transverse[1], transverse[0], transverse[0], transverse[1]],
                                   mode='lines', line=dict(color='gray', width=2), showlegend=False), row=1, col=1)
        fig.add_trace(go.Scatter3d(x=[z_out] * 5, y=transverse,
                                   z=[transverse[1], transverse[1], transverse[0], transverse[0], transverse[1]],
                                   mode='lines', line=dict(color='gray', width=2), showlegend=False), row=1, col=1)
    else:
        x_vol = [z_in, z_in, z_in, z_in]
        y_vol = [-1.5, 1.5, 1.5, -1.5]
        z_vol = [-1.5, -1.5, 1.5, 1.5]
        fig.add_trace(
            go.Mesh3d(x=x_vol, y=y_vol, z=z_vol, i=[0, 0], j=[1, 2], k=[2, 3], color=color, opacity=0.2, name=name),
            row=1, col=1)
        fig.add_trace(go.Scatter3d(x=[z_in] * 5, y=transverse,
                                   z=[transverse[1], transverse[1], transverse[0], transverse[0], transverse[1]],
                                   mode='lines', line=dict(color=color, width=3), showlegend=False), row=1, col=1)


if insert_wp:
    draw_optical_element(z_wp_in, z_wp_out, 'white', 'Wave Plate', True)
    if show_axis:
        fa_x = [-1.5 * np.cos(wp_angle), 1.5 * np.cos(wp_angle)]
        fa_y = [-1.5 * np.sin(wp_angle), 1.5 * np.sin(wp_angle)]
        fig.add_trace(go.Scatter3d(x=[z_wp_in, z_wp_in], y=fa_x, z=fa_y, mode='lines',
                                   line=dict(color='orange', width=5, dash='dash'), name='Fast Axis'), row=1, col=1)

if insert_pol:
    draw_optical_element(z_pol, z_pol, 'cyan', 'Polarizer', False)
    if show_axis:
        ta_x = [-1.5 * np.cos(pol_angle), 1.5 * np.cos(pol_angle)]
        ta_y = [-1.5 * np.sin(pol_angle), 1.5 * np.sin(pol_angle)]
        fig.add_trace(go.Scatter3d(x=[z_pol, z_pol], y=ta_x, z=ta_y, mode='lines', line=dict(color='cyan', width=5),
                                   name='Transmission Axis'), row=1, col=1)

if show_combined:
    fig.add_trace(go.Scatter3d(x=[z_end] * len(z[z >= (z_pol if insert_pol else z_wp_out)]),
                               y=Ex[z >= (z_pol if insert_pol else z_wp_out)],
                               z=Ey[z >= (z_pol if insert_pol else z_wp_out)],
                               mode='lines', line=dict(color='magenta', width=3), name='Final Polarization'), row=1,
                  col=1)


# --- Helper Function for Poincaré Spheres ---
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
    fig.add_trace(
        go.Scatter3d(x=ref_x, y=ref_y, z=ref_z, mode='markers+text', marker=dict(color='gray', size=3), text=ref_labels,
                     textposition='bottom center', textfont=dict(color='white', size=12), hoverinfo='skip',
                     showlegend=False), row=row, col=col)

    fig.add_trace(go.Scatter3d(x=[0, stokes_vec[0]], y=[0, stokes_vec[1]], z=[0, stokes_vec[2]], mode='lines',
                               line=dict(color='cyan', width=4), hoverinfo='skip', showlegend=False), row=row, col=col)
    fig.add_trace(go.Scatter3d(x=[stokes_vec[0]], y=[stokes_vec[1]], z=[stokes_vec[2]], mode='markers',
                               marker=dict(color='magenta', size=8), hoverinfo='skip', showlegend=False), row=row,
                  col=col)


# --- Render Spheres ---
add_poincare_sphere(fig, row=2, col=1, stokes_vec=S_in, name_prefix="Incident")
add_poincare_sphere(fig, row=2, col=2, stokes_vec=S_out, name_prefix="Transmitted")

# --- Operators on Spheres ---
if insert_wp:
    n_x, n_y = np.cos(2 * wp_angle), np.sin(2 * wp_angle)
    fig.add_trace(go.Scatter3d(x=[-n_x * 1.1, n_x * 1.2], y=[-n_y * 1.1, n_y * 1.2], z=[0, 0], mode='lines',
                               line=dict(color='orange', width=4, dash='dash'), hoverinfo='skip', showlegend=False),
                  row=2, col=1)

    if retardance > 0:
        center = np.array([n_x, n_y, 0]) * 1.15
        e1, e2 = np.array([-n_y, n_x, 0]), np.array([0, 0, 1])
        arc_t = np.linspace(0, retardance, 40)
        radius = 0.25
        arc_x = center[0] + radius * (np.cos(arc_t) * e1[0] + np.sin(arc_t) * e2[0])
        arc_y = center[1] + radius * (np.cos(arc_t) * e1[1] + np.sin(arc_t) * e2[1])
        arc_z = center[2] + radius * (np.cos(arc_t) * e1[2] + np.sin(arc_t) * e2[2])

        fig.add_trace(
            go.Scatter3d(x=arc_x, y=arc_y, z=arc_z, mode='lines', line=dict(color='gold', width=4), hoverinfo='skip',
                         showlegend=False), row=2, col=1)

        u_dir = radius * (-np.sin(retardance) * e1[0] + np.cos(retardance) * e2[0])
        v_dir = radius * (-np.sin(retardance) * e1[1] + np.cos(retardance) * e2[1])
        w_dir = radius * (-np.sin(retardance) * e1[2] + np.cos(retardance) * e2[2])
        # Note: anchor="tail" connects the wide base of the cone to the end of the arc
        fig.add_trace(go.Cone(x=[arc_x[-1]], y=[arc_y[-1]], z=[arc_z[-1]], u=[u_dir], v=[v_dir], w=[w_dir],
                              colorscale=[[0, 'gold'], [1, 'gold']], showscale=False, sizemode="absolute", sizeref=0.1,
                              anchor="tail", hoverinfo='skip', showlegend=False), row=2, col=1)
        # Formatted annotation using the pi multiple
        fig.add_trace(
            go.Scatter3d(x=[arc_x[-1]], y=[arc_y[-1]], z=[arc_z[-1]], mode='text', text=[f"Γ = {retardance_pi:.2f}π"],
                         textposition='top right', textfont=dict(color='gold', size=12), hoverinfo='skip',
                         showlegend=False), row=2, col=1)

if insert_pol:
    fig.add_trace(go.Scatter3d(x=[0, S_pol_axis[0]], y=[0, S_pol_axis[1]], z=[0, S_pol_axis[2]], mode='lines',
                               line=dict(color='white', width=4, dash='dashdot'), hoverinfo='skip', showlegend=False),
                  row=2, col=2)
    fig.add_trace(go.Scatter3d(x=[S_pol_axis[0]], y=[S_pol_axis[1]], z=[S_pol_axis[2]], mode='markers+text',
                               marker=dict(color='white', size=6), text=[f"Pol ({intensity_percent:.0f}%)<br>"],
                               textposition='top center', textfont=dict(color='white', size=12), hoverinfo='skip',
                               showlegend=False), row=2, col=2)
    fig.add_trace(go.Scatter3d(x=[S_out[0], S_pol_axis[0]], y=[S_out[1], S_pol_axis[1]], z=[S_out[2], S_pol_axis[2]],
                               mode='lines', line=dict(color='rgba(255, 255, 255, 0.4)', width=2, dash='dot'),
                               hoverinfo='skip', showlegend=False), row=2, col=2)

# --- Global Layout Formatting ---
scene_poincare_config = dict(
    xaxis=dict(title='', range=[-1.2, 1.2], showticklabels=False, showgrid=False, zeroline=False),
    yaxis=dict(title='', range=[-1.2, 1.2], showticklabels=False, showgrid=False, zeroline=False),
    zaxis=dict(title='', range=[-1.2, 1.2], showticklabels=False, showgrid=False, zeroline=False),
    aspectratio=dict(x=1, y=1, z=1),
    camera=dict(eye=dict(x=1.3, y=1.3, z=1.3))
)

layout_args = dict(
    height=1000,
    margin=dict(l=10, r=10, b=10, t=40),
    scene=dict(
        xaxis=dict(title='Propagation (z)', range=[z_start, z_end]),
        yaxis=dict(title='E_x', range=[-1.5, 1.5]),
        zaxis=dict(title='E_y', range=[-1.5, 1.5]),
        aspectratio=dict(x=4 if insert_pol else 3, y=1, z=1),
        camera=dict(eye=dict(x=1.2, y=-2.8, z=1.2))
    ),
    scene2=scene_poincare_config,
    scene3=scene_poincare_config
)

fig.update_layout(**layout_args)
st.plotly_chart(fig, use_container_width=True)