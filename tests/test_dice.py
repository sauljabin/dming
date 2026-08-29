import random
import unittest
from unittest.mock import patch

from click.testing import CliRunner
from faker import Faker

from dming.cli import _roll
from dming.dice import roll, roll_details

faker = Faker()


class TestNormalRoll(unittest.TestCase):
    @patch("dming.dice.random")
    def test_d20_roll(self, mock_random):
        generated_dice = random.randint(1, 20)
        expected_value = generated_dice
        mock_random.randint.return_value = generated_dice

        result = roll("d20")
        self.assertEqual((f"{expected_value}", expected_value), result)

    @patch("dming.dice.random")
    def test_1d20_roll(self, mock_random):
        generated_dice = random.randint(1, 20)
        expected_value = generated_dice
        mock_random.randint.return_value = generated_dice

        result = roll("1d20")
        self.assertEqual((f"{expected_value}", expected_value), result)

    @patch("dming.dice.random")
    def test_6d6_roll(self, mock_random):
        generated_dice = [1, 2, 3, 4, 5, 6, 6]
        expected_value = 21
        mock_random.randint.side_effect = generated_dice

        result = roll("6d6")
        self.assertEqual((f"{expected_value}", expected_value), result)

    @patch("dming.dice.random")
    def test_1d20_plus3_roll(self, mock_random):
        generated_dice = [1, 2, 3, 4, 5, 6, 7]
        mock_random.randint.side_effect = generated_dice

        result = roll("d20+4")
        self.assertEqual(("1+4", 5), result)

    @patch("dming.dice.random")
    def test_2d100_roll(self, mock_random):
        generated_dice = [58, 34, 32]
        mock_random.randint.side_effect = generated_dice

        result = roll("2d100")
        self.assertEqual(("92", 92), result)

    @patch("dming.dice.random")
    def test_roll_details_include_each_die_in_formula(self, mock_random):
        mock_random.randint.side_effect = [4, 4]

        details = roll_details("2d20")

        self.assertEqual("4+4", details.formula)
        self.assertEqual((4, 4), details.groups[0].rolls)

    @patch("dming.dice.random")
    def test_1d20_minus3_roll(self, mock_random):
        generated_dice = [20, 19, 18, 17, 16, 15, 14]
        mock_random.randint.side_effect = generated_dice

        result = roll("d20-4")
        self.assertEqual(("20-4", 16), result)

    @patch("dming.dice.random")
    def test_invalid_roll(self, mock_random):
        generated_dice = [1, 2, 3, 4, 5, 6]
        mock_random.randint.side_effect = generated_dice

        with self.assertRaises(Exception) as context:
            roll("xd1")

        self.assertEqual("not allowed characters", f"{context.exception}")


class TestKeepHighestRoll(unittest.TestCase):
    @patch("dming.dice.random")
    def test_2d20kh_roll(self, mock_random):
        generated_dice = [20, 10]
        expected_value = 20
        mock_random.randint.side_effect = generated_dice

        result = roll("2d20kh")
        self.assertEqual((f"{expected_value}", expected_value), result)

    @patch("dming.dice.random")
    def test_2d20kh_plus2_roll(self, mock_random):
        generated_dice = [20, 10]
        mock_random.randint.side_effect = generated_dice

        result = roll("2d20kh+2")
        self.assertEqual(("20+2", 22), result)

    @patch("dming.dice.random")
    def test_2d20kh1_roll(self, mock_random):
        generated_dice = [19, 9]
        expected_value = 19
        mock_random.randint.side_effect = generated_dice

        result = roll("2d20kh1")
        self.assertEqual((f"{expected_value}", expected_value), result)

    @patch("dming.dice.random")
    def test_roll_details_identify_selected_die(self, mock_random):
        mock_random.randint.side_effect = [9, 19]

        details = roll_details("2d20kh1")

        self.assertEqual((9, 19), details.groups[0].rolls)
        self.assertEqual((1,), details.groups[0].selected_indices)
        self.assertEqual((19,), details.groups[0].selected)

    @patch("dming.dice.random")
    def test_2d20kh1_plus3_roll(self, mock_random):
        generated_dice = [19, 9]
        mock_random.randint.side_effect = generated_dice

        result = roll("2d20kh1+3")
        self.assertEqual(("19+3", 22), result)

    @patch("dming.dice.random")
    def test_2d20kh1_minus3_roll(self, mock_random):
        generated_dice = [19, 9]
        mock_random.randint.side_effect = generated_dice

        result = roll("2d20kh1-3")
        self.assertEqual(("19-3", 16), result)

    @patch("dming.dice.random")
    def test_2d20kh1_plus1d20_plus3_roll(self, mock_random):
        generated_dice = [19, 9, 15, 16]
        mock_random.randint.side_effect = generated_dice

        result = roll("2d20kh1+1d20+3")
        self.assertEqual(("19+15+3", 37), result)


