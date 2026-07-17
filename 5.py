from typing import List, Set, Tuple

with open("5.in.txt", "rt") as file:
	INPUT = [[y for y in x.strip()] for x in file.readlines()]

def deepcopy(src: List[List[str]]) -> List[List[str]]:
	return [list(y) for y in src]

# PART 1
def score1(map: List[List[str]]) -> Set[Tuple[int, int]]:
	seen = set()
	x, y = 0, 0
	while (x, y) not in seen:
		seen.add((x, y))
		c = map[y][x]
		if c == ">":
			x += 1
		elif c == "<":
			x -= 1
		elif c == "^":
			y -= 1
		elif c == "v":
			y += 1
	return seen
print(f"part 1: {len(score1(INPUT))}")

# PART 2
def variations(traveled: Set[Tuple[int, int]]):
	for x, y in traveled:
		if x <= 0 or y <= 0 or x >= len(INPUT[0])-1 or y >= len(INPUT)-1:
			continue
		for c in (">", "<", "v", "^"):
			if INPUT[y][x] == c:
				continue
			clone = deepcopy(INPUT)
			clone[y][x] = c
			yield clone
result = max(((m, len(score1(m))) for m in variations(score1(INPUT))), key=lambda x: x[1])[1]
print(f"part 2: {result}")

TURN_MAP = {
	False: {
		">": ">",
		"<": "<",
		"^": "^",
		"v": "v"
	},
	True: {
		">": "v",
		"<": "^",
		"^": ">",
		"v": "<"
	}
}

# PART 3
def score3(map: List[List[str]]) -> Set[Tuple[int, int]]:
	seen = set()
	x, y = 0, 0
	illegal = 3
	while True:
		been_here = (x, y) in seen
		if been_here:
			if illegal == 0:
				break
			illegal -= 1
		seen.add((x, y))
		c = TURN_MAP[been_here][map[y][x]]
		if c == ">":
			x += 1
		elif c == "<":
			x -= 1
		elif c == "^":
			y -= 1
		elif c == "v":
			y += 1
	return seen
result = max(((m, len(score3(m))) for m in variations(score3(INPUT))), key=lambda x: x[1])[1]
print(f"part 3: {result}")