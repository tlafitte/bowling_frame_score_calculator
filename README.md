# Bowling Frame Score Calculator

A Python module for calculating individual bowling frame scores.

## Problem Description

This calculator is part of a bowling scoring system where:
- **Alice's module** handles pin counting and indicates fouls/splits
- **This module** calculates frame scores from roll data
- **Bob's module** displays the scorecard

The calculator accepts an array of rolls and returns an array of frame scores, handling incomplete games where strikes and spares cannot yet be fully scored.

## Features

- Calculates individual frame scores (not cumulative/running totals)
- Handles strikes (10 + next 2 rolls)
- Handles spares (10 + next 1 roll)
- Handles open frames (sum of 2 rolls)
- Returns `None` for incomplete frames
- Supports games in progress (partial games)
- Input validation with descriptive error messages
- Comprehensive test coverage

## Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd <repo-directory>

# Install dependencies
pip install -r requirements.txt
```

## Usage

```python
from frame_scores_calc import calculate_frame_scores

# Example: Game in progress
rolls = [4, 5, "X", 8]
scores = calculate_frame_scores(rolls)
print(scores)  # [9, None, None]

# Example: After third frame second roll
rolls = [4, 5, "X", 8, 1]
scores = calculate_frame_scores(rolls)
print(scores)  # [9, 19, 9]

# Example: Spare scoring
rolls = [1, "/", 5, 3]
scores = calculate_frame_scores(rolls)
print(scores)  # [15, 8]
```

### Input Format

**Valid roll values:**
- `0-9`: Integer representing pins knocked down
- `"X"`: Strike (all 10 pins on first roll)
- `"/"`: Spare (remaining pins knocked down on second roll)

**Returns:**
- List of integers (frame scores) or `None` (incomplete frames)

## Running Tests

```bash
# Run all tests
pytest test_frame_scores_calc.py -v

# Run with coverage
pytest test_frame_scores_calc.py --cov=frame_scores_calc --cov-report=term-missing

# Run specific test class
pytest test_frame_scores_calc.py::TestStrikes -v
```

## Test Coverage

The test suite includes:
- Strike scenarios (single, consecutive, perfect game)
- Spare scenarios (single, consecutive, with strikes)
- Open frames and mixed games
- Incomplete games at various stages
- 10th frame special rules
- Input validation and error cases
- Edge cases

## Examples

### Strike Scoring
```python
# Strike needs 2 more rolls to score
calculate_frame_scores(["X"])  # [None]
calculate_frame_scores(["X", 5, 3])  # [18, 8]

# Consecutive strikes (turkey)
calculate_frame_scores(["X", "X", "X", 5, 2])  # [30, 25, 17, 7]
```

### Spare Scoring
```python
# Spare needs 1 more roll to score
calculate_frame_scores([5, "/"])  # [None]
calculate_frame_scores([5, "/", 4, 2])  # [14, 6]
```

### 10th Frame
```python
# Open frame (no bonus)
calculate_frame_scores([1, 1] * 9 + [4, 5])  # [2]*9 + [9]

# Spare gets 1 bonus roll
calculate_frame_scores([1, 1] * 9 + [4, "/", 7])  # [2]*9 + [17]

# Strike gets 2 bonus rolls
calculate_frame_scores([1, 1] * 9 + ["X", 7, 2])  # [2]*9 + [19]
```

## Design Decisions

1. **Input Validation**: Validates rolls upfront with clear error messages for better debugging
2. **Separation of Concerns**: `_roll_value()` and `_validate_rolls()` are separate helper functions
3. **Fail-Fast**: Raises `ValueError` for invalid input rather than silently failing
4. **Incomplete Game Support**: Returns `None` for frames that cannot yet be scored
5. **10-Frame Limit**: Stops processing after 10 frames (standard bowling game length)

## Code Structure

```
frame_scores_calc.py         # Main calculator module
├── calculate_frame_scores() # Public API
├── _roll_value()            # Convert roll symbols to pin counts
└── _validate_rolls()        # Input validation

test_frame_scores_calc.py    # Comprehensive test suite
├── TestPromptExamples       # Tests from problem spec
├── TestStrikes              # Strike scoring scenarios
├── TestSpares               # Spare scoring scenarios
├── TestOpenFrames           # Open frame scenarios
├── TestIncompleteGames      # Games in progress
├── TestTenthFrame           # 10th frame special rules
├── TestInputValidation      # Error handling
└── TestEdgeCases            # Edge cases and tricky scenarios
```


