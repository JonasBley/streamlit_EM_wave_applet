"""Run with: python -m unittest discover -s tests -v."""
from pathlib import Path
import re
import sys
import unittest
from urllib.parse import urlparse, parse_qs

import numpy as np
from streamlit.testing.v1 import AppTest
from latex2mathml.converter import convert

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from challenges import CHALLENGES, CONDITIONS, step_setup

SOURCE = (ROOT / 'app.py').read_text(encoding='utf-8') + '''
st.session_state['_test_derived'] = derived_state
st.session_state['_test_met'] = target_met
st.session_state['_test_figure'] = fig.to_dict()
'''


def button(app, label):
    return next(b for b in app.button if b.label == label)


class FeedbackTests(unittest.TestCase):
    def app(self, journey):
        app = AppTest.from_string(SOURCE, default_timeout=20)
        app.session_state['show_landing'] = False
        app.session_state['assigned_journey'] = journey
        app.query_params['pid'] = 'participant A+&/ä'
        return app.run()

    def clean(self, app):
        self.assertEqual(len(app.exception), 0, str(app.exception))

    def test_complete_both_journeys_and_review(self):
        expected = [[-.5, np.sqrt(.75), 0], [0,1,0], [0,0,1], [0,0,-1],
                    [-1,0,0], [0,1,0], [1,0,0], [1,0,0], [0,1,0]]
        for journey in CONDITIONS:
            app = self.app(journey)
            self.clean(app)
            for index in range(9):
                self.assertEqual(app.session_state.current_step, index)
                self.assertEqual(app.session_state.show_poincare, journey == 'Polarization 1' and index >= 2)
                button(app, '✅ Show Solution').click().run()
                self.clean(app)
                self.assertTrue(app.session_state['_test_met'], (journey, index))
                np.testing.assert_allclose(app.session_state['_test_derived']['S_final'], expected[index], atol=1e-12)
                self.assertTrue(any('Example solution shown' in m.value for m in app.markdown))
                if index in (6,7):
                    self.assertAlmostEqual(app.session_state['_test_derived']['intensity_percent'], 50)
                if index == 8:
                    self.assertAlmostEqual(app.session_state['_test_derived']['intensity_percent'], 100)
                button(app, '👣 Next Step ➔').click().run()
                self.clean(app)
            url = app.get('link_button')[0].proto.url
            self.assertEqual(parse_qs(urlparse(url).query), {'pid':['participant A+&/ä'], 'journey':[journey]})
            self.assertEqual(any('Poincaré' in c.label for c in app.checkbox), journey == 'Polarization 1')
            # Completion edits must not leak back into the canonical solved state.
            app.number_input(key='pol_angle_deg_num').set_value(123).run()
            button(app, '⬅️ Back').click().run()
            self.clean(app)
            self.assertTrue(app.session_state['_test_met'])
            self.assertEqual(app.session_state.pol_angle_deg, 45)
            self.assertTrue(any('Solved example for review' in m.value for m in app.markdown))
            button(app, '🔄 Reset').click().run()
            self.clean(app)
            self.assertEqual(app.session_state.current_step, 8)
            self.assertEqual(app.session_state.wp_angle_deg, 0)
            self.assertEqual(app.session_state.retardance_pi, 0)
            self.assertEqual(app.number_input(key='wp_angle_deg_num').value, 0)
            self.assertFalse(app.session_state['_test_met'])
            # Walk back through every solved page and reset each one.
            for index in range(7,-1,-1):
                button(app, '⬅️ Back').click().run()
                self.clean(app)
                self.assertTrue(app.session_state['_test_met'], index)
                button(app, '🔄 Reset').click().run()
                self.clean(app)
                for key, value in step_setup(journey,index).items():
                    self.assertEqual(app.session_state[key], value, (index,key))
            self.assertTrue(button(app,'⬅️ Back').disabled)

    def test_extinction_and_control_restriction(self):
        for journey in CONDITIONS:
            app = self.app(journey)
            for key, value in step_setup(journey, 9).items():
                app.session_state[key] = value
            app.session_state.current_step = 9
            app.session_state.E_x_amp = 1.0
            app.session_state.insert_wp = False
            app.session_state.pol_angle_deg = 90.0
            app.session_state.show_poincare = True
            app.run()
            self.clean(app)
            self.assertIsNone(app.session_state['_test_derived']['S_final'])
            self.assertEqual(app.metric[0].value, '0.00%')
            if journey == 'Polarization 1':
                lines = [t for t in app.session_state['_test_figure']['data'] if t.get('name') == 'Schematic connection']
                self.assertEqual(len(lines), 1)
                self.assertFalse(lines[0]['visible'])
            else:
                self.assertFalse(app.session_state.show_poincare)

    def test_rounded_entry_and_shared_conditions(self):
        app = self.app('Polarization 2')
        for key, value in step_setup('Polarization 2',1).items():
            app.session_state[key] = value
        app.session_state.current_step = 1
        app.run()
        app.number_input(key='E_x_amp_num').set_value(.707).run()
        self.clean(app)
        self.assertTrue(app.session_state['_test_met'])
        self.assertEqual(app.slider(key='E_x_amp_slider').value, .707)
        app.number_input(key='E_x_amp_num').set_value(.710).run()
        self.assertFalse(app.session_state['_test_met'])
        for index in range(10):
            a, b = [step_setup(name,index) for name in CONDITIONS]
            a.pop('show_poincare'); b.pop('show_poincare')
            self.assertEqual(a,b)
            control = CHALLENGES['Polarization 2']['steps'][index]
            sphere = CHALLENGES['Polarization 1']['steps'][index]
            for field in ('text','task','explanation','example'):
                self.assertTrue(sphere.get(field,'').startswith(control.get(field,'')))
            self.assertNotIn('sphere', control.get('text','').lower())

    def test_all_formulas_convert(self):
        for challenge in CHALLENGES.values():
            for step in challenge['steps']:
                for value in step.values():
                    if isinstance(value,str):
                        for match in re.finditer(r'\$\$(.*?)\$\$|\$(.*?)\$', value, re.S):
                            convert(match.group(1) or match.group(2))


if __name__ == '__main__':
    unittest.main()
