# tests/test_escape_room.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import importlib.util

spec = importlib.util.spec_from_file_location(
    "escape_room",
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "escape-room.py"),
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def test_build_system_prompt_contains_location():
    state = {"location": "pavilion", "inventory": [], "solved": [], "alex_trust": 2, "turns_remaining": 15}
    prompt = mod.build_system_prompt(state)
    assert "pavilion" in prompt
    assert "2/5" in prompt
    assert "15" in prompt


def test_build_system_prompt_with_puzzle_event():
    state = {"location": "court", "inventory": ["cipher_note"], "solved": ["cipher_note"],
             "alex_trust": 0, "turns_remaining": 19}
    prompt = mod.build_system_prompt(state, "FOUND_CIPHER_NOTE")
    assert "cipher note" in prompt.lower()


def test_build_system_prompt_no_event():
    state = {"location": "library", "inventory": ["shed_key"], "solved": ["shed_key"],
             "alex_trust": 3, "turns_remaining": 10}
    prompt = mod.build_system_prompt(state, None)
    assert "GAME EVENT" not in prompt


def test_build_system_prompt_unknown_event_ignored():
    state = {"location": "court", "inventory": [], "solved": [], "alex_trust": 0, "turns_remaining": 20}
    prompt = mod.build_system_prompt(state, "MYSTERY_EVENT")
    # unknown events should not raise; prompt still valid
    assert "court" in prompt
