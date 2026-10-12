"""Repeatable allocation and browser-URL recovery, without participant logs."""

import base64
import binascii
import hashlib
import json
import math
import re

from challenges import CHALLENGES, CONDITION_VERSION, CONDITIONS, step_setup

# Generated once for this study. Keep this seed and condition order fixed after
# recruitment starts: changing either would reassign returning study codes.
# This is a public randomization seed, not a password or an encryption key.
ALLOCATION_SEED = "b8c2c5f48fcd571ef9a333cda8103780"
ALLOCATION_CONDITIONS = ("Polarization 1", "Polarization 2")
RESUME_VERSION = 1
RESUME_MAX_LENGTH = 2048

NUMERIC_CONTROLS = {
    "E_x_amp": (0.0, 1.0),
    "phase_relative_pi": (0.0, 2.0),
    "wp_angle_deg": (0.0, 180.0),
    "retardance_pi": (0.0, 2.0),
    "pol_angle_deg": (0.0, 180.0),
}
BOOLEAN_CONTROLS = (
    "insert_wp", "insert_pol", "show_combined", "show_ex", "show_ey",
    "show_axis", "show_poincare",
)


def normalize_study_code(value):
    """Accept the current six-character code and proposed eight-character code.

    The existing pre-survey uppercases four letters + day (01--31). The proposed
    future format adds another pair of letters. Do not collect names or dates.
    """
    code = value.strip()
    if not re.fullmatch(r"(?:[A-Za-z]{4}|[A-Za-z]{6})(?:0[1-9]|[12][0-9]|3[01])", code):
        return None
    return code.upper()


def condition_for_code(code):
    """A fixed-seed hash gives repeatable, approximately 1:1 allocation.

    Identical codes receive identical conditions, including across server
    restarts; no database of codes or assignments is needed. This does not
    enforce equal group sizes or guarantee that different people have unique
    codes. Never use Python's process-randomized built-in hash() here.
    """
    normalized = normalize_study_code(code)
    if normalized is None:
        raise ValueError("Invalid study code")
    digest = hashlib.sha256(f"{ALLOCATION_SEED}:{normalized}".encode("ascii")).digest()
    return ALLOCATION_CONDITIONS[digest[0] % len(ALLOCATION_CONDITIONS)]


def _code_fingerprint(code):
    return hashlib.sha256(code.encode("ascii")).hexdigest()[:16]


def encode_resume(code, state):
    """Store only current UI settings in the URL, not timing or action history."""
    values = {key: state[key] for key in (*NUMERIC_CONTROLS, *BOOLEAN_CONTROLS)}
    payload = {
        "v": RESUME_VERSION, "study": CONDITION_VERSION,
        "code": _code_fingerprint(code), "step": state["current_step"],
        "values": values, "hint": state.get("show_hint", False),
        "origin": state.get("solution_origin"), "reset": state.get("view_reset", 0),
    }
    raw = json.dumps(payload, separators=(",", ":"), allow_nan=False).encode("utf-8")
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def decode_resume(token, code, journey):
    """Validate untrusted URL state and restore only controls allowed on a step.

    The checkpoint is a convenience for refresh recovery, not authentication or
    independent proof of completion. Condition assignment never comes from it.
    """
    if not token or len(token) > RESUME_MAX_LENGTH:
        return None
    try:
        raw = base64.b64decode(token + "=" * (-len(token) % 4), altchars=b"-_", validate=True)
        payload = json.loads(raw)
        if not isinstance(payload, dict):
            return None
        if (payload.get("v") != RESUME_VERSION or payload.get("study") != CONDITION_VERSION
                or payload.get("code") != _code_fingerprint(code)):
            return None
        step = payload.get("step")
        if type(step) is not int or not 0 <= step < len(CHALLENGES[journey]["steps"]):
            return None
        values = payload.get("values")
        if not isinstance(values, dict):
            return None
        for key, (low, high) in NUMERIC_CONTROLS.items():
            value = values.get(key)
            if type(value) not in (int, float) or not math.isfinite(value) or not low <= value <= high:
                return None
        if any(type(values.get(key)) is not bool for key in BOOLEAN_CONTROLS):
            return None
        origin = payload.get("origin")
        if origin not in (None, "shown", "review") or type(payload.get("hint")) is not bool:
            return None
        reset = payload.get("reset", 0)
        if type(reset) is not int or not 0 <= reset <= 1_000_000:
            return None

        state = step_setup(journey, step, solved=origin == "review")
        for key in NUMERIC_CONTROLS:
            if key not in state["disable_keys"]:
                state[key] = float(values[key])
        if state["show_toggles"]:
            for key in BOOLEAN_CONTROLS:
                if key not in state["disable_keys"]:
                    state[key] = values[key]
        if not CONDITIONS[journey]["sphere"]:
            state["show_poincare"] = False
        state.update(current_step=step, show_hint=payload["hint"],
                     solution_origin=origin, view_reset=reset)
        return state
    except (ValueError, TypeError, KeyError, UnicodeError, binascii.Error, RecursionError, OverflowError):
        return None


def input_format(step):
    """Match displayed precision to the selectable increment."""
    decimals = len(str(step).rstrip("0").partition(".")[2])
    return f"%.{decimals}f"
