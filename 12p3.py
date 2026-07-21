from typing import Dict, List, Tuple

with open("12.in.txt") as file:
	INPUT = [x.strip() for x in file]
numberOf2DCards = len(INPUT) // 2
CALLED_NUMBERS: List[int] = [int(x) for x in " ".join(INPUT[:numberOf2DCards]).split(" ")]
CARD: List[List[List[List[int]]]] = [[[[0]*5 for _ in range(5)] for _ in range(5)] for _ in range(5)]
positionOfNumber: Dict[int, Tuple[int, int, int, int]] = {}
MARKED = -1

for i, n in enumerate(int(x) for x in " ".join(INPUT[numberOf2DCards + 1:]).split(" ")):
	x = i % 5
	y = (i // 5) % 5
	z = (i // 25) % 5
	w = (i // 125)
	CARD[x][y][z][w] = n
	positionOfNumber[n] = (x, y, z, w)

DIRECTIONS = []
for da in (-1, 0, 1):
	for db in (-1, 0, 1):
		for dc in (-1, 0, 1):
			for dd in (-1, 0, 1):
				if (da, db, dc, dd) == (0, 0, 0, 0):
					continue
				for x in (da, db, dc, dd):
					if x != 0:
						if x > 0:
							DIRECTIONS += [(da, db, dc, dd)]
						break


# optimization here would be to only check the hyper-rows
# that include the marked number but...
# checking full hypercube each time is still fast enough *shrugs*
def countBingos():
	total = 0
	for x in range(5):
		for y in range(5):
			for z in range(5):
				for w in range(5):
					for dx, dy, dz, dw in DIRECTIONS:
						end_x = x + dx * 4
						end_y = y + dy * 4
						end_z = z + dz * 4
						end_w = w + dw * 4
						
						if not (
							0 <= end_x < 5 and
							0 <= end_y < 5 and
							0 <= end_z < 5 and
							0 <= end_w < 5
						):
							continue
						bingo = True
						for i in range(5):
							if CARD[x + dx * i][y + dy * i][z + dz * i][w + dw * i] != MARKED:
								bingo = False
								break
						if bingo:
							total += 1
	return total


for i, n in enumerate(CALLED_NUMBERS):
	x, y, z, w = positionOfNumber[n]
	CARD[x][y][z][w] = MARKED

	if countBingos() >= 5:
		break

print("part 3", n)