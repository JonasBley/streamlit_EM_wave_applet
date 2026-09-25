"""Shared polarization tasks and the sphere-specific instructional intervention."""
from copy import deepcopy

BALANCED_AMPLITUDE = 2 ** -0.5

# Confirmed study mapping; historical pilot records are not relabelled here.
CONDITION_VERSION = "2026-09-25-feedback"
CONDITIONS = {
    "Polarization 1": {"sphere": True, "instruction": "shared plus sphere guidance"},
    "Polarization 2": {"sphere": False, "instruction": "shared"},
}

SHARED_STEPS = [{'text': '<b>Step 1 of 9: The Macroscopic Wave</b><br><b>Polarization</b> describes the pattern traced by the electric-field '
          'direction over time at a fixed position.<br>Classical light is an electromagnetic wave where the electric field '
          '$\\vec{E}$ is confined to the transverse $x$-$y$ plane, oscillating perpendicular to the direction of propagation. '
          'Polarized light can be described by the so-called Jones vector $\\vec{E} = \\begin{pmatrix} E_x \\\\ E_y '
          'e^{i\\varphi} \\end{pmatrix}$. This vector describes the electromagnetic wave with its maximum amplitudes in $x$ and '
          '$y$-direction, $E_x$ and $E_y$, and a relative phase between the components of the electromagnetic wave. Here we '
          'normalize the incident intensity to one: $|E_x|^2+|E_y|^2=1$. A Jones vector need not be normalized: after a '
          'polarizer, its squared norm gives the remaining intensity relative to the incident beam.',
  'task': 'You are starting with a completely vertically polarized state $\\mathbf{J}_{V}= \\begin{pmatrix} 0 \\\\ 1 '
          '\\end{pmatrix}$. Move the slider to $E_x=0.5$ and watch the change in the electric field components and the combined '
          'wave in the applet below. Move it around for a closer look. Notice how the amplitude in $y$ direction $E_y$ is not '
          'the same as $E_x$.',
  'hint': 'Focus on the <b>Incident Wave</b> section. Adjust the first slider until the Amplitude $E_x$ reads exactly '
          '<b>0.50</b>.',
  'setup': {'insert_wp': False,
            'insert_pol': False,
            'show_poincare': False,
            'E_x_amp': 0.0,
            'phase_relative_pi': 0.0,
            'show_toggles': False,
            'disable_keys': ['phase_relative_pi']},
  'target': {'E_x_amp': 0.5},
  'solution': {'E_x_amp': 0.5},
  'explanation': 'Because our incident Jones vector is normalized ($I = |E_x|^2 + |E_y|^2 = 1$), fixing the horizontal field '
                 'amplitude to $E_x = 0.5$ forces the vertical field amplitude component to automatically balance to: $$E_y = '
                 '\\sqrt{1.0 - 0.5^2} = \\sqrt{0.75} \\approx 0.866$$ Since no relative phase shift is present ($\\varphi = 0$), '
                 'the wave remains linearly polarized, but the unequal component amplitudes tilt the net polarization angle away '
                 'from the standard $45^\\circ$ line. Click on the Next Step button below the applet to proceed.'},
 {'text': '<b>Step 2 of 9: Constructing Standard States</b><br>Any state of polarization $\\mathbf{J}$ can be expressed as a '
          'linear combination of horizontal $\\mathbf{J}_H=\\begin{pmatrix}1 \\\\ 0\\end{pmatrix}$ and vertical '
          '$\\mathbf{J}_V=\\begin{pmatrix}0 \\\\ 1\\end{pmatrix}$ basis vectors: $$\\mathbf{J}=\\alpha \\mathbf{J}_H+ '
          '\\beta\\mathbf{J}_V,$$ where $\\alpha$ and $\\beta$ are complex numbers. For our unit-intensity incident wave we '
          'choose $|\\alpha|^2+|\\beta|^2=1$. This normalization describes polarization separately from intensity; a transmitted '
          'Jones vector can have a smaller squared norm.',
  'task': 'Now, create an approximately <b>diagonal</b> state, which requires equal amplitudes: $\\mathbf{J}_{D} = '
          '\\frac{1}{\\sqrt{2}} \\left(\\mathbf{J}_H+\\mathbf{J}_V\\right)= \\frac{1}{\\sqrt{2}} \\begin{pmatrix} 1 \\\\ 1 '
          '\\end{pmatrix}$.',
  'hint': 'You want the amplitudes to be perfectly balanced. Start with $|E_x|^2+|E_y|^2=1$, and require that $|E_x|=|E_y|$. '
          'What are $|E_x|$ and $|E_y|$ in that case?',
  'setup': {'show_toggles': False, 'disable_keys': ['phase_relative_pi']},
  'target': {'E_x_amp': BALANCED_AMPLITUDE, 'phase_relative_pi': [0.0, 2.0]},
  'solution': {'E_x_amp': BALANCED_AMPLITUDE, 'phase_relative_pi': 0.0},
  'explanation': 'A purely diagonal state $\\mathbf{J}_D$ implies that the spatial oscillations along the horizontal and '
                 'vertical channels are perfectly symmetric and in-phase. Mathematically, this dictates that $|\\alpha| = '
                 '|\\beta|$, requiring: $$E_x = E_y = \\frac{1}{\\sqrt{2}} \\approx 0.707.$$ Setting the relative phase to '
                 '$\\varphi = 0$ (or $2\\pi$) keeps the components in geometric phase synchronization, forcing the electric '
                 'field vector to sweep out a linear path at exactly $+45^\\circ$ in the transverse plane.'},
 {'text': '<b>Step 3 of 9: Circular States</b><br>Notice how the diagonal state you just created features perfectly balanced '
          'amplitudes and no phase shift $\\varphi=0$.<br><br><b>Circular convention:</b> We use '
          '$\\vec{E}(z,t)=\\mathrm{Re}[\\mathbf{J}e^{i(kz-\\omega t)}]$. We call $(1,+i)/\\sqrt{2}$ right-circular and '
          '$(1,-i)/\\sqrt{2}$ left-circular. At $z=0$, the right-circular field turns from $+x$ toward $+y$ as time increases: '
          'counterclockwise when looking toward the source (against $+z$, with $x$ right and $y$ up). Looking along propagation '
          'reverses that apparent sense. The plotted helix is a spatial snapshot at one time, not a time animation.',
  'task': 'Starting with a diagonally polarized state, introduce a relative phase shift to create a <b>Right-Circular</b> state. '
          'Watch the behavior of the electric field components along the propagation axis:<br>$\\mathbf{J}_{R} = '
          '\\frac{1}{\\sqrt{2}} \\begin{pmatrix} 1 \\\\ e^{i\\pi/2} \\end{pmatrix} = \\frac{1}{\\sqrt{2}} \\begin{pmatrix} 1 '
          '\\\\ i \\end{pmatrix}$',
  'hint': 'A right-circular state requires equal amplitudes (which you already have) but a $\\pi/2$ phase shift.',
  'setup': {'show_poincare': False, 'show_toggles': False, 'disable_keys': ['E_x_amp']},
  'target': {'E_x_amp': BALANCED_AMPLITUDE, 'phase_relative_pi': 0.5},
  'solution': {'E_x_amp': BALANCED_AMPLITUDE, 'phase_relative_pi': 0.5},
  'explanation': 'By adding a relative phase shift of $\\varphi = \\frac{\\pi}{2}$ while keeping equal amplitudes ($E_x = E_y$), '
                 'the horizontal component reaches its maximum displacement exactly when the vertical component passes through '
                 'zero. In the Jones notation, this introduces the imaginary unit ($e^{i\\pi/2} = i$). This continuous '
                 'quarter-wave delay causes the combined electric field vector to rotate circularly as it propagates through '
                 'space.<br><br>Here is a summary of the standard polarization states:<br>• <b>Horizontal:</b> $\\mathbf{J}_H = '
                 '\\begin{pmatrix} 1 \\\\ 0 \\end{pmatrix}$<br>• <b>Vertical:</b> $\\mathbf{J}_V = \\begin{pmatrix} 0 \\\\ 1 '
                 '\\end{pmatrix}$<br>• <b>Diagonal:</b> $\\mathbf{J}_D = \\frac{1}{\\sqrt{2}}\\begin{pmatrix} 1 \\\\ 1 '
                 '\\end{pmatrix}$<br>• <b>Anti-Diagonal:</b> $\\mathbf{J}_A = \\frac{1}{\\sqrt{2}}\\begin{pmatrix} 1 \\\\ -1 '
                 '\\end{pmatrix}$<br>• <b>Right-Circular:</b> $\\mathbf{J}_R = \\frac{1}{\\sqrt{2}}\\begin{pmatrix} 1 \\\\ i '
                 '\\end{pmatrix}$<br>• <b>Left-Circular:</b> $\\mathbf{J}_L = \\frac{1}{\\sqrt{2}}\\begin{pmatrix} 1 \\\\ -i '
                 '\\end{pmatrix}$<br><br>Notice two key algebraic rules: First, the linear states ($\\mathbf{J}_H$, '
                 '$\\mathbf{J}_V$, $\\mathbf{J}_D$, and $\\mathbf{J}_A$) can be written with real components after removing a '
                 'common (global) phase; when both components are nonzero, their relative phase is $0$ or $\\pi$. Second, the '
                 'diagonal and circular states ($\\mathbf{J}_D$, $\\mathbf{J}_A$, $\\mathbf{J}_L$, and $\\mathbf{J}_R$) all '
                 'share perfectly balanced amplitudes where $|E_x| = |E_y|$.'},
 {'text': '<b>Step 4 of 9: Wave Plates (Retarders)</b><br>A wave plate has different refractive indices along two axes, called '
          'the fast and slow axes, and orthogonally decomposes light to introduce a phase delay $\\Gamma$ between these two '
          'axes. If the fast axis angle is at $0^\\circ$ (horizontal), within the Jones formalism it can be described with the '
          'matrix $\\mathbf{M}(\\Gamma) = \\begin{pmatrix} 1 & 0 \\\\ 0 & e^{i\\Gamma} \\end{pmatrix}.$ The retardance $\\Gamma$ '
          'is directly proportional to the physical thickness of the wave plate. It only changes the relative phase of a Jones '
          'vector $\\begin{pmatrix} E_x \\\\ E_y e^{i\\varphi} \\end{pmatrix}$:<br><br> $\\begin{pmatrix} 1 & 0 \\\\ 0 & '
          'e^{i\\Gamma} \\end{pmatrix}\\begin{pmatrix} E_x \\\\ E_y e^{i\\varphi} \\end{pmatrix}=\\begin{pmatrix} E_x \\\\ E_y '
          'e^{i(\\varphi+\\Gamma)} \\end{pmatrix}.$<br><br> We have inserted a wave plate (WP) into the beam path.',
  'task': 'Starting with a diagonal incident wave ($E_x = E_y = \\frac{1}{\\sqrt{2}}$), find the retardance $\\Gamma$ necessary '
          'to output a left-circularly polarized state.',
  'hint': 'To rotate a diagonal vector to a left-circular one, the relative phase needs to be shifted by more than $\\pi$.',
  'setup': {'insert_wp': True,
            'E_x_amp': BALANCED_AMPLITUDE,
            'phase_relative_pi': 0.0,
            'wp_angle_deg': 0.0,
            'retardance_pi': 0.0,
            'show_toggles': False,
            'show_poincare': False,
            'disable_keys': ['E_x_amp', 'phase_relative_pi', 'wp_angle_deg']},
  'target': {'E_x_amp': BALANCED_AMPLITUDE, 'retardance_pi': 1.5},
  'solution': {'retardance_pi': 1.5},
  'explanation': 'The incident wave is diagonally polarized: $\\mathbf{J}_{in} = \\frac{1}{\\sqrt{2}}\\begin{pmatrix} 1 \\\\ 1 '
                 '\\end{pmatrix}$. The wave plate operator is: $$\\mathbf{M}(0^\\circ, 3\\pi/2) =  \\begin{pmatrix} 1 & 0 \\\\ 0 '
                 '& e^{3i\\pi/2}=-i \\end{pmatrix}$$ Multiplying this operator by the incident wave yields: $$\\begin{pmatrix} 1 '
                 '& 0 \\\\ 0 & -i \\end{pmatrix}\\cdot \\frac{1}{\\sqrt{2}} \\begin{pmatrix} 1 \\\\ 1 \\end{pmatrix} = '
                 "\\frac{1}{\\sqrt{2}}\\begin{pmatrix} 1 \\\\ -i \\end{pmatrix} = \\mathbf{J}_L.$$ Physically, the wave plate's "
                 'fast axis is aligned horizontally ($\\Delta = 0^\\circ$). Setting the retardance to $\\Gamma = 1.5\\pi$ delays '
                 'the vertical component of the wave by $\\frac{3\\pi}{2}$ (which is geometrically equivalent to '
                 '$-\\frac{\\pi}{2}$). This transforms the in-phase diagonal oscillation into a left-handed spiral, creating '
                 'left-circularly polarized light.',
  'example': '<b>Example: a half-wave plate with a horizontal fast axis.</b> For diagonal input, '
             '$$\\begin{pmatrix}1&0\\\\0&-1\\end{pmatrix}\\frac{1}{\\sqrt{2}}\\begin{pmatrix}1\\\\1\\end{pmatrix}=\\frac{1}{\\sqrt{2}}\\begin{pmatrix}1\\\\-1\\end{pmatrix}.$$ '
             'The horizontal component is unchanged and the vertical component gains a phase of $\\pi$, giving anti-diagonal '
             'light. Intensity is unchanged.'},
 {'text': '<b>Step 5 of 9: Rotating the wave plate</b><br>Turning the wave plate by an angle $\\Delta$ is equivalent to a '
          'coordinate transformation of the $x$-$y$ plane—a rotation back and forth using the rotation matrix '
          '$\\mathbf{R}(\\Delta) = \\begin{pmatrix} \\cos\\Delta & -\\sin\\Delta \\\\ \\sin\\Delta & \\cos\\Delta '
          '\\end{pmatrix}$. You can also think of the coordinate transformation as tilting your head while the polarization of '
          'the incident light tilts along and the wave plate stays where it is. The combined operator is $\\mathbf{M}(\\Delta, '
          '\\Gamma) = \\mathbf{R}(\\Delta) \\mathbf{M}(\\Gamma) \\mathbf{R}(-\\Delta)$.',
  'task': 'Starting with a right-handed circularly polarized incident wave ($E_x = E_y = \\frac{1}{\\sqrt{2}}$ and '
          '$\\varphi=\\frac{\\pi}{2}$), find the <i>fast axis angle</i> $\\Delta$ necessary to output a <b>vertical</b> state.',
  'hint': 'You need to counteract the $\\pi/2$ phase shift of the circular state to make it linearly polarized, and '
          'simultaneously rotate it to be vertical. Think about how a quarter-wave plate can achieve this.',
  'setup': {'insert_wp': True,
            'E_x_amp': BALANCED_AMPLITUDE,
            'phase_relative_pi': 0.5,
            'wp_angle_deg': 0.0,
            'retardance_pi': 0.5,
            'show_toggles': False,
            'show_poincare': False,
            'disable_keys': ['E_x_amp', 'phase_relative_pi', 'retardance_pi']},
  'target': {'E_x_amp': BALANCED_AMPLITUDE, 'phase_relative_pi': 0.5, 'retardance_pi': 0.5, 'wp_angle_deg': 135.0},
  'solution': {'E_x_amp': BALANCED_AMPLITUDE, 'phase_relative_pi': 0.5, 'retardance_pi': 0.5, 'wp_angle_deg': 135.0},
  'explanation': 'The incident wave is right-circular: $\\mathbf{J}_{in} = \\frac{1}{\\sqrt{2}}\\begin{pmatrix} 1 \\\\ i '
                 '\\end{pmatrix}$. We require a final linear vertical state: $\\mathbf{J}_{out} = \\begin{pmatrix} 0 \\\\ 1 '
                 '\\end{pmatrix}$. A quarter-wave plate ($\\Gamma = 0.5\\pi$) introduces the necessary relative phase shift to '
                 'mathematically cancel out the imaginary component, converting the circular polarization into a linear '
                 'polarization. Orienting the wave plate fast axis to $\\Delta = 135^\\circ$ aligns the fast and slow axes such '
                 'that the output wave projection along the horizontal axis perfectly destructs, leaving purely vertical light.'},
 {'text': '<b>Step 6 of 9: Mastering Wave Plates</b><br>As a reminder, a wave plate is a unitary operator that alters the phase '
          "relationship of the wave components. Let's test your intuition.",
  'task': 'Start with a <b>horizontal</b> incident wave. Find the retardance and the fast axis angle needed to rotate the state '
          'to create a <b>diagonal</b> state (+45$^\\circ$ angle of the combined wave vector).',
  'hint': 'A half-wave plate ($\\Gamma = 1.0\\pi$) acts as a mirror, reflecting the linear polarization angle across its fast '
          'axis. To get from $0^\\circ$ to $45^\\circ$, where should the mirror line be?',
  'setup': {'wp_angle_deg': 0.0,
            'retardance_pi': 0.0,
            'E_x_amp': 1.0,
            'phase_relative_pi': 0.0,
            'show_toggles': False,
            'show_poincare': False,
            'disable_keys': ['E_x_amp', 'phase_relative_pi']},
  'target': {'E_x_amp': 1.0, 'S_final': [0, 1, 0]},
  'solution': {'retardance_pi': 1.0, 'wp_angle_deg': 22.5},
  'explanation': 'We begin at horizontal polarization and want to map to diagonal polarization. A half-wave plate ($\\Gamma = '
                 '1.0\\pi$) reflects the incident polarization angle about its fast axis. For horizontal input the output angle is $2\\Delta$. To rotate '
                 'from $0^\\circ$ (horizontal) to $45^\\circ$ (diagonal), a possible solution uses exactly half the total '
                 'rotation as the fast axis angle: $$\\Delta = \\frac{45^\\circ}{2} = 22.5^\\circ$$'},
 {'text': '<b>Step 7 of 9: Linear Polarizers</b><br>Unlike a wave plate, a linear polarizer is a <i>non-unitary</i> operator—it '
          'absorbs light and reduces overall intensity (defined as the absolute value of the Jones vector squared). A horizontal '
          'polarizer projects the electric field onto the $x$-axis, represented by the matrix:<br><br>$\\mathbf{P}(0^\\circ) = '
          '\\begin{pmatrix} 1 & 0 \\\\ 0 & 0 \\end{pmatrix}$<br><br>Just like the wave plate, turning the polarizer applies a '
          'coordinate rotation: $\\mathbf{P}(\\theta) = \\mathbf{R}(\\theta) \\mathbf{P}(0^\\circ) \\mathbf{R}(-\\theta)$.',
  'task': 'For the diagonal incident wave shown, find the transmission angle $\\theta$ that gives a pure <b>horizontal</b> '
          'output. An input perpendicular to the transmission axis would instead be blocked completely.',
  'hint': "You want the final state to be purely horizontal. Turn your Polarizer's transmission Axis so that it fits the axis of "
          'polarization of outgoing light that you want. Notice how the intensity drops to exactly 50% as you project the '
          'diagonal vector.',
  'setup': {'insert_wp': False,
            'insert_pol': True,
            'pol_angle_deg': 90.0,
            'E_x_amp': BALANCED_AMPLITUDE,
            'phase_relative_pi': 0.0,
            'show_toggles': False,
            'show_poincare': False,
            'disable_keys': ['E_x_amp', 'phase_relative_pi']},
  'target': {'pol_angle_deg': [0.0, 180.0]},
  'solution': {'pol_angle_deg': 0.0},
  'explanation': 'The incident diagonal wave is represented by $\\mathbf{J}_{in} = \\mathbf{J}_{D}  = '
                 '\\frac{1}{\\sqrt{2}}\\begin{pmatrix} 1 \\\\ 1 \\end{pmatrix}$. To output a purely horizontal state, the '
                 'polarizer must completely block the vertical components of the field. Setting the polarizer angle to $\\theta '
                 '= 0^\\circ$ initializes the projection matrix $\\mathbf{P}(0^\\circ) = \\begin{pmatrix} 1 & 0 \\\\ 0 & 0 '
                 '\\end{pmatrix}$. Multiplying the vector yields: $$\\mathbf{P}(0^\\circ)\\mathbf{J}_{in} = \\begin{pmatrix} 1 & '
                 '0 \\\\ 0 & 0 \\end{pmatrix} \\left[\\frac{1}{\\sqrt{2}}\\begin{pmatrix} 1 \\\\ 1 \\end{pmatrix}\\right] = '
                 '\\begin{pmatrix} \\frac{1}{\\sqrt{2}} \\\\ 0 \\end{pmatrix}$$ Evaluating the transmitted beam intensity '
                 'mathematically: $$I = |E_x|^2 + |E_y|^2 = \\left|\\frac{1}{\\sqrt{2}}\\right|^2 + 0 = 0.50$$ Exactly 50% of '
                 "the beam's energy is absorbed because the polarizer filters out the orthogonal vertical component.",
  'example': '<b>Example: a vertical polarizer.</b> For diagonal input, '
             '$$\\begin{pmatrix}0&0\\\\0&1\\end{pmatrix}\\frac{1}{\\sqrt{2}}\\begin{pmatrix}1\\\\1\\end{pmatrix}=\\begin{pmatrix}0\\\\1/\\sqrt{2}\\end{pmatrix}.$$ '
             'It removes the horizontal component and transmits the vertical component. The output intensity is '
             '$0^2+(1/\\sqrt{2})^2=1/2$, or 50% of the input.'},
 {'text': "<b>Step 8 of 9: Putting it all together</b><br>Let's combine operators!",
  'task': 'Let the incident wave be <b>vertical</b> ($E_x=0.0$). Your goal is to pass this light through BOTH a wave plate and a '
          'polarizer to achieve a final transmitted state that is <b>horizontal</b> with an intensity of exactly <b>50%</b> of '
          'the original beam.',
  'hint': 'For example, you can first use a Quarter-Wave plate to transform the vertical light into a Right-Circular state, then '
          'project it using the polarizer.',
  'setup': {'insert_wp': True,
            'insert_pol': True,
            'E_x_amp': 0.0,
            'phase_relative_pi': 0.0,
            'wp_angle_deg': 0.0,
            'retardance_pi': 0.0,
            'pol_angle_deg': 90.0,
            'show_toggles': False,
            'show_poincare': False,
            'disable_keys': ['E_x_amp', 'phase_relative_pi']},
  'target': {'S_final': [1.0, 0.0, 0.0], 'intensity_percent': 50.0},
  'solution': {'retardance_pi': 0.5, 'wp_angle_deg': 45.0, 'pol_angle_deg': 0.0},
  'explanation': 'We track this sequence step-by-step through the optical train:<br>1. <b>Incident State:</b> The wave starts as '
                 'purely vertical light: $\\mathbf{J}_{in} = \\begin{pmatrix} 0 \\\\ 1 \\end{pmatrix}$.<br>2. <b>Wave Plate '
                 'Action:</b> Setting the quarter-wave plate ($\\Gamma = 0.5\\pi$) to a physical angle of $\\Delta = 45^\\circ$ '
                 'introduces a phase shift that transforms the linear wave into right-circular light: $\\mathbf{J}_{wp} = '
                 '\\frac{1}{\\sqrt{2}}\\begin{pmatrix} 1 \\\\ i \\end{pmatrix}$.<br>3. <b>Polarizer Action:</b> The circular '
                 'wave then encounters a linear polarizer at $\\theta = 0^\\circ$. Applying the projection matrix filters out '
                 'the vertical phase component entirely: $$\\mathbf{P}(0^\\circ)\\mathbf{J}_{wp} = \\begin{pmatrix} 1 & 0 \\\\ 0 '
                 '& 0 \\end{pmatrix} \\left[\\frac{1}{\\sqrt{2}}\\begin{pmatrix} 1 \\\\ i \\end{pmatrix}\\right] = '
                 '\\begin{pmatrix} \\frac{1}{\\sqrt{2}} \\\\ 0 \\end{pmatrix}$$ This results in a purely horizontal output wave '
                 'with a final intensity of $|\\frac{1}{\\sqrt{2}}|^2 = 0.50$.'},
 {'text': "<b>Step 9 of 9: The Final Challenge</b><br>Let's combine operators for a lossless transmission!",
  'task': 'Start with an incident <b>Right-Circular</b> wave. Your goal is to use BOTH the wave plate and the polarizer to '
          'output a pure <b>Diagonal</b> state (+45$^\\circ$) with an intensity of exactly <b>100%</b> (no light absorbed).',
  'hint': 'To get 100% intensity through the polarizer, the wave entering it must already be perfectly diagonal. Find the wave '
          'plate retardance and angle that cancels the circular phase shift and aligns the wave diagonally, then match the '
          'polarizer angle.',
  'setup': {'insert_wp': True,
            'insert_pol': True,
            'E_x_amp': BALANCED_AMPLITUDE,
            'phase_relative_pi': 0.5,
            'wp_angle_deg': 0.0,
            'retardance_pi': 0.0,
            'pol_angle_deg': 0.0,
            'show_toggles': False,
            'show_poincare': False,
            'disable_keys': ['E_x_amp', 'phase_relative_pi']},
  'target': {'S_final': [0.0, 1.0, 0.0], 'intensity_percent': 100.0},
  'solution': {'retardance_pi': 0.5, 'wp_angle_deg': 90.0, 'pol_angle_deg': 45.0},
  'explanation': 'To achieve 100% transmission through a linear polarizer, the light entering it must already perfectly match '
                 'its transmission axis. Therefore, your wave plate must convert the Right-Circular light directly into Diagonal '
                 'light. Mathematically, a quarter-wave plate ($\\Gamma = 0.5\\pi$) with its fast axis vertical ($\\Delta = '
                 '90^\\circ$) delays the horizontal component relative to the vertical one, canceling out the initial phase '
                 'shift of the circular light and bringing both components perfectly in-phase. This yields a linear diagonal '
                 'wave. Finally, turning the polarizer to $\\theta = 45^\\circ$ matches this wave, allowing it to pass through '
                 'entirely without absorption. Note: A fast axis of $0^\\circ$ and retardance of $1.5\\pi$ is also a valid '
                 'mathematical solution!'},
 {'text': '<b>Tutorial Completed!</b><br>Congratulations, you have finished the interactive physics module. Feel free to play '
          'around with the optical elements below. When you are ready to proceed with the study, click the return button at the '
          'bottom of the screen.<br>',
  'task': '',
  'setup': {'insert_wp': True, 'insert_pol': True, 'show_toggles': True, 'show_poincare': False, 'disable_keys': []},
  'target': {}}]

