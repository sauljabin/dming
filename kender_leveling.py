LEVELS = 20
START_LEVEL = 2

for i in range(START_LEVEL, LEVELS + 1):
    print(f"Level: {i}, inspiration: {sum(range(START_LEVEL, i + 1))}")
