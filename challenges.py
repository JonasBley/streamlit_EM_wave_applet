# challenges.py

# Stokes coordinates
# Horizontal: [1, 0, 0]
# Vertical: [-1, 0, 0]
# Diagonal (+45°): [0, 1, 0]
# Anti-Diagonal (-45°): [0, -1, 0]
# Right-Circular: [0, 0, 1]
# Left-Circular: [0, 0, -1]

CHALLENGES = {
    "Master Tutorial: The Polarization Journey": {
        "steps": [
            {
                "text": r"<b>Step 1: The Macroscopic Wave</b><br>Light is an electromagnetic wave where the electric field $\vec{E}$ is confined to the transverse $x$-$y$ plane, oscillating perpendicular to the direction of propagation. The wave can be described by the Jones vector $\vec{E} = \begin{pmatrix} E_x \\ E_y e^{i\varphi} \end{pmatrix}$. The absolute value of the amplitudes of the Jones vector squared must add up to one: $|E_X|^2+|E_Y|^2=1$.",
                "task": r"Move the slider to $E_x=0.5$ and watch the change in the electric field components and the combined wave in the applet below. Notice how the amplitude in $y$ direction $E_y$ is not the same as $E_x$. Click on the Next Step button below the applet to proceed and learn why.",
                "hint": r"Focus on the <b>Incident Wave</b> section. Adjust the first slider until the Amplitude $E_x$ reads exactly <b>0.50</b>.",
                "setup": {"insert_wp": False, "insert_pol": False, "show_poincare": False, "E_x_amp": 0.0, "phase_relative_pi": 0.0, "show_toggles": False},
                "target": {"E_x_amp": 0.5},
                "solution": {"E_x_amp": 0.5}
            },
            {
                "text": r"<b>Step 2: Constructing Standard States</b><br>Any state of polarization $\mathbf{J}$ can be expressed as a linear combination of horizontal $\mathbf{J}_H=\begin{pmatrix}1 \\ 0\end{pmatrix}$ and vertical $\mathbf{J}_V=\begin{pmatrix}0 \\ 1\end{pmatrix}$ basis vectors: $$\mathbf{J}=\alpha \mathbf{J}_H+ \beta\mathbf{J}_V,$$ where $\alpha$ and $\beta$ are complex numbers. In the Jones formalism, the resulting vector has to be normalized, i.e., $|\alpha|^2+|\beta|^2=1$",
                "task": r"Create an approximately <b>Diagonal</b> state, which requires equal amplitudes: $\mathbf{J}_{D} = \frac{1}{\sqrt{2}} \left(\mathbf{J}_H+\mathbf{J}_V\right)= \frac{1}{\sqrt{2}} \begin{pmatrix} 1 \\ 1 \end{pmatrix}$.",
                "hint": r"You want the amplitudes to be perfectly balanced. Since $|E_x|^2+|E_y|^2=1$, you need an amplitude of roughly $\sqrt{1/2}\approx 0.71 $.",
                "setup": {"show_toggles": False},
                "target": {"E_x_amp": 0.71, "phase_relative_pi": [0.0, 2.0]},
                "solution": {"E_x_amp": 0.71, "phase_relative_pi": 0.0}
            },
            {
                "text": r"<b>Step 3: The Poincaré Sphere</b><br>We have now revealed the <b>Poincaré Sphere</b> below the applet. Notice how the Diagonal state you just created maps exactly to the equator.",
                "task": r"Now, introduce a relative phase shift to create a <b>Right-Circular</b> state (Phase = 0.5π). Watch the state vector leave the equator and travel to the North Pole:<br>$\mathbf{J}_{R} = \frac{1}{\sqrt{2}} \begin{pmatrix} 1 \\ e^{i\pi/2} \end{pmatrix} = \frac{1}{\sqrt{2}} \begin{pmatrix} 1 \\ i \end{pmatrix}$",
                "hint": r"Circular states require equal amplitudes (which you already have) but a $\pi/2$ phase shift.",
                "setup": {"show_poincare": True, "show_toggles": False},
                "target": {"E_x_amp": 0.71, "phase_relative_pi": 0.5},
                "solution": {"E_x_amp": 0.71, "phase_relative_pi": 0.5}
            },
            {
                "text": r"<b>Step 4: Wave Plates (Retarders)</b><br>A wave plate orthogonally decomposes light and introduces a phase delay $\Gamma$ between the fast and slow axes. If the fast axis angle is at $0^\circ$ (horizontal), within the Jones formalism it can be described with the matrix $\mathbf{M}(\Gamma) = \begin{pmatrix} 1 & 0 \\ 0 & e^{i\Gamma} \end{pmatrix}$, which only changes the relative phase of a Jones vector $\begin{pmatrix} E_x \\ E_y e^{i\varphi} \end{pmatrix}$:<br><br> $\begin{pmatrix} 1 & 0 \\ 0 & e^{i\Gamma} \end{pmatrix}\begin{pmatrix} E_x \\ E_y e^{i\varphi} \end{pmatrix}=\begin{pmatrix} E_x \\ E_y e^{i(\varphi+\Gamma)} \end{pmatrix}.$<br><br> We have inserted a wave plate (WP) and the Poincaré sphere now shows the WP operator as a rotation axis (orange dashed line). On the Poincaré sphere, the Retardance is the angle of rotation around the axis of the wave plate operator that is given by the WP Fast axis Angle.",
                "task": r"Starting with a Horizontal incident wave ($E_x = 1.0$), find the Retardance $\Gamma$ necessary to output a <b>Vertical</b> state.",
                "hint": r"To rotate a horizontal vector to a vertical one, you must completely invert the axis. This requires a half-wave plate.",
                "setup": {"insert_wp": True, "E_x_amp": 1.0, "phase_relative_pi": 0.0, "wp_angle_deg": 45.0, "retardance_pi": 0.0, "show_toggles": False},
                "target": {"retardance_pi": [1.0], "wp_angle_deg": [45]},
                "solution": {"retardance_pi": 1.0, "wp_angle_deg": 45.0}
            },
            {
                "text": r"<b>Step 5: Rotating the wave plate</b> Turning the wave plate by an angle $\theta$ is equivalent to a coordinate transformation of the $x$-$y$ plane—a rotation back and forth using the rotation matrix $\mathbf{R}(\theta) = \begin{pmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{pmatrix}$. The combined operator is $\mathbf{M}(\theta, \Gamma) = \mathbf{R}(-\theta) \mathbf{M}(\Gamma) \mathbf{R}(\theta)$. The Retardance $\Gamma$ is characterized by the rotation angle, and the Fast Axis Angle $\Delta$ is represented by the azimuthal angle $2\Delta$ of the WP operator axis on the equator of the sphere.",
                "task": r"Starting with a right-handed circularly polarized incident wave ($E_x = E_z = \frac{1}{\sqrt{2}}$ and $\varphi=\frac{\pi}{2}$), find the <i>Fast Axis Angle</i> $\Delta$ necessary to output a <b>Vertical</b> state.",
                "hint": r"Rotating a right-handed circularly polarized vector to a vertical one requires a $pi/2$ rotation on the sphere, i.e., a quarter-wave plate with retardance $pi/2$. The rotation axis must be chosen such that the vector travels clockwise around the sphere, meaning it has to be rotated by more than 90 degrees counterclockwise.",
                "setup": {"insert_wp": True, "E_x_amp": 0.707, "phase_relative_pi": 0.5, "wp_angle_deg": 0.0, "retardance_pi": 0.5, "show_toggles": False},
                "target": {"E_x_amp": 0.707, "phase_relative_pi": 0.5, "retardance_pi": 0.5, "wp_angle_deg": 135.0},
                "solution": {"E_x_amp": 0.707, "phase_relative_pi": 0.5, "retardance_pi": 0.5, "wp_angle_deg": 135.0}
            },
            {
                "text": r"<b>Step 6: Mastering Wave Plates</b><br>As a reminder, a wave plate is a unitary operator that acts as a pure geometric rotation on the sphere. The rotation axis lies on the equator at an azimuthal angle $2\Delta$ (where $\Delta$ is the physical <i>Fast Axis Angle</i>), and the rotation amount is the <i>Retardance</i> $\Gamma$. Let's test your intuition.",
                "task": r"Start with a <b>Horizontal</b> incident wave. Find the Retardance and the Fast Axis Angle needed to rotate the state to create a <b>Diagonal</b> state.",
                "hint": r"To travel along the equator (Horizontal) to the Diagonal state, your rotation axis on the sphere needs to reflect around an axis that is exactly $45^\circ$ away from Horizontal.",
                "setup": {"wp_angle_deg": 0.0, "retardance_pi": 0.0, "E_x_amp": 1.0, "phase_relative_pi": 0.0, "show_toggles": False},
                "target": {"E_x_amp": 1.0, "S_final": [0, 1, 0]},
                "solution": {"retardance_pi": 1.0, "wp_angle_deg": 22.5}
            },
            {
                "text": r"<b>Step 7: Linear Polarizers</b><br>Unlike a wave plate, a linear polarizer is a <i>non-unitary</i> operator—it absorbs light and reduces overall intensity. A horizontal polarizer projects the electric field onto the $x$-axis, represented by the matrix:<br><br>$\mathbf{P}(0^\circ) = \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix}$<br><br>On the Poincaré sphere, this acts as a projection straight through the volume of the sphere onto the transmission axis state. Just like the wave plate, turning the polarizer applies a coordinate rotation: $\mathbf{P}(\theta) = \mathbf{R}(-\theta) \mathbf{P}(0^\circ) \mathbf{R}(\theta)$.",
                "task": r"Find the transmission angle $\theta$ that projects an incident <b>Diagonal</b> state into a pure <b>Horizontal</b> state.",
                "hint": r"You want the final state to sit on the pure Horizontal axis of the sphere. Turn your Polarizer's Transmission Axis so that it fits the axis of polarization of outgoing light that you want. Notice how the intensity drops to exactly 50% as you project the Diagonal vector.",
                "setup": {"insert_wp": False, "insert_pol": True, "pol_angle_deg": 90.0, "E_x_amp": 0.71, "phase_relative_pi": 0.0, "show_toggles": False},
                "target": {"pol_angle_deg": [0.0, 180.0]},
                "solution": {"pol_angle_deg": 0.0}
            },
            {
                "text": r"<b>Step 8: The Final Challenge</b><br>Let's combine operators!",
                "task": r"Let the incident wave be <b>vertical</b> ($E_x=0.0$). Your goal is to pass this light through BOTH a wave plate and a polarizer to achieve a final transmitted state that is <b>Horizontal</b> with an intensity of exactly <b>50%</b> of the original beam.",
                "hint": r"First use a Quarter-Wave plate to transform the Vertical light into a Right-Circular state, then project it using the polarizer.)",
                "setup": {"insert_wp": True, "insert_pol": True, "E_x_amp": 0.0, "phase_relative_pi": 0.0, "wp_angle_deg": 0.0, "retardance_pi": 0.0, "pol_angle_deg": 90.0, "show_toggles": False},
                "target": {"retardance_pi": 0.5, "wp_angle_deg": [45.0, 135.0], "pol_angle_deg": [0.0, 180.0]},
                "solution": {"retardance_pi": 0.5, "wp_angle_deg": 45.0, "pol_angle_deg": 0.0}
            },
            {
                "text": r"Done. Congratulations, you completed the tutorial. Feel free to play around with the applet!",
                "task": r"",
                "setup": {"insert_wp": True, "insert_pol": True, "show_toggles": True},
                "target": {}
            }
        ]
    },
    "Free Play": {
        "steps": [
            {
                "text": r"<b>Free Play Mode</b><br>Explore the simulation freely.",
                "task": r"Use the toggles and sliders below to interact with the wave plates and polarizers. There are no targets to reach.",
                "setup": {"show_poincare": True, "show_toggles": True},
                "target": {}
            }
        ]
    }
}