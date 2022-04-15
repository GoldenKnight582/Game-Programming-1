# Tyler Cobb
# ETGG1101-05 Lab 05

# Initialization
import pygame
import random

pygame.init()

# Images, Fonts, Static Font Messages
idleSheet = pygame.image.load("images\\vlad_idle.png")
idleSheet.set_colorkey((94, 66, 41))
walkSheet = pygame.image.load("images\\vlad_walking.png")
walkSheet.set_colorkey((94, 66, 41))
attackSheet = pygame.image.load("images\\vlad_attack.png")
attackSheet.set_colorkey((94, 66, 41))
fireSheet = pygame.image.load("images\\fireShot.bmp")
fireSheet.set_colorkey((221, 118, 36))
star = pygame.image.load("images\\star.png")
fontObj = pygame.font.Font("fonts\\Notable-Regular.ttf", 16)
credText = fontObj.render("Sprite From https://www.renerstilesets.de/", False, (100, 175, 100), (0, 0, 0))
pauseInst = fontObj.render("Press F2 To Pause", False, (100, 100, 100), (0, 0, 0))
pauseText = fontObj.render("-- Paused (F2 to Toggle) --", False, (100, 100, 100), (0, 0, 0))

# Variables
win_w = 800
win_h = 600
win = pygame.display.set_mode((win_w, win_h))
clock = pygame.time.Clock()
done = False
x = 400
y = 300
cur_frame = 0
cur_direction = 0
move_min = 10
spriteSize = 96
state = "idle"
vladSpeed = 100
shotSpeed = 150
mousePos = (400, 300)
directionRL = 0
directionUD = 0
anim_delay = 0.083
anim_timer = anim_delay
star_x = random.randint(0, win_w)
star_y = random.randint(0, win_h)
score = 0
shot_frame = 0
shot_size = 64
shot_x = 0
shot_y = 0
shotMode = False
modeDebug = False
pause = False