class TestKeepLowestRoll(unittest.TestCase):
    @patch("dming.dice.random")
    def test_2d20kl_roll(self, mock_random):
        generated_dice = [20, 10]
        expected_value = 10
        mock_random.randint.side_effect = generated_dice

        result = roll("2d20kl")
        self.assertEqual((f"{expected_value}", expected_value), result)

    @patch("dming.dice.random")
    def test_2d20kl_plus2_roll(self, mock_random):
        generated_dice = [20, 10]
        mock_random.randint.side_effect = generated_dice

        result = roll("2d20kl+2")
        self.assertEqual(("10+2", 12), result)

    @patch("dming.dice.random")
    def test_2d20kl1_roll(self, mock_random):
        generated_dice = [19, 9]
        expected_value = 9
        mock_random.randint.side_effect = generated_dice

        result = roll("2d20kl1")
        self.assertEqual((f"{expected_value}", expected_value), result)

    @patch("dming.dice.random")
    def test_2d20kl1_plus3_roll(self, mock_random):
        generated_dice = [19, 9]
        mock_random.randint.side_effect = generated_dice

        result = roll("2d20kl1+3")
        self.assertEqual(("9+3", 12), result)

    @patch("dming.dice.random")
    def test_2d20kl1_minus3_roll(self, mock_random):
        generated_dice = [19, 9]
        mock_random.randint.side_effect = generated_dice

        result = roll("2d20kl1-3")
        self.assertEqual(("9-3", 6), result)

    @patch("dming.dice.random")
    def test_2d20kl1_plus1d20_plus3_roll(self, mock_random):
        generated_dice = [19, 9, 15, 16]
        mock_random.randint.side_effect = generated_dice

        result = roll("2d20kl1+1d20+3")
        self.assertEqual(("9+15+3", 27), result)


class TestDropHighestRoll(unittest.TestCase):
    @patch("dming.dice.random")
    def test_2d20dh_roll(self, mock_random):
        generated_dice = [20, 10]
        expected_value = 10
        mock_random.randint.side_effect = generated_dice

        result = roll("2d20dh")
        self.assertEqual((f"{expected_value}", expected_value), result)

    @patch("dming.dice.random")
    def test_2d20dh_plus2_roll(self, mock_random):
        generated_dice = [20, 10]
        mock_random.randint.side_effect = generated_dice

        result = roll("2d20dh+2")
        self.assertEqual(("10+2", 12), result)

    @patch("dming.dice.random")
    def test_2d20dh1_roll(self, mock_random):
        generated_dice = [19, 9]
        expected_value = 9
        mock_random.randint.side_effect = generated_dice

        result = roll("2d20dh1")
        self.assertEqual((f"{expected_value}", expected_value), result)

    @patch("dming.dice.random")
    def test_2d20dh1_plus3_roll(self, mock_random):
        generated_dice = [19, 9]
        mock_random.randint.side_effect = generated_dice

        result = roll("2d20dh1+3")
        self.assertEqual(("9+3", 12), result)

    @patch("dming.dice.random")
    def test_2d20dh1_minus3_roll(self, mock_random):
        generated_dice = [19, 9]
        mock_random.randint.side_effect = generated_dice

        result = roll("2d20dh1-3")
        self.assertEqual(("9-3", 6), result)

    @patch("dming.dice.random")
    def test_2d20dh1_plus1d20_plus3_roll(self, mock_random):
        generated_dice = [19, 9, 15, 16]
        mock_random.randint.side_effect = generated_dice

        result = roll("2d20dh1+1d20+3")
        self.assertEqual(("9+15+3", 27), result)


