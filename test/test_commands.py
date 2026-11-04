import pytest
from dieRoller import process_input

def test_process_input_quit():
    """Ensure the 'quit' command returns the correct action."""
    result, action = process_input("quit", [])
    assert action == 'quit'
    assert result is None

def test_process_input_history():
    """Ensure the 'history' and 'h' commands return the correct action."""
    _, action1 = process_input("history", [])
    assert action1 == 'history'

    _, action2 = process_input("h", [])
    assert action2 == 'history'

def test_process_input_help():
    """Ensure the 'help' and '?' commands return the correct action."""
    _, action1 = process_input("help", [])
    assert action1 == 'help'

    _, action2 = process_input("?", [])
    assert action2 == 'help'

def test_process_input_valid_roll():
    """Ensure a valid roll string returns a 'roll' action and a Roll object."""
    result, action = process_input("3d6", [])
    assert action == 'roll'
    assert result is not None
    # We check if it's a Roll object by checking for the 'summary' property
    assert hasattr(result, 'summary')

def test_process_input_invalid_roll():
    """Ensure an invalid roll string returns an error action."""
    result, action = process_input("invalid-input", [])
    assert action.startswith('error:')
    assert result is None
