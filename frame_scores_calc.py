def _roll_value(roll, previous_roll=None):
    """
    Convert roll symbols to pin counts.
    previous_roll is needed to compute spare values.
    """
    if roll == "X":
        return 10
    if roll == "/":
        return 10 - previous_roll
    return int(roll)


def calculate_frame_scores(rolls):
    """
    Calculate bowling frame scores for a game in progress.
    
    Args:
        rolls: List of roll values. Valid values are:
            - Integers 0-9: pins knocked down
            - 'X': strike (all 10 pins)
            - '/': spare (remaining pins after first roll)
    
    Returns:
        list: Frame scores (int or None for incomplete frames)
    
    Raises:
        ValueError: If rolls contain invalid values or impossible combinations
    """
    _validate_rolls(rolls)
    
    frame_scores = []
    i = 0  # index into rolls
    frame = 1

    while frame <= 10 and i < len(rolls):
        roll1 = rolls[i]

        # STRIKE
        if roll1 == "X":
            # Need two more rolls to score this frame
            if i + 2 >= len(rolls):
                frame_scores.append(None)
            else:
                next1 = _roll_value(rolls[i+1])
                # spare can't appear right after a strike, so safe
                next2 = _roll_value(rolls[i+2], next1)
                frame_scores.append(10 + next1 + next2)
            i += 1
            frame += 1
            continue

        # Otherwise, need a second roll
        if i + 1 >= len(rolls):
            frame_scores.append(None)
            break

        roll2 = rolls[i+1]

        # SPARE
        if roll2 == "/":
            if i + 2 >= len(rolls):  # spare needs next roll
                frame_scores.append(None)
            else:
                next1 = _roll_value(rolls[i+2])
                frame_scores.append(10 + next1)
            i += 2
            frame += 1
            continue

        # OPEN FRAME
        val1 = _roll_value(roll1)
        val2 = _roll_value(roll2)
        frame_scores.append(val1 + val2)

        i += 2
        frame += 1

    return frame_scores


def _validate_rolls(rolls):
    """Validate roll input before processing."""
    if not isinstance(rolls, list):
        raise ValueError("Rolls must be a list")
    
    for i, roll in enumerate(rolls):
        # Check valid types
        if roll == 'X' or roll == '/':
            continue
        if isinstance(roll, int) and 0 <= roll <= 9:
            continue
        raise ValueError(f"Invalid roll at index {i}: {roll}")
    
    # Check spare doesn't appear as first roll of a frame
    i = 0
    while i < len(rolls):
        if rolls[i] == '/':
            raise ValueError(f"Spare '/' cannot be first roll of frame (index {i})")
        if rolls[i] == 'X':
            i += 1
        else:
            i += 2  # skip second roll of frame
