from typing import Dict


with open("8.in.txt", "tr") as file:
	INPUT = file.readlines()

# PART 1
rules1: Dict[str, str] = {}
for line in (x.strip().split(' ') for x in INPUT):
	src, targets = line[0], "".join(line[1:])
	if src in rules1:
		continue
	rules1[src] = targets
population = "AB"
for i in range(7):
	new_population = ""
	for l in population:
		new_population += rules1[l]
	population = new_population
print(f"part 1: {len(population)}")

# PART 2
rules2: Dict[str, str] = {}
for line in ("".join(x.strip().split(' ')) for x in INPUT):
	src, targets = line[:2], line[2:]
	if src in rules2:
		continue
	rules2[src] = rules2[src[::-1]] = targets
population = "AB"
for i in range(7):
	new_population = ""
	for l1, l2 in zip(population[:-1], population[1:]):
		new_population += l1 + rules2[f"{l1}{l2}"]
	new_population += l2
	population = new_population
print(f"part 2: {len(population)}")

# PART 3 - pair counting
rules3: Dict[str, Dict[str, int]] = {}
for line in ("".join(x.strip().split(' ')) for x in INPUT):
	def add_new_rule(src, targets):
		if src in rules3:
			return
		newpairs = {}
		for l1, l2 in zip(targets[:-1], targets[1:]):
			k = f"{l1}{l2}"
			newpairs[k] = newpairs.get(k, 0) + 1
		rules3[src] = newpairs
	add_new_rule(line[:2], f"{line[0]}{line[2:]}{line[1]}")
	add_new_rule(line[:2][::-1], f"{line[1]}{line[2:]}{line[0]}")
population = {
	"AB": 1
}
for i in range(21):
	new_population = {}
	for k, v in population.items():
		mutated = rules3[k]
		for ik, iv in mutated.items():
			new_population[ik] = new_population.get(ik, 0) + iv * v
	population = new_population
print(f"part 3: {sum(population.values()) + 1}")