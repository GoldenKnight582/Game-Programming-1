import pygame
import level_manager

pygame.init()
win_dim = (1000, 600)
win = pygame.display.set_mode(win_dim)
done = False
LM = level_manager.LevelManager(win)
while not done:
    LM.update()

    done = LM.handle_input()

    LM.draw()

pygame.quit()
