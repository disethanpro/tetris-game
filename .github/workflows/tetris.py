import pygame
import random

# 初始化Pygame
pygame.init()

# 设置屏幕大小
screen_width = 300
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# 设置颜色
black = (0, 0, 0)
white = (255, 255, 255)

# 设置方块大小
block_size = 30

# 定义形状
shapes = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]]
]

class Tetris:
    def __init__(self):
        self.board = [[0 for _ in range(10)] for _ in range(20)]
        self.shape = random.choice(shapes)
        self.shape_x = 3
        self.shape_y = 0
        self.score = 0
        self.game_over = False

    def draw_board(self):
        for y in range(20):
            for x in range(10):
                if self.board[y][x] == 1:
                    pygame.draw.rect(screen, white, (x * block_size, y * block_size, block_size, block_size))

    def draw_shape(self):
        for y in range(len(self.shape)):
            for x in range(len(self.shape[y])):
                if self.shape[y][x] == 1:
                    pygame.draw.rect(screen, white, ((self.shape_x + x) * block_size, (self.shape_y + y) * block_size, block_size, block_size))

    def rotate_shape(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def valid_move(self, dx, dy):
        for y in range(len(self.shape)):
            for x in range(len(self.shape[y])):
                if self.shape[y][x] == 1:
                    if (self.shape_y + y + dy >= 20 or
                        self.shape_x + x + dx >= 10 or
                        self.shape_x + x + dx < 0 or
                        self.board[self.shape_y + y + dy][self.shape_x + x + dx] == 1):
                        return False
        return True

    def lock_shape(self):
        for y in range(len(self.shape)):
            for x in range(len(self.shape[y])):
                if self.shape[y][x] == 1:
                    self.board[self.shape_y + y][self.shape_x + x] = 1
        self.clear_lines()
        self.shape = random.choice(shapes)
        self.shape_x = 3
        self.shape_y = 0
        if not self.valid_move(0, 0):
            self.game_over = True

    def clear_lines(self):
        new_board = [[0 for _ in range(10)] for _ in range(20)]
        new_y = 19
        for y in range(19, -1, -1):
            if 0 in self.board[y]:
                new_board[new_y] = self.board[y]
                new_y -= 1
            else:
                self.score += 1
        self.board = new_board

    def update(self):
        if self.valid_move(0, 1):
            self.shape_y += 1
        else:
            self.lock_shape()

# 创建Tetris对象
tetris = Tetris()

# 设置时钟
clock = pygame.time.Clock()

# 游戏主循环
running = True
while running:
    screen.fill(black)
    tetris.draw_board()
    tetris.draw_shape()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and tetris.valid_move(-1, 0):
                tetris.shape_x -= 1
            elif event.key == pygame.K_RIGHT and tetris.valid_move(1, 0):
                tetris.shape_x += 1
            elif event.key == pygame.K_DOWN and tetris.valid_move(0, 1):
                tetris.shape_y += 1
            elif event.key == pygame.K_UP:
                tetris.rotate_shape()
                if not tetris.valid_move(0, 0):
                    for _ in range(3):
                        tetris.rotate_shape()

    tetris.update()
    pygame.display.flip()
    clock.tick(10)

pygame.quit()
