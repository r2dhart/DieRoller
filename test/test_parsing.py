import pytest
from dieRoller import DiceComponents, DiceExpressionError

def test_valid_expressions():
    """Test that valid expressions parse correctly into DiceComponents."""
    # Standard roll
    comp = DiceComponents.from_expression("3d6")
    assert comp.num_dice == 3
    assert comp.dice_type == 6
    assert comp.drop_count == 0

    # Modifier
    comp = DiceComponents.from_expression("3d6+2")
    assert comp.modifier_value == 2
    assert comp.modifier_sign == 1

    # Drop count
    comp = DiceComponents.from_expression("4d6-drop")
    assert comp.drop_count == 1

    # Drop specific
    comp = DiceComponents.from_expression("4d6-drop2")
    assert comp.drop_count == 2

    # Advantage
    comp = DiceComponents.from_expression("2d20-adv")
    assert comp.advantage is True

def test_invalid_formats():
    """Test that malformed strings raise DiceExpressionError."""
    with pytest.raises(DiceExpressionError):
        DiceComponents.from_expression("invalid")

    with pytest.raises(DiceExpressionError):
        DiceComponents.from_expression("3d6+")

def test_invalid_die_type():
    """Test that die types outside the allowed range (1-100) raise errors."""
    with pytest.raises(DiceExpressionError):
        DiceComponents.from_expression("1d101")

def test_invalid_drop_count():
    """Test that dropping all or more dice than rolled raises an error."""
    with pytest.raises(DiceExpressionError):
        DiceComponents.from_expression("3d6-drop3")

    with pytest.raises(DiceExpressionError):
        DiceComponents.from_expression("2d20-drop3")
