from typing import Dict, List, Tuple


with open("12.in.txt") as file:
	INPUT = [x.strip() for x in file]
numberOfCards = len(INPUT) // 2
CALLED_NUMBERS: List[int] = [int(x) for x in " ".join(INPUT[:numberOfCards]).split(" ")]
CARDS: List[List[List[int]]] = [[[0]*5 for _ in range(5)] for _ in range(numberOfCards)]
positionOfNumber: Dict[int, Tuple[int, int, int]] = {}
BINGOS_PER_CARD = [0] * numberOfCards
MARKED = -1

for c, line in enumerate(INPUT[numberOfCards + 1:]):
	numbers = [int(x) for x in line.split(" ")]
	for i, n in enumerate(numbers):
		x = i % 5
		y = i // 5
		CARDS[c][x][y] = n
		positionOfNumber[n] = (c, x, y)
assert len(positionOfNumber.keys()) == numberOfCards * 25

def recalculateCard(c: int) -> int:
	card = CARDS[c]
	total = 0
	for y in range(5):
		if card[0][y] == card[1][y] == card[2][y] == card[3][y] == card[4][y] == MARKED:
			total += 1
	for x in range(5):
		if card[x][0] == card[x][1] == card[x][2] == card[x][3] == card[x][4] == MARKED:
			total += 1
	if card[0][0] == card[1][1] == card[2][2] == card[3][3] == card[4][4] == MARKED:
		total += 1
	if card[4][0] == card[3][1] == card[2][2] == card[1][3] == card[0][4] == MARKED:
		total += 1
	BINGOS_PER_CARD[c] = total
	return total

for i, n in enumerate(CALLED_NUMBERS):
	c, x, y = positionOfNumber[n]
	CARDS[c][x][y] = MARKED
	recalculateCard(c)

	if sum(BINGOS_PER_CARD) >= 5:
		break

print("part 1", n)