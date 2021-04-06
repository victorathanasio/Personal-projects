import pygame
from utils.bird import Bird
from utils.ground import Ground
from utils.pipe import Pipe
from utils.score import Score
import os

WINDOW_HEIGHT = 700
WINDOW_WIDTH = 1200
theme = "Theme_mvp"

pygame.init()
clock = pygame.time.Clock()
running = True
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Initialize
bird = Bird(theme=theme)
pipe_distance = WINDOW_WIDTH / 6
pipes = []
ground = Ground(theme=theme)
path = os.path.join("Assets/", theme)
background = pygame.image.load(
    os.path.join(path, "bg_big.png")).convert_alpha()
window.blit(background, (0, 0))
time = 0
not_finish = 100

while not_finish > 00:
    if not running:
        not_finish -= 1
    time += 1
    clock.tick(60)
    window.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            bird.jump()
            bird.angle=0
        if event.type == pygame.QUIT:
            running = False

    # collision
    for pipe in pipes:
        if pipe.collision(bird):
            bird.alive = False
            running = False
    if ground.collide(bird):
        bird.alive = False
        running = False

    # movement
    bird.angle=0
    bird.move()
    if running:
        for pipe in pipes:
            pipe.move()
        ground.move()

    # Pipe management
    if time % 90 == 0:
        pipes.append(Pipe(theme=theme))

    for i, pipe in enumerate(pipes):
        if pipe.expired():
            pipes.pop(i)

    # draw
    for pipe in pipes:
        pipe.draw(window)
    bird.angle=0
    bird.draw(window)

    ground.draw(window)


    pygame.display.flip()

# end main loop
pygame.quit()
