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
                "text": r"<b>Step 1: The Macroscopic Wave</b><br>Light is an electromagnetic wave where the electric field $\vec{E}$ is confined to the transverse $x$-$y$ plane, oscillating perpendicular to the direction of propagation. The wave can be described by the Jones vector $\vec{E} = \begin{pmatrix} E_x \\ E_y e^{i\varphi} \end{pmatrix}$. The absolute value of the amplitudes of the Jones vector squared must add up to one: $|E_X|^2+|E_Y|^2=1$.",
                "task": r"Move the slider to $E_x=0.5$ and watch the change in the electric field components and the combined wave in the applet below. Notice how the amplitude in $y$ direction $E_y$ is not the same as $E_x$.",
                "hint": r"Focus on the <b>Incident Wave</b> section. Adjust the first slider until the Amplitude $E_x$ reads exactly <b>0.50</b>.",
                "setup": {"insert_wp": False, "insert_pol": False, "show_poincare": False, "E_x_amp": 0.0, "phase_relative_pi": 0.0, "show_toggles": False},
                "target": {"E_x_amp": 0.5},
                "solution": {"E_x_amp": 0.5},
                "explanation": r"Because the total energy intensity of the normalized plane wave is conserved ($I = |E_x|^2 + |E_y|^2 = 1$), fixing the horizontal field amplitude to $E_x = 0.5$ forces the vertical field amplitude component to automatically balance to: $$E_y = \sqrt{1.0 - 0.5^2} = \sqrt{0.75} \approx 0.866$$ Since no relative phase shift is present ($\varphi = 0$), the wave remains linearly polarized, but the unequal component amplitudes tilt the net polarization angle away from the standard $45^\circ$ line. Click on the Next Step button below the applet to proceed."
            },
            {
                "text": r"<b>Step 2: Constructing Standard States</b><br>Any state of polarization $\mathbf{J}$ can be expressed as a linear combination of horizontal $\mathbf{J}_H=\begin{pmatrix}1 \\ 0\end{pmatrix}$ and vertical $\mathbf{J}_V=\begin{pmatrix}0 \\ 1\end{pmatrix}$ basis vectors: $$\mathbf{J}=\alpha \mathbf{J}_H+ \beta\mathbf{J}_V,$$ where $\alpha$ and $\beta$ are complex numbers. In the Jones formalism, the resulting vector has to be normalized, i.e., $|\alpha|^2+|\beta|^2=1$",
                "task": r"Create an approximately <b>diagonal</b> state, which requires equal amplitudes: $\mathbf{J}_{D} = \frac{1}{\sqrt{2}} \left(\mathbf{J}_H+\mathbf{J}_V\right)= \frac{1}{\sqrt{2}} \begin{pmatrix} 1 \\ 1 \end{pmatrix}$.",
                "hint": r"You want the amplitudes to be perfectly balanced. Since $|E_x|^2+|E_y|^2=1$, you need an amplitude of roughly $\sqrt{1/2}\approx 0.71 $.",
                "setup": {"show_toggles": False},
                "target": {"E_x_amp": 0.71, "phase_relative_pi": [0.0, 2.0]},
                "solution": {"E_x_amp": 0.71, "phase_relative_pi": 0.0},
                "explanation": r"A purely diagonal state $\mathbf{J}_D$ implies that the spatial oscillations along the horizontal and vertical channels are perfectly symmetric and in-phase. Mathematically, this dictates that $|\alpha| = |\beta|$, requiring: $$E_x = E_y = \frac{1}{\sqrt{2}} \approx 0.707$$ Setting the relative phase to $\varphi = 0$ (or $2\pi$) keeps the components in geometric phase synchronization, forcing the electric field vector to sweep out a linear path at exactly $+45^\circ$ in the transverse plane."
            },
            {
                "text": r"<b>Step 3: The Poincaré Sphere</b><br>We have now revealed the <b>Poincaré Sphere</b> below the applet. Notice how the diagonal state you just created maps exactly to the equator.",
                "task": r"Now, introduce a relative phase shift to create a <b>Right-Circular</b> state (Phase = 0.5π). Watch the state vector leave the equator and travel to the north pole:<br>$\mathbf{J}_{R} = \frac{1}{\sqrt{2}} \begin{pmatrix} 1 \\ e^{i\pi/2} \end{pmatrix} = \frac{1}{\sqrt{2}} \begin{pmatrix} 1 \\ i \end{pmatrix}$",
                "hint": r"Circular states require equal amplitudes (which you already have) but a $\pi/2$ phase shift.",
                "setup": {"show_poincare": True, "show_toggles": False},
                "target": {"E_x_amp": 0.71, "phase_relative_pi": 0.5},
                "solution": {"E_x_amp": 0.71, "phase_relative_pi": 0.5},
                "explanation": r"By adding a relative phase shift of $\varphi = \frac{\pi}{2}$ while keeping equal amplitudes ($E_x = E_y$), the horizontal component reaches its maximum displacement exactly when the vertical component passes through zero. In the Jones notation, this introduces the imaginary unit ($e^{i\pi/2} = i$). The polarization vector is moved from the equator towards the north pole of the sphere by an angle of $\pi/2$."
            },
            {
                "text": r"<b>Step 4: Wave Plates (Retarders)</b><br>A wave plate orthogonally decomposes light and introduces a phase delay $\Gamma$ between the fast and slow axes. If the fast axis angle is at $0^\circ$ (horizontal), within the Jones formalism it can be described with the matrix $\mathbf{M}(\Gamma) = \begin{pmatrix} 1 & 0 \\ 0 & e^{i\Gamma} \end{pmatrix}$, which only changes the relative phase of a Jones vector $\begin{pmatrix} E_x \\ E_y e^{i\varphi} \end{pmatrix}$:<br><br> $\begin{pmatrix} 1 & 0 \\ 0 & e^{i\Gamma} \end{pmatrix}\begin{pmatrix} E_x \\ E_y e^{i\varphi} \end{pmatrix}=\begin{pmatrix} E_x \\ E_y e^{i(\varphi+\Gamma)} \end{pmatrix}.$<br><br> We have inserted a wave plate (WP) and the Poincaré sphere now shows the WP operator as a rotation axis (orange dashed line). On the Poincaré sphere, the retardance is the angle of rotation around the axis of the wave plate operator that is given by the WP Fast axis angle.",
                "task": r"Starting with a horizontal incident wave ($E_x = 1.0$), find the retardance $\Gamma$ necessary to output a <b>vertical</b> state.",
                "hint": r"To rotate a horizontal vector to a vertical one, you must completely invert the axis. This requires a half-wave plate.",
                "setup": {"insert_wp": True, "E_x_amp": 1.0, "phase_relative_pi": 0.0, "wp_angle_deg": 45.0, "retardance_pi": 0.0, "show_toggles": False},
                "target": {"retardance_pi": [1.0], "wp_angle_deg": [45]},
                "solution": {"retardance_pi": 1.0, "wp_angle_deg": 45.0},
                "explanation": r"The incident beam is horizontally polarized: $\mathbf{J}_{in} = \begin{pmatrix} 1 \\ 0 \end{pmatrix}$. The wave plate fast axis sits at $\Delta = 45^\circ$, making the system operator: $$\mathbf{M}(45^\circ, \pi) = \begin{pmatrix} \cos^2(45^\circ) + e^{i\pi}\sin^2(45^\circ) & \sin(45^\circ)\cos(45^\circ)(1 - e^{i\pi}) \\ \sin(45^\circ)\cos(45^\circ)(1 - e^{i\pi}) & \sin^2(45^\circ) + e^{i\pi}\cos^2(45^\circ) \end{pmatrix} = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$$ Multiplying this operator by the incident wave yields: $$\begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix} \begin{pmatrix} 1 \\ 0 \end{pmatrix} = \begin{pmatrix} 0 \\ 1 \end{pmatrix} = \mathbf{J}_V$$ Geometrically on the Poincaré sphere, the wave plate fast axis at $\Delta = 45^\circ$ creates a rotation axis pointing towards the diagonal state ($2\Delta = 90^\circ$). Setting the retardance to $\Gamma = 1.0\pi$ triggers a perfect $180^\circ$ geometric flip around this diagonal axis, mapping the horizontal state point cleanly to the vertical state point on the opposing side of the equator."
            },
            {
                "text": r"<b>Step 5: Rotating the wave plate</b><br>Turning the wave plate by an angle $\theta$ is equivalent to a coordinate transformation of the $x$-$y$ plane—a rotation back and forth using the rotation matrix $\mathbf{R}(\theta) = \begin{pmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{pmatrix}$. The combined operator is $\mathbf{M}(\theta, \Gamma) = \mathbf{R}(-\theta) \mathbf{M}(\Gamma) \mathbf{R}(\theta)$. The retardance $\Gamma$ is characterized by the rotation angle, and the fast axis angle $\Delta$ is represented by the azimuthal angle $2\Delta$ of the WP operator axis on the equator of the sphere.",
                "task": r"Starting with a right-handed circularly polarized incident wave ($E_x = E_z = \frac{1}{\sqrt{2}}$ and $\varphi=\frac{\pi}{2}$), find the <i>fast axis angle</i> $\Delta$ necessary to output a <b>vertical</b> state.",
                "hint": r"Rotating a right-handed circularly polarized vector to a vertical one requires a $\pi/2$ rotation on the sphere. The rotation axis must be chosen such that the vector travels clockwise around the sphere, meaning it has to be rotated by more than 90 degrees counterclockwise.",
                "setup": {"insert_wp": True, "E_x_amp": 0.707, "phase_relative_pi": 0.5, "wp_angle_deg": 0.0, "retardance_pi": 0.5, "show_toggles": False},
                "target": {"E_x_amp": 0.707, "phase_relative_pi": 0.5, "retardance_pi": 0.5, "wp_angle_deg": 135.0},
                "solution": {"E_x_amp": 0.707, "phase_relative_pi": 0.5, "retardance_pi": 0.5, "wp_angle_deg": 135.0},
                "explanation": r"The incident wave is right-circular: $\mathbf{J}_{in} = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 \\ i \end{pmatrix}$, corresponding to the north pole on the sphere. We require a final linear vertical state: $\mathbf{J}_{out} = \begin{pmatrix} 0 \\ 1 \end{pmatrix}$, located at the backside on the equator. Geometrically, moving from the pole to the equator requires a rotation of exactly $\Gamma = 90^\circ = 0.5\pi$ (a quarter-wave plate). To rotate the state vector from the top down directly into the vertical axis point, the rotation axis must be perpendicular to both vectors on the equator. Orienting the wave plate fast axis to $\Delta = 135^\circ$ creates an operator axis on the sphere at $2\Delta = 270^\circ$ (the anti-diagonal state axis). A clockwise quarter-turn rotation around this axis sweeps the state vector down along the meridian, landing perfectly on the vertical point."
            },
            {
                "text": r"<b>Step 6: Mastering Wave Plates</b><br>As a reminder, a wave plate is a unitary operator that acts as a pure geometric rotation on the sphere. The rotation axis lies on the equator at an azimuthal angle $2\Delta$ (where $\Delta$ is the physical <i>fast axis angle</i>), and the rotation amount is the <i>retardance</i> $\Gamma$. Let's test your intuition.",
                "task": r"Start with a <b>horizontal</b> incident wave. Find the retardance and the fast axis angle needed to rotate the state to create a <b>diagonal</b> state.",
                "hint": r"To travel along the equator (horizontal) to the diagonal state, your rotation axis on the sphere needs to reflect around an axis that is between the horizontal and diagonal axes on the sphere.",
                "setup": {"wp_angle_deg": 0.0, "retardance_pi": 0.0, "E_x_amp": 1.0, "phase_relative_pi": 0.0, "show_toggles": False},
                "target": {"E_x_amp": 1.0, "S_final": [0, 1, 0]},
                "solution": {"retardance_pi": 1.0, "wp_angle_deg": 22.5},
                "explanation": r"We begin at horizontal polarization and want to map directly to diagonal polarization along the equatorial plane. To execute this move using a half-wave plate ($\Gamma = 1.0\pi$, which acts as a $180^\circ$ flip), the rotation axis on the sphere must be positioned exactly halfway between the initial and target states on the equator. The angular separation between horizontal ($0^\circ$ on the sphere) and diagonal ($90^\circ$ on the sphere) is $90^\circ$. The bisection axis must sit at an azimuthal position of exactly: $$2\Delta = \frac{90^\circ}{2} = 45^\circ$$ The required fast axis angle is therefore $22.5^\circ$."
            },
            {
                "text": r"<b>Step 7: Linear Polarizers</b><br>Unlike a wave plate, a linear polarizer is a <i>non-unitary</i> operator—it absorbs light and reduces overall intensity. A horizontal polarizer projects the electric field onto the $x$-axis, represented by the matrix:<br><br>$\mathbf{P}(0^\circ) = \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix}$<br><br>On the Poincaré sphere, this acts as a projection straight through the volume of the sphere onto the transmission axis state. Just like the wave plate, turning the polarizer applies a coordinate rotation: $\mathbf{P}(\theta) = \mathbf{R}(-\theta) \mathbf{P}(0^\circ) \mathbf{R}(\theta)$.",
                "task": r"Find the transmission angle $\theta$ that projects an incident <b>diagonal</b> state into a pure <b>horizontal</b> state.",
                "hint": r"You want the final state to sit on the pure horizontal axis of the sphere. Turn your Polarizer's transmission Axis so that it fits the axis of polarization of outgoing light that you want. Notice how the intensity drops to exactly 50% as you project the diagonal vector.",
                "setup": {"insert_wp": False, "insert_pol": True, "pol_angle_deg": 90.0, "E_x_amp": 0.71, "phase_relative_pi": 0.0, "show_toggles": False},
                "target": {"pol_angle_deg": [0.0, 180.0]},
                "solution": {"pol_angle_deg": 0.0},
                "explanation": r"The incident diagonal wave is represented by $\mathbf{J}_{in} = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 \\ 1 \end{pmatrix}$. To output a purely horizontal state, the polarizer must completely block the vertical components of the field. Setting the polarizer angle to $\theta = 0^\circ$ initializes the projection matrix $\mathbf{P}(0^\circ) = \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix}$. Multiplying the vector yields: $$\mathbf{P}(0^\circ)\mathbf{J}_{in} = \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix} \left[\frac{1}{\sqrt{2}}\begin{pmatrix} 1 \\ 1 \end{pmatrix}\right] = \begin{pmatrix} \frac{1}{\sqrt{2}} \\ 0 \end{pmatrix}$$ Evaluating the transmitted beam intensity explains Malus's Law mathematically: $$I = |E_x|^2 + |E_y|^2 = \left|\frac{1}{\sqrt{2}}\right]^2 + 0 = 0.50$$ Exactly 50% of the beam's energy is absorbed because the polarizer filters out the orthogonal vertical component."
            },
            {
                "text": r"<b>Step 8: The Final Challenge</b><br>Let's combine operators!",
                "task": r"Let the incident wave be <b>vertical</b> ($E_x=0.0$). Your goal is to pass this light through BOTH a wave plate and a polarizer to achieve a final transmitted state that is <b>horizontal</b> with an intensity of exactly <b>50%</b> of the original beam.",
                "hint": r"First use a Quarter-Wave plate to transform the vertical light into a Right-Circular state, then project it using the polarizer.)",
                "setup": {"insert_wp": True, "insert_pol": True, "E_x_amp": 0.0, "phase_relative_pi": 0.0, "wp_angle_deg": 0.0, "retardance_pi": 0.0, "pol_angle_deg": 90.0, "show_toggles": False},
                "target": {"retardance_pi": 0.5, "wp_angle_deg": [45.0, 135.0], "pol_angle_deg": [0.0, 180.0]},
                "solution": {"retardance_pi": 0.5, "wp_angle_deg": 45.0, "pol_angle_deg": 0.0},
                "explanation": r"We track this sequence step-by-step through the optical train:<br>1. <b>Incident State:</b> The wave starts as purely vertical light: $\mathbf{J}_{in} = \begin{pmatrix} 0 \\ 1 \end{pmatrix}$.<br>2. <b>Wave Plate Action:</b> Setting the quarter-wave plate ($\Gamma = 0.5\pi$) to a physical angle of $\Delta = 45^\circ$ places the rotation axis at the diagonal position on the sphere. A $90^\circ$ rotation pushes the state vector from the equator straight up to the north pole, transforming the wave into right-circular light: $\mathbf{J}_{wp} = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 \\ i \end{pmatrix}$.<br>3. **Polarizer Action:** The circular wave then encounters a linear polarizer at $\theta = 0^\circ$. Applying the projection matrix filters out the vertical phase component entirely: $$\mathbf{P}(0^\circ)\mathbf{J}_{wp} = \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix} \left[\frac{1}{\sqrt{2}}\begin{pmatrix} 1 \\ i \end{pmatrix}\right] = \begin{pmatrix} \frac{1}{\sqrt{2}} \\ 0 \end{pmatrix}$$ This results in a purely horizontal output wave with a final intensity of $|\frac{1}{\sqrt{2}}|^2 = 0.50$ (50% power). On the sphere, the state vector is projected straight through the center volume from the north pole down to the horizontal equatorial anchor point."
            },
            {
                "text": r"Done. Congratulations, you completed the tutorial. The codeword to proceed in the study is <b>horizontal light</b>. Please copy this, go back to the survey, and enter to proceed. Feel free to play around with the applet!<br>",
                "task": r"",
                "setup": {"insert_wp": True, "insert_pol": True, "show_toggles": True},
                "target": {}
            }
        ]
    },
