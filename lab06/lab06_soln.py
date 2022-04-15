# Tyler Cobb
# ETGG1801-05 Lab 6

# Initialization
import lab06_utility as util
import pygame

pygame.init()

# Variables
win_w = 800
win_h = 600
win = pygame.display.set_mode((win_w, win_h))
shape_delay = 5
shape_timer = shape_delay
mouse_delay = 0.0025
mouse_timer = mouse_delay
rotation_speed = 90
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 18)
drag = False
hover = False
first_shape = True
done = False
pause = False

# Font Messages
line2 = font.render("Press F1 to pause", False, (100, 100, 0), (0, 0, 0))

while not done:
    # Updates
    delta_time = clock.tick() / 1000
    frame_rate = clock.get_fps()
    mouse_button = pygame.mouse.get_pressed()
    mouse_timer -= delta_time
    mousePos = pygame.mouse.get_pos()
    mouse_x = mousePos[0]
    mouse_y = mousePos[1]
    if mouse_timer <= 0:
        mouse_diff_x = mousePos[0]
        mouse_diff_y = mousePos[1]
        mouse_timer = mouse_delay

    if not pause:
        if not drag:
            shape_timer -= delta_time
        if first_shape:
            shape_radius, shape_points, origin_x, origin_y, orientation = util.create_shape(win_w, win_h)
        if shape_timer <= 0:
            win.fill((0, 0, 0))
            shape_radius, shape_points, origin_x, origin_y, orientation = util.create_shape(win_w, win_h)
            shape_timer = shape_delay
        if not drag:
            orientation += rotation_speed * delta_time
    hover = util.inside(shape_points, origin_x, origin_y, shape_radius, orientation, mouse_x, mouse_y)

    # Font Message Updates
    line1 = font.render("FPS: " + str((round(frame_rate, 0))) + " (F1 to pause)", False, (100, 100, 0), (0, 0, 0))
    # converting frame_rate to int led to crash when pausing
    # error that infinity could not be converted to integer
    line3 = font.render("Rotation: " + str(int(orientation)), False, (100, 100, 0), (0, 0, 0))
    line4 = font.render("Time until respawn: " + str(round(shape_timer, 1)) + " (space to trigger now)", False, (100, 100, 0), (0, 0, 0))

    # Input
    # Event Handling
    event = pygame.event.poll()
    # Quit and Pause Keys
    if event.type == pygame.QUIT:
        done = True
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            done = True
        elif event.key == pygame.K_F1:
            if not pause:
                pause = True
            else:
                pause = False
        # Manually Spawn New Shape
        elif event.key == pygame.K_SPACE:
            win.fill((0, 0, 0))
            shape_radius, shape_points, origin_x, origin_y, orientation = util.create_shape(win_w, win_h)
            shape_timer = shape_delay
    elif event.type == pygame.MOUSEMOTION and mouse_button[0] and hover:
        drag = True
        origin_x += event.rel[0]
        origin_y += event.rel[1]

    # Click and Drag // Device Polling
#    if hover and mouse_button[0]:
#        origin_x = origin_x + (mouse_x - mouse_diff_x)
#        origin_y = origin_y + (mouse_y - mouse_diff_y)
#        drag = True
    # The user is no longer holding down the mouse button
    if event.type == pygame.MOUSEBUTTONUP:
        drag = False

    # Drawing
    # Font Message Drawing
    win.blit(line1, (0, 0))
    win.blit(line2, (0, 18))
    win.blit(line3, (0, 36))
    win.blit(line4, (0, 54))
    # Shape Drawing
    if first_shape:
        util.draw_shape(shape_points, origin_x, origin_y, shape_radius, orientation, win, hover)
        first_shape = False
    util.draw_shape(shape_points, origin_x, origin_y, shape_radius, orientation, win, hover)
    win.fill((0, 0, 0))