class TestDropLowestRoll(unittest.TestCase):
    @patch("dming.dice.random")
    def test_2d20dl_roll(self, mock_random):
        generated_dice = [20, 10]
        expected_value = 20
        mock_random.randint.side_effect = generated_dice

        result = roll("2d20dl")
        self.assertEqual((f"{expected_value}", expected_value), result)

    @patch("dming.dice.random")
    def test_2d20dl_plus2_roll(self, mock_random):
        generated_dice = [20, 10]
        mock_random.randint.side_effect = generated_dice

        result = roll("2d20dl+2")
        self.assertEqual(("20+2", 22), result)

    @patch("dming.dice.random")
    def test_2d20dl1_roll(self, mock_random):
        generated_dice = [19, 9]
        expected_value = 19
        mock_random.randint.side_effect = generated_dice

        result = roll("2d20dl1")
        self.assertEqual((f"{expected_value}", expected_value), result)

    @patch("dming.dice.random")
    def test_2d20dl1_plus3_roll(self, mock_random):
        generated_dice = [19, 9]
        mock_random.randint.side_effect = generated_dice

        result = roll("2d20dl1+3")
        self.assertEqual(("19+3", 22), result)

    @patch("dming.dice.random")
    def test_2d20dl1_minus3_roll(self, mock_random):
        generated_dice = [19, 9]
        mock_random.randint.side_effect = generated_dice

        result = roll("2d20dl1-3")
        self.assertEqual(("19-3", 16), result)

    @patch("dming.dice.random")
    def test_2d20dl1_plus1d20_plus3_roll(self, mock_random):
        generated_dice = [19, 9, 15, 16]
        mock_random.randint.side_effect = generated_dice

        result = roll("2d20dl1+1d20+3")
        self.assertEqual(("19+15+3", 37), result)


class TestRollCli(unittest.TestCase):
    @patch("dming.dice.random")
    def test_plain_details_show_rolls_selection_and_formula(self, mock_random):
        mock_random.randint.side_effect = [19, 9]

        result = CliRunner().invoke(_roll, ["--details", "--plain", "2d20kh1"])

        self.assertEqual(0, result.exit_code)
        self.assertIn("Roll:    2d20kh1", result.output)
        self.assertIn("2d20kh1: 19, 9 -> 19 (keep highest 1)", result.output)
        self.assertIn("Math:    19", result.output)
        self.assertIn("Result:  19", result.output)
        self.assertNotIn("Rolled:", result.output)
        self.assertNotIn("Rule:", result.output)
        self.assertNotIn("\x1b[", result.output)

    @patch("dming.dice.random")
    def test_details_show_every_unfiltered_die(self, mock_random):
        mock_random.randint.side_effect = [4, 4]

        result = CliRunner().invoke(_roll, ["--details", "--plain", "2d20"])

        self.assertEqual(0, result.exit_code)
        self.assertIn("Math:   4 + 4", result.output)
        self.assertIn("Result: 8", result.output)

    @patch("dming.dice.random")
    def test_plain_details_have_no_styling_or_emojis(self, mock_random):
        mock_random.randint.side_effect = [19, 9]

        result = CliRunner().invoke(_roll, ["--details", "--plain", "2d20kh1"])

        self.assertEqual(0, result.exit_code)
        self.assertIn("Roll:    2d20kh1", result.output)
        self.assertIn("Math:    19", result.output)
        self.assertIn("Result:  19", result.output)
        self.assertNotIn("🎲", result.output)
        self.assertNotIn("\x1b[", result.output)

    @patch("dming.dice.random")
    def test_rich_filters_stay_with_their_dice_groups(self, mock_random):
        mock_random.randint.side_effect = [5, 7, 5, 7, 13, 10, 5, 9]

        result = CliRunner().invoke(
            _roll,
            ["--details", "1d6+1d8+4d20kh2+2d20kl1+15"],
        )

        self.assertEqual(0, result.exit_code)
        self.assertIn("4d20kh2: 5, 7, 13, 10 → 13, 10 (keep highest 2)", result.output)
        self.assertIn("2d20kl1: 5, 9 → 5 (keep lowest 1)", result.output)
        self.assertNotIn("Rule:", result.output)

    @patch("dming.dice.random")
    def test_plain_result_is_only_the_number(self, mock_random):
        mock_random.randint.return_value = 12

        result = CliRunner().invoke(_roll, ["--plain", "d20"])

        self.assertEqual(0, result.exit_code)
        self.assertEqual("12\n", result.output)

    def test_verbose_short_option_is_replaced(self):
        result = CliRunner().invoke(_roll, ["-v", "d20"])

        self.assertNotEqual(0, result.exit_code)
        self.assertIn("No such option '-v'", result.output)

    def test_no_color_option_is_removed(self):
        result = CliRunner().invoke(_roll, ["--no-color", "d20"])

        self.assertNotEqual(0, result.exit_code)
        self.assertIn("No such option '--no-color'", result.output)
