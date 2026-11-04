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
