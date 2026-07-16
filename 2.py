FILE = "2.in.txt"
with open(FILE, "rt") as file:
	INPUT = file.read().strip()

# PART 1
wall = [0] * 100
position = 0
for s in INPUT:
	position += 1 if s == ">" else -1
	position = position % 100
	wall[position] += 1
highest_index = max(range(len(wall)), key=wall.__getitem__)
output = (highest_index + 1) * wall[highest_index]
print(f"part 1: {output}")

# PART 2
hits = 0
robot_position = 0
wall_position = 0
for r, w in zip(INPUT, INPUT[::-1]):
	robot_position = (robot_position + (1 if r == ">" else -1)) % 100
	wall_position = (wall_position + (1 if w == ">" else -1)) % 100
	if robot_position == wall_position:
		hits += 1
print(f"part 2: {hits}")

# PART 3
wall = [0] * 100
robot_position = 0
for r1, r2 in zip(INPUT, INPUT[::-1]):
	robot_position = (robot_position + (1 if r1 == ">" else -1) + (1 if r2 == "<" else -1)) % 100
	wall[robot_position] += 1
highest_index, highest_value = max(enumerate(wall), key=lambda x: x[1])
output = (highest_index + 1) * highest_value
print(f"part 3: {output}")