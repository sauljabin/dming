import unittest

from click.testing import CliRunner

from dming.cli import _convert, _distance, _weight
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
    def test_convert_group_exposes_distance_and_weight(self):
        result = CliRunner().invoke(_convert, ["--help"])

        self.assertEqual(0, result.exit_code)
        self.assertIn("distance", result.output)
        self.assertIn("weight", result.output)

    def test_distance_defaults_render_three_tables(self):
        result = CliRunner().invoke(_distance)

        self.assertEqual(0, result.exit_code)
        self.assertIn("📏 Inches to Meters", result.output)
        self.assertIn("📏 Feet to Meters", result.output)
        self.assertIn("📏 Miles to Kilometers", result.output)
        self.assertIn("Squares", result.output)

    def test_all_conversion_tables_have_the_same_width(self):
        distance = CliRunner().invoke(_distance)
        weight = CliRunner().invoke(_weight)

        distance_borders = [line for line in distance.output.splitlines() if line.startswith("┏")]
        weight_border = next(line for line in weight.output.splitlines() if line.startswith("┏"))

        self.assertEqual(3, len(distance_borders))
        self.assertEqual({len(weight_border)}, {len(line) for line in distance_borders})

    def test_custom_distance_renders_only_requested_units(self):
        result = CliRunner().invoke(_distance, ["--foot", "30", "--foot", "5"])

        self.assertEqual(0, result.exit_code)
        self.assertIn("📏 Feet to Meters", result.output)
        self.assertIn("1.52", result.output)
        self.assertIn("1.00", result.output)
        self.assertNotIn("Inches to Meters", result.output)
        self.assertNotIn("Miles to Kilometers", result.output)

    def test_weight_defaults_render_metric_columns(self):
        result = CliRunner().invoke(_weight)

        self.assertEqual(0, result.exit_code)
        self.assertIn("⚖️ Pounds to Metric", result.output)
        self.assertIn("Grams", result.output)
        self.assertIn("Kilograms", result.output)
        self.assertIn("453.59", result.output)
        self.assertIn("0.45", result.output)

    def test_custom_weight_values_are_rendered(self):
        result = CliRunner().invoke(_weight, ["--pound", "2.5"])

        self.assertEqual(0, result.exit_code)
        self.assertIn("2.5", result.output)
        self.assertIn("1133.98", result.output)
        self.assertIn("1.13", result.output)

    def test_rejects_nonpositive_custom_values(self):
        for command, option in ((_distance, "--foot"), (_weight, "--pound")):
            with self.subTest(option=option):
                result = CliRunner().invoke(command, [option, "0"])

                self.assertEqual(2, result.exit_code)
                self.assertIn("0 is not in the range x>0", result.output)
