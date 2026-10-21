"""Refresh, code validation, allocation, and survey-handoff regressions."""

import base64
import json
from pathlib import Path
import sys
import unittest
from urllib.parse import parse_qs, urlparse

from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from challenges import CONDITIONS, step_setup
from study_session import condition_for_code, decode_resume, encode_resume, normalize_study_code


def button(app, label):
    return next(b for b in app.button if b.label == label)


def code_for(journey):
    return next(code for day in range(1, 32)
                if condition_for_code(code := f'TEST{day:02}') == journey)


class StudySessionTests(unittest.TestCase):
    def app(self, params, start=False):
        app = AppTest.from_file(str(ROOT / 'app.py'), default_timeout=20)
        app.query_params.update(params)
        app.run()
        self.assertFalse(app.exception)
        if start:
            button(app, '🚀 I understand, start the tutorial!').click().run()
            self.assertFalse(app.exception)
        return app

    def refresh(self, app):
        # A genuinely new Streamlit session receives only the browser URL.
        return self.app(dict(app.query_params))

    def test_code_validation_and_normalization(self):
        self.assertEqual(normalize_study_code(' mapl05 '), 'MAPL05')
        self.assertEqual(normalize_study_code('aapr05'), 'AAPR05')
        for code in ('', '123', 'ABC05', 'ABCD00', 'ABCD32', 'ÄBCD05', 'AB CD05', 'ABCD05<script>', 'AAPRBN05'):
            self.assertIsNone(normalize_study_code(code), code)

    def test_allocation_is_stable_and_both_conditions_exist(self):
        assignments = {condition_for_code(f'TEST{day:02}') for day in range(1, 32)}
        self.assertEqual(assignments, set(CONDITIONS))
        self.assertEqual(condition_for_code(' mapl05 '), condition_for_code('MAPL05'))
        # Protect the allocation seed/order from accidental changes mid-study.
        self.assertEqual(condition_for_code('MAPL05'), 'Polarization 2')
        self.assertEqual(condition_for_code('TEST01'), 'Polarization 1')

    def test_missing_invalid_codes_cannot_start_tutorial(self):
        for params in ({}, {'pid': 'invalid'}, {'pid': 'ABCD00', 'lang': 'de'}, {'pid': 'AAPRBN05'}):
            app = self.app(params)
            self.assertEqual(len(app.warning), 1)
            self.assertEqual(len(app.slider), 0)
            self.assertFalse(any('start the tutorial' in b.label for b in app.button))
            self.assertIn('Your study code is missing or invalid.', app.warning[0].value)
            url = app.get('link_button')[0].proto.url
            self.assertEqual(urlparse(url).path, '/index.php/861912')
            self.assertEqual(parse_qs(urlparse(url).query), {'lang': ['en']})

    def test_refresh_preserves_step_values_hints_and_condition(self):
        for journey in CONDITIONS:
            code = code_for(journey)
            app = self.app({'pid': code.lower(), 'lang': 'de', 'journey': 'incorrect'}, start=True)
            self.assertEqual(app.session_state.assigned_journey, journey)
            app.number_input(key='E_x_amp_num').set_value(.5).run()
            button(app, '👣 Next Step ➔').click().run()
            app.number_input(key='E_x_amp_num').set_value(.707).run()
            button(app, '💡 Show Hint').click().run()
            fresh = self.refresh(app)
            self.assertEqual(fresh.session_state.current_step, 1)
            self.assertEqual(fresh.session_state.assigned_journey, journey)
            self.assertEqual(fresh.session_state.study_code, code)
            self.assertEqual(fresh.session_state.survey_language, 'en')
            self.assertEqual(fresh.query_params['lang'], ['en'])
            self.assertEqual(fresh.number_input(key='E_x_amp_num').value, .707)
            self.assertTrue(fresh.session_state.show_hint)
            self.assertFalse(button(fresh, '👣 Next Step ➔').disabled)
            # Reopening the original link loses the checkpoint, not assignment.
            reopened = self.app({'pid': code})
            self.assertEqual(reopened.session_state.assigned_journey, journey)
            self.assertTrue(reopened.session_state.show_landing)

    def test_completion_refresh_preserves_toggles_and_survey_handoff(self):
        for journey in CONDITIONS:
            code = code_for(journey)
            state = step_setup(journey, 9)
            state.update(current_step=9, E_x_amp=.6, phase_relative_pi=.25,
                         wp_angle_deg=30., retardance_pi=.75, pol_angle_deg=123.,
                         show_combined=False, show_ex=False)
            app = self.app({'pid': code, 'lang': 'de', 'resume': encode_resume(code, state)})
            app.number_input(key='pol_angle_deg_num').set_value(50).run()
            fresh = self.refresh(app)
            self.assertEqual(fresh.session_state.current_step, 9)
            self.assertEqual(fresh.number_input(key='pol_angle_deg_num').value, 50)
            self.assertFalse(fresh.checkbox(key='show_combined').value)
            self.assertFalse(fresh.checkbox(key='show_ex').value)
            self.assertEqual(fresh.session_state.show_poincare, journey == 'Polarization 1')
            url = fresh.get('link_button')[0].proto.url
            self.assertEqual(urlparse(url).path, '/index.php/385657')
            self.assertEqual(parse_qs(urlparse(url).query), {
                'pid': [code], 'journey': [journey], 'lang': ['en'], 'appletcomplete': ['1'],
            })
            button(fresh, '🔄 Reset Page').click().run()
            reset = self.refresh(fresh)
            self.assertEqual(reset.session_state.current_step, 9)
            self.assertEqual(reset.number_input(key='pol_angle_deg_num').value, 45)
            self.assertTrue(reset.checkbox(key='show_combined').value)
            button(reset, '⬅️ Back one Page').click().run()
            review = self.refresh(reset)
            self.assertEqual(review.session_state.current_step, 8)
            self.assertEqual(review.session_state.solution_origin, 'review')
            self.assertFalse(button(review, '👣 Next Step ➔').disabled)

    def test_bad_checkpoint_cannot_crash_or_switch_condition(self):
        code = code_for('Polarization 2')
        state = step_setup('Polarization 2', 9)
        state['current_step'] = 9
        token = encode_resume(code, state)
        payload = json.loads(base64.urlsafe_b64decode(token + '=' * (-len(token) % 4)))
        changes = [
            {'step': -1}, {'step': 10}, {'step': True}, {'v': 999},
            {'code': 'another participant'}, {'values': []}, {'reset': 'invalid'},
            {'values': {**payload['values'], 'E_x_amp': 2}},
            {'values': {**payload['values'], 'E_x_amp': float('nan')}},
            {'values': {**payload['values'], 'E_x_amp': 10 ** 400}},
        ]
        for change in changes:
            modified = base64.urlsafe_b64encode(json.dumps({**payload, **change}).encode()).decode()
            self.assertIsNone(decode_resume(modified, code, 'Polarization 2'), change)
        for invalid in ('broken!', 'x' * 3000, 'W10='):
            self.assertIsNone(decode_resume(invalid, code, 'Polarization 2'))
        state['show_poincare'] = True
        restored = decode_resume(encode_resume(code, state), code, 'Polarization 2')
        self.assertFalse(restored['show_poincare'])
        app = self.app({'pid': code, 'resume': 'broken!', 'journey': 'Polarization 1'})
        self.assertEqual(app.session_state.assigned_journey, 'Polarization 2')
        self.assertTrue(app.session_state.show_landing)

    def test_code_change_does_not_inherit_progress(self):
        app = self.app({'pid': 'MAPL05'}, start=True)
        button(app, '✅ Show Solution').click().run()
        button(app, '👣 Next Step ➔').click().run()
        app.query_params['pid'] = 'ABCD06'
        app.run()
        self.assertFalse(app.exception)
        self.assertEqual(app.session_state.current_step, 0)
        self.assertEqual(app.session_state.assigned_journey, condition_for_code('ABCD06'))
        self.assertTrue(app.session_state.show_landing)


if __name__ == '__main__':
    unittest.main()
