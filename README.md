# DieRoller 🎲

A lightweight, command-line dice roller designed for tabletop RPGs (like D&D) and board games. It supports complex dice expressions including multiple dice, specific die types, and modifiers.

## ✨ Features

- **Flexible Expressions**: Input rolls like `3d6+2`, `1d20-1`, or just `2d10`.
- **Modifier Support**: Automatically handles both addition and subtraction modifiers.
- **Advantage & Disadvantage**: Use `-adv` or `-dis` to automatically roll 2 dice and keep the highest or lowest result, respectively.
- **Drop Mechanics**: Use `-drop` to drop the lowest die (defaults to 1) or `-dropN` to drop a specific number of lowest results (e.g., `4d6-drop2`).
- **Input Validation**: Ensures correct formatting, valid die types (1-100), and ensures at least one die remains after dropping.
- **Clean Output**: Displays the individual results of every die rolled, the final total, and a summary of any applied mechanics (Advantage/Disadvantage/Drop).

## 🚀 Getting Started

### Prerequisites
- Python 3.x installed on your machine.

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/DieRoller.git

## How to Use
Enter your dice roll into the prompt. The application supports the following syntax:

### 1. Basic Rolls & Modifiers
- **Basic**: [number]d[die_type]
> ***Example**: 3d6 (Rolls three 6-sided dice)*
- **Addition**: [number]d[die_type]+[value]
> ***Example**: 1d20+5 (Rolls a 20-sided die and adds 5)*
- **Subtraction**: [number]d[die_type]-[value]
> ***Example**: 2d10-2 (Rolls two 10-sided dice and subtracts 2)*

### 2. Drop Mechanics
- **Standard Drop**: [number]d[die_type]-drop
> ***Example**: 4d6-drop (Rolls four 6-sided dice and drops the lowest one)*
- **Custom Drop**: [number]d[die_type]-drop[N]
> ***Example**: 4d6-drop2 (Rolls four 6-sided dice and drops the two lowest)*

### 3. Advantage & Disadvantage
- **Advantage**: 2d20-adv (Rolls two 20-sided dice and keeps the higher result)
- **Disadvantage**: 2d20-dis (Rolls two 20-sided dice and keeps the lower result)

### 4. Application Commands
- **History**: Type history or h to see the last 10 results.
- **Help**: Type help or ? to see the syntax guide.
- **Quit**: Type quit to exit the application.

### 📝 Examples
- 3d6+2 - Rolls 3 six-sided dice and adds 2.
- 2d20-adv - Rolls 20-sided dice with Advantage (keeps highest).
- 4d6-drop2 - Rolls 4 six-sided dice and drops the 2 lowest results.
- 1d100-dis - Rolls a 100-sided die with Disadvantage (keeps lowest).
