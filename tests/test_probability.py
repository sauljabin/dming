import unittest
from unittest.mock import patch

from click.testing import CliRunner

from dming.cli import _table, dming
from dming.probability import (
    InvalidProbabilityError,
    parse_die,
    probability_rows,
    success_probability,
)


class TestProbability(unittest.TestCase):
    def test_parse_die_with_modifiers(self):
        self.assertEqual((20, 0), (parse_die("d20").sides, parse_die("d20").modifier))
        self.assertEqual((20, 5), (parse_die("d20+5").sides, parse_die("d20+5").modifier))
        self.assertEqual((20, -3), (parse_die("d20-3").sides, parse_die("d20-3").modifier))

    def test_reject_invalid_expressions(self):
        for expression in ("d0", "1d20", "2d20", "d20kh1", "d20+d6", "D20", "d20+x"):
            with self.subTest(expression=expression), self.assertRaises(InvalidProbabilityError):
                parse_die(expression)

    def test_known_d20_probabilities(self):
        spec = parse_die("d20")
        rows = {row.target: row for row in probability_rows(spec)}

        self._assert_probabilities(rows[1], (1.0, 1.0, 1.0))
        self._assert_probabilities(rows[10], (0.55, 0.7975, 0.3025))
        self._assert_probabilities(rows[20], (0.05, 0.0975, 0.0025))

    def test_modifier_probabilities_are_clamped(self):
        positive = parse_die("d20+5")
        negative = parse_die("d20-5")

        self.assertEqual(1.0, success_probability(positive, 1))
        self.assertEqual(0.05, success_probability(positive, 25))
        self.assertEqual(0.0, success_probability(positive, 26))
        self.assertEqual(0.05, success_probability(negative, 15))
        self.assertEqual(0.0, success_probability(negative, 20))

    def test_default_target_range_accounts_for_modifier(self):
        self.assertEqual(tuple(range(1, 26)), self._targets(probability_rows(parse_die("d20+5"))))
        self.assertEqual(tuple(range(1, 21)), self._targets(probability_rows(parse_die("d20-5"))))

    def test_target_range_can_be_overridden(self):
        rows = probability_rows(parse_die("d20"), min_target=5, max_target=7)

        self.assertEqual((5, 6, 7), self._targets(rows))

    def test_reject_invalid_target_range(self):
        with self.assertRaisesRegex(
            InvalidProbabilityError,
            "minimum target cannot exceed maximum target",
        ):
            probability_rows(parse_die("d20"), min_target=10, max_target=5)

    def _assert_probabilities(self, row, expected):
        actual = row.standard, row.advantage, row.disadvantage
        for actual_value, expected_value in zip(actual, expected, strict=True):
            self.assertAlmostEqual(expected_value, actual_value)

    @staticmethod
    def _targets(rows):
        return tuple(row.target for row in rows)


class TestProbabilityCli(unittest.TestCase):
    def test_table_renders_rich_probabilities(self):
        result = CliRunner().invoke(_table, ["d20", "--min-target", "10", "--max-target", "10"])

        self.assertEqual(0, result.exit_code)
        self.assertIn("🎲 Probability · d20", result.output)
        self.assertIn("Target", result.output)
        self.assertIn("Advantage", result.output)
        self.assertIn("Disadvantage", result.output)
        self.assertIn("55.00%", result.output)
        self.assertIn("79.75%", result.output)
        self.assertIn("30.25%", result.output)

    def test_table_uses_modified_expression_as_column(self):
        result = CliRunner().invoke(
            _table,
            ["d20+5", "--min-target", "25", "--max-target", "25"],
        )

        self.assertEqual(0, result.exit_code)
        self.assertIn("d20+5", result.output)
        self.assertIn("5.00%", result.output)
        self.assertIn("9.75%", result.output)
        self.assertIn("0.25%", result.output)

    def test_table_rejects_inverted_range(self):
        result = CliRunner().invoke(
            _table,
            ["d20", "--min-target", "10", "--max-target", "5"],
        )

        self.assertEqual(1, result.exit_code)
        self.assertIn("minimum target cannot exceed maximum target", result.output)

    def test_table_rejects_nonpositive_target_option(self):
        result = CliRunner().invoke(_table, ["d20", "--min-target", "0"])

        self.assertEqual(2, result.exit_code)
        self.assertIn("0 is not in the range x>=1", result.output)

    @patch("dming.dice.random")
    def test_grouped_roll_uses_existing_command(self, mock_random):
        mock_random.randint.return_value = 12

        result = CliRunner().invoke(dming, ["roll", "--plain", "d20"])

        self.assertEqual(0, result.exit_code)
        self.assertEqual("12\n", result.output)

    def test_group_exposes_table_and_roll(self):
        result = CliRunner().invoke(dming, ["--help"])

        self.assertEqual(0, result.exit_code)
        self.assertIn("roll", result.output)
        self.assertIn("table", result.output)
