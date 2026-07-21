# input file:
# each 3-line segment is separate test case
#
# [4spaces][id][4spaces][2spaces]
# [id][2spaces][source id][2spaces][id][2spaces]
# [empty line]

# mutation rules:
# sprouts mutate only into sprouts
# stems replace mutated sprouts
# stems are never replaced
# if you two sprouts compete for same position
#  higher id wins

# NOTE: quality wise this is definitely
# the worst script of this repo
# you have been warned, I don't wanna hear any complaints

from typing import Dict, List, Set, Tuple
Point = Tuple[int, int]
Ruleset = Dict[int, Tuple[int, int, int]]

with open("11.in.txt", "rt") as file:
	INPUT = file.readlines()
	TESTCASES = [INPUT[3*k:3*k+2] for k in range(len(INPUT) // 3 + 1)]
	TESTCASES = [[y.replace("XX", "-1") for y in x] for x in TESTCASES]
	RULES = [[line[12*k:12*k+10] for k in range(len(t[1]) // 12 + 1) for line in t] for t in TESTCASES]
	PARSED = [dict((int(r[2*k+1][4:6]), (int(r[2*k+1][0:2]), int(r[2*k][4:6]), int(r[2*k+1][8:10]))) for k in range(len(r) // 2)) for r in RULES]
	# key = int(r[2*k+1][4:6])
	# TOP: int(r[2*k][4:6])
	# LEFT: int(r[2*k+1][0:2])
	# RIGHT: int(r[2*k+1][8:10])
WIDTH = 600 + len(PARSED) * 10
HEIGHT = 110

AIR = -9
STEM = -1
def execute(rules: List[Ruleset]):
	grid: List[List[int]] = [[AIR] * HEIGHT for _ in range(WIDTH)]
	for i in range(len(rules)):
		grid[305 + i * 10][0] = i * 100
	sprouts: List[Set[Point]] = [{(305 + i * 10, 0)} for i in range(len(rules))]
	active_stems: List[Set[Point]] = [set() for _ in range(len(rules))]
	all_objects: List[Set[Point]] = [{(305 + i * 10, 0)} for i in range(len(rules))]
	year = 0

	while year < 100 and sum(len(x) for x in sprouts) > 0:
		year += 1
		for i in range(len(rules)):
			grid, sprouts[i], active_stems[i], all_objects[i] = evolve(rules[i], grid, sprouts[i], active_stems[i], all_objects[i], i * 100)
		for i in range(len(rules)):
			required_energy = len(all_objects[i]) * 3
			produced_energy, active_stems[i] = producing_energy(grid, active_stems[i])
			if year >= 5 and required_energy > produced_energy:
				sprouts[i].clear()
				active_stems[i].clear()
			# draw_tree(grid, f"{year=}", f"{produced_energy}/{required_energy}")
		# draw_tree(grid, f"{year=}", "")
		# input()
	return sum(len(x) for x in all_objects)

def execute_offspring_wars(original_rules: List[Ruleset]):
	# FIRST TIME AROUND
	rules = original_rules.copy()
	grid: List[List[int]] = [[AIR] * HEIGHT for _ in range(WIDTH)]
	for i in range(len(rules)):
		grid[305 + i * 10][0] = i * 100
	sprouts: List[Set[Point]] = [{(305 + i * 10, 0)} for i in range(len(rules))]
	active_stems: List[Set[Point]] = [set() for _ in range(len(rules))]
	all_objects: List[Set[Point]] = [{(305 + i * 10, 0)} for i in range(len(rules))]

	def dogeneration():
		nonlocal grid, rules, sprouts, active_stems, all_objects
		year = 0
		while year < 100 and sum(len(x) for x in sprouts) > 0:
			year += 1
			for i in range(len(rules)):
				grid, sprouts[i], active_stems[i], all_objects[i] = evolve(rules[i], grid, sprouts[i], active_stems[i], all_objects[i], i * 100)
			for i in range(len(rules)):
				required_energy = len(all_objects[i]) * 3
				produced_energy, active_stems[i] = producing_energy(grid, active_stems[i])
				if year >= 5 and required_energy > produced_energy:
					sprouts[i].clear()
					active_stems[i].clear()
				# draw_tree(grid, f"{year=}", f"{produced_energy}/{required_energy}")
			# draw_tree(grid, f"{year=}", "")
			# input()

	def intermission():
		nonlocal grid, rules, sprouts, active_stems, all_objects
		for x in range(WIDTH):
			target = AIR
			for y in range(HEIGHT):
				v = grid[x][y]
				grid[x][y] = AIR
				if v >= 0:
					target = (v // 100) * 100
			grid[x][0] = target
		# draw_tree(grid, "intermission 1")
		new_rules: List[Ruleset] = []
		sprouts = []
		all_objects = []
		for x in range(WIDTH):
			v = grid[x][0]
			if v == AIR:
				continue
			i = v // 100
			grid[x][0] = len(new_rules) * 100
			new_rules += [rules[i]]
			sprouts += [{(x, 0)}]
			all_objects += [{(x, 0)}]
		# all_objects
		rules = new_rules
		active_stems = [set() for _ in range(len(rules))]
	
	dogeneration()
	intermission()
	dogeneration()
	intermission()
	dogeneration()

	# draw_tree(grid, "end")

	return sum(len(x) for x in all_objects)

def producing_energy(grid: List[List[int]], stems: Set[Point]):
	total = 0
	new_stems = stems.copy()
	for x, y in stems:
		height = min(y + 1, 10)
		multi = 3
		scan_y = y + 1
		while multi > 0 and scan_y < HEIGHT:
			if grid[x][scan_y] == STEM:
				multi -= 1
			scan_y += 1
		if multi == 0:
			new_stems.remove((x, y))
			continue
		total += height * multi
	return total, new_stems

def evolve(rules: Ruleset, grid: List[List[int]], sprouts: Set[Point], active_stems: Set[Point], all_objects: Set[Point], offset: int):
	def isStem(v: int):
		return v != AIR and (v < offset or v >= (offset + 100))
	new_grid = [list(x) for x in grid]
	new_sprouts: Set[Point] = set()
	for x, y in sprouts:
		new_grid[x][y] = STEM
		active_stems.add((x, y))
	for x, y in sprouts:
		left = rules[grid[x][y] - offset][0]
		top = rules[grid[x][y] - offset][1]
		right = rules[grid[x][y] - offset][2]
		if left >= 0 and not isStem(new_grid[x-1][y]) and left > new_grid[x-1][y] - offset:
			new_grid[x-1][y] = left + offset
			new_sprouts.add((x-1, y))
			all_objects.add((x-1, y))
		if top >= 0 and not isStem(new_grid[x][y+1]) and top > new_grid[x][y+1] - offset:
			new_grid[x][y+1] = top + offset
			new_sprouts.add((x, y+1))
			all_objects.add((x, y+1))
		if right >= 0 and not isStem(new_grid[x+1][y]) and right > new_grid[x+1][y] - offset:
			new_grid[x+1][y] = right + offset
			new_sprouts.add((x+1, y))
			all_objects.add((x+1, y))
	return new_grid, new_sprouts, active_stems, all_objects

def draw_tree(grid: List[List[int]], pre: str = "", post=""):
	left, right, top, bottom = WIDTH, 0, 0, HEIGHT
	for x, col in enumerate(grid):
		for y, i in enumerate(col):
			if i == AIR:
				continue
			if left > x:
				left = x
			if right < x:
				right = x
			if top < y:
				top = y
			if bottom > y:
				bottom = y
	print("-" * (right - left + 1), pre)
	for y in range(bottom, top + 1)[::-1]:
		for x in range(left, right + 1):
			i = grid[x][y]
			if i == AIR:
				print(".", end="")
			elif i == STEM:
				print("#", end="")
			elif i >= 0:
				print("@", end="")
			else:
				print("what is this?", i)
		print("")
	print("-" * (right - left + 1), post)

print("part 1", sum(execute([r]) for r in PARSED))
print("part 2", execute(PARSED))
print("part 3", execute_offspring_wars(PARSED))