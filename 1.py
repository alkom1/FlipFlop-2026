FILE = "1.in.txt"

with open(FILE, "rt") as file:
	LIST = [int(x) for x in file.readlines()]

# PART 1
sum = 0
for number in LIST:
	sum += max(0, 60 - number)
print(f"part 1: {sum}")

# PART 2
sum = 0
for number in LIST:
	delta = abs(60 - number)
	sum += delta if number <= 60 else delta * 5
print(f"part 2: {sum}")

# PART 3
sum = 0
len = len(LIST) // 2
for i in range(len):
	src = LIST[i]
	target = LIST[len + i]
	delta = abs(target - src)
	sum += delta if src <= target else delta * 5
print(f"part 3: {sum}")