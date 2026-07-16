with open("4.in.txt", "rt") as file:
	INPUT = [x.strip() for x in file]

# PART 1
s = sum((1 if "-" in x else 0) for x in INPUT[3:-401])
print(f"part 1: {s}")

# PART 2
swaps = 0
leafs_only = list(x for x in INPUT[-2:2:-1] if "-" in x)
leaf_pairs = list(zip(leafs_only[:-1], leafs_only[1:]))
for src, trg in leaf_pairs:
	if src != trg:
		swaps += 1
print(f"part 2: {swaps}")

# PART 3
rounds = 0
while len(leaf_pairs) > 0:
	leaf_pairs_clone = leaf_pairs[:]
	leaf_pairs = []
	for src, trg in leaf_pairs_clone[:-1]:
		if src == trg:
			leaf_pairs += [(src, trg)]
			continue
		if len(leaf_pairs) > 0:
			leaf_pairs[-1] = (leaf_pairs[-1][0], trg)
	rounds += 1
print(f"part 3: {rounds}")
"""
L
L
 R
 R
L
L
"""
"""
L, L
L, R <-
R, R
R, L
L, L
"""