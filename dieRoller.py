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
    drop_count: int
    advantage: bool
    disadvantage: bool

    @classmethod
    def from_expression(cls, expression: str) -> DiceComponents:
        """Parses a string and returns a DiceComponents instance."""
        expression = expression.strip()
        # Regex: num_dice, d, dice_type, optional modifier, optional -drop, optional -adv/-dis
        pattern = r"^(\d+)d(\d+)([+-]\d+)?(-drop\d*)?(-adv|-dis)?$"
        match = re.fullmatch(pattern, expression)

        if not match:
            raise DiceExpressionError(
                f"Invalid format '{expression}'. Expected format like '3d6', '3d6+2', '4d6-drop', '2d20-adv', or '2d20-dis'."
            )

        num_dice_str, dice_type_str, modifier_str, drop_str, adv_dis_str = match.groups()

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

        drop_count = 0
        if drop_str:
            if drop_str == "-drop":
                # Default to dropping 1 die if no number is provided
                drop_count = 1
            else:
                try:
                    # Extract digits from "-dropN"
                    drop_count = int(drop_str.replace("-drop", ""))
                except ValueError:
                    raise DiceExpressionError(f"Invalid drop count in expression '{expression}'.")

            if drop_count >= num_dice:
                raise DiceExpressionError(
                    f"Invalid drop count {drop_count}. You must leave at least one die remaining from {num_dice}."
                )

        advantage = adv_dis_str == "-adv"
        disadvantage = adv_dis_str == "-dis"

        return cls(
            num_dice=num_dice,
            dice_type=dice_type,
            modifier_sign=modifier_sign,
            modifier_value=modifier_value,
            drop_count=drop_count,
            advantage=advantage,
            disadvantage=disadvantage
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
        # Advantage/Disadvantage typically requires rolling 2 dice
        if components.advantage or components.disadvantage:
            results = [random.randint(1, components.dice_type),
                        random.randint(1, components.dice_type)]

            if components.advantage:
                results = [max(results)]
            elif components.disadvantage:
                results = [min(results)]
        else:
            results = [random.randint(1, components.dice_type) for _ in range(components.num_dice)]

        # 3. Handle logic (like dropping the lowest)
        # Note: drop_count logic is checked here for standard rolls.
        # Advantage/Disadvantage logic is already handled above.
        if components.drop_count > 0 and len(results) > components.drop_count:
            results.sort()
            # Remove the 'drop_count' lowest results
            results = results[components.drop_count:]

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
        status_msg = ""
        if self.components.advantage:
            status_msg = " (Advantage)"
        elif self.components.disadvantage:
            status_msg = " (Disadvantage)"

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

            if roll.components.drop_count > 0:
                print(f"({roll.components.drop_count} lowest roll(s) dropped)")
            elif roll.components.advantage:
                print("(Advantage applied: kept highest)")
            elif roll.components.disadvantage:
                print("(Disadvantage applied: kept lowest)")

        except (ValueError, IndexError, DiceExpressionError) as e:
            print(f"Invalid input: {e}")

if __name__ == '__main__':
    main()
