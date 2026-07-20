from collections import defaultdict
from itertools import count
from dataclasses import dataclass, field
from typing import Dict, Generator, List, Literal, Set, Tuple
import heapq
from math import inf, sqrt
import cProfile
from functools import cache
Point = Tuple[int, int]

with open("9.test.txt", "rt") as file:
	INPUT = [list(x.strip()) for x in file]
	WIDTH = len(INPUT[0])
	HEIGHT = len(INPUT)

PART:Literal[1, 2, 3] = 3

@dataclass(frozen=True)
class State:
	position: Point
	red: Point
	blue: Point

	@staticmethod
	def new(p: Point) -> 'State':
		return State(p, (-1, -1), (-1, -1))
	
	@staticmethod
	def clone(other: 'State', p: Point|None=None, r:Point|None=None, b:Point|None=None) -> 'State':
		p = p if p is not None else other.position
		r = r if r is not None else other.red
		b = b if b is not None else other.blue
		if r > b:
			r, b = b, r
		return State(p, r, b)

start: Point = (-1, -1)
end: Point = (-1, -1)
for y, row in enumerate(INPUT):
	for x, c in enumerate(row):
		if c == 'S':
			start = (x, y)
		if c == 'E':
			end = (x, y)
assert start
assert end

DIRECTIONS = ((1,0), (-1,0), (0,1), (0,-1))

@cache
def isRoom(p: Point) -> bool:
	return INPUT[p[1]][p[0]] in ('.', 'S', 'E')

@cache
def findFurthestAway(a: Point, minDepth: int = 2) -> List[Point]:
	results: Set[Point] = set()
	for d in DIRECTIONS:
			depth = 1
			while True:
				point = (a[0] + d[0] * depth, a[1] + d[1] * depth)
				if not isRoom(point):
					depth -= 1
					break
				depth += 1
			if depth >= minDepth:
				point = (a[0] + d[0] * depth, a[1] + d[1] * depth)
				results.add(point)
	return list(results)

def get_neighbors(initial: State) -> Generator[State]:
	# possible actions:
	#  1. move in cardinal directions if there isnt a wall (1+2+3)
	for d in DIRECTIONS:
		point = (initial.position[0] + d[0], initial.position[1] + d[1])
		if isRoom(point):
			yield State.clone(initial, p = point)
	#  2. move across the whole hallway (2)
	if PART == 2:
		yield from (State.clone(initial, p = point) for point in findFurthestAway(initial.position))
	#  3. shoot red/blue portal in cardinal directions (3)
	if PART == 3:
		yield from (State.clone(initial, r = point) for point in findFurthestAway(initial.position, minDepth=0))
		yield from (State.clone(initial, b = point) for point in findFurthestAway(initial.position, minDepth=0))
	#  4. move through the portal if its on the current tile (3)
	if PART == 3 and initial.red != (-1, -1) and initial.blue != (-1, -1) and initial.red != initial.blue:
		if initial.position == initial.red:
			yield State.clone(initial, p = initial.blue)
		if initial.position == initial.blue:
			yield State.clone(initial, p = initial.red)


# A*
def astar():
	def walking_distance(a: Point, b: Point) -> int:
		return abs(a[0] - b[0]) + abs(a[1] - b[1])
	def h(s: State) -> float:
		if (-1, -1) in (s.red, s.blue):
			return walking_distance(s.position, end)
		return min(
			walking_distance(s.position, end),
			walking_distance(s.position, s.blue) + walking_distance(s.red, end),
			walking_distance(s.position, s.red) + walking_distance(s.blue, end)
		)

	def reconstruct_path(current: State):
		print(g_score[current])

	counter = count()
	initial_state = State.new(start)
	open_set: List[Tuple[float, int, State]] = []
	came_from: Dict['State', 'State'] = {}
	g_score: Dict[State, int] = defaultdict(lambda: 1_000_000)
	g_score[initial_state] = 0
	f_score: Dict[State, float] = defaultdict(lambda: inf)
	f_score[initial_state] = h(initial_state)
	heapq.heappush(open_set, (f_score[initial_state], next(counter), initial_state))

	while len(open_set) > 0:
		old_cost, _, current = heapq.heappop(open_set)
		if old_cost > g_score[current] + h(current):
			continue
		if current.position == end:
			reconstruct_path(current)
			break
		for n in get_neighbors(current):
			tentative_g_score = g_score[current] + 1
			if tentative_g_score < g_score[n]:
				came_from[n] = current
				g_score[n] = tentative_g_score
				f_score[n] = tentative_g_score + h(n)
				heapq.heappush(open_set, (f_score[n], next(counter), n))

cProfile.run('astar()', sort="tottime")
print("end")
print("findFurthestAway", findFurthestAway.cache_info())

# PART 1: 1338
# PART 2: 491