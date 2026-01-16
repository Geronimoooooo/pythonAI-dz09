import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__) or ".")

from unittest.mock import patch

import lotoMenuModul
import lotoModul

class TestModulLoto(unittest.TestCase):

    def test_keg_init(self):
        self.keg = lotoModul.Keg()
        self.assertTrue(self.keg, 0)
        self.assertTrue(1 <= self.keg.num <= 90)


    def test_card_init(self):
        self.card = lotoModul.Card()
        self.assertTrue(self.card, 0)

    def test_init_requires_list(self):
        with self.assertRaises(TypeError):
            lotoModul.Card(users_numbers="not a list")

    def test_init_requires_15_numbers(self):
        with self.assertRaises(ValueError):
            lotoModul.Card(users_numbers=list(range(1, 10)))

    def test_init_requires_uniques(self):
        nums = [1] * 15
        with self.assertRaises(ValueError):
            lotoModul.Card(users_numbers=nums)

class TestGenerateUniqueNumbers(unittest.TestCase):
    def test_length_uniqueness_and_bounds_default(self):
        nums = lotoMenuModul.generate_unique_numbers(15)
        self.assertEqual(len(nums), 15)
        self.assertEqual(len(set(nums)), 15)
        self.assertTrue(all(1 <= x <= 90 for x in nums))

    def test_custom_bounds(self):
        nums = lotoMenuModul.generate_unique_numbers(10, minbound=5, maxbound=20)
        self.assertEqual(len(nums), 10)
        self.assertEqual(len(set(nums)), 10)
        self.assertTrue(all(5 <= x <= 20 for x in nums))

    def test_too_many_numbers_raises(self):
        # In range 1..3 we can only generate 3 unique numbers
        with self.assertRaises(ValueError):
            lotoMenuModul.generate_unique_numbers(4, minbound=1, maxbound=3)

class TestCountScores(unittest.TestCase):
    def test_draw_message_when_counts_equal(self):
        # user1count == compcount => "Пока никто..."
        scores = [1, 2]
        self.assertEqual(
            lotoMenuModul.count_scores(scores),
            "Пока никто не победил. Попробуй еще раз!",
        )

    def test_user_vs_comp_user_wins(self):
        scores = [1, 1, 2]
        result = lotoMenuModul.count_scores(scores)
        self.assertIsInstance(result, tuple)
        self.assertIn("Баллы игрока 1: 2", result[0])
        self.assertIn("Баллы компьютера: 1", result[1])
        self.assertIn("Игрок победил", result[1])

    def test_user_vs_comp_comp_wins(self):
        scores = [1, 2, 2]
        result = lotoMenuModul.count_scores(scores)
        self.assertIsInstance(result, tuple)
        self.assertIn("Баллы игрока 1: 1", result[0])
        self.assertIn("Баллы компьютера: 2", result[1])
        self.assertIn("Компьютер победил", result[1])

    def test_user_vs_user_user2_wins(self):
        # Here code uses 4 as user2 win marker
        scores = [1, 4, 4]
        result = lotoMenuModul.count_scores(scores)
        self.assertIsInstance(result, tuple)
        self.assertIn("Баллы игрока 1: 1", result[0])
        self.assertIn("Баллы игрока 2: 2", result[1])
        self.assertIn("Игрок 2 победил", result[1])

    def test_all_unknown_codes_returns_no_winner_message(self):
        # With current logic: when counts are all 0, the first equality check triggers
        scores = [9, 9, 9]
        self.assertEqual(
            lotoMenuModul.count_scores(scores),
            "Пока никто не победил. Попробуй еще раз!",
        )

class TestGamePlayRoundRegime1(unittest.TestCase):
    def _make_game_regime1(self):
        user_numbers = list(range(1, 16))
        with patch("lotoModul.lotoMenuModul.generate_unique_numbers", return_value=list(range(1, 91))):
            game = lotoModul.Game(game_regime=1, user_numbers=user_numbers)
        return game

    @patch("builtins.input", return_value="y")
    def test_user_marks_number_not_on_card_loses(self, _):
        game = self._make_game_regime1()
        game._Game__kegs = [90]  # 90 is not in 1..15
        result = game.play_round()
        self.assertEqual(result, 0)

    @patch("builtins.input", return_value="n")
    def test_user_does_not_mark_number_on_card_loses(self, _):
        game = self._make_game_regime1()
        game._Game__kegs = [1]  # 1 is in card
        result = game.play_round()
        self.assertEqual(result, 0)
class TestGamePlayRoundRegime2(unittest.TestCase):
    def _make_game_regime2(self):
        user_numbers = list(range(1, 16))
        with patch("lotoModul.lotoMenuModul.generate_unique_numbers", return_value=list(range(1, 91))):
            game = lotoModul.Game(game_regime=2, user_numbers=user_numbers)
        return game

    def test_first_player_mistake_returns_3(self):
        game = self._make_game_regime2()
        game._Game__kegs = [90]  # not on card
        # first prompt only
        with patch("builtins.input", return_value="y"):
            result = game.play_round()
        self.assertEqual(result, 3)
