import csv
import io
import json
import unittest
from unittest.mock import patch

from click.testing import CliRunner

from dming.cli import dming


class TestOutputFormats(unittest.TestCase):
    def test_every_table_command_supports_every_format(self):
        commands = (
            ("chance", "d20", "--min-target", "10", "--max-target", "10"),
            ("convert", "inches", "1"),
            ("convert", "feet", "5"),
            ("convert", "miles", "1"),
            ("convert", "pounds", "1"),
            ("rules", "abilities"),
            ("rules", "advancement"),
            ("rules", "carrying"),
            ("rules", "difficulty"),
            ("rules", "proficiency"),
            ("rules", "sizes"),
        )
        for command in commands:
            for output_format in ("rich", "plain", "json", "csv"):
                with self.subTest(command=command, output_format=output_format):
                    result = CliRunner().invoke(
                        dming,
                        [*command, "--format", output_format],
                    )
                    self.assertEqual(0, result.exit_code)
                    self.assertTrue(result.output)
                    if output_format == "json":
                        self.assertIsInstance(json.loads(result.output), list)
                    elif output_format == "csv":
                        self.assertTrue(list(csv.DictReader(io.StringIO(result.output))))

    def test_global_json_format_is_inherited(self):
        result = CliRunner().invoke(
            dming,
            ["--format", "json", "chance", "d20", "--min-target", "10", "--max-target", "10"],
        )

        self.assertEqual(0, result.exit_code)
        self.assertEqual(
            [
                {
                    "target": 10,
                    "roll_needed": 10,
                    "standard": 0.55,
                    "advantage": 0.7975000000000001,
                    "disadvantage": 0.30250000000000005,
                }
            ],
            json.loads(result.output),
        )

    def test_leaf_format_overrides_global_format(self):
        result = CliRunner().invoke(
            dming,
            [
                "--format",
                "json",
                "chance",
                "d20",
                "--min-target",
                "10",
                "--max-target",
                "10",
                "--format",
                "csv",
            ],
        )

        self.assertEqual(0, result.exit_code)
        row = next(csv.DictReader(io.StringIO(result.output)))
        self.assertEqual("10", row["target"])
        self.assertEqual("0.55", row["standard"])

    def test_plain_tables_are_tab_delimited_without_styling(self):
        result = CliRunner().invoke(
            dming,
            ["rules", "advancement", "--format", "plain"],
        )

        self.assertEqual(0, result.exit_code)
        self.assertTrue(result.output.startswith("Level\tExperience Points\tProficiency Bonus\n"))
        self.assertNotIn("📖", result.output)
        self.assertNotIn("\x1b[", result.output)

    @patch("dming.dice.random")
    def test_roll_leaf_csv_overrides_global_json(self, mock_random):
        mock_random.randint.return_value = 7

        result = CliRunner().invoke(
            dming,
            ["--format", "json", "roll", "d20", "--format", "csv"],
        )

        self.assertEqual(0, result.exit_code)
        self.assertEqual(
            [{"expression": "d20", "result": "7"}],
            list(csv.DictReader(io.StringIO(result.output))),
        )

    def test_plain_alias_rejects_nonplain_format(self):
        result = CliRunner().invoke(
            dming,
            ["--format", "json", "roll", "--plain", "d20"],
        )

        self.assertEqual(2, result.exit_code)
        self.assertIn("--plain cannot be combined with a non-plain --format", result.output)
