"""A simple dice roller for tabletop gaming with modifier support."""

from __future__ import annotations

import random
import re
from dataclasses import dataclass
from typing import Optional

# Constants
MIN_DICE_TYPE = 1
MAX_DICE_TYPE = 100

class DiceExpressionError(ValueError):
    """Custom exception for dice expression parsing errors."""

@dataclass(frozen=True)
class DiceComponents:
    """Data structure for parsed dice expressions (Metadata)."""
    num_dice: int
    dice_type: int
    modifier_sign: int
    modifier_value: int
    drop_lowest: bool

    @classmethod
    def from_expression(cls, expression: str) -> DiceComponents:
        """Parses a string and returns a DiceComponents instance."""
        expression = expression.strip()
        # Regex: num_dice, d, dice_type, optional modifier, optional -drop
        pattern = r"^(\d+)d(\d+)([+-]\d+)?(-drop)?$"
        match = re.fullmatch(pattern, expression)

        if not match:
            raise DiceExpressionError(
                f"Invalid format '{expression}'. Expected format like '3d6', '3d6+2', or '4d6-drop'."
            )

        num_dice_str, dice_type_str, modifier_str, drop_str = match.groups()

        try:
            num_dice = int(num_dice_str)
            dice_type = int(dice_type_str)
        except ValueError:
            raise DiceExpressionError(f"Invalid numbers in expression '{expression}'.")

        if dice_type < MIN_DICE_TYPE or dice_type > MAX_DICE_TYPE:
            raise DiceExpressionError(
                f"Invalid die type {dice_type}. Supported range: {MIN_DICE_TYPE}-{MAX_DICE_TYPE}."
            )

        modifier_sign = 0
        modifier_value = 0
        if modifier_str:
            modifier_sign = 1 if modifier_str.startswith('+') else -1
            modifier_value = int(modifier_str[1:])

        drop_lowest = drop_str is not None and drop_str == "-drop"

        return cls(
            num_dice=num_dice,
            dice_type=dice_type,
            modifier_sign=modifier_sign,
            modifier_value=modifier_value,
            drop_lowest=drop_lowest
        )

@dataclass(frozen=True)
class Roll:
    """Represents the result of a dice roll."""
    results: list[int]
    total: int
    components: DiceComponents

    @classmethod
    def from_expression(cls, expression: str) -> Roll:
        """Factory method to parse a string and generate a Roll object."""
        # 1. Parse the metadata
        components = DiceComponents.from_expression(expression)

        # 2. Perform the roll
        results = [random.randint(1, components.dice_type) for _ in range(components.num_dice)]

        # 3. Handle logic (like dropping the lowest)
        if components.drop_lowest and len(results) > 1:
            results.sort()
            results.pop(0)

        # 4. Calculate final total
        total_modifier = components.modifier_sign * components.modifier_value
        final_total = sum(results) + total_modifier

        return cls(
            results=results,
            total=final_total,
            components=components
        )

    @property
    def summary(self) -> str:
        """Returns a formatted string of the roll result."""
        if self.components.modifier_sign != 0:
            sign_str = "+" if self.components.modifier_sign == 1 else "-"
            return f"Rolls: {self.results}{sign_str}{self.components.modifier_value}"
        return f"Rolls: {self.results}"


def main() -> None:
    """Main loop for the dice roller application."""
    while True:
        user_input = input("Enter the dice roll (e.g., '1d4', '3d6+2', '4d6-drop'): ")

        if user_input.lower() == 'quit':
            print("Goodbye!")
            break

        try:
            # Instead of a tuple, we get a single object with properties
            roll = Roll.from_expression(user_input)

            # Access properties directly
            print(roll.summary)
            print(f"Total: {roll.total}")

            if roll.components.drop_lowest:
                print("(Lowest roll dropped)")

        except (ValueError, IndexError, DiceExpressionError) as e:
            print(f"Invalid input: {e}")


if __name__ == '__main__':
    main()
