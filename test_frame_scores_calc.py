"""
Unit tests for bowling frame score calculator.

Run with: pytest test_frame_scores_calc.py -v
"""

import pytest
from frame_scores_calc import calculate_frame_scores


class TestPromptExamples:
    """Test cases directly from the problem specification."""
    
    def test_incomplete_game_with_pending_strike(self):
        """[4, 5, "X", 8] should return [9, nil, nil]"""
        result = calculate_frame_scores([4, 5, "X", 8])
        assert result == [9, None, None]
    
    def test_completed_frames_after_strike(self):
        """[4, 5, "X", 8, 1] should return [9, 19, 9]"""
        result = calculate_frame_scores([4, 5, "X", 8, 1])
        assert result == [9, 19, 9]
    
    def test_spare_with_next_roll(self):
        """[1, "/", 5, 3] should return [15, 8]"""
        result = calculate_frame_scores([1, "/", 5, 3])
        assert result == [15, 8]


class TestStrikes:
    """Test cases for strike scoring."""
    
    def test_single_strike_incomplete(self):
        """Strike without next two rolls returns None"""
        assert calculate_frame_scores(["X"]) == [None]
        assert calculate_frame_scores(["X", 5]) == [None, None]
    
    def test_single_strike_complete(self):
        """Strike with next two rolls scores correctly"""
        result = calculate_frame_scores(["X", 5, 3])
        assert result == [18, 8]
    
    def test_consecutive_strikes(self):
        """Multiple strikes in a row (turkey)"""
        result = calculate_frame_scores(["X", "X", "X", 5, 2])
        assert result == [30, 25, 17, 7]
    
    def test_all_strikes(self):
        """Perfect game through 10 frames"""
        result = calculate_frame_scores(["X"] * 12)
        assert result == [30, 30, 30, 30, 30, 30, 30, 30, 30, 30]


class TestSpares:
    """Test cases for spare scoring."""
    
    def test_spare_incomplete(self):
        """Spare without next roll returns None"""
        result = calculate_frame_scores([5, "/"])
        assert result == [None]
    
    def test_spare_complete(self):
        """Spare with next roll scores correctly"""
        result = calculate_frame_scores([5, "/", 4, 2])
        assert result == [14, 6]
    
    def test_consecutive_spares(self):
        """Multiple spares in a row"""
        result = calculate_frame_scores([1, "/", 2, "/", 5, 3])
        assert result == [12, 15, 8]
    
    def test_spare_followed_by_strike(self):
        """Spare then strike"""
        result = calculate_frame_scores([1, "/", "X", 5, 2])
        assert result == [20, 17, 7]


class TestOpenFrames:
    """Test cases for open frames (no strike or spare)."""
    
    def test_simple_open_frames(self):
        """Basic open frame scoring"""
        result = calculate_frame_scores([3, 4, 2, 5])
        assert result == [7, 7]
    
    def test_gutter_balls(self):
        """All zeros"""
        result = calculate_frame_scores([0, 0, 0, 0])
        assert result == [0, 0]
    
    def test_mixed_frames(self):
        """Mix of strikes, spares, and open frames"""
        result = calculate_frame_scores([1, 4, 4, 5, "X", 0, 1, 7, "/", 6, 4, "X", 2, "/", 6, 4, 5])
        # Frame 1: 1+4 = 5
        # Frame 2: 4+5 = 9
        # Frame 3: X + 0+1 = 11
        # Frame 4: 0+1 = 1
        # Frame 5: 7+/ + 6 = 16
        # Frame 6: 6+4 = 10
        # Frame 7: X + 2+/ = 20 (strike + spare = 10+2+8)
        # Frame 8: 2+/ + 6 = 16 (spare + next roll)
        # Frame 9: 6+4 = 10
        # Frame 10: 5 (incomplete)
        assert result == [5, 9, 11, 1, 16, 10, 20, 16, 10, None]


