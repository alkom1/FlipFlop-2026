from typing import List, Tuple

Point = Tuple[int, int]
with open("7.in.txt", "rt") as file:
	MOVEMENT = list(file.readline().strip())
	INSTRUCTION_LENGTH = len(MOVEMENT)
	file.readline()
	SUSHI: List[Point] = [(int(a), int(b)) for a, b in (x.split(',') for x in file)]

# PART 1
snake = (0, 0)
sushi_index = 0
sushi_eaten = 0
for m in MOVEMENT[:INSTRUCTION_LENGTH // 2]:
	current = SUSHI[sushi_index]
	if snake == current:
		sushi_eaten += 1
		sushi_index += 1
	snakeX, snakeY = snake
	if m == '>':
		snake = (snakeX + 1, snakeY)
	elif m == '<':
		snake = (snakeX - 1, snakeY)
	elif m == '^':
		snake = (snakeX, snakeY + 1)
	elif m == 'v':
		snake = (snakeX, snakeY - 1)
if snake == current:
	sushi_eaten += 1
print(f"part 1: {sushi_eaten}")

# PART 2
snake = (0, 0)
snake_body: List[Point] = []
sushi_index = 0
for m in MOVEMENT:
	snakeX, snakeY = snake
	old_body = snake_body.copy()
	snake_body = [snake] + snake_body
	if m == '>':
		snake = (snakeX + 1, snakeY)
	elif m == '<':
		snake = (snakeX - 1, snakeY)
	elif m == '^':
		snake = (snakeX, snakeY + 1)
	elif m == 'v':
		snake = (snakeX, snakeY - 1)
	eaten = False
	current = SUSHI[sushi_index]
	if snake == current:
		eaten = True
		sushi_index += 1
	if snake in snake_body:
		if snake != old_body[-1] or eaten:
			break
	if not eaten:
		snake_body.pop()
print(f"part 2: {len(snake_body)}")

# PART 3
snake = (0, 0)
snake_body: List[Point] = []
sushi_index = 0
ate_itself = 0
for i, m in enumerate(MOVEMENT):
	snakeX, snakeY = snake
	if m == '>':
		new_head = (snakeX + 1, snakeY)
	elif m == '<':
		new_head = (snakeX - 1, snakeY)
	elif m == '^':
		new_head = (snakeX, snakeY + 1)
	elif m == 'v':
		new_head = (snakeX, snakeY - 1)
	eaten = False
	current = SUSHI[sushi_index] if sushi_index < len(SUSHI) else (-1, -1)
	if new_head == current: # pylint: disable=E0606
		eaten = True
		sushi_index += 1
	if new_head in snake_body and (eaten or new_head != snake_body[-1]):
		ate_itself += 1
		idx = snake_body.index(new_head)
		snake_body = snake_body[:idx]
	snake_body.insert(0, snake)
	if not eaten:
		snake_body.pop()
	snake = new_head
print(f"part 3: {(len(snake_body) + 1) * ate_itself}")