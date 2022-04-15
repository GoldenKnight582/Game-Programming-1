import pygame
import target
import player

# Pygame startup / create initial variables
pygame.init()
win_w = 800
win_h = 600
win = pygame.display.set_mode((win_w, win_h))
clock = pygame.time.Clock()
done = False
debug = True
paused = False
font = pygame.font.SysFont("Courier New", 16)       # Bad, but easy:-)

playfield_buffer = 10
playfield = pygame.Rect(playfield_buffer, playfield_buffer, win_w - playfield_buffer * 2, win_h - playfield_buffer * 2)
target_list = []
target_spawners = [target.TargetSpawner(0, 200, 100, 35), target.TargetSpawner(800, 600, -50, -100)]
p = player.Player(400, 300)

# GAME LOOP
while not done:
    # UPDATE
    delta_time = clock.tick() / 1000
    if paused:
        delta_time = 0
    # ... update the target spawners and targets
    for ts in target_spawners:
        ts.update(delta_time, playfield, target_list)
    for t in target_list:
        t.update(delta_time, playfield)
    # ... update the player
    p.update(delta_time, playfield)
    if p.hit_detection(target_list):
        # The player was hit and its health (i.e. radius) has reached 0.  End the game
        done = True

    # INPUT
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        done = True
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            done = True
        elif event.key == pygame.K_PAGEDOWN:
            playfield_buffer = max(playfield_buffer - 5, 0)
            playfield = pygame.Rect(playfield_buffer, playfield_buffer, win_w - playfield_buffer * 2,
                                    win_h - playfield_buffer * 2)
        elif event.key == pygame.K_PAGEUP:
            playfield_buffer = min(playfield_buffer + 5, win_h / 2 - 10)
            playfield = pygame.Rect(playfield_buffer, playfield_buffer, win_w - playfield_buffer * 2,
                                    win_h - playfield_buffer * 2)
        elif event.key == pygame.K_F1:
            debug = not debug
        elif event.key == pygame.K_p:
            paused = not paused
    p.process_input(event)

    # DRAW
    win.fill((128, 128, 128))
    pygame.draw.rect(win, (0, 0, 0), playfield)
    for ts in target_spawners:
        ts.draw(win)
    for t in target_list:
        t.draw(win)
    p.draw(win)
    temps = font.render("Score: " + str(p.score), False, (255, 255, 255), (0, 0, 0))
    win.blit(temps, (win_w // 2 - temps.get_width() // 2, win_h - temps.get_height()))
    if debug:
        text_lines = []
        text_lines.append("# Targets: " + str(len(target_list)))
        text_lines.append("# Bullets: " + str(len(p.bullet_list)))
        # You can comment this out if not doing gamepad stuff
        if p.used_keyboard_last:
            text_lines.append("Using mouse and keyboard controls")
        else:
            text_lines.append("Using gamepad")
        y = 0
        for line in text_lines:
            temps = font.render(line, False, (255, 255, 0), (0, 0, 0))
            win.blit(temps, (400, y))
            y += temps.get_height() + 3
    if paused:
        temps = font.render("- PAUSED -", False, (128,128,128), (0,0,0))
        win.blit(temps, ((win_w - temps.get_width()) // 2, (win_h - temps.get_height()) // 2))

    pygame.display.flip()


# SHUTDOWN
pygame.quit()