"Polarization 2": {
        "steps": [
            {
                "text": r"<b>Step 1: The Macroscopic Wave</b><br>Light is an electromagnetic wave where the electric field $\vec{E}$ is confined to the transverse $x$-$y$ plane, oscillating perpendicular to the direction of propagation. The wave can be described by the Jones vector $\vec{E} = \begin{pmatrix} E_x \\ E_y e^{i\varphi} \end{pmatrix}$. The absolute value of the amplitudes of the Jones vector squared must add up to one: $|E_X|^2+|E_Y|^2=1$.",
                "task": r"Move the slider to $E_x=0.5$ and watch the change in the electric field components and the combined wave in the applet below. Notice how the amplitude in $y$ direction $E_y$ is not the same as $E_x$. Click on the Next Step button below to proceed.",
                "hint": r"Focus on the <b>Incident Wave</b> section. Adjust the first slider until the Amplitude $E_x$ reads exactly <b>0.50</b>.",
                "setup": {"insert_wp": False, "insert_pol": False, "show_poincare": False, "E_x_amp": 0.0, "phase_relative_pi": 0.0, "show_toggles": False},
                "target": {"E_x_amp": 0.5},
                "solution": {"E_x_amp": 0.5},
                "explanation": r"Because the total energy intensity of the normalized plane wave is conserved ($I = |E_x|^2 + |E_y|^2 = 1$), fixing the horizontal field amplitude to $E_x = 0.5$ forces the vertical field amplitude component to automatically balance to: $$E_y = \sqrt{1.0 - 0.5^2} = \sqrt{0.75} \approx 0.866$$ Since no relative phase shift is present ($\varphi = 0$), the wave remains linearly polarized, but the unequal component amplitudes tilt the net polarization angle away from the standard $45^\circ$ line. Click on the Next Step button below to proceed."
            },
            {
                "text": r"<b>Step 2: Constructing Standard States</b><br>Any state of polarization $\mathbf{J}$ can be expressed as a linear combination of horizontal $\mathbf{J}_H=\begin{pmatrix}1 \\ 0\end{pmatrix}$ and vertical $\mathbf{J}_V=\begin{pmatrix}0 \\ 1\end{pmatrix}$ basis vectors: $$\mathbf{J}=\alpha \mathbf{J}_H+ \beta\mathbf{J}_V,$$ where $\alpha$ and $\beta$ are complex numbers. In the Jones formalism, the resulting vector has to be normalized, i.e., $|\alpha|^2+|\beta|^2=1$",
                "task": r"Create an approximately <b>diagonal</b> state, which requires equal amplitudes: $\mathbf{J}_{D} = \frac{1}{\sqrt{2}} \left(\mathbf{J}_H+\mathbf{J}_V\right)= \frac{1}{\sqrt{2}} \begin{pmatrix} 1 \\ 1 \end{pmatrix}$.",
                "hint": r"You want the amplitudes to be perfectly balanced. Since $|E_x|^2+|E_y|^2=1$, you need an amplitude of roughly $\sqrt{1/2}\approx 0.71 $.",
                "setup": {"show_toggles": False, "show_poincare": False},
                "target": {"E_x_amp": 0.71, "phase_relative_pi": [0.0, 2.0]},
                "solution": {"E_x_amp": 0.71, "phase_relative_pi": 0.0},
                "explanation": r"A purely diagonal state $\mathbf{J}_D$ implies that the spatial oscillations along the horizontal and vertical channels are perfectly symmetric and in-phase. Mathematically, this dictates that $|\alpha| = |\beta|$, requiring: $$E_x = E_y = \frac{1}{\sqrt{2}} \approx 0.707$$ Setting the relative phase to $\varphi = 0$ (or $2\pi$) keeps the components in phase synchronization, forcing the electric field vector to sweep out a linear path at exactly $+45^\circ$ in the transverse plane."
            },
            {
                "text": r"<b>Step 3: Circular States</b><br>Notice how the diagonal state you just created features perfectly balanced amplitudes but no phase shift.",
                "task": r"Now, introduce a relative phase shift to create a <b>Right-Circular</b> state (Phase = 0.5π). Watch the behavior of the electric field components along the propagation axis:<br>$\mathbf{J}_{R} = \frac{1}{\sqrt{2}} \begin{pmatrix} 1 \\ e^{i\pi/2} \end{pmatrix} = \frac{1}{\sqrt{2}} \begin{pmatrix} 1 \\ i \end{pmatrix}$",
                "hint": r"Circular states require equal amplitudes (which you already have) but a $\pi/2$ phase shift.",
                "setup": {"show_poincare": False, "show_toggles": False},
                "target": {"E_x_amp": 0.71, "phase_relative_pi": 0.5},
                "solution": {"E_x_amp": 0.71, "phase_relative_pi": 0.5},
                "explanation": r"By adding a relative phase shift of $\varphi = \frac{\pi}{2}$ while keeping equal amplitudes ($E_x = E_y$), the horizontal component reaches its maximum displacement exactly when the vertical component passes through zero. In the Jones notation, this introduces the imaginary unit ($e^{i\pi/2} = i$). This continuous quarter-wave delay causes the combined electric field vector to rotate circularly as it propagates through space."
            },
            {
                "text": r"<b>Step 4: Wave Plates (Retarders)</b><br>A wave plate orthogonally decomposes light and introduces a phase delay $\Gamma$ between the fast and slow axes. If the fast axis angle is at $0^\circ$ (horizontal), within the Jones formalism it can be described with the matrix $\mathbf{M}(\Gamma) = \begin{pmatrix} 1 & 0 \\ 0 & e^{i\Gamma} \end{pmatrix}$, which only changes the relative phase of a Jones vector $\begin{pmatrix} E_x \\ E_y e^{i\varphi} \end{pmatrix}$:<br><br> $\begin{pmatrix} 1 & 0 \\ 0 & e^{i\Gamma} \end{pmatrix}\begin{pmatrix} E_x \\ E_y e^{i\varphi} \end{pmatrix}=\begin{pmatrix} E_x \\ E_y e^{i(\varphi+\Gamma)} \end{pmatrix}.$<br><br> We have inserted a wave plate (WP) into the beam path.",
                "task": r"Starting with a horizontal incident wave ($E_x = 1.0$), find the retardance $\Gamma$ necessary to output a <b>vertical</b> state.",
                "hint": r"To change a horizontal vector to a vertical one, you must completely invert the phase relationship along the diagonal axes. This requires a half-wave plate.",
                "setup": {"insert_wp": True, "E_x_amp": 1.0, "phase_relative_pi": 0.0, "wp_angle_deg": 45.0, "retardance_pi": 0.0, "show_toggles": False, "show_poincare": False},
                "target": {"retardance_pi": [1.0], "wp_angle_deg": [45]},
                "solution": {"retardance_pi": 1.0, "wp_angle_deg": 45.0},
                "explanation": r"The incident beam is horizontally polarized: $\mathbf{J}_{in} = \begin{pmatrix} 1 \\ 0 \end{pmatrix}$. The wave plate fast axis sits at $\Delta = 45^\circ$, making the system operator: $$\mathbf{M}(45^\circ, \pi) = \begin{pmatrix} \cos^2(45^\circ) + e^{i\pi}\sin^2(45^\circ) & \sin(45^\circ)\cos(45^\circ)(1 - e^{i\pi}) \\ \sin(45^\circ)\cos(45^\circ)(1 - e^{i\pi}) & \sin^2(45^\circ) + e^{i\pi}\cos^2(45^\circ) \end{pmatrix} = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$$ Multiplying this operator by the incident wave yields: $$\begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix} \begin{pmatrix} 1 \\ 0 \end{pmatrix} = \begin{pmatrix} 0 \\ 1 \end{pmatrix} = \mathbf{J}_V$$ The $\Gamma = 1.0\pi$ retardance successfully flips the polarization by exactly $90^\circ$ relative to the fast axis."
            },
            {
                "text": r"<b>Step 5: Rotating the wave plate</b><br>Turning the wave plate by an angle $\theta$ is equivalent to a coordinate transformation of the $x$-$y$ plane—a rotation back and forth using the rotation matrix $\mathbf{R}(\theta) = \begin{pmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{pmatrix}$. The combined operator is $\mathbf{M}(\theta, \Gamma) = \mathbf{R}(-\theta) \mathbf{M}(\Gamma) \mathbf{R}(\theta)$.",
                "task": r"Starting with a right-handed circularly polarized incident wave ($E_x = E_z = \frac{1}{\sqrt{2}}$ and $\varphi=\frac{\pi}{2}$), find the <i>fast axis angle</i> $\Delta$ necessary to output a <b>vertical</b> state.",
                "hint": r"You need to counteract the $\pi/2$ phase shift of the circular state to make it linearly polarized, and simultaneously rotate it to be vertical. Think about how a quarter-wave plate can achieve this.",
                "setup": {"insert_wp": True, "E_x_amp": 0.707, "phase_relative_pi": 0.5, "wp_angle_deg": 0.0, "retardance_pi": 0.5, "show_toggles": False, "show_poincare": False},
                "target": {"E_x_amp": 0.707, "phase_relative_pi": 0.5, "retardance_pi": 0.5, "wp_angle_deg": 135.0},
                "solution": {"E_x_amp": 0.707, "phase_relative_pi": 0.5, "retardance_pi": 0.5, "wp_angle_deg": 135.0},
                "explanation": r"The incident wave is right-circular: $\mathbf{J}_{in} = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 \\ i \end{pmatrix}$. We require a final linear vertical state: $\mathbf{J}_{out} = \begin{pmatrix} 0 \\ 1 \end{pmatrix}$. A quarter-wave plate ($\Gamma = 0.5\pi$) introduces the necessary relative phase shift to mathematically cancel out the imaginary component, converting the circular polarization into a linear polarization. Orienting the wave plate fast axis to $\Delta = 135^\circ$ aligns the fast and slow axes such that the output wave projection along the horizontal axis perfectly destructs, leaving purely vertical light."
            },
            {
                "text": r"<b>Step 6: Mastering Wave Plates</b><br>As a reminder, a wave plate is a unitary operator that alters the phase relationship of the wave components. Let's test your intuition.",
                "task": r"Start with a <b>horizontal</b> incident wave. Find the retardance and the fast axis angle needed to rotate the state to create a <b>diagonal</b> state.",
                "hint": r"A half-wave plate ($\Gamma = 1.0\pi$) acts as a mirror, reflecting the linear polarization angle across its fast axis. To get from $0^\circ$ to $45^\circ$, where should the mirror line be?",
                "setup": {"wp_angle_deg": 0.0, "retardance_pi": 0.0, "E_x_amp": 1.0, "phase_relative_pi": 0.0, "show_toggles": False, "show_poincare": False},
                "target": {"E_x_amp": 1.0, "S_final": [0, 1, 0]},
                "solution": {"retardance_pi": 1.0, "wp_angle_deg": 22.5},
                "explanation": r"We begin at horizontal polarization and want to map to diagonal polarization. A half-wave plate ($\Gamma = 1.0\pi$) rotates a linear polarization plane by an angle $2\Delta$ relative to its incident angle. To rotate from $0^\circ$ (horizontal) to $45^\circ$ (diagonal), the required fast axis angle is exactly half the total rotation: $$\Delta = \frac{45^\circ}{2} = 22.5^\circ$$"
            },
            {
                "text": r"<b>Step 7: Linear Polarizers</b><br>Unlike a wave plate, a linear polarizer is a <i>non-unitary</i> operator—it absorbs light and reduces overall intensity. A horizontal polarizer projects the electric field onto the $x$-axis, represented by the matrix:<br><br>$\mathbf{P}(0^\circ) = \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix}$<br><br>Just like the wave plate, turning the polarizer applies a coordinate rotation: $\mathbf{P}(\theta) = \mathbf{R}(-\theta) \mathbf{P}(0^\circ) \mathbf{R}(\theta)$.",
                "task": r"Find the transmission angle $\theta$ that projects an incident <b>diagonal</b> state into a pure <b>horizontal</b> state.",
                "hint": r"You want the final state to be purely horizontal. Turn your Polarizer's transmission Axis so that it fits the axis of polarization of outgoing light that you want. Notice how the intensity drops to exactly 50% as you project the diagonal vector.",
                "setup": {"insert_wp": False, "insert_pol": True, "pol_angle_deg": 90.0, "E_x_amp": 0.71, "phase_relative_pi": 0.0, "show_toggles": False, "show_poincare": False},
                "target": {"pol_angle_deg": [0.0, 180.0]},
                "solution": {"pol_angle_deg": 0.0},
                "explanation": r"The incident diagonal wave is represented by $\mathbf{J}_{in} = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 \\ 1 \end{pmatrix}$. To output a purely horizontal state, the polarizer must completely block the vertical components of the field. Setting the polarizer angle to $\theta = 0^\circ$ initializes the projection matrix $\mathbf{P}(0^\circ) = \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix}$. Multiplying the vector yields: $$\mathbf{P}(0^\circ)\mathbf{J}_{in} = \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix} \left[\frac{1}{\sqrt{2}}\begin{pmatrix} 1 \\ 1 \end{pmatrix}\right] = \begin{pmatrix} \frac{1}{\sqrt{2}} \\ 0 \end{pmatrix}$$ Evaluating the transmitted beam intensity explains Malus's Law mathematically: $$I = |E_x|^2 + |E_y|^2 = \left|\frac{1}{\sqrt{2}}\right]^2 + 0 = 0.50$$ Exactly 50% of the beam's energy is absorbed because the polarizer filters out the orthogonal vertical component."
            },
            {
                "text": r"<b>Step 8: The Final Challenge</b><br>Let's combine operators!",
                "task": r"Let the incident wave be <b>vertical</b> ($E_x=0.0$). Your goal is to pass this light through BOTH a wave plate and a polarizer to achieve a final transmitted state that is <b>horizontal</b> with an intensity of exactly <b>50%</b> of the original beam.",
                "hint": r"First use a Quarter-Wave plate to transform the vertical light into a Right-Circular state, then project it using the polarizer.",
                "setup": {"insert_wp": True, "insert_pol": True, "E_x_amp": 0.0, "phase_relative_pi": 0.0, "wp_angle_deg": 0.0, "retardance_pi": 0.0, "pol_angle_deg": 90.0, "show_toggles": False, "show_poincare": False},
                "target": {"retardance_pi": 0.5, "wp_angle_deg": [45.0, 135.0], "pol_angle_deg": [0.0, 180.0]},
                "solution": {"retardance_pi": 0.5, "wp_angle_deg": 45.0, "pol_angle_deg": 0.0},
                "explanation": r"We track this sequence step-by-step through the optical train:<br>1. <b>Incident State:</b> The wave starts as purely vertical light: $\mathbf{J}_{in} = \begin{pmatrix} 0 \\ 1 \end{pmatrix}$.<br>2. <b>Wave Plate Action:</b> Setting the quarter-wave plate ($\Gamma = 0.5\pi$) to a physical angle of $\Delta = 45^\circ$ introduces a phase shift that transforms the linear wave into right-circular light: $\mathbf{J}_{wp} = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 \\ i \end{pmatrix}$.<br>3. <b>Polarizer Action:</b> The circular wave then encounters a linear polarizer at $\theta = 0^\circ$. Applying the projection matrix filters out the vertical phase component entirely: $$\mathbf{P}(0^\circ)\mathbf{J}_{wp} = \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix} \left[\frac{1}{\sqrt{2}}\begin{pmatrix} 1 \\ i \end{pmatrix}\right] = \begin{pmatrix} \frac{1}{\sqrt{2}} \\ 0 \end{pmatrix}$$ This results in a purely horizontal output wave with a final intensity of $|\frac{1}{\sqrt{2}}|^2 = 0.50$ (50% power)."
            },
            {
                "text": r"Done. Congratulations, you completed the tutorial. The codeword to proceed in the study is <b>vertical light</b>. Please copy this, go back to the survey, and enter to proceed. Feel free to play around with the applet!<br>",
                "task": r"",
                "setup": {"insert_wp": True, "insert_pol": True, "show_toggles": True, "show_poincare": False},
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