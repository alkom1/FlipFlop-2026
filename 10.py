from typing import Dict, List, Tuple
from tqdm import tqdm

with open("10.in.txt") as file:
	INPUT = [x.strip() for x in file]

instruction_list: List[Tuple[int,...]] = []
labels: Dict[int, int] = {}

#parse
for line in INPUT:
	if line.startswith("be"): # label
		labels[line.count("na")] = len(instruction_list)
	if not line.startswith("ba"):
		continue # instructions
	parts = [x.count("na") for x in line[2:].split("ne")]
	instruction_list += [(*parts,)]

def execute(limit: int = 0, r0: int = 0, r1: int = 0) -> Tuple[List[int], int]:
	# execute
	registers = [0] * 16
	registers[0] = r0
	registers[1] = r1
	pc = 0
	count = 0
	while pc < len(instruction_list) and (limit == 0 or count < 5000000):
		ins, args = instruction_list[pc][0], instruction_list[pc][1:]
		pc += 1
		count += 1
		if ins == 0:
			val, dest_reg = args
			registers[dest_reg] = val
		elif ins == 1:
			src_reg, dest_reg = args
			registers[dest_reg] = registers[src_reg]
		elif ins == 2:
			src_reg1, src_reg2, dest_reg = args
			registers[dest_reg] = (registers[src_reg1] + registers[src_reg2]) % 65536
		elif ins == 3:
			src_reg1, src_reg2, dest_reg = args
			registers[dest_reg] = (registers[src_reg1] - registers[src_reg2]) % 65536
		elif ins == 4:
			src_reg1, src_reg2, dest_reg = args
			registers[dest_reg] = (registers[src_reg1] * registers[src_reg2]) % 65536
		elif ins == 5:
			src_reg1, src_reg2, dest_reg = args
			if registers[src_reg2] == 0:
				registers[dest_reg] = 0
			else:
				registers[dest_reg] = (registers[src_reg1] % registers[src_reg2]) % 65536
		elif ins == 6:
			reg = args[0]
			registers[reg] = (registers[reg] + 1) % 65536
		elif ins == 7:
			reg = args[0]
			registers[reg] = (registers[reg] - 1) % 65536
		elif ins == 8:
			label = args[0]
			pc = labels[label]
		elif ins == 9:
			reg, label = args
			if registers[reg] == 0:
				pc = labels[label]
		elif ins == 10:
			reg, label = args
			if registers[reg] > 0:
				pc = labels[label]
		else:
			print("BIG BAD")
			break
	return registers, count

print(f"part 1: {execute()[0][0]}")

s = 0
for i in tqdm(range(100)):
	_, c = execute(limit=5000000, r0=i)
	if c >= 5000000:
		s += 1

print(f"part 2: {s}")

s = 0
for i in tqdm(range(16*16)):
	r1, r0 = i // 16, i % 16
	rs, c = execute(r0=r0, r1=r1, limit=5000000)
	if c >= 5000000:
		s += 1

print("part 3:", int(s * (2 ** 16 / 16)))

# somewhere in here there's an error cause i marked only 63 infinite loops
# (+6 means that every r0=16k+6, where k=0,1,2.. is infinite loop)
# r1=0:  +6 +8 +12
# r1=1:  +11
# r1=2:  everything except +8
# r1=3:  nothing
# r1=4:  +0
# r1=5:  +0 +12
# r1=6:  1-8, 10-13
# r1=7:  +3 +7 +9
# r1=8:  +0 +10 +12
# r1=9:  nothing
# r1=10: everything except +0
# r1=11: nothing
# r1=12: nothing
# r1=13: +9
# r1=14: +6
# r1=15: +3 +6 8-11