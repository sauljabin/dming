# SPDX-License-Identifier: CC-BY-4.0
"""Reference data adapted from SRD 5.2.1.

DMing adds metric conversions, grid-square equivalents, Python data structures,
and CLI-oriented formatting to the source tables.
"""

ABILITY_MODIFIERS: tuple[tuple[str, int], ...] = (
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
)

DIFFICULTY_CLASSES: tuple[tuple[str, int], ...] = (
    ("Very Easy", 5),
    ("Easy", 10),
    ("Medium", 15),
    ("Hard", 20),
    ("Very Hard", 25),
    ("Nearly Impossible", 30),
)

PROFICIENCY_BONUSES: tuple[tuple[str, int], ...] = (
    ("Up to 4", 2),
    ("5–8", 3),
    ("9–12", 4),
    ("13–16", 5),
    ("17–20", 6),
    ("21–24", 7),
    ("25–28", 8),
    ("29–30", 9),
)

CREATURE_SIZES: tuple[tuple[str, str, str, str], ...] = (
    ("Tiny", "2½ by 2½", "0.76 by 0.76", "4 per square"),
    ("Small", "5 by 5", "1.52 by 1.52", "1 square"),
    ("Medium", "5 by 5", "1.52 by 1.52", "1 square"),
    ("Large", "10 by 10", "3.05 by 3.05", "4 squares (2 by 2)"),
    ("Huge", "15 by 15", "4.57 by 4.57", "9 squares (3 by 3)"),
    ("Gargantuan", "20 by 20", "6.10 by 6.10", "16 squares (4 by 4)"),
)

CARRYING_CAPACITIES: tuple[tuple[str, float, float], ...] = (
    ("Tiny", 7.5, 15),
    ("Small/Medium", 15, 30),
    ("Large", 30, 60),
    ("Huge", 60, 120),
    ("Gargantuan", 120, 240),
)

LEVEL_ADVANCEMENT: tuple[tuple[int, int, int], ...] = (
    (1, 0, 2),
    (2, 300, 2),
    (3, 900, 2),
    (4, 2_700, 2),
    (5, 6_500, 3),
    (6, 14_000, 3),
    (7, 23_000, 3),
    (8, 34_000, 3),
    (9, 48_000, 4),
    (10, 64_000, 4),
    (11, 85_000, 4),
    (12, 100_000, 4),
    (13, 120_000, 5),
    (14, 140_000, 5),
    (15, 165_000, 5),
    (16, 195_000, 5),
    (17, 225_000, 6),
    (18, 265_000, 6),
    (19, 305_000, 6),
    (20, 355_000, 6),
)
