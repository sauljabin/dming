feet = [1, 2, 2.5, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 120]

for f in feet:
    result = f * 0.3048
    print(f"Feet: {f}, convertion to meters: {round(result, 2)}")