SPHERE_GUIDANCE = {2: {'text': 'We have now revealed the <b>Poincaré sphere</b>. The diagonal state maps to the equator. Linear states lie on the '
             'equator; their relative phase is $0$ or $\\pi$ when both components are nonzero.',
     'task': 'On the sphere, the target is the north pole.',
     'explanation': 'The state moves from the equator to the north pole through $\\pi/2$. The reference positions are '
                    'horizontal: front equator; vertical: back equator; diagonal: right equator; anti-diagonal: left equator; '
                    'right-circular: north pole; left-circular: south pole. These directions refer to the default view. '
                    'Equal-amplitude states lie in the vertical plane spanned by the diagonal and right-circular axes.',
     'hint': 'A right-circular state requires equal amplitudes (which you already have) but a $\\pi/2$ phase shift.'},
 3: {'text': 'The Poincaré sphere now shows the WP operator as a rotation axis (orange dashed line). On the Poincaré sphere, the '
             'retardance is the angle of rotation around the axis of the wave plate operator.',
     'explanation': 'Geometrically on the Poincaré sphere, the wave plate fast axis at $\\Delta = 0^\\circ$ creates a rotation '
                    'axis pointing towards the horizontal state. Setting the retardance to $\\Gamma = 1.5\\pi$ rotates the '
                    'diagonal vector around this axis by 270$^\\circ$, leaving the vector at the bottom of the sphere.',
     'hint': 'Look at the orange dashed rotation axis on the sphere. How far do you need to rotate the vector for it to reach '
             'the bottom pole?'},
 4: {'text': 'The retardance $\\Gamma$ is the rotation angle on the sphere, and the fast axis angle $\\Delta$ sets the azimuthal '
             'angle $2\\Delta$ of the WP operator axis on the equator.',
     'explanation': 'The input is at the north pole and the target at the vertical point on the equator. A quarter-turn about '
                    'the anti-diagonal axis ($2\\Delta=270^\\circ$) takes the state to that target.',
     'hint': 'A $\\pi/2$ rotation takes the north pole to the equator. Choose an equatorial operator axis perpendicular to both '
             'the north-pole input and the vertical target.'},
 5: {'text': 'On the sphere a wave plate acts as a rotation. Its axis lies on the equator at azimuth $2\\Delta$, and its '
             'rotation angle is the retardance $\\Gamma$.',
     'explanation': 'We begin at horizontal polarization and want to map directly to diagonal polarization along the equatorial '
                    'plane. To execute this move using a half-wave plate ($\\Gamma = 1.0\\pi$, which acts as a $180^\\circ$ '
                    'flip), the rotation axis on the sphere must be positioned exactly halfway between the initial and target '
                    'states on the equator. The angular separation between horizontal ($0^\\circ$ on the sphere) and diagonal '
                    '($90^\\circ$ on the sphere) is $90^\\circ$. The bisection axis must sit at an azimuthal position of '
                    'exactly: $$2\\Delta = \\frac{90^\\circ}{2} = 45^\\circ.$$ A fast axis angle that leads to the correct '
                    'solution is therefore $22.5^\\circ$.',
     'hint': 'To travel along the equator (horizontal) to the diagonal state, your rotation axis on the sphere needs to reflect '
             'around an axis that is between the horizontal and diagonal axes on the sphere.'},
 6: {'text': '<b>Schematic correction:</b> The dotted line connects the input and normalized transmitted states schematically. '
             'It is not a physical trajectory or a Euclidean projection through the sphere. The Jones vector is projected onto '
             "the transmission axis; the surviving light has that axis's polarization. If transmission is zero, no output "
             'polarization state is defined.',
     'hint': "You want the final state to sit on the pure horizontal axis of the sphere. Turn your Polarizer's transmission Axis "
             'so that it fits the axis of polarization of outgoing light that you want. Notice how the intensity drops to '
             'exactly 50% as you project the diagonal vector.'},
 7: {'explanation': 'On the sphere, the quarter-wave plate has its rotation axis at the diagonal point; it moves the vertical '
                    'state to the north pole. The dotted connection from there to the horizontal output is schematic, not a '
                    'physical path through the sphere.'},
 8: {'explanation': 'On the sphere, the input is at the north pole and the target is the diagonal point on the equator. A fast '
                    'axis of $\\Delta=90^\\circ$ puts the rotation axis at the vertical state. A quarter-wave retardance rotates '
                    'the input to the diagonal state.',
     'hint': 'To get 100% intensity through the polarizer, the light hitting it must already be Diagonal. Use the wave plate to '
             'rotate the Right-Circular state (north pole) to the Diagonal state on the equator, then align the polarizer to let '
             'it all through.'}}

