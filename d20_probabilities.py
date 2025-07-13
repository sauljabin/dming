D20 = 20


def probability(target):
    return (D20 + 1 - target) / D20


def advantage(target):
    return 1 - (1 - probability(target)) ** 2


def disadvantage(target):
    return probability(target) ** 2


for face in range(1, D20 + 1):
    print(
        f"target: {face}, d20: {probability(face) * 100:.2f}%, advantage: {advantage(face) * 100:.2f}%, disadvantage: {disadvantage(face) * 100:.2f}%")
