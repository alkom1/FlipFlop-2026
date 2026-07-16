import itertools, string

with open("3.in.txt", "rt") as file:
	INPUT = [x.strip() for x in file.readlines()]

# PART 1
def lowercase(password: str) -> int:
	return sum(1 for c in password if c.islower())

def uppercase(password: str) -> int:
	return sum(1 for c in password if c.isupper())

def digits(password: str) -> int:
	return sum(1 for c in password if c.isdigit())

def score1(password: str) -> int:
	return len(password) * (
		(1 if lowercase(password) > 0 else 0) + 
		(1 if uppercase(password) > 0 else 0) + 
		(1 if digits(password) > 0 else 0)
	)
best_password = max(INPUT, key=score1)
print(f"part 1: {best_password}")

# PART 2
def sevens(password: str) -> bool:
	return "7" in password and not any(c.isdigit() and c != "7" for c in password)
def sequence_length(password: str, index: int) -> int:
	l = 0
	for c in password[index:]:
		if c == password[index]:
			l += 1
		else:
			break
	return l
def sequences(password: str) -> int:
	r = max(((i, c, sequence_length(password, i)) for i, c in enumerate(password)), key=lambda x: x[2])[2]
	return r if r >= 3 else 0
def redgreenblue(password: str) -> bool:
	return any(x in password for x in ("red", "green", "blue"))
def score2(password: str) -> int:
	return len(password) * (
		(1 if lowercase(password) > 0 else 0) + 
		(1 if uppercase(password) > 0 else 0) + 
		(1 if digits(password) > 0 else 0) + 
		(7 if sevens(password) else 0) + 
		(sequences(password) ** 2)
	) * (3 if redgreenblue(password) else 1)
best_password = max(INPUT, key=score2)
print(f"part 2: {best_password}")

# PART 3
ALLCHARS = string.ascii_lowercase + string.ascii_uppercase + string.digits
def score3(c: str) -> int:
	return sum(score2(p + c) for p in INPUT)
best = max(((c, score3(c)) for c in ALLCHARS), key=lambda x: x[1])
print(f"part 3: {best[0]} - {best[1]}")