CHALLENGES = {}
for name, condition in CONDITIONS.items():
    steps = deepcopy(SHARED_STEPS)
    for index, step in enumerate(steps):
        step["setup"]["show_poincare"] = condition["sphere"] and index >= 2
        if condition["sphere"]:
            for field, guidance in SPHERE_GUIDANCE.get(index, {}).items():
                if field == "hint":
                    step[field] = guidance
                else:
                    step[field] = step.get(field, "") + "<br><br>" + guidance
    CHALLENGES[name] = {"steps": steps, "condition": condition, "version": CONDITION_VERSION}

CHALLENGES["Free Play"] = {'steps': [{'text': '<b>Free Play Mode</b><br>Explore the simulation freely.',
            'task': 'Use the toggles and sliders below to interact with the wave plates and polarizers. There are no targets to '
                    'reach.',
            'setup': {'show_poincare': True, 'show_toggles': True, 'disable_keys': []},
            'target': {}}]}

def step_setup(challenge_name, step_index, solved=False):
    """Deterministic start: earlier canonical solutions, then this step's setup.

    Back loads a solved example; reset loads this task's starting state.
    Neither depends on edits made on a later page.
    """
    state = {
        "E_x_amp": 2 ** -0.5, "phase_relative_pi": 0.0,
        "insert_wp": True, "wp_angle_deg": 0.0, "retardance_pi": 0.5,
        "insert_pol": False, "pol_angle_deg": 90.0,
        "show_poincare": False, "show_toggles": False, "disable_keys": [],
    }
    steps = CHALLENGES[challenge_name]["steps"]
    for index, step in enumerate(steps[:step_index + 1]):
        state.update(deepcopy(step.get("setup", {})))
        if index < step_index or solved:
            state.update(deepcopy(step.get("solution", {})))
    return state


GLOSSARY = r"""
**Amplitude:** maximum size of a field component; its square contributes to intensity.

**Relative phase:** how far one component's oscillation is shifted relative to the other.

**Jones vector:** two complex components recording the transverse electric field's amplitudes and relative phase. A common global phase does not change polarization.

**Optical-element axes:** directions used to resolve the field. A polarizer transmits the component along its transmission axis.

**Fast/slow axes:** perpendicular directions in a wave plate with lower/higher refractive index; the slow component accumulates an extra phase relative to the fast component.

**Retardance:** that extra relative phase, denoted $\Gamma$ here.

**Unitary:** preserves the squared norm (intensity), as an ideal wave plate does.

**Non-unitary:** need not preserve that norm; a polarizer removes the perpendicular component.
"""
SPHERE_GLOSSARY = r"""
**Poincaré sphere:** a map of normalized polarization states, not physical space. Linear states lie on its equator and circular states at its poles.

**Stokes coordinates:** the three coordinates locating a normalized state on this sphere. Intensity is reported separately; zero light has no normalized polarization state.

**Operator axis:** the axis about which a wave plate rotates the state on the sphere; its equatorial angle is twice the physical fast-axis angle.
"""
