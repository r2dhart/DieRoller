"""A simple dice roller for tabletop gaming with modifier support."""

from __future__ import annotations

import random


class DiceExpressionError(ValueError):
    """Custom exception for dice expression parsing errors."""

def parse_dice_expression(expression: str) -> dict:
    """Parse a dice expression string into components."""
    expression = expression.strip()

    # Determine if we have a modifier and which operator to use
    plus_idx = expression.rfind('+')
    minus_idx = expression.rfind('-')

    # Find the rightmost modifier operator
    has_plus = plus_idx >= 0
    has_minus = minus_idx >= 0

    if not has_plus and not has_minus:
        # No modifier at all - just pure dice notation (e.g., '3d6')
        die_part = expression
        modifier_sign = 0
        modifier_value = 0
        modifier_value_str = ''
    elif has_plus and has_minus:
        # Both exist - use whichever comes last (standard operator precedence)
        if plus_idx > minus_idx:
            modifier_sign = 1
            die_part, modifier_value_str = expression.rsplit('+', 1)
        else:
            modifier_sign = -1
            die_part, modifier_value_str = expression.rsplit('-', 1)
    elif has_plus:
        # Only + exists
        modifier_sign = 1
        die_part, modifier_value_str = expression.rsplit('+', 1)
    else:
        # Only - exists
        modifier_sign = -1
        die_part, modifier_value_str = expression.rsplit('-', 1)

    # Parse dice part (ensure 'd' separator exists)
    if 'd' not in die_part:
        raise DiceExpressionError(
            f"Invalid dice format '{expression}'. "
            f"Must contain a 'd' separator."
        )

    num_dice_str, dice_type_str = die_part.split('d', 1)

    if not num_dice_str or not dice_type_str:
        raise DiceExpressionError(
            f"Invalid dice format '{expression}'. "
            f"Both number of dice and die type must be numbers."
        )

    try:
        num_dice = int(num_dice_str)
        dice_type = int(dice_type_str.strip())
    except ValueError:
        raise DiceExpressionError(
            f"Invalid number in '{expression}'. "
            f"Both the count and die type must be integers."
        )

    # Validate inputs
    if dice_type < 1 or dice_type > 100:
        raise DiceExpressionError(
            f"Invalid die type {dice_type}. "
            f"Supported die types are between 1 and 100."
        )

    if num_dice < 0:
        raise DiceExpressionError(
            f"Cannot roll a negative number of dice in '{expression}'."
        )

    # Parse modifier value (if there was one)
    modifier_value = 0  # Initialize to default for no-modifier case
    if modifier_value_str:
        try:
            modifier_value = int(modifier_value_str.strip())
        except ValueError:
            raise DiceExpressionError(
                f"Invalid modifier '{modifier_value_str}' in '{expression}'. "
                f"Modifier must be an integer."
            )

    return {
        'num_dice': num_dice,
        'dice_type': dice_type,
        'modifier_sign': modifier_sign,
        'modifier_value': modifier_value,
    }

def roll_dice(expression: str) -> tuple[list[int], int]:
    """Roll dice and apply modifier.

    Args:
        expression: The dice expression to roll (e.g., '3d6+2').

    Returns:
        A tuple of (results_list, final_total).

    Raises:
        DiceExpressionError: If the expression cannot be parsed.
    """
    components = parse_dice_expression(expression)

    results: list[int] = []

    for _ in range(components['num_dice']):
        roll: int = random.randint(1, components['dice_type'])
        results.append(roll)

    # Apply modifier
    total_modifier: int = (components['modifier_sign']
                           * components['modifier_value']
                           if components['modifier_sign'] else 0)

    final_total: int = sum(results) + total_modifier

    return results, final_total


def main() -> None:
    """Main loop for the dice roller application."""
    while True:
        user_input = input("Enter the dice roll (e.g., '1d4', '3d6+2', etc.): ")

        if user_input.lower() == 'quit':
            print("Goodbye!")
            break

        try:
            results, total = roll_dice(user_input)

            # Get modifier for display
            components = parse_dice_expression(user_input)

            # Display in your desired format
            if components['modifier_sign']:
                modifier_str = f"+{components['modifier_value']}" if components['modifier_sign'] == 1 else f"-{components['modifier_value']}"
                print(f"Rolls: {results}{modifier_str}")
            else:
                print(f"Rolls: {results}")

            print(f"Total: {total}")

        except (ValueError, IndexError, DiceExpressionError) as e:
            print(f"Invalid input: {e}")


if __name__ == '__main__':
    main()
