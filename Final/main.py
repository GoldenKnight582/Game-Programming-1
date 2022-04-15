import pygame
import classes
import math

# For hit detection between dots
def get_distance(x1, y1, x2, y2):
    if x2 > x1:
        adjacent = x2 - x1
    elif x1 > x2:
        adjacent = x1 - x2
    if y2 > y1:
        opposite = y2 - y1
    elif y1 > y2:
        opposite = y1 - y2

    distance = (opposite ** 2 + adjacent ** 2) ** 0.5

    return distance


pygame.init()

win_dim = (800, 600)
win = pygame.display.set_mode(win_dim)
done = False
clock = pygame.time.Clock()
spinners = []
dots = []
font = pygame.font.SysFont("Century", 14)

while not done:
    delta_time = clock.tick() / 1000

    # Update
    for spinner in spinners:
        spinner.update(delta_time)
        # Create dots here and add them to one central dot list
        if spinner.dot_timer <= 0:
            new_dot = classes.Dot(spinner.apex[0], spinner.apex[1], win)
            new_dot.horizontal_speed = new_dot.speed * math.cos(math.radians(spinner.cur_angle))
            new_dot.vertical_speed = -new_dot.speed * math.sin(math.radians(spinner.cur_angle))
            dots.append(new_dot)
            spinner.dot_timer = spinner.dot_delay
        # Remove the spinner after two full rotations
        if spinner.rotation >= 720:
            spinners.remove(spinner)
    for dot in dots:
        dot.update(delta_time)
        # Hit Detection
        if dot.mode == "Dot":
            for dot2 in dots:
                if dot2.mode == "Dot":
                    if dot == dot2:
                        # Don't register a hit for checking the same dot
                        pass
                    else:
                        dist = get_distance(dot.x, dot.y, dot2.x, dot2.y)
                        if dist < dot.radius + dot2.radius:
                            # Turn into rings on hit
                            dot.end_x = dot.x
                            dot.end_y = dot.y
                            dot.mode = "Ring"
                            dot2.end_x = dot2.x
                            dot2.end_y = dot2.y
                            dot2.mode = "Ring"
        # Remove when the ring is totally black
        total_color = dot.rc1 + dot.rc2 + dot.rc3
        if total_color < 0:
            dots.remove(dot)

    # Input
    event = pygame.event.poll()
    # Quit Program
    if event.type == pygame.QUIT:
        done = True
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            done = True
    # Spawn Spinners
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            if len(spinners) < 4:
                mouse_pos = pygame.mouse.get_pos()
                new_spinner = classes.Spinner(mouse_pos[0], mouse_pos[1], win)
                spinners.append(new_spinner)
            elif len(spinners) == 4:
                # If there are 4 spinners, remove the oldest one and add a new one
                del spinners[0]
                mouse_pos = pygame.mouse.get_pos()
                new_spinner = classes.Spinner(mouse_pos[0], mouse_pos[1], win)
                spinners.append(new_spinner)

    # Draw
    win.fill((0, 0, 0))
    for spinner in spinners:
        spinner.draw()
    for dot in dots:
        dot.draw()
    # Text
    temp = font.render("# Spinners (4 max) :  " + str(len(spinners)), False, (255, 255, 0))
    win.blit(temp, (0, 0))
    temp = font.render("# Dots (no limit) :  " + str(len(dots)), False, (255, 255, 0))
    win.blit(temp, (win_dim[0] // 2 - temp.get_width() // 2, 0))
    pygame.display.flip()

