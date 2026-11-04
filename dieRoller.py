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

def print_help() -> None:
    """Prints the help menu for the dice roller."""
    help_text = """
--- DieRoller Help Menu ---
Supported Syntax:
  - Basic:      [num]d[type] (e.g., 3d6)
  - Modifiers:  [num]d[type][+/-][mod] (e.g., 3d6+2, 1d20-1)
  - Drop Logic: [num]d[type]-drop (drops lowest 1)
                [num]d[type]-dropN (drops N lowest, e.g., 4d6-drop2)
  - Advantage:  2d20-adv (rolls 2, keeps highest)
  - Disadvantage: 2d20-dis (rolls 2, keeps lowest)

Commands:
  - history / h : Show the last 10 rolls
  - help / ?    : Show this menu
  - quit        : Exit the application
    """
    print(help_text)

def process_input(user_input: str, history: list[Roll]) -> tuple[Optional[Roll], str]:
    """
    Processes the user input and returns a tuple of (Roll object or None, action_type).
    The action_type can be 'roll', 'history', 'help', 'quit', or 'error: <message>'.
    """
    user_input_clean = user_input.strip().lower()

    if user_input_clean == 'quit':
        return None, 'quit'

    if user_input_clean in ('history', 'h'):
        return None, 'history'

    if user_input_clean in ('help', '?'):
        return None, 'help'

    try:
        roll = Roll.from_expression(user_input)
        return roll, 'roll'
    except (ValueError, IndexError, DiceExpressionError) as e:
        return None, f'error: {e}'

def main() -> None:
    """Main loop for the dice roller application."""
    # Initialize an empty list to store recent rolls
    history: list[Roll] = []
    MAX_HISTORY = 10  # Keep the last 10 rolls

    while True:
        user_input = input("Enter the dice roll (e.g., '1d4', '3d6+2', '4d6-drop'): ")
        roll, action = process_input(user_input, history)

        if action == 'quit':
            print("Goodbye!")
            break

        elif action == 'history':
            if not history:
                print("No history yet.")
            else:
                print(f"--- Last {len(history)} Rolls ---")
                # Print history in reverse order (most recent first)
                for i, roll in enumerate(reversed(history), 1):
                    print(f"{i}. {roll.summary} | Total: {roll.total}")
            continue

        elif action =='help':
            print_help()
            continue

        elif action.startswith('error: '):
            print(f"Invalid input: {action.split(': ', 1)[1]}")
            continue

        elif roll:
            # Print the current result
            print(roll.summary)
            print(f"Total: {roll.total}")

            if roll.components.drop_count > 0:
                print(f"({roll.components.drop_count} lowest roll(s) dropped)")
            elif roll.components.advantage:
                print("(Advantage applied: kept highest)")
            elif roll.components.disadvantage:
                print("(Disadvantage applied: kept lowest)")

            # Add the new roll to history
            history.append(roll)
            # Ensure we only keep the last MAX_HISTORY rolls
            if len(history) > MAX_HISTORY:
                history.pop(0)

if __name__ == '__main__':
    main()
