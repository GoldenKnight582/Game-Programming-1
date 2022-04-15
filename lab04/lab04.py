import pygame
import time

# Pygame Setup
pygame.init()
win_width = 800
win_height = 600
window = pygame.display.set_mode((win_width, win_height))

# Images
bg = pygame.image.load("images\\forest.png")
heart = pygame.image.load("images\\heart.png")
spritesheet = pygame.image.load("images\\princess_walking.bmp")
spritesheet.set_colorkey((97, 68, 43))

# Variables
cur_frame = 0
steps = 0
cur_direction = 0
loop_count = 0
sprite_size = 96
x = 400
y = 300
bgx = 200
bgy = 200
hx = 380
hy = 230
bg_width = bg.get_width()
bg_height = bg.get_height()
h_width = heart.get_width()
h_height = heart.get_height()
anim_delay = 0.05
fontObj = pygame.font.Font("fonts\\Notable-Regular.ttf", 26)

# Loop through each frame
while cur_frame < 8 and cur_direction < 8:
    window.blit(bg, (0, 0), (bgx, bgy, win_width, win_height))
    window.blit(heart, (hx, hy), (0, 0, h_width, h_height))
    stepCount = fontObj.render("# Steps " + str(steps) + "/256", False, (255, 255, 0), (0, 0, 0))
    bgPos = fontObj.render("Background Position: (" + str(bgx) + "," + str(bgy) + ")", False, (255, 255, 0), (0, 0, 0))
    hPos = fontObj.render("(" + str(hx) + ", " + str(hy) + ")", False, (255, 255, 255))
    hPos_width = hPos.get_width()
    window.blit(bgPos, (0, 0))
    window.blit(stepCount, (0, 50))
    window.blit(hPos, (hx + h_width // 2 - hPos_width // 2, hy - h_height))
    window.blit(spritesheet, (x - sprite_size // 2, y - sprite_size // 2),
                (cur_frame * sprite_size, cur_direction * sprite_size, sprite_size, sprite_size))
    pygame.display.flip()
    time.sleep(anim_delay)
    steps += 1
    cur_frame += 1
    if cur_direction == 0:
        bgx += 2
        hx -= 2
    elif cur_direction == 1:
        bgx += 2
        bgy -= 2
        hx -= 2
        hy += 2
    elif cur_direction == 2:
        bgy -= 2
        hy += 2
    elif cur_direction == 3:
        bgx -= 2
        bgy -= 2
        hx += 2
        hy += 2
    elif cur_direction == 4:
        bgx -= 2
        hx += 2
    elif cur_direction == 5:
        bgx -= 2
        bgy += 2
        hx += 2
        hy -= 2
    elif cur_direction == 6:
        bgy += 2
        hy -= 2
    else:
        bgx += 2
        bgy += 2
        hx -= 2
        hy -= 2
    if cur_frame == 8:
        cur_frame = 0
        loop_count += 1
        if loop_count == 4:
            loop_count = 0
            cur_frame = 0
            cur_direction += 1
# End Pygame
pygame.quit()