# Game Loop
while not done:
    delta_time = clock.tick() / 1000
    if not pause:
        # * Updates *
        anim_timer -= delta_time
        frame_rate = int(clock.get_fps())
        shotDiag = (((shotSpeed * delta_time) ** 2) / 2) ** 0.5
        # Star Spawn Bounds
        if star_x >= 751:
            star_x = 750
        elif star_x <= 49:
            star_x = 50
        if star_y >= 551:
            star_y = 550
        elif star_y <= 49:
            star_y = 50
        # State Updates
        if state == "attacking":
            spriteSheet = attackSheet
            spriteSize = 128
        elif state == "walking":
            spriteSheet = walkSheet
            spriteSize = 96
        else:
            spriteSheet = idleSheet
            spriteSize = 96
        # Idle Animation Updates
        if state == "idle":
            if directionRL == "R" and directionUD == "S":
                cur_direction = 0
                shot_x = x + spriteSize
                shot_y = y + shot_size // 2
                if anim_timer <= 0:
                    cur_frame += 1
                    anim_timer = anim_delay
            elif directionUD == "U" and directionRL == "R":
                cur_direction = 1
                shot_x = x + shot_size
                shot_y = y
                if anim_timer <= 0:
                    cur_frame += 1
                    anim_timer = anim_delay
            elif directionUD == "U" and directionRL == "S":
                cur_direction = 2
                shot_x = x + spriteSize // 2
                shot_y = y - spriteSize // 4
                if anim_timer <= 0:
                    cur_frame += 1
                    anim_timer = anim_delay
            elif directionUD == "U" and directionRL == "L":
                cur_direction = 3
                shot_x = x
                shot_y = y - shot_size // 4
                if anim_timer <= 0:
                    cur_frame += 1
                    anim_timer = anim_delay
            elif directionRL == "L" and directionUD == "S":
                cur_direction = 4
                shot_x = x - spriteSize // 4
                shot_y = y + shot_size // 2
                if anim_timer <= 0:
                    cur_frame += 1
                    anim_timer = anim_delay
            elif directionUD == "D" and directionRL == "L":
                cur_direction = 5
                shot_x = x - spriteSize // 4
                shot_y = y + spriteSize // 2
                if anim_timer <= 0:
                    cur_frame += 1
                    anim_timer = anim_delay
            elif directionUD == "D" and directionRL == "S":
                cur_direction = 6
                shot_x = x + shot_size // 2
                shot_y = y + spriteSize
                if anim_timer <= 0:
                    cur_frame += 1
                    anim_timer = anim_delay
            elif directionUD == "D" and directionRL == "R":
                cur_direction = 7
                shot_x = x + shot_size
                shot_y = y + spriteSize // 2
                if anim_timer <= 0:
                    cur_frame += 1
                    anim_timer = anim_delay
            if cur_frame > 11:
                cur_frame = 0
        # Attack Animation Updates
        if state == "attacking":
            if cur_direction == 0:
                shot_x += shotSpeed * delta_time
                if anim_timer <= 0:
                    shot_frame += 1
                    cur_frame += 1
                    anim_timer = anim_delay
            elif cur_direction == 1:
                shot_x += shotDiag
                shot_y -= shotDiag
                if anim_timer <= 0:
                    shot_frame += 1
                    cur_frame += 1
                    anim_timer = anim_delay
            elif cur_direction == 2:
                shot_y -= shotSpeed * delta_time
                if anim_timer <= 0:
                    shot_frame += 1
                    cur_frame += 1
                    anim_timer = anim_delay
            elif cur_direction == 3:
                shot_x -= shotDiag
                shot_y -= shotDiag
                if anim_timer <= 0:
                    shot_frame += 1
                    cur_frame += 1
                    anim_timer = anim_delay
            elif cur_direction == 4:
                shot_x -= shotSpeed * delta_time
                if anim_timer <= 0:
                    shot_frame += 1
                    cur_frame += 1
                    anim_timer = anim_delay
            elif cur_direction == 5:
                shot_x -= shotDiag
                shot_y += shotDiag
                if anim_timer <= 0:
                    shot_frame += 1
                    cur_frame += 1
                    anim_timer = anim_delay
            elif cur_direction == 6:
                shot_y += shotSpeed * delta_time
                if anim_timer <= 0:
                    shot_frame += 1
                    cur_frame += 1
                    anim_timer = anim_delay
            elif cur_direction == 7:
                shot_x += shotDiag
                shot_y += shotDiag
                if anim_timer <= 0:
                    shot_frame += 1
                    cur_frame += 1
                    anim_timer = anim_delay
            if cur_frame > 11:
                cur_frame = 0
                state = "idle"
            if shot_frame > 2:
                shot_frame = 0
        # Movement Updates
        if state == "walking":
            if directionRL == "R" and directionUD == "S":
                cur_direction = 0
                x += vladSpeed * delta_time
                if anim_timer <= 0:
                    cur_frame += 1
                    anim_timer = anim_delay
            elif directionUD == "U" and directionRL == "R":
                diagDistance = (((vladSpeed * delta_time) ** 2) / 2) ** 0.5
                cur_direction = 1
                y -= diagDistance
                x += diagDistance
                if anim_timer <= 0:
                    cur_frame += 1
                    anim_timer = anim_delay
            elif directionUD == "U" and directionRL == "S":
                cur_direction = 2
                y -= vladSpeed * delta_time
                if anim_timer <= 0:
                    cur_frame += 1
                    anim_timer = anim_delay
            elif directionUD == "U" and directionRL == "L":
                diagDistance = (((vladSpeed * delta_time) ** 2) / 2) ** 0.5
                cur_direction = 3
                y -= diagDistance
                x -= diagDistance
                if anim_timer <= 0:
                    cur_frame += 1
                    anim_timer = anim_delay
            elif directionRL == "L" and directionUD == "S":
                cur_direction = 4
                x -= vladSpeed * delta_time
                if anim_timer <= 0:
                    cur_frame += 1
                    anim_timer = anim_delay
            elif directionUD == "D" and directionRL == "L":
                diagDistance = (((vladSpeed * delta_time) ** 2) / 2) ** 0.5
                cur_direction = 5
                y += diagDistance
                x -= diagDistance
                if anim_timer <= 0:
                    cur_frame += 1
                    anim_timer = anim_delay
            elif directionUD == "D" and directionRL == "S":
                cur_direction = 6
                y += vladSpeed * delta_time
                if anim_timer <= 0:
                    cur_frame += 1
                    anim_timer = anim_delay
            elif directionUD == "D" and directionRL == "R":
                diagDistance = (((vladSpeed * delta_time) ** 2) / 2) ** 0.5
                cur_direction = 7
                y += diagDistance
                x += diagDistance
                if anim_timer <= 0:
                    cur_frame += 1
                    anim_timer = anim_delay
            if cur_frame > 7:
                cur_frame = 0
                anim_timer = anim_delay

        # HUD Updates
        fpsText = fontObj.render("FPS: " + str(frame_rate), False, (255, 255, 0), (0, 0, 0))
        dirText = fontObj.render("Cur Direction: " + str(cur_direction), False, (255, 255, 0), (0, 0, 0))
        frameText = fontObj.render("Cur Frame: " + str(cur_frame), False, (255, 255, 0), (0, 0, 0))
        posText = fontObj.render("Cur Position: (" + str(int(x)) + "," + str(int(y)) + ")", False, (255, 255, 0), (0, 0, 0))
        stateText = fontObj.render("Cur State: " + state, False, (255, 255, 0), (0, 0, 0))
        scoreText = fontObj.render("Score: " + str(score), False, (255, 255, 255), (0, 0, 0))

        # Bounding Updates
        if cur_direction == 0:
            attackBound = pygame.Rect(int(x) - 30, int(y) - 25, 80, 40)
        elif cur_direction == 1:
            attackBound = pygame.Rect(int(x) + 5, int(y) - 55, 65, 40)
        elif cur_direction == 2:
            attackBound = pygame.Rect(int(x) - 10, int(y) - 60, 40, 55)
        elif cur_direction == 3:
            attackBound = pygame.Rect(int(x) - 50, int(y) - 55, 65, 40)
        elif cur_direction == 4:
            attackBound = pygame.Rect(int(x) - 50, int(y) - 50, 80, 40)
        elif cur_direction == 5:
            attackBound = pygame.Rect(int(x) - 50, int(y) - 30, 50, 70)
        elif cur_direction == 6:
            attackBound = pygame.Rect(int(x) - 25, int(y), 40, 60)
        elif cur_direction == 7:
            attackBound = pygame.Rect(int(x), int(y) - 25, 50, 70)

        starBound = pygame.Rect(star_x, star_y, star.get_width(), star.get_height())
        if shotMode:
            shotBound = pygame.Rect(int(shot_x) - shot_size, int(shot_y) - shot_size, shot_size, shot_size)
        # Collision Checks
        if state == "attacking":
            if attackBound.colliderect(starBound):
                star_x = random.randint(0, win_w)
                star_y = random.randint(0, win_h)
                score += 100
            if shotMode:
                if shotBound.colliderect(starBound):
                    star_x = random.randint(0, win_w)
                    star_y = random.randint(0, win_h)
                    score += 100
        # Score Updates
        if score >= 1000:
            shotMode = True
    # Input
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        done = True
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            done = True
        elif event.key == pygame.K_F1:
            if not modeDebug:
                modeDebug = True
            else:
                modeDebug = False
        elif event.key == pygame.K_F2:
            if not pause:
                pause = True
            else:
                pause = False

    mousePos = pygame.mouse.get_pos()
    mouse_x = mousePos[0]
    mouse_y = mousePos[1]
    # Direction Check
    if int(mouse_x) > int(x) + move_min:
        directionRL = "R"
    elif int(mouse_x) < int(x) - move_min:
        directionRL = "L"
    else:
        directionRL = "S"
    if int(mouse_y) > int(y) + move_min:
        directionUD = "D"
    elif int(mouse_y) < int(y) - move_min:
        directionUD = "U"
    else:
        directionUD = "S"
    mouseButton = pygame.mouse.get_pressed()
    if mouseButton[0]:
        if state == "idle":
            state = "walking"
            cur_frame = 0
    elif mouseButton[2]:
        state = "attacking"
        cur_frame = 0
    else:
        if state == "walking":
            state = "idle"
            cur_frame = 0

    # Drawing
    win.fill((0, 0, 0))

    # Text
    win.blit(scoreText, (400 - scoreText.get_width() // 2, 0))
    win.blit(credText, (260, 575))
    if not pause:
        win.blit(pauseInst, (585, 485))
    else:
        win.blit(pauseText, (win_w // 2 - pauseText.get_width() // 2, win_h // 2))

    # Sprites
    win.blit(star, (star_x, star_y), (0, 0, star.get_width(), star.get_height()))
    win.blit(spriteSheet, (int(x) - spriteSize // 2, int(y) - spriteSize // 2),
            (cur_frame * spriteSize, cur_direction * spriteSize, spriteSize, spriteSize))

    # Shot Sprite
    if state == "attacking":
        if shotMode:
            win.blit(fireSheet, (int(shot_x) - shot_size, int(shot_y) - shot_size),
                     (shot_frame * shot_size, cur_direction * shot_size, shot_size, shot_size))

    # Debug Mode - Bounding Boxes
    if modeDebug:
        pygame.draw.rect(win, (255, 255, 0), starBound, 1)
        if state == "attacking":
            if cur_direction == 0:
                pygame.draw.rect(win, (255, 255, 0), attackBound, 1)
            elif cur_direction == 1:
                pygame.draw.rect(win, (255, 255, 0), attackBound, 1)
            elif cur_direction == 2:
                pygame.draw.rect(win, (255, 255, 0), attackBound, 1)
            elif cur_direction == 3:
                pygame.draw.rect(win, (255, 255, 0), attackBound, 1)
            elif cur_direction == 4:
                pygame.draw.rect(win, (255, 255, 0), attackBound, 1)
            elif cur_direction == 5:
                pygame.draw.rect(win, (255, 255, 0), attackBound, 1)
            elif cur_direction == 6:
                pygame.draw.rect(win, (255, 255, 0), attackBound, 1)
            elif cur_direction == 7:
                pygame.draw.rect(win, (255, 255, 0), attackBound, 1)
            if shotMode:
                pygame.draw.rect(win, (255, 255, 0), shotBound, 1)
        # Debug HUD
        win.blit(fpsText, (0, 455))
        win.blit(dirText, (0, 485))
        win.blit(frameText, (0, 515))
        win.blit(posText, (0, 545))
        win.blit(stateText, (0, 575))
    pygame.display.flip()