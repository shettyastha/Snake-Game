import pygame
import time
import random

pygame.init()

# Define colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Define display settings
dis_width = 800
dis_height = 600
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()
snake_block = 10

font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)

# Load sound effects
t_sound = pygame.mixer.Sound(r'C:\Users\Aastha\.vscode\Python\t.wav')
c_sound = pygame.mixer.Sound(r'C:\Users\Aastha\.vscode\Python\c.wav')

# Define levels
levels = [
    {"speed": 15, "obstacles": []},
    {"speed": 18, "obstacles": [[200, 200], [400, 400], [600, 200]]},
    {"speed": 22, "obstacles": [[150, 150], [300, 300], [450, 450], [600, 150]]},
]

def show_score(score, high_score, level):
    value = score_font.render("Score: " + str(score), True, black)
    dis.blit(value, [0, 0])
    high_value = score_font.render("High Score: " + str(high_score), True, black)
    dis.blit(high_value, [0, 35])
    level_value = score_font.render("Level: " + str(level), True, black)
    dis.blit(level_value, [0, 70])

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

def draw_obstacles(obstacles):
    for obs in obstacles:
        pygame.draw.rect(dis, red, [obs[0], obs[1], snake_block, snake_block])

def load_high_score():
    try:
        with open('high_score.txt', 'r') as f:
            return int(f.read())
    except FileNotFoundError:
        return 0

def save_high_score(high_score):
    with open('high_score.txt', 'w') as f:
        f.write(str(high_score))

def gameLoop():
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1
    score = 0
    level = 0  # Start at level 0
    high_score = load_high_score()

    current_level = levels[level]
    snake_speed = current_level["speed"]
    obstacles = current_level["obstacles"]

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    while not game_over:
        
        while game_close == True:
            dis.fill(blue)
            message("You Lost! Press Q-Quit or C-Play Again", red)
            show_score(score, high_score, level)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            pygame.mixer.Sound.play(c_sound)
            game_close = True

        for obs in obstacles:
            if x1 == obs[0] and y1 == obs[1]:
                pygame.mixer.Sound.play(c_sound)
                game_close = True

        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        draw_obstacles(obstacles)

        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                pygame.mixer.Sound.play(c_sound)
                game_close = True

        our_snake(snake_block, snake_list)
        show_score(score, high_score, level)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            pygame.mixer.Sound.play(t_sound)
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            length_of_snake += 1
            score += 1

            if score % 10 == 0:  # Increase level every 10 points
                level += 1
                if level < len(levels):
                    current_level = levels[level]
                    snake_speed = current_level["speed"]
                    obstacles = current_level["obstacles"]

        if score > high_score:
            high_score = score
            save_high_score(high_score)

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()