class TestIncompleteGames:
    """Test cases for games in progress."""
    
    def test_empty_rolls(self):
        """Empty array returns empty result"""
        result = calculate_frame_scores([])
        assert result == []
    
    def test_single_roll(self):
        """One roll, not a strike, returns None"""
        result = calculate_frame_scores([5])
        assert result == [None]
    
    def test_incomplete_second_frame(self):
        """First frame complete, second incomplete"""
        result = calculate_frame_scores([4, 5, 3])
        assert result == [9, None]
    
    def test_nine_frames_complete(self):
        """Nine complete frames"""
        rolls = [1, 1] * 9  # Nine frames of 1,1
        result = calculate_frame_scores(rolls)
        assert result == [2] * 9


class TestTenthFrame:
    """Test cases specific to the 10th frame."""
    
    def test_tenth_frame_open(self):
        """Tenth frame with open frame (no bonus rolls)"""
        rolls = [1, 1] * 9 + [4, 5]
        result = calculate_frame_scores(rolls)
        assert result == [2] * 9 + [9]
    
    def test_tenth_frame_spare(self):
        """Tenth frame with spare gets bonus roll"""
        rolls = [1, 1] * 9 + [4, "/", 7]
        result = calculate_frame_scores(rolls)
        assert result == [2] * 9 + [17]
    
    def test_tenth_frame_strike(self):
        """Tenth frame with strike gets two bonus rolls"""
        rolls = [1, 1] * 9 + ["X", 7, 2]
        result = calculate_frame_scores(rolls)
        assert result == [2] * 9 + [19]


class TestInputValidation:
    """Test cases for input validation."""
    
    def test_invalid_roll_type_string(self):
        """Invalid string roll raises ValueError"""
        with pytest.raises(ValueError, match="Invalid roll"):
            calculate_frame_scores([1, 2, "Z", 3])
    
    def test_invalid_roll_too_high(self):
        """Roll value > 9 raises ValueError"""
        with pytest.raises(ValueError, match="Invalid roll"):
            calculate_frame_scores([1, 2, 11, 3])
    
    def test_invalid_roll_negative(self):
        """Negative roll raises ValueError"""
        with pytest.raises(ValueError, match="Invalid roll"):
            calculate_frame_scores([1, 2, -1, 3])
    
    def test_spare_as_first_roll(self):
        """Spare cannot be first roll of frame"""
        with pytest.raises(ValueError, match="cannot be first roll"):
            calculate_frame_scores(["/", 5])
    
    def test_spare_after_strike_invalid(self):
        """Spare as first roll after strike is invalid"""
        with pytest.raises(ValueError, match="cannot be first roll"):
            calculate_frame_scores(["X", "/", 5])
    
    def test_non_list_input(self):
        """Non-list input raises ValueError"""
        with pytest.raises(ValueError, match="must be a list"):
            calculate_frame_scores("X55")
    
    def test_string_number_invalid(self):
        """String numbers like "5" should fail"""
        with pytest.raises(ValueError, match="Invalid roll"):
            calculate_frame_scores(["5", "4"])


class TestEdgeCases:
    """Additional edge cases."""
    
    def test_alternating_strikes_and_spares(self):
        """Alternating strikes and spares"""
        result = calculate_frame_scores(["X", 5, "/", "X", 5, "/"])
        assert result == [20, 20, 20, None]
    
    def test_all_spares(self):
        """All spares through 10 frames"""
        rolls = [5, "/"] * 10 + [5]  # 10 spares + bonus roll
        result = calculate_frame_scores(rolls)
        assert result == [15] * 10
    
    def test_worst_game(self):
        """All gutter balls"""
        rolls = [0, 0] * 10
        result = calculate_frame_scores(rolls)
        assert result == [0] * 10
    
    def test_strike_then_gutter_balls(self):
        """Strike followed by two gutter balls"""
        result = calculate_frame_scores(["X", 0, 0, 5, 4])
        assert result == [10, 0, 9]
