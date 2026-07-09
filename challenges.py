# challenges.py

# Stokes coordinates
# Horizontal: [1, 0, 0]
# Vertical: [-1, 0, 0]
# Diagonal (+45°): [0, 1, 0]
# Anti-Diagonal (-45°): [0, -1, 0]
# Right-Circular: [0, 0, 1]
# Left-Circular: [0, 0, -1]

CHALLENGES = {
    "Polarization 1": {
        "steps": [
            {
                "text": r"<b>Step 1 of 9: The Macroscopic Wave</b><br>Classical light is an electromagnetic wave where the electric field $\vec{E}$ is confined to the transverse $x$-$y$ plane, oscillating perpendicular to the direction of propagation. Polarized light can be described by the so-called Jones vector $\vec{E} = \begin{pmatrix} E_x \\ E_y e^{i\varphi} \end{pmatrix}$. This vector describes the electromagnetic wave with its maximum amplitudes in $x$ and $y$-direction, $E_x$ and $E_y$, and a relative phase between the components of the electromagnetic wave. The absolute value of the amplitudes of the Jones vector squared must add up to one: $|E_X|^2+|E_Y|^2=1$.",
                "task": r"You are starting with a completely vertically polarized state $\mathbf{J}_{V}== \begin{pmatrix} 0 \\ 1 \end{pmatrix}$. Move the slider to $E_x=0.5$ and watch the change in the electric field components and the combined wave in the applet below. Move it around for a closer look. Notice how the amplitude in $y$ direction $E_y$ is not the same as $E_x$.",
                "hint": r"Focus on the <b>Incident Wave</b> section. Adjust the first slider until the Amplitude $E_x$ reads exactly <b>0.50</b>.",
                "setup": {"insert_wp": False, "insert_pol": False, "show_poincare": False, "E_x_amp": 0.0, "phase_relative_pi": 0.0, "show_toggles": False, "disable_keys": ["phase_relative_pi"]},
                "target": {"E_x_amp": 0.5},
                "solution": {"E_x_amp": 0.5},
                "explanation": r"Because the Jones vector is normalized ($|E_x|^2 + |E_y|^2 = 1$), fixing the horizontal field amplitude to $E_x = 0.5$ forces the vertical field amplitude component to automatically balance to: $$E_y = \sqrt{1.0 - 0.5^2} = \sqrt{0.75} \approx 0.866$$ Since no relative phase shift is present ($\varphi = 0$), the wave remains linearly polarized, but the unequal component amplitudes tilt the net polarization angle away from the $45^\circ$ line. Click on the Next Step button below the applet to proceed."
            },
            {
                "text": r"<b>Step 2 of 9: Constructing Standard States</b><br>Any state of polarization $\mathbf{J}$ can be expressed as a linear combination of horizontal $\mathbf{J}_H=\begin{pmatrix}1 \\ 0\end{pmatrix}$ and vertical $\mathbf{J}_V=\begin{pmatrix}0 \\ 1\end{pmatrix}$ basis vectors: $$\mathbf{J}=\alpha \mathbf{J}_H+ \beta\mathbf{J}_V,$$ where $\alpha$ and $\beta$ are complex numbers. In the Jones formalism, the resulting vector has to be normalized, i.e., $|\alpha|^2+|\beta|^2=1$",
                "task": r"Now, create an approximately <b>diagonal</b> state, which requires equal amplitudes: $\mathbf{J}_{D} = \frac{1}{\sqrt{2}} \left(\mathbf{J}_H+\mathbf{J}_V\right)= \frac{1}{\sqrt{2}} \begin{pmatrix} 1 \\ 1 \end{pmatrix}$.",
                "hint": r"You want the amplitudes to be perfectly balanced. Start with $|E_x|^2+|E_y|^2=1$, and require that $|E_x|=|E_y|$. What are $|E_x|$ and $|E_y|$ in that case?",
                "setup": {"show_toggles": False, "disable_keys": ["phase_relative_pi"]},
                "target": {"E_x_amp": 0.71, "phase_relative_pi": [0.0, 2.0]},
                "solution": {"E_x_amp": 0.71, "phase_relative_pi": 0.0},
                "explanation": r"A purely diagonal state $\mathbf{J}_D$ implies that the spatial oscillations along the horizontal and vertical channels are perfectly symmetric and in-phase. Mathematically, this dictates that $|\alpha| = |\beta|$, requiring: $$E_x = E_y = \frac{1}{\sqrt{2}} \approx 0.707$$ Setting the relative phase to $\varphi = 0$ (or $2\pi$) keeps the components in geometric phase synchronization, forcing the electric field vector to sweep out a linear path at exactly $+45^\circ$ in the transverse plane."
            },
            {
                "text": r"<b>Step 3 of 9: The Poincaré Sphere</b><br>We have now revealed the <b>Poincaré Sphere</b> below the applet. Notice how the diagonal state you just created maps exactly to the equator because there is no phase shift $\varphi=0$.",
                "task": r"Starting with a diagonally polarized state, introduce a relative phase shift to create a <b>Right-Circular</b> state located at the north pole of the sphere. Watch the state vector leave the equator and travel to the north pole:<br>$\mathbf{J}_{R} = \frac{1}{\sqrt{2}} \begin{pmatrix} 1 \\ e^{i\pi/2} \end{pmatrix} = \frac{1}{\sqrt{2}} \begin{pmatrix} 1 \\ i \end{pmatrix}$",
                "hint": r"A right-circular state requires equal amplitudes (which you already have) but a $\pi/2$ phase shift.",
                "setup": {"show_poincare": True, "show_toggles": False, "disable_keys": ["E_x_amp"]},
                "target": {"E_x_amp": 0.71, "phase_relative_pi": 0.5},
                "solution": {"E_x_amp": 0.71, "phase_relative_pi": 0.5},
                "explanation": r"By adding a relative phase shift of $\varphi = \frac{\pi}{2}$ while keeping equal amplitudes ($E_x = E_y$), the horizontal component reaches its maximum displacement exactly when the vertical component passes through zero. In the Jones notation, this introduces the imaginary unit ($e^{i\pi/2} = i$). The polarization vector is moved from the equator towards the north pole of the sphere by an angle of $\pi/2$.<br><br>Here is a summary of the standard polarization states and their positions on the Poincaré sphere:<br>• <b>Horizontal:</b> $\mathbf{J}_H = \begin{pmatrix} 1 \\ 0 \end{pmatrix}$ (Front equator)<br>• <b>Vertical:</b> $\mathbf{J}_V = \begin{pmatrix} 0 \\ 1 \end{pmatrix}$ (Back equator)<br>• <b>Diagonal:</b> $\mathbf{J}_D = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 \\ 1 \end{pmatrix}$ (Right equator)<br>• <b>Anti-Diagonal:</b> $\mathbf{J}_A = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 \\ -1 \end{pmatrix}$ (Left equator)<br>• <b>Right-Circular:</b> $\mathbf{J}_R = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 \\ i \end{pmatrix}$ (North pole)<br>• <b>Left-Circular:</b> $\mathbf{J}_L = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 \\ -i \end{pmatrix}$ (South pole)<br><br>Notice two key geometric rules: First, all states located on the equator of the sphere completely lack a complex phase shift. Second, all states with perfectly balanced amplitudes ($|E_x| = |E_y|$) are restricted to the vertical cross-section plane spanned by the $\mathbf{J}_D$ and $\mathbf{J}_R$ axes."
            },
            {
                "text": r"<b>Step 4 of 9: Wave Plates (Retarders)</b><br>A wave plate orthogonally decomposes light and introduces a phase delay $\Gamma$ between the fast and slow axes. If the fast axis angle is at $0^\circ$ (horizontal), within the Jones formalism it can be described with the matrix $\mathbf{M}(\Gamma) = \begin{pmatrix} 1 & 0 \\ 0 & e^{i\Gamma} \end{pmatrix}.$ The retardance $\Gamma$ is directly proportional to the physical thickness of the wave plate. It only changes the relative phase of a Jones vector $\begin{pmatrix} E_x \\ E_y e^{i\varphi} \end{pmatrix}$:<br><br> $\begin{pmatrix} 1 & 0 \\ 0 & e^{i\Gamma} \end{pmatrix}\begin{pmatrix} E_x \\ E_y e^{i\varphi} \end{pmatrix}=\begin{pmatrix} E_x \\ E_y e^{i(\varphi+\Gamma)} \end{pmatrix}.$<br><br> We have inserted a wave plate (WP) into the beam path. The Poincaré sphere now shows the WP operator as a rotation axis (orange dashed line). On the Poincaré sphere, the retardance is the angle of rotation around the axis of the wave plate operator.",
                "task": r"Starting with a diagonal incident wave ($E_x = E_y = 0.707$), find the retardance $\Gamma$ necessary to output a left-circularly polarized state.",
                "hint": r"Look at the orange dashed rotation axis on the sphere. How far do you need to rotate the vector for it to reach the bottom pole?",
                "setup": {"insert_wp": True, "E_x_amp": 0.71, "phase_relative_pi": 0.0, "wp_angle_deg": 0.0, "retardance_pi": 0.0, "show_toggles": False, "disable_keys": ["E_x_amp", "phase_relative_pi", "wp_angle_deg"]},
                "target": {"E_x_amp": 0.71, "retardance_pi": 1.5},
                "solution": {"retardance_pi": 1.5},
                "explanation": r"The incident wave is diagonally polarized: $\mathbf{J}_{in} = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 \\ 1 \end{pmatrix}$. The wave plate operator is: $$\mathbf{M}(45^\circ, \pi) =  \begin{pmatrix} 1 & 0 \\ 0 & e^{3i\pi/2}=-i \end{pmatrix}$$ Multiplying this operator by the incident wave yields: $$\begin{pmatrix} 1 & 0 \\ 0 & -i \end{pmatrix}\cdot \frac{1}{\sqrt{2}} \begin{pmatrix} 1 \\ 1 \end{pmatrix} = \begin{pmatrix} 1 \\ -i \end{pmatrix} = \mathbf{J}_L.$$ Geometrically on the Poincaré sphere, the wave plate fast axis at $\Delta = 0^\circ$ creates a rotation axis pointing towards the horizontal state. Setting the retardance to $\Gamma = 1.5\pi$ rotates the diagonal vector around this axis by 270$^\circ$, leaving the vector at the bottom of the sphere."
            },
            {
                "text": r"<b>Step 5 of 9: Rotating the wave plate</b><br>Turning the wave plate by an angle $\theta$ is equivalent to a coordinate transformation of the $x$-$y$ plane—a rotation back and forth using the rotation matrix $\mathbf{R}(\theta) = \begin{pmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{pmatrix}$. The combined operator is $\mathbf{M}(\theta, \Gamma) = \mathbf{R}(-\theta) \mathbf{M}(\Gamma) \mathbf{R}(\theta)$. The retardance $\Gamma$ is characterized by the rotation angle, and the fast axis angle $\Delta$ is represented by the azimuthal angle $2\Delta$ of the WP operator axis on the equator of the sphere.",
                "task": r"Starting with a right-handed circularly polarized incident wave ($E_x = E_z = \frac{1}{\sqrt{2}}$ and $\varphi=\frac{\pi}{2}$), find the <i>fast axis angle</i> $\Delta$ necessary to output a <b>vertical</b> state.",
                "hint": r"Rotating a right-handed circularly polarized vector to a vertical one requires a $\pi/2$ rotation on the sphere. The rotation axis must be chosen such that the vector travels clockwise around the sphere, meaning it has to be rotated by more than 90 degrees counterclockwise.",
                "setup": {"insert_wp": True, "E_x_amp": 0.707, "phase_relative_pi": 0.5, "wp_angle_deg": 0.0, "retardance_pi": 0.5, "show_toggles": False, "disable_keys": ["E_x_amp", "phase_relative_pi", "retardance_pi"]},
                "target": {"E_x_amp": 0.707, "phase_relative_pi": 0.5, "retardance_pi": 0.5, "wp_angle_deg": 135.0},
                "solution": {"E_x_amp": 0.707, "phase_relative_pi": 0.5, "retardance_pi": 0.5, "wp_angle_deg": 135.0},
                "explanation": r"The incident wave is right-circular: $\mathbf{J}_{in} = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 \\ i \end{pmatrix}$, corresponding to the north pole on the sphere. We require a final linear vertical state: $\mathbf{J}_{out} = \begin{pmatrix} 0 \\ 1 \end{pmatrix}$, located at the backside on the equator. Geometrically, moving from the pole to the equator requires a rotation of exactly $\Gamma = 90^\circ = 0.5\pi$ (a quarter-wave plate). To rotate the state vector from the top down directly into the vertical axis point, the rotation axis must be perpendicular to both vectors on the equator. Orienting the wave plate fast axis to $\Delta = 135^\circ$ creates an operator axis on the sphere at $2\Delta = 270^\circ$ (the anti-diagonal state axis). A clockwise quarter-turn rotation around this axis sweeps the state vector down along the meridian, landing perfectly on the vertical point."
            },
            {
                "text": r"<b>Step 6 of 9: Mastering Wave Plates</b><br>As a reminder, a wave plate is a unitary operator that acts as a pure geometric rotation on the sphere. The rotation axis lies on the equator at an azimuthal angle $2\Delta$ (where $\Delta$ is the physical <i>fast axis angle</i>), and the rotation amount is the <i>retardance</i> $\Gamma$. Let's test your intuition.",
                "task": r"Start with a <b>horizontal</b> incident wave. Find the retardance and the fast axis angle needed to rotate the state to create a <b>diagonal</b> state (+45$^\circ$ angle of the combined wave vector).",
                "hint": r"To travel along the equator (horizontal) to the diagonal state, your rotation axis on the sphere needs to reflect around an axis that is between the horizontal and diagonal axes on the sphere.",
                "setup": {"wp_angle_deg": 0.0, "retardance_pi": 0.0, "E_x_amp": 1.0, "phase_relative_pi": 0.0, "show_toggles": False, "disable_keys": ["E_x_amp", "phase_relative_pi"]},
                "target": {"E_x_amp": 1.0, "S_final": [0, 1, 0]},
                "solution": {"retardance_pi": 1.0, "wp_angle_deg": 22.5},
                "explanation": r"We begin at horizontal polarization and want to map directly to diagonal polarization along the equatorial plane. To execute this move using a half-wave plate ($\Gamma = 1.0\pi$, which acts as a $180^\circ$ flip), the rotation axis on the sphere must be positioned exactly halfway between the initial and target states on the equator. The angular separation between horizontal ($0^\circ$ on the sphere) and diagonal ($90^\circ$ on the sphere) is $90^\circ$. The bisection axis must sit at an azimuthal position of exactly: $$2\Delta = \frac{90^\circ}{2} = 45^\circ$$ The required fast axis angle is therefore $22.5^\circ$."
            },
            {
                "text": r"<b>Step 7 of 9: Linear Polarizers</b><br>Unlike a wave plate, a linear polarizer is a <i>non-unitary</i> operator—it absorbs light and reduces overall intensity (defined as the absolute value of the Jones vector squared). A horizontal polarizer projects the electric field onto the $x$-axis, represented by the matrix:<br><br>$\mathbf{P}(0^\circ) = \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix}$<br><br>On the Poincaré sphere, this acts as a projection straight through the volume of the sphere onto the transmission axis state. Just like the wave plate, turning the polarizer applies a coordinate rotation: $\mathbf{P}(\theta) = \mathbf{R}(-\theta) \mathbf{P}(0^\circ) \mathbf{R}(\theta)$.",
                "task": r"Find the transmission angle $\theta$ that projects any incident state into a pure <b>horizontal</b> state.",
                "hint": r"You want the final state to sit on the pure horizontal axis of the sphere. Turn your Polarizer's transmission Axis so that it fits the axis of polarization of outgoing light that you want. Notice how the intensity drops to exactly 50% as you project the diagonal vector.",
                "setup": {"insert_wp": False, "insert_pol": True, "pol_angle_deg": 90.0, "E_x_amp": 0.71, "phase_relative_pi": 0.0, "show_toggles": False, "disable_keys": ["E_x_amp", "phase_relative_pi"]},
                "target": {"pol_angle_deg": [0.0, 180.0]},
                "solution": {"pol_angle_deg": 0.0},
                "explanation": r"The incident diagonal wave is represented by $\mathbf{J}_{in} = \mathbf{J}_{D} =\frac{1}{\sqrt{2}}\begin{pmatrix} 1 \\ 1 \end{pmatrix}$. To output a purely horizontal state, the polarizer must completely block the vertical components of the field. Setting the polarizer angle to $\theta = 0^\circ$ initializes the projection matrix $\mathbf{P}(0^\circ) = \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix}$. Multiplying the vector yields: $$\mathbf{P}(0^\circ)\mathbf{J}_{in} = \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix} \left[\frac{1}{\sqrt{2}}\begin{pmatrix} 1 \\ 1 \end{pmatrix}\right] = \begin{pmatrix} \frac{1}{\sqrt{2}} \\ 0 \end{pmatrix}$$ Evaluating the transmitted beam intensity mathematically: $$I = |E_x|^2 + |E_y|^2 = \left|\frac{1}{\sqrt{2}}\right]^2 + 0 = 0.50$$ Exactly 50% of the beam's energy is absorbed because the polarizer filters out the orthogonal vertical component."
            },
            {
                "text": r"<b>Step 8 of 9: Putting it all together</b><br>Let's combine operators!",
                "task": r"Let the incident wave be <b>vertical</b> ($E_x=0.0$). Your goal is to pass this light through BOTH a wave plate and a polarizer to achieve a final transmitted state that is <b>horizontal</b> with an intensity of exactly <b>50%</b> of the original beam.",
                "hint": r"For example, you can first use a Quarter-Wave plate to transform the vertical light into a Right-Circular state, then project it using the polarizer.",
                "setup": {"insert_wp": True, "insert_pol": True, "E_x_amp": 0.0, "phase_relative_pi": 0.0, "wp_angle_deg": 0.0, "retardance_pi": 0.0, "pol_angle_deg": 90.0, "show_toggles": False, "disable_keys": ["E_x_amp", "phase_relative_pi"]},
                "target": {"S_final": [1.0, 0.0, 0.0], "intensity_percent": 50.0},
                "solution": {"retardance_pi": 0.5, "wp_angle_deg": 45.0, "pol_angle_deg": 0.0},
                "explanation": r"We track this sequence step-by-step through the optical train:<br>1. <b>Incident State:</b> The wave starts as purely vertical light: $\mathbf{J}_{in} = \begin{pmatrix} 0 \\ 1 \end{pmatrix}$.<br>2. <b>Wave Plate Action:</b> Setting the quarter-wave plate ($\Gamma = 0.5\pi$) to a physical angle of $\Delta = 45^\circ$ places the rotation axis at the diagonal position on the sphere. A $90^\circ$ rotation pushes the state vector from the equator straight up to the north pole, transforming the wave into right-circular light: $\mathbf{J}_{wp} = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 \\ i \end{pmatrix}$.<br>3. <b>Polarizer Action:</b> The circular wave then encounters a linear polarizer at $\theta = 0^\circ$. Applying the projection matrix filters out the vertical phase component entirely: $$\mathbf{P}(0^\circ)\mathbf{J}_{wp} = \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix} \left[\frac{1}{\sqrt{2}}\begin{pmatrix} 1 \\ i \end{pmatrix}\right] = \begin{pmatrix} \frac{1}{\sqrt{2}} \\ 0 \end{pmatrix}$$ This results in a purely horizontal output wave with a final intensity of $|\frac{1}{\sqrt{2}}|^2 = 0.50$. On the sphere, the state vector is projected straight through the center volume from the north pole down to the horizontal equatorial anchor point."
            },
            {
                "text": r"<b>Step 9 of 9: The Final Challenge</b><br>Let's combine operators for a lossless transmission!",
                "task": r"Start with an incident <b>Right-Circular</b> wave. Your goal is to use BOTH the wave plate and the polarizer to output a pure <b>Diagonal</b> state (+45$^\circ$) with an intensity of exactly <b>100%</b> (no light absorbed).",
                "hint": r"To get 100% intensity through the polarizer, the light hitting it must already be Diagonal. Use the wave plate to rotate the Right-Circular state (north pole) to the Diagonal state on the equator, then align the polarizer to let it all through.",
                "setup": {"insert_wp": True, "insert_pol": True, "E_x_amp": 0.707, "phase_relative_pi": 0.5, "wp_angle_deg": 0.0, "retardance_pi": 0.0, "pol_angle_deg": 0.0, "show_toggles": False, "disable_keys": ["E_x_amp", "phase_relative_pi"]},
                "target": {"S_final": [0.0, 1.0, 0.0], "intensity_percent": 100.0},
                "solution": {"retardance_pi": 0.5, "wp_angle_deg": 90.0, "pol_angle_deg": 45.0},
                "explanation": r"To achieve 100% transmission through a linear polarizer, the light entering it must already perfectly match its transmission axis. Therefore, your wave plate must convert the Right-Circular light directly into Diagonal light. On the Poincaré sphere, this means rotating the state vector from the north pole down to the +45$^\circ$ diagonal point on the equator. Setting the fast axis to $\Delta = 90^\circ$ creates a rotation axis pointing to the vertical state. A quarter-wave retardance ($\Gamma = 0.5\pi$) rotates the pole exactly 90$^\circ$ to the diagonal state. Finally, turning the polarizer to $\theta = 45^\circ$ allows this diagonal light to pass through entirely without absorption. Note: A fast axis of $0^\circ$ and retardance of $1.5\pi$ is also a valid mathematical solution!"
            },
            {
                "text": r"<b>Tutorial Completed!</b><br>Congratulations, you have finished the interactive physics module. Feel free to play around with the optical elements above. When you are ready to proceed with the study, click the return button at the bottom of the screen.<br>",
                "task": r"",
                "setup": {"insert_wp": True, "insert_pol": True, "show_toggles": True, "disable_keys": []},
                "target": {}
            }
        ]
    },
    "Polarization 2": {
        "steps": [
            {
                "text": r"<b>Step 1 of 9: The Macroscopic Wave</b><br>Classical light is an electromagnetic wave where the electric field $\vec{E}$ is confined to the transverse $x$-$y$ plane, oscillating perpendicular to the direction of propagation. Polarized light can be described by the so-called Jones vector $\vec{E} = \begin{pmatrix} E_x \\ E_y e^{i\varphi} \end{pmatrix}$. This vector describes the electromagnetic wave with its maximum amplitudes in $x$ and $y$-direction, $E_x$ and $E_y$, and a relative phase between the components of the electromagnetic wave. The absolute value of the amplitudes of the Jones vector squared must add up to one: $|E_X|^2+|E_Y|^2=1$.",
                "task": r"You are starting with a completely vertically polarized state $\mathbf{J}_{V}== \begin{pmatrix} 0 \\ 1 \end{pmatrix}$. Move the slider to $E_x=0.5$ and watch the change in the electric field components and the combined wave in the applet below. Move it around for a closer look. Notice how the amplitude in $y$ direction $E_y$ is not the same as $E_x$.",
                "hint": r"Focus on the <b>Incident Wave</b> section. Adjust the first slider until the Amplitude $E_x$ reads exactly <b>0.50</b>.",
                "setup": {"insert_wp": False, "insert_pol": False, "show_poincare": False, "E_x_amp": 0.0, "phase_relative_pi": 0.0, "show_toggles": False, "disable_keys": ["phase_relative_pi"]},
                "target": {"E_x_amp": 0.5},
                "solution": {"E_x_amp": 0.5},
                "explanation": r"Because the Jones vector is normalized ($I = |E_x|^2 + |E_y|^2 = 1$), fixing the horizontal field amplitude to $E_x = 0.5$ forces the vertical field amplitude component to automatically balance to: $$E_y = \sqrt{1.0 - 0.5^2} = \sqrt{0.75} \approx 0.866$$ Since no relative phase shift is present ($\varphi = 0$), the wave remains linearly polarized, but the unequal component amplitudes tilt the net polarization angle away from the standard $45^\circ$ line. Click on the Next Step button below the applet to proceed."
            },
            {
                "text": r"<b>Step 2 of 9: Constructing Standard States</b><br>Any state of polarization $\mathbf{J}$ can be expressed as a linear combination of horizontal $\mathbf{J}_H=\begin{pmatrix}1 \\ 0\end{pmatrix}$ and vertical $\mathbf{J}_V=\begin{pmatrix}0 \\ 1\end{pmatrix}$ basis vectors: $$\mathbf{J}=\alpha \mathbf{J}_H+ \beta\mathbf{J}_V,$$ where $\alpha$ and $\beta$ are complex numbers. In the Jones formalism, the resulting vector has to be normalized, i.e., $|\alpha|^2+|\beta|^2=1$",
                "task": r"Now, create an approximately <b>diagonal</b> state, which requires equal amplitudes: $\mathbf{J}_{D} = \frac{1}{\sqrt{2}} \left(\mathbf{J}_H+\mathbf{J}_V\right)= \frac{1}{\sqrt{2}} \begin{pmatrix} 1 \\ 1 \end{pmatrix}$.",
                "hint": r"You want the amplitudes to be perfectly balanced. Start with $|E_x|^2+|E_y|^2=1$, and require that $|E_x|=|E_y|$. What are $|E_x|$ and $|E_y|$ in that case?",
                "setup": {"show_toggles": False, "disable_keys": ["phase_relative_pi"]},
                "target": {"E_x_amp": 0.71, "phase_relative_pi": [0.0, 2.0]},
                "solution": {"E_x_amp": 0.71, "phase_relative_pi": 0.0},
                "explanation": r"A purely diagonal state $\mathbf{J}_D$ implies that the spatial oscillations along the horizontal and vertical channels are perfectly symmetric and in-phase. Mathematically, this dictates that $|\alpha| = |\beta|$, requiring: $$E_x = E_y = \frac{1}{\sqrt{2}} \approx 0.707.$$ Setting the relative phase to $\varphi = 0$ (or $2\pi$) keeps the components in geometric phase synchronization, forcing the electric field vector to sweep out a linear path at exactly $+45^\circ$ in the transverse plane."
            },
            {
                "text": r"<b>Step 3 of 9: Circular States</b><br>Notice how the diagonal state you just created features perfectly balanced amplitudes and no phase shift $\varphi=0$.",
                "task": r"Starting with a diagonally polarized state, introduce a relative phase shift to create a <b>Right-Circular</b> state. Watch the behavior of the electric field components along the propagation axis:<br>$\mathbf{J}_{R} = \frac{1}{\sqrt{2}} \begin{pmatrix} 1 \\ e^{i\pi/2} \end{pmatrix} = \frac{1}{\sqrt{2}} \begin{pmatrix} 1 \\ i \end{pmatrix}$",
                "hint": r"A right-circular state requires equal amplitudes (which you already have) but a $\pi/2$ phase shift.",
                "setup": {"show_poincare": False, "show_toggles": False, "disable_keys": ["E_x_amp"]},
                "target": {"E_x_amp": 0.71, "phase_relative_pi": 0.5},
                "solution": {"E_x_amp": 0.71, "phase_relative_pi": 0.5},
                "explanation": r"By adding a relative phase shift of $\varphi = \frac{\pi}{2}$ while keeping equal amplitudes ($E_x = E_y$), the horizontal component reaches its maximum displacement exactly when the vertical component passes through zero. In the Jones notation, this introduces the imaginary unit ($e^{i\pi/2} = i$). This continuous quarter-wave delay causes the combined electric field vector to rotate circularly as it propagates through space.<br><br>Here is a summary of the standard polarization states:<br>• <b>Horizontal:</b> $\mathbf{J}_H = \begin{pmatrix} 1 \\ 0 \end{pmatrix}$<br>• <b>Vertical:</b> $\mathbf{J}_V = \begin{pmatrix} 0 \\ 1 \end{pmatrix}$<br>• <b>Diagonal:</b> $\mathbf{J}_D = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 \\ 1 \end{pmatrix}$<br>• <b>Anti-Diagonal:</b> $\mathbf{J}_A = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 \\ -1 \end{pmatrix}$<br>• <b>Right-Circular:</b> $\mathbf{J}_R = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 \\ i \end{pmatrix}$<br>• <b>Left-Circular:</b> $\mathbf{J}_L = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 \\ -i \end{pmatrix}$<br><br>Notice two key algebraic rules: First, the linear states ($\mathbf{J}_H$, $\mathbf{J}_V$, $\mathbf{J}_D$, and $\mathbf{J}_A$) completely lack a complex phase shift. Second, the diagonal and circular states ($\mathbf{J}_D$, $\mathbf{J}_A$, $\mathbf{J}_L$, and $\mathbf{J}_R$) all share perfectly balanced amplitudes where $|E_x| = |E_y|$."
            },
            {
                "text": r"<b>Step 4 of 9: Wave Plates (Retarders)</b><br>A wave plate has different refractive indices along two axes, called the fast and slow axes, and orthogonally decomposes light to introduce a phase delay $\Gamma$ between these two axes. If the fast axis angle is at $0^\circ$ (horizontal), within the Jones formalism it can be described with the matrix $\mathbf{M}(\Gamma) = \begin{pmatrix} 1 & 0 \\ 0 & e^{i\Gamma} \end{pmatrix}.$ The retardance $\Gamma$ is directly proportional to the physical thickness of the wave plate. It only changes the relative phase of a Jones vector $\begin{pmatrix} E_x \\ E_y e^{i\varphi} \end{pmatrix}$:<br><br> $\begin{pmatrix} 1 & 0 \\ 0 & e^{i\Gamma} \end{pmatrix}\begin{pmatrix} E_x \\ E_y e^{i\varphi} \end{pmatrix}=\begin{pmatrix} E_x \\ E_y e^{i(\varphi+\Gamma)} \end{pmatrix}.$<br><br> We have inserted a wave plate (WP) into the beam path.",
                "task": r"Starting with a diagonal incident wave ($E_x = E_y = \frac{1}{\sqrt{2}}$), find the retardance $\Gamma$ necessary to output a left-circularly polarized state.",
                "hint": r"To rotate a diagonal vector to a left-circular one, the wave component $E_y$ needs to be shifted by more than $\pi$.",
                "setup": {"insert_wp": True, "E_x_amp": 0.71, "phase_relative_pi": 0.0, "wp_angle_deg": 0.0, "retardance_pi": 0.0, "show_toggles": False, "show_poincare": False, "disable_keys": ["E_x_amp", "phase_relative_pi", "wp_angle_deg"]},
                "target": {"E_x_amp": 0.71, "retardance_pi": 1.5},
                "solution": {"retardance_pi": 1.5},
                "explanation": r"The incident wave is diagonally polarized: $\mathbf{J}_{in} = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 \\ 1 \end{pmatrix}$. The wave plate operator is: $$\mathbf{M}(45^\circ, \pi) =  \begin{pmatrix} 1 & 0 \\ 0 & e^{3i\pi/2}=-i \end{pmatrix}$$ Multiplying this operator by the incident wave yields: $$\begin{pmatrix} 1 & 0 \\ 0 & -i \end{pmatrix}\cdot \frac{1}{\sqrt{2}} \begin{pmatrix} 1 \\ 1 \end{pmatrix} = \begin{pmatrix} 1 \\ -i \end{pmatrix} = \mathbf{J}_L.$$ Physically, the wave plate's fast axis is aligned horizontally ($\Delta = 0^\circ$). Setting the retardance to $\Gamma = 1.5\pi$ delays the vertical component of the wave by $\frac{3\pi}{2}$ (which is geometrically equivalent to $-\frac{\pi}{2}$). This transforms the in-phase diagonal oscillation into a left-handed spiral, creating left-circularly polarized light."
            },
            {
                "text": r"<b>Step 5 of 9: Rotating the wave plate</b><br>Turning the wave plate by an angle $\theta$ is equivalent to a coordinate transformation of the $x$-$y$ plane—a rotation back and forth using the rotation matrix $\mathbf{R}(\theta) = \begin{pmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{pmatrix}$. You can also think of the coordinate transformation as tilting your head while the polarization of the incident light tilts along and the wave plate stays where it is. The combined operator is $\mathbf{M}(\theta, \Gamma) = \mathbf{R}(-\theta) \mathbf{M}(\Gamma) \mathbf{R}(\theta)$.",
                "task": r"Starting with a right-handed circularly polarized incident wave ($E_x = E_z = \frac{1}{\sqrt{2}}$ and $\varphi=\frac{\pi}{2}$), find the <i>fast axis angle</i> $\Delta$ necessary to output a <b>vertical</b> state.",
                "hint": r"You need to counteract the $\pi/2$ phase shift of the circular state to make it linearly polarized, and simultaneously rotate it to be vertical. Think about how a quarter-wave plate can achieve this.",
                "setup": {"insert_wp": True, "E_x_amp": 0.707, "phase_relative_pi": 0.5, "wp_angle_deg": 0.0, "retardance_pi": 0.5, "show_toggles": False, "show_poincare": False, "disable_keys": ["E_x_amp", "phase_relative_pi", "retardance_pi"]},
                "target": {"E_x_amp": 0.707, "phase_relative_pi": 0.5, "retardance_pi": 0.5, "wp_angle_deg": 135.0},
                "solution": {"E_x_amp": 0.707, "phase_relative_pi": 0.5, "retardance_pi": 0.5, "wp_angle_deg": 135.0},
                "explanation": r"The incident wave is right-circular: $\mathbf{J}_{in} = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 \\ i \end{pmatrix}$. We require a final linear vertical state: $\mathbf{J}_{out} = \begin{pmatrix} 0 \\ 1 \end{pmatrix}$. A quarter-wave plate ($\Gamma = 0.5\pi$) introduces the necessary relative phase shift to mathematically cancel out the imaginary component, converting the circular polarization into a linear polarization. Orienting the wave plate fast axis to $\Delta = 135^\circ$ aligns the fast and slow axes such that the output wave projection along the horizontal axis perfectly destructs, leaving purely vertical light."
            },
            {
                "text": r"<b>Step 6 of 9: Mastering Wave Plates</b><br>As a reminder, a wave plate is a unitary operator that alters the phase relationship of the wave components. Let's test your intuition.",
                "task": r"Start with a <b>horizontal</b> incident wave. Find the retardance and the fast axis angle needed to rotate the state to create a <b>diagonal</b> state (+45$^\circ$ angle of the combined wave vector).",
                "hint": r"A half-wave plate ($\Gamma = 1.0\pi$) acts as a mirror, reflecting the linear polarization angle across its fast axis. To get from $0^\circ$ to $45^\circ$, where should the mirror line be?",
                "setup": {"wp_angle_deg": 0.0, "retardance_pi": 0.0, "E_x_amp": 1.0, "phase_relative_pi": 0.0, "show_toggles": False, "show_poincare": False, "disable_keys": ["E_x_amp", "phase_relative_pi"]},
                "target": {"E_x_amp": 1.0, "S_final": [0, 1, 0]},
                "solution": {"retardance_pi": 1.0, "wp_angle_deg": 22.5},
                "explanation": r"We begin at horizontal polarization and want to map to diagonal polarization. A half-wave plate ($\Gamma = 1.0\pi$) rotates a linear polarization plane by an angle $2\Delta$ relative to its incident angle. To rotate from $0^\circ$ (horizontal) to $45^\circ$ (diagonal), the required fast axis angle is exactly half the total rotation: $$\Delta = \frac{45^\circ}{2} = 22.5^\circ$$"
            },
            {
                "text": r"<b>Step 7 of 9: Linear Polarizers</b><br>Unlike a wave plate, a linear polarizer is a <i>non-unitary</i> operator—it absorbs light and reduces overall intensity (defined as the absolute value of the Jones vector squared). A horizontal polarizer projects the electric field onto the $x$-axis, represented by the matrix:<br><br>$\mathbf{P}(0^\circ) = \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix}$<br><br>Just like the wave plate, turning the polarizer applies a coordinate rotation: $\mathbf{P}(\theta) = \mathbf{R}(-\theta) \mathbf{P}(0^\circ) \mathbf{R}(\theta)$.",
                "task": r"Find the transmission angle $\theta$ that projects any incident state into a pure <b>horizontal</b> state.",
                "hint": r"You want the final state to be purely horizontal. Turn your Polarizer's transmission Axis so that it fits the axis of polarization of outgoing light that you want. Notice how the intensity drops to exactly 50% as you project the diagonal vector.",
                "setup": {"insert_wp": False, "insert_pol": True, "pol_angle_deg": 90.0, "E_x_amp": 0.71, "phase_relative_pi": 0.0, "show_toggles": False, "show_poincare": False, "disable_keys": ["E_x_amp", "phase_relative_pi"]},
                "target": {"pol_angle_deg": [0.0, 180.0]},
                "solution": {"pol_angle_deg": 0.0},
                "explanation": r"The incident diagonal wave is represented by $\mathbf{J}_{in} = \mathbf{J}_{D}  = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 \\ 1 \end{pmatrix}$. To output a purely horizontal state, the polarizer must completely block the vertical components of the field. Setting the polarizer angle to $\theta = 0^\circ$ initializes the projection matrix $\mathbf{P}(0^\circ) = \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix}$. Multiplying the vector yields: $$\mathbf{P}(0^\circ)\mathbf{J}_{in} = \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix} \left[\frac{1}{\sqrt{2}}\begin{pmatrix} 1 \\ 1 \end{pmatrix}\right] = \begin{pmatrix} \frac{1}{\sqrt{2}} \\ 0 \end{pmatrix}$$ Evaluating the transmitted beam intensity mathematically: $$I = |E_x|^2 + |E_y|^2 = \left|\frac{1}{\sqrt{2}}\right]^2 + 0 = 0.50$$ Exactly 50% of the beam's energy is absorbed because the polarizer filters out the orthogonal vertical component."
            },
            {
                "text": r"<b>Step 8 of 9: Putting it all together</b><br>Let's combine operators!",
                "task": r"Let the incident wave be <b>vertical</b> ($E_x=0.0$). Your goal is to pass this light through BOTH a wave plate and a polarizer to achieve a final transmitted state that is <b>horizontal</b> with an intensity of exactly <b>50%</b> of the original beam.",
                "hint": r"For example, you can first use a Quarter-Wave plate to transform the vertical light into a Right-Circular state, then project it using the polarizer.",
                "setup": {"insert_wp": True, "insert_pol": True, "E_x_amp": 0.0, "phase_relative_pi": 0.0, "wp_angle_deg": 0.0, "retardance_pi": 0.0, "pol_angle_deg": 90.0, "show_toggles": False, "show_poincare": False, "disable_keys": ["E_x_amp", "phase_relative_pi"]},
                "target": {"S_final": [1.0, 0.0, 0.0], "intensity_percent": 50.0},
                "solution": {"retardance_pi": 0.5, "wp_angle_deg": 45.0, "pol_angle_deg": 0.0},
                "explanation": r"We track this sequence step-by-step through the optical train:<br>1. <b>Incident State:</b> The wave starts as purely vertical light: $\mathbf{J}_{in} = \begin{pmatrix} 0 \\ 1 \end{pmatrix}$.<br>2. <b>Wave Plate Action:</b> Setting the quarter-wave plate ($\Gamma = 0.5\pi$) to a physical angle of $\Delta = 45^\circ$ introduces a phase shift that transforms the linear wave into right-circular light: $\mathbf{J}_{wp} = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 \\ i \end{pmatrix}$.<br>3. <b>Polarizer Action:</b> The circular wave then encounters a linear polarizer at $\theta = 0^\circ$. Applying the projection matrix filters out the vertical phase component entirely: $$\mathbf{P}(0^\circ)\mathbf{J}_{wp} = \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix} \left[\frac{1}{\sqrt{2}}\begin{pmatrix} 1 \\ i \end{pmatrix}\right] = \begin{pmatrix} \frac{1}{\sqrt{2}} \\ 0 \end{pmatrix}$$ This results in a purely horizontal output wave with a final intensity of $|\frac{1}{\sqrt{2}}|^2 = 0.50$."
            },
            {
                "text": r"<b>Step 9 of 9: The Final Challenge</b><br>Let's combine operators for a lossless transmission!",
                "task": r"Start with an incident <b>Right-Circular</b> wave. Your goal is to use BOTH the wave plate and the polarizer to output a pure <b>Diagonal</b> state (+45$^\circ$) with an intensity of exactly <b>100%</b> (no light absorbed).",
                "hint": r"To get 100% intensity through the polarizer, the wave entering it must already be perfectly diagonal. Find the wave plate retardance and angle that cancels the circular phase shift and aligns the wave diagonally, then match the polarizer angle.",
                "setup": {"insert_wp": True, "insert_pol": True, "E_x_amp": 0.707, "phase_relative_pi": 0.5,
                          "wp_angle_deg": 45.0, "retardance_pi": 0.0, "pol_angle_deg": 0.0, "show_toggles": False,
                          "show_poincare": False, "disable_keys": ["E_x_amp", "phase_relative_pi"]},
                "target": {"S_final": [0.0, 1.0, 0.0], "intensity_percent": 100.0},
                "solution": {"retardance_pi": 0.5, "wp_angle_deg": 90.0, "pol_angle_deg": 45.0},
                "explanation": r"To achieve 100% transmission through a linear polarizer, the light entering it must already perfectly match its transmission axis. Therefore, your wave plate must convert the Right-Circular light directly into Diagonal light. Mathematically, a quarter-wave plate ($\Gamma = 0.5\pi$) with its fast axis vertical ($\Delta = 90^\circ$) delays the horizontal component relative to the vertical one, canceling out the initial phase shift of the circular light and bringing both components perfectly in-phase. This yields a linear diagonal wave. Finally, turning the polarizer to $\theta = 45^\circ$ matches this wave, allowing it to pass through entirely without absorption. Note: A fast axis of $0^\circ$ and retardance of $1.5\pi$ is also a valid mathematical solution!"
            },
            {
                "text": r"<b>Tutorial Completed!</b><br>Congratulations, you have finished the interactive physics module. Feel free to play around with the optical elements above. When you are ready to proceed with the study, click the return button at the bottom of the screen.<br>",
                "task": r"",
                "setup": {"insert_wp": True, "insert_pol": True, "show_toggles": True, "show_poincare": False,
                          "disable_keys": []},
                "target": {}
            }
        ]
    },
    "Free Play": {
        "steps": [
            {
                "text": r"<b>Free Play Mode</b><br>Explore the simulation freely.",
                "task": r"Use the toggles and sliders below to interact with the wave plates and polarizers. There are no targets to reach.",
                "setup": {"show_poincare": True, "show_toggles": True, "disable_keys": []},
                "target": {}
            }
        ]
    }
}