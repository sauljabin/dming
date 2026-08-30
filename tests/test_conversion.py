import csv
import io
import json
import unittest

from click.testing import CliRunner

from dming.cli import dming
from dming.commands.convert import convert, feet, inches, miles, pounds
from dming.conversion import (
    DEFAULT_FEET,
    DEFAULT_INCHES,
    DEFAULT_MILES,
    DEFAULT_POUNDS,
    feet_to_meters,
    feet_to_squares,
    inches_to_meters,
    inches_to_squares,
    miles_to_kilometers,
    miles_to_squares,
    pounds_to_grams,
    pounds_to_kilograms,
    sorted_unique,
)


class TestConversions(unittest.TestCase):
    def test_exact_metric_conversions(self):
        self.assertEqual(0.0254, inches_to_meters(1))
        self.assertEqual(0.3048, feet_to_meters(1))
        self.assertEqual(1.609344, miles_to_kilometers(1))
        self.assertEqual(453.59237, pounds_to_grams(1))
        self.assertEqual(0.45359237, pounds_to_kilograms(1))

    def test_square_conversions(self):
        self.assertAlmostEqual(1 / 60, inches_to_squares(1))
        self.assertEqual(1, feet_to_squares(5))
        self.assertEqual(1056, miles_to_squares(1))

    def test_curated_defaults(self):
        self.assertEqual((1, 2, 3, 6, 12, 24, 36), DEFAULT_INCHES)
        self.assertEqual(
            (1, 2, 2.5, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 120),
            DEFAULT_FEET,
        )
        self.assertEqual((0.25, 0.5, 1, 2, 3, 5, 10), DEFAULT_MILES)
        self.assertEqual((1, 2, 5, 10, 15, 20, 25, 50, 75, 100, 150, 200), DEFAULT_POUNDS)

    def test_custom_values_are_sorted_and_deduplicated(self):
        self.assertEqual((2.5, 5, 30), sorted_unique((30, 5, 2.5, 5)))


class TestConversionCli(unittest.TestCase):
    def test_convert_group_exposes_unit_commands(self):
        result = CliRunner().invoke(convert, ["--help"])

        self.assertEqual(0, result.exit_code)
        for command in ("inches", "feet", "miles", "pounds"):
            with self.subTest(command=command):
                self.assertIn(command, result.output)
        self.assertNotIn("distance", convert.commands)
        self.assertNotIn("weight", convert.commands)

    def test_unit_defaults_render_one_table_each(self):
        expected = (
            (inches, "📏 Inches to Meters", "(in.)"),
            (feet, "📏 Feet to Meters", "(ft.)"),
            (miles, "📏 Miles to Kilometers", "(mi.)"),
            (pounds, "⚖️ Pounds to Kilograms", "(lb.)"),
        )
        for command, title, unit in expected:
            with self.subTest(command=command.name):
                result = CliRunner().invoke(command)
                self.assertEqual(0, result.exit_code)
                self.assertIn(title, result.output)
                self.assertIn(unit, result.output)

    def test_all_conversion_tables_have_the_same_width(self):
        borders = []
        for command in (inches, feet, miles, pounds):
            result = CliRunner().invoke(command)
            borders.append(
                next(line for line in result.output.splitlines() if line.startswith("┏"))
            )

        self.assertEqual(1, len({len(border) for border in borders}))

    def test_custom_values_are_positional_sorted_and_deduplicated(self):
        result = CliRunner().invoke(feet, ["30", "5", "5"])

        self.assertEqual(0, result.exit_code)
        self.assertIn("1.52", result.output)
        self.assertIn("9.14", result.output)
        self.assertEqual(1, result.output.count("1.52"))

    def test_pounds_render_kilograms_without_grams(self):
        result = CliRunner().invoke(pounds, ["2.5"])

        self.assertEqual(0, result.exit_code)
        self.assertIn("1.13", result.output)
        self.assertNotIn("Grams", result.output)

    def test_rejects_nonpositive_values(self):
        for command in (inches, feet, miles, pounds):
            with self.subTest(command=command.name):
                result = CliRunner().invoke(command, ["0"])
                self.assertEqual(2, result.exit_code)
                self.assertIn("0 is not in the range x>0", result.output)

    def test_json_preserves_unrounded_numbers(self):
        result = CliRunner().invoke(feet, ["5", "--format", "json"])

        self.assertEqual(0, result.exit_code)
        self.assertEqual(
            [{"feet": 5.0, "meters": 1.524, "squares": 1.0}],
            json.loads(result.output),
        )

    def test_csv_has_semantic_headers(self):
        result = CliRunner().invoke(miles, ["1", "--format", "csv"])

        self.assertEqual(0, result.exit_code)
        rows = list(csv.DictReader(io.StringIO(result.output)))
        self.assertEqual(["miles", "kilometers", "squares"], list(rows[0]))
        self.assertEqual("1.609344", rows[0]["kilometers"])

    def test_removed_commands_are_unknown(self):
        for command in ("distance", "weight"):
            with self.subTest(command=command):
                result = CliRunner().invoke(dming, ["convert", command])
                self.assertEqual(2, result.exit_code)
                self.assertIn(f"No such command '{command}'", result.output)
