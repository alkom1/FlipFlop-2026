from dataclasses import dataclass, field
from typing import Dict, List, Tuple
import string

with open("6.in.txt", "rt") as file:
	INPUT = [list(x.strip()) for x in file]
	HEIGHT = len(INPUT)
	WIDTH = len(INPUT[0])

Point = Tuple[int, int]
@dataclass
class MapSpot:
	neighbors: List['Gear'] = field(default_factory=list)

@dataclass
class Light(MapSpot):
	pass

@dataclass
class Gear(MapSpot):
	rotation: str = '0'
	group: int = -1
	active: bool = True

@dataclass
class BluetoothInput(Gear):
	pass

@dataclass
class BluetoothOutput(Gear):
	pass

@dataclass
class Bluetooth():
	input: Point = (0, 0)
	output: Point = (0, 0)

def execute(gear_signs:Tuple[str,...]=(), ignore_bluetooth=True, prime_rule=False):
	existing: Dict[Point, 'MapSpot'] = {}
	bluetooth: Dict[str, 'Bluetooth'] = {}
	lights: List['Light'] = []
	group_counts: Dict[int, int] = {}
	

	def populate(map: List[List[str]]) -> Point:
		# create objects
		for y, row in enumerate(map):
			for x, c in enumerate(row):
				if c == 'S':
					start = (x, y)
					existing[start] = Gear()
				elif c in gear_signs:
					existing[(x, y)] = Gear()
				elif c == '*':
					existing[(x, y)] = Light()
					lights.append(existing[(x, y)]) # type: ignore
				elif c in string.ascii_letters and not ignore_bluetooth:
					item = bluetooth.get(c.lower()) or Bluetooth()
					if c in string.ascii_lowercase:
						item.input = (x, y)
					elif c in string.ascii_uppercase:
						item.output = (x, y)
					bluetooth[c.lower()] = item
		# add bluetooth gears
		for c, item in bluetooth.items():
			existing[item.input] = BluetoothInput()
			existing[item.output] = BluetoothOutput()
		# list neighbors
		def get_gear_neighbors(x: int, y: int) -> List['Gear']:
			result: List['Gear'] = []
			for ix, iy in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):
				if ix < 0 or iy < 0 or ix >= WIDTH or iy >= HEIGHT:
					continue
				item = existing.get((ix, iy))
				if isinstance(item, Gear):
					result += [item]
			return result
		for (x, y), item in existing.items():
			item.neighbors = get_gear_neighbors(x, y) # type: ignore
		for c, item in bluetooth.items():
			existing[item.input].neighbors += [existing[item.output]] # type: ignore
		# groups
		if prime_rule:
			q: List[Tuple[int, 'Gear']] = []
			for i, item in enumerate(bluetooth.values()):
				q += [(i, existing[item.output])] # type: ignore
			while len(q) > 0:
				i, g = q.pop(0) # yeah yeah i know
				if g.group >= 0:
					continue
				g.group = i
				if isinstance(g, Gear) and not isinstance(g, BluetoothInput) and not isinstance(g, BluetoothOutput):
					group_counts[i] = group_counts.get(i, 0) + 1
				q += [(i, n) for n in g.neighbors]
			def isprime(n): return not any(n % i == 0 for i in range(2,n))
			for b in bluetooth.values():
				if isprime(group_counts[existing[b.output].group]): # type: ignore
					existing[b.input].active = False # type: ignore
					existing[b.output].active = False # type: ignore
		return start

	start = populate(INPUT)
	def dfs2(start: Gear, rotation: str):
		if start.rotation != '0' or not start.active:
			return
		start.rotation = rotation
		for n in start.neighbors:
			dfs2(n, 'R' if rotation=='L' else 'L')
	dfs2(existing[start], 'L') # type: ignore

	result = 0
	for l in lights:
		if any(n.rotation == 'R' for n in l.neighbors):
			result = (result << 1) | 1
		elif any(n.rotation == 'L' for n in l.neighbors):
			result = (result << 1)
	return result

part1 = execute(('#',), True, False)
part2 = execute(('#', '3'), False, False)
part3 = execute(('#', '3'), False, True)

print(f"part 1: {part1}\npart 2: {part2}\npart 3: {part3}")