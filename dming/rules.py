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
