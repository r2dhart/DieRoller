"""A simple dice roller for tabletop gaming with modifier support."""

from __future__ import annotations

import random
import re
from dataclasses import dataclass
from typing import Optional

# Constants for easy maintainability
MIN_DICE_TYPE = 1
MAX_DICE_TYPE = 100

@dataclass(frozen=True)
class DiceComponents:
    """Data structure for parsed dice expressions."""
    num_dice: int
    dice_type: int
    modifier_sign: int
    modifier_value: int

class DiceExpressionError(ValueError):
    """Custom exception for dice expression parsing errors."""

def parse_dice_expression(expression: str) -> DiceComponents:
    """
    Parse a dice expression string into a DiceComponents object using Regex.
    Example inputs: '3d6', '3d6+2', '1d20-5'
    """
    expression = expression.strip()

    # Regex breakdown:
    # ^(\d+)     : Start with one or more digits (number of dice)
    # d          : The 'd' separator
    # (\d+)      : One or more digits (dice type)
    # ([+-]\d+)? : Optional group: a plus or minus followed by digits (modifier)
    # $          : End of string
    pattern = r"^(\d+)d(\d+)([+-]\d+)?$"
    match = re.fullmatch(pattern, expression)

    if not match:
        raise DiceExpressionError(
            f"Invalid format '{expression}'. Expected format like '3d6', '3d6+2', or '1d20-5'."
        )

    num_dice_str, dice_type_str, modifier_str = match.groups()

    try:
            num_dice = int(num_dice_str)
            dice_type = int(dice_type_str)
    except ValueError:
        # This is technically handled by \d+ in regex, but kept for safety
        raise DiceExpressionError(f"Invalid numbers in expression '{expression}'.")

    # Validation
    if dice_type < MIN_DICE_TYPE or dice_type > MAX_DICE_TYPE:
        raise DiceExpressionError(
            f"Invalid die type {dice_type}. Supported range: {MIN_DICE_TYPE}-{MAX_DICE_TYPE}."
        )

    # Parse Modifier
    modifier_sign = 0
    modifier_value = 0
    if modifier_str:
        modifier_sign = 1 if modifier_str.startswith('+') else -1
        modifier_value = int(modifier_str[1:])  # Strip the + or - sign

    return DiceComponents(
        num_dice=num_dice,
        dice_type=dice_type,
        modifier_sign=modifier_sign,
        modifier_value=modifier_value
    )

def roll_dice(expression: str) -> tuple[list[int], int, DiceComponents]:
    """
    Roll dice and apply modifier.

    Returns:
        A tuple of (results_list, final_total, components_object).
    """
    components = parse_dice_expression(expression)

    # Performance: Use list comprehension for rolling
    results = [random.randint(1, components.dice_type) for _ in range(components.num_dice)]

    total_modifier = components.modifier_sign * components.modifier_value
    final_total = sum(results) + total_modifier

    return results, final_total, components


def main() -> None:
    """Main loop for the dice roller application."""
    while True:
        user_input = input("Enter the dice roll (e.g., '1d4', '3d6+2', etc.): ")

        if user_input.lower() == 'quit':
            print("Goodbye!")
            break

        try:
            results, total, components = roll_dice(user_input)

            # Get modifier for display
            components = parse_dice_expression(user_input)

            # Display in your desired format
            if components.modifier_sign != 0:
                sign_str = "+" if components.modifier_sign == 1 else "-"
                print(f"Rolls: {results}{sign_str}{components.modifier_value}")
            else:
                print(f"Rolls: {results}")

            print(f"Total: {total}")
        except (ValueError, IndexError, DiceExpressionError) as e:
            print(f"Invalid input: {e}")


if __name__ == '__main__':
    main()
