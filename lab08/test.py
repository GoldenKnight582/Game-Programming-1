import pygame
import math

pygame.init()

win_dim = (800, 600)
win = pygame.display.set_mode(win_dim)
x = 400
y = 300
speed = 0.5
bullet_timer = 0.5
radius = 30
clock = pygame.time.Clock()

while True:
    delta_time = clock.tick() / 1000
    bullet_timer -= delta_time

    # Exit shit
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        break
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            break

    pygame.draw.circle(win, (255, 0, 0), (x, y), radius)
    pygame.draw.circle(win, (255, 255, 255), (x, y), radius - radius // 5)
    pygame.draw.circle(win, (255, 0, 0), (x, y), radius - 2 * radius // 5)
    pygame.draw.circle(win, (255, 255, 255), (x, y), radius - 3 * radius // 5)
    pygame.draw.circle(win, (255, 0, 0), (x, y), radius - 4 * radius // 5)
    pygame.display.flip()

pygame.quit()