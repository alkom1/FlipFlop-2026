from typing import Dict, List, Tuple


with open("12.in.txt") as file:
	INPUT = [x.strip() for x in file]
numberOf2DCards = len(INPUT) // 2
numberOf3DCards = numberOf2DCards // 5
CALLED_NUMBERS: List[int] = [int(x) for x in " ".join(INPUT[:numberOf2DCards]).split(" ")]
CARDS: List[List[List[List[int]]]] = [[[[0]*5 for _ in range(5)] for _ in range(5)] for _ in range(numberOf3DCards)]
positionOfNumber: Dict[int, Tuple[int, int, int, int]] = {}
BINGOS_PER_CARD = [0] * numberOf3DCards
MARKED = -1

args = [iter(INPUT[numberOf2DCards + 1:])] * 5
for c, lines in enumerate(zip(*args, strict=True)):
	numbers = [int(x) for x in " ".join(lines).split(" ")]
	for i, n in enumerate(numbers):
		x = i % 5
		y = (i // 5) % 5
		z = i // 25
		CARDS[c][x][y][z] = n
		positionOfNumber[n] = (c, x, y, z)

DIRECTIONS = [
	(1, 0, 0),
	(0, 1, 0),
	(0, 0, 1),

	(1, 1, 0),
	(1, -1, 0),
	(1, 0, 1),
	(1, 0, -1),
	(0, 1, 1),
	(0, 1, -1),

	(1, 1, 1),
	(1, 1, -1),
	(1, -1, 1),
	(1, -1, -1),
]

def recalculate3Dcard(c: int):
	card = CARDS[c]
	total = 0
	for x in range(5):
		for y in range(5):
			for z in range(5):
				for dx, dy, dz in DIRECTIONS:
					end_x = x + dx * 4
					end_y = y + dy * 4
					end_z = z + dz * 4
					
					if not (
						0 <= end_x < 5 and
						0 <= end_y < 5 and
						0 <= end_z < 5
					):
						continue
					bingo = True
					for i in range(5):
						if card[x + dx * i][y + dy * i][z + dz * i] != MARKED:
							bingo = False
							break
					if bingo:
						total += 1
	BINGOS_PER_CARD[c] = total


for i, n in enumerate(CALLED_NUMBERS):
	c, x, y, z = positionOfNumber[n]
	CARDS[c][x][y][z] = MARKED
	recalculate3Dcard(c)

	if sum(BINGOS_PER_CARD) >= 5:
		break

print("part 2", n)