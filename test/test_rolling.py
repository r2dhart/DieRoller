import pytest
from unittest.mock import patch
from dieRoller import Roll

# We use @patch to intercept calls to random.randint.
# This ensures that every time random.randint is called during this test,
# it returns the values we specify in 'side_effect'.

@patch('dieRoller.random.randint')
def test_roll_total_basic(mock_randint):
    """Test that a simple roll returns the correct sum of mocked dice."""
    # Force the 3 dice to return 2, 4, and 6
    mock_randint.side_effect = [2, 4, 6]

    roll = Roll.from_expression("3d6")

    assert roll.results == [2, 4, 6]
    assert roll.total == 12

@patch('dieRoller.random.randint')
def test_modifier_addition(mock_randint):
    """Test that positive modifiers are added correctly to the total."""
    # Force the 1 die to return 4
    mock_randint.side_effect = [4]

    roll = Roll.from_expression("1d6+2")

    assert roll.results == [4]
    assert roll.total == 6

@patch('dieRoller.random.randint')
def test_advantage_logic(mock_randint):
    """Test that advantage correctly keeps the higher of two dice."""
    # Roll 1: 10, Roll 2: 20. Advantage should keep 20.
    mock_randint.side_effect = [10, 20]

    roll = Roll.from_expression("2d20-adv")

    assert roll.results == [20]
    assert roll.total == 20

@patch('dieRoller.random.randint')
def test_disadvantage_logic(mock_randint):
    """Test that disadvantage correctly keeps the lower of two dice."""
    # Roll 1: 10, Roll 2: 20. Disadvantage should keep 10.
    mock_randint.side_effect = [10, 20]

    roll = Roll.from_expression("2d20-dis")

    assert roll.results == [10]
    assert roll.total == 10

@patch('dieRoller.random.randint')
def test_drop_logic(mock_randint):
    """Test that drop logic removes the lowest dice correctly."""
    # Roll 4 dice: 2, 5, 8, 10. Drop 2 lowest (2 and 5).
    # The remaining dice should be [8, 10]
    mock_randint.side_effect = [2, 5, 8, 10]

    roll = Roll.from_expression("4d6-drop2")

    assert roll.results == [8, 10]
    assert roll.total == 18
