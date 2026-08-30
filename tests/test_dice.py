import csv
import io
import json
import random
import unittest
from unittest.mock import patch

from click.testing import CliRunner

from dming.commands.roll import roll_command
from dming.dice import InvalidDiceError, roll, roll_details


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
    def test_roll_details_include_each_die_in_calculation(self, mock_random):
        mock_random.randint.side_effect = [4, 4]

        details = roll_details("2d20")

        self.assertEqual("4+4", details.calculation)
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

        with self.assertRaises(InvalidDiceError) as context:
            roll("xd1")

        self.assertEqual("invalid term: xd1", f"{context.exception}")

    @patch("dming.dice.random")
    def test_whitespace_is_accepted(self, mock_random):
        mock_random.randint.return_value = 10

        self.assertEqual(("10+4-2", 12), roll(" d20 + 4 - 2 "))

    def test_invalid_expressions_raise_domain_error(self):
        expected = {
            "": "roll expression cannot be empty",
            "+": "an operator must be followed by a term",
            "d0": "die must have at least 1 side",
            "0d20": "dice count must be at least 1",
            "2d20kh0": "filter count must be at least 1",
            "2d20kh3": "filter count cannot exceed dice count",
            "1d20++2": "operators must appear between terms",
            "d20/2": "invalid term: d20/2",
        }
        for expression, message in expected.items():
            with (
                self.subTest(expression=expression),
                self.assertRaisesRegex(InvalidDiceError, message),
            ):
                roll(expression)


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
    def test_plain_details_show_rolls_selection_and_calculation(self, mock_random):
        mock_random.randint.side_effect = [19, 9]

        result = CliRunner().invoke(roll_command, ["--details", "--plain", "2d20kh1"])

        self.assertEqual(0, result.exit_code)
        self.assertIn("Roll:        2d20kh1", result.output)
        self.assertIn("2d20kh1:     19, 9 -> 19 (keep highest 1)", result.output)
        self.assertIn("Calculation: 19", result.output)
        self.assertIn("Result:      19", result.output)
        self.assertNotIn("Rolled:", result.output)
        self.assertNotIn("Rule:", result.output)
        self.assertNotIn("\x1b[", result.output)

    @patch("dming.dice.random")
    def test_details_show_every_unfiltered_die(self, mock_random):
        mock_random.randint.side_effect = [4, 4]

        result = CliRunner().invoke(roll_command, ["--details", "--plain", "2d20"])

        self.assertEqual(0, result.exit_code)
        self.assertIn("Calculation: 4 + 4", result.output)
        self.assertIn("Result:      8", result.output)

    @patch("dming.dice.random")
    def test_plain_details_have_no_styling_or_emojis(self, mock_random):
        mock_random.randint.side_effect = [19, 9]

        result = CliRunner().invoke(roll_command, ["--details", "--plain", "2d20kh1"])

        self.assertEqual(0, result.exit_code)
        self.assertIn("Roll:        2d20kh1", result.output)
        self.assertIn("Calculation: 19", result.output)
        self.assertIn("Result:      19", result.output)
        self.assertNotIn("🎲", result.output)
        self.assertNotIn("\x1b[", result.output)

    @patch("dming.dice.random")
    def test_rich_filters_stay_with_their_dice_groups(self, mock_random):
        mock_random.randint.side_effect = [5, 7, 5, 7, 13, 10, 5, 9]

        result = CliRunner().invoke(
            roll_command,
            ["--details", "1d6+1d8+4d20kh2+2d20kl1+15"],
        )

        self.assertEqual(0, result.exit_code)
        self.assertIn("4d20kh2: 5, 7, 13, 10 → 13, 10 (keep highest 2)", result.output)
        self.assertIn("2d20kl1: 5, 9 → 5 (keep lowest 1)", result.output)
        self.assertNotIn("Rule:", result.output)

    @patch("dming.dice.random")
    def test_plain_result_is_only_the_number(self, mock_random):
        mock_random.randint.return_value = 12

        result = CliRunner().invoke(roll_command, ["--plain", "d20"])

        self.assertEqual(0, result.exit_code)
        self.assertEqual("12\n", result.output)

    def test_verbose_short_option_is_replaced(self):
        result = CliRunner().invoke(roll_command, ["-v", "d20"])

        self.assertNotEqual(0, result.exit_code)
        self.assertIn("No such option '-v'", result.output)

    def test_no_color_option_is_removed(self):
        result = CliRunner().invoke(roll_command, ["--no-color", "d20"])

        self.assertNotEqual(0, result.exit_code)
        self.assertIn("No such option '--no-color'", result.output)

    @patch("dming.dice.random")
    def test_json_result_is_one_object(self, mock_random):
        mock_random.randint.return_value = 12

        result = CliRunner().invoke(roll_command, ["d20", "--format", "json"])

        self.assertEqual(0, result.exit_code)
        self.assertEqual({"expression": "d20", "result": 12}, json.loads(result.output))

    @patch("dming.dice.random")
    def test_detailed_csv_has_structured_groups(self, mock_random):
        mock_random.randint.side_effect = [19, 9]

        result = CliRunner().invoke(
            roll_command,
            ["2d20kh1", "--details", "--format", "csv"],
        )

        self.assertEqual(0, result.exit_code)
        row = next(csv.DictReader(io.StringIO(result.output)))
        self.assertEqual("19", row["result"])
        self.assertEqual("19", row["calculation"])
        groups = json.loads(row["groups"])
        self.assertEqual([19, 9], groups[0]["rolls"])
        self.assertEqual([0], groups[0]["selected_indices"])

    def test_invalid_roll_is_friendly(self):
        result = CliRunner().invoke(roll_command, ["d0", "--format", "json"])

        self.assertEqual(1, result.exit_code)
        self.assertIn("Invalid roll: die must have at least 1 side", result.output)
