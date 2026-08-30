import csv
import io
import json
import unittest

from click.testing import CliRunner

from dming.cli import dming
from dming.commands.rules import (
    abilities,
    advancement,
    carrying,
    difficulty,
    proficiency,
    rules,
    sizes,
)
from dming.rules import (
    ABILITY_MODIFIERS,
    CARRYING_CAPACITIES,
    CREATURE_SIZES,
    DIFFICULTY_CLASSES,
    LEVEL_ADVANCEMENT,
    PROFICIENCY_BONUSES,
)


class TestRulesData(unittest.TestCase):
    def test_srd_ability_modifiers(self):
        self.assertEqual(
            (
                ("1", -5),
                ("2–3", -4),
                ("4–5", -3),
                ("6–7", -2),
                ("8–9", -1),
                ("10–11", 0),
                ("12–13", 1),
                ("14–15", 2),
                ("16–17", 3),
                ("18–19", 4),
                ("20–21", 5),
                ("22–23", 6),
                ("24–25", 7),
                ("26–27", 8),
                ("28–29", 9),
                ("30", 10),
            ),
            ABILITY_MODIFIERS,
        )

    def test_srd_difficulty_classes(self):
        self.assertEqual(
            (
                ("Very Easy", 5),
                ("Easy", 10),
                ("Medium", 15),
                ("Hard", 20),
                ("Very Hard", 25),
                ("Nearly Impossible", 30),
            ),
            DIFFICULTY_CLASSES,
        )

    def test_srd_proficiency_bonuses(self):
        self.assertEqual(
            (
                ("Up to 4", 2),
                ("5–8", 3),
                ("9–12", 4),
                ("13–16", 5),
                ("17–20", 6),
                ("21–24", 7),
                ("25–28", 8),
                ("29–30", 9),
            ),
            PROFICIENCY_BONUSES,
        )

    def test_srd_creature_sizes(self):
        self.assertEqual(
            (
                ("Tiny", "2½ by 2½", "0.76 by 0.76", "4 per square"),
                ("Small", "5 by 5", "1.52 by 1.52", "1 square"),
                ("Medium", "5 by 5", "1.52 by 1.52", "1 square"),
                ("Large", "10 by 10", "3.05 by 3.05", "4 squares (2 by 2)"),
                ("Huge", "15 by 15", "4.57 by 4.57", "9 squares (3 by 3)"),
                ("Gargantuan", "20 by 20", "6.10 by 6.10", "16 squares (4 by 4)"),
            ),
            CREATURE_SIZES,
        )

    def test_srd_carrying_capacities(self):
        self.assertEqual(
            (
                ("Tiny", 7.5, 15),
                ("Small/Medium", 15, 30),
                ("Large", 30, 60),
                ("Huge", 60, 120),
                ("Gargantuan", 120, 240),
            ),
            CARRYING_CAPACITIES,
        )

    def test_srd_character_advancement(self):
        self.assertEqual(20, len(LEVEL_ADVANCEMENT))
        self.assertEqual((1, 0, 2), LEVEL_ADVANCEMENT[0])
        self.assertEqual((5, 6_500, 3), LEVEL_ADVANCEMENT[4])
        self.assertEqual((11, 85_000, 4), LEVEL_ADVANCEMENT[10])
        self.assertEqual((17, 225_000, 6), LEVEL_ADVANCEMENT[16])
        self.assertEqual((20, 355_000, 6), LEVEL_ADVANCEMENT[-1])


class TestRulesCli(unittest.TestCase):
    def test_rules_without_subcommand_shows_help(self):
        result = CliRunner().invoke(rules)

        self.assertEqual(0, result.exit_code)
        self.assertIn("Usage:", result.output)
        self.assertEqual(
            {"abilities", "advancement", "carrying", "difficulty", "proficiency", "sizes"},
            set(rules.commands),
        )

    def test_abilities_table(self):
        result = CliRunner().invoke(abilities)

        self.assertEqual(0, result.exit_code)
        self.assertIn("📖 Ability Modifiers · SRD 5.2.1", result.output)
        self.assertIn("2–3", result.output)
        self.assertIn("−5", result.output)
        self.assertIn("+10", result.output)

    def test_difficulty_table(self):
        result = CliRunner().invoke(difficulty)

        self.assertEqual(0, result.exit_code)
        self.assertIn("📖 Typical Difficulty Classes · SRD 5.2.1", result.output)
        self.assertIn("Very Easy", result.output)
        self.assertIn("Nearly Impossible", result.output)
        self.assertIn("30", result.output)

    def test_proficiency_table(self):
        result = CliRunner().invoke(proficiency)

        self.assertEqual(0, result.exit_code)
        self.assertIn("📖 Proficiency Bonus · SRD 5.2.1", result.output)
        self.assertIn("Level or CR", result.output)
        self.assertIn("Up to 4", result.output)
        self.assertIn("29–30", result.output)
        self.assertIn("+9", result.output)

    def test_sizes_table(self):
        result = CliRunner().invoke(sizes)

        self.assertEqual(0, result.exit_code)
        self.assertIn("📖 Creature Size and Space · SRD 5.2.1", result.output)
        self.assertIn("Space (ft.)", result.output)
        self.assertIn("Space (m.)", result.output)
        self.assertIn("2½ by 2½", result.output)
        self.assertIn("0.76 by 0.76", result.output)
        self.assertIn("6.10 by 6.10", result.output)
        self.assertIn("4 per square", result.output)
        self.assertIn("16 squares (4 by 4)", result.output)

    def test_carrying_table(self):
        result = CliRunner().invoke(carrying)

        self.assertEqual(0, result.exit_code)
        self.assertIn("📖 Carrying Capacity · SRD 5.2.1", result.output)
        self.assertIn("Creature Size", result.output)
        self.assertIn("Drag/Lift/Push", result.output)
        self.assertIn("Small/Medium", result.output)
        self.assertIn("Str. × 7.5", result.output)
        self.assertIn("Str. × 3.40", result.output)
        self.assertIn("Str. × 240", result.output)
        self.assertIn("Str. × 108.86", result.output)
        self.assertIn("(lb.)", result.output)
        self.assertIn("(kg.)", result.output)

    def test_root_group_exposes_rules_and_existing_commands(self):
        result = CliRunner().invoke(dming, ["--help"])

        self.assertEqual(0, result.exit_code)
        for command in ("chance", "convert", "roll", "rules"):
            with self.subTest(command=command):
                self.assertIn(command, result.output)

    def test_advancement_rich_table(self):
        result = CliRunner().invoke(advancement)

        self.assertEqual(0, result.exit_code)
        self.assertIn("📖 Character Advancement · SRD 5.2.1", result.output)
        self.assertIn("Experience Points", result.output)
        self.assertIn("355000", result.output.replace(",", ""))
        self.assertIn("+6", result.output)

    def test_advancement_json_has_native_numbers(self):
        result = CliRunner().invoke(advancement, ["--format", "json"])

        self.assertEqual(0, result.exit_code)
        rows = json.loads(result.output)
        self.assertEqual(20, len(rows))
        self.assertEqual(
            {"level": 20, "experience_points": 355_000, "proficiency_bonus": 6},
            rows[-1],
        )

    def test_rules_csv_uses_semantic_headers(self):
        result = CliRunner().invoke(carrying, ["--format", "csv"])

        self.assertEqual(0, result.exit_code)
        row = next(csv.DictReader(io.StringIO(result.output)))
        self.assertIn("carry_kilograms_multiplier", row)
        self.assertEqual("3.401942775", row["carry_kilograms_multiplier"])
