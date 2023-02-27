import pygame
from random import randint


# Creer la fenetre
sw = 640
sh = 480
screen = pygame.display.set_mode((sw, sh))

bg_color = pygame.Color(22, 41, 85)

# creer grille de jeu
tiles_x = 32
tiles_y = 24

tile_w = sw // tiles_x
tile_h = sh // tiles_y

# creer le serpent
snk_x, snk_y = tiles_x // 4, tiles_y // 2
snake = [
    [snk_x, snk_y],
    [snk_x-1, snk_y],
    [snk_x-2, snk_y]
]

# creer nourriture
food = [tiles_x//2, tiles_y//2]


def menu():
    screen.fill((255, 255, 255))
    pygame.font.init()
    textf = pygame.font.SysFont(None, 34)
    textg = textf.render("APPUYER SUR SPACE POUR COMMENCER", 1, (0, 0, 0))
    screen.blit(textg, (100, 100))
    pygame.display.flip()

    # game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    jouer()


def drawFood():
    food_color = pygame.Color(210, 45, 60)
    food_rect = pygame.Rect((food[0]*tile_w, food[1]*tile_h), (tile_w, tile_h))
    pygame.draw.rect(screen, food_color, food_rect)


def drawSnake():
    snk_color = pygame.Color(60, 215, 60)
    for cell in snake:
        cell_rect = pygame.Rect(
            (cell[0]*tile_w, cell[1]*tile_h), (tile_w, tile_h))
        pygame.draw.rect(screen, snk_color, cell_rect)


def updateSnake(direction):
    global food
    dirX, dirY = direction
    head = snake[0].copy()
    head[0] = (head[0]+dirX) % tiles_x
    head[1] = (head[1]+dirY) % tiles_y

    if head in snake[1:]:
        return False
    elif head == food:
        food = None
        while food is None:
            newfood = [
                randint(0, tiles_x-1),
                randint(0, tiles_y-1)
            ]
            food = newfood if newfood not in snake else None

    else:
        snake.pop()

    snake.insert(0, head)
    return True


def jouer():

    # game loop
    running = True
    direction = [1, 0]
    while running:
        pygame.time.Clock().tick(20)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                # droite pour droite
                if event.key == pygame.K_RIGHT and not direction == [-1, 0]:
                    direction = [1, 0]
                # gauche pour gauche
                if event.key == pygame.K_LEFT and not direction == [1, 0]:
                    direction = [-1, 0]
                # haut pour haut
                if event.key == pygame.K_UP and not direction == [0, 1]:
                    direction = [0, -1]
                # bas pour bas
                if event.key == pygame.K_DOWN and not direction == [0, -1]:
                    direction = [0, 1]

        # update
        if updateSnake(direction) == False:
            screen.fill(bg_color)
            pygame.font.init()
            textf = pygame.font.SysFont(None, 34)
            textg = textf.render(
                "OH LE NUL IL A PERDU", 1, (0, 0, 0))
            screen.blit(textg, (180, 200))
            pygame.display.update()
            running = False
            break

        # dessin
        screen.fill(bg_color)

        drawFood()
        drawSnake()

        pygame.display.update()


menu()
