# Tyler Cobb
# ETGG1801-05 Lab 07
import pygame
import random
import lab07_util as util


# Pygame init
pygame.init()
win_w = 600
win_h = 600
win = pygame.display.set_mode((win_w, win_h))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Courier New", 16)

# Game variables
board = util.create_board()
game_over = False
current_turn = 1
state = "select start square"
start_square = None
ai_timer = random.uniform(1.0, 2.5)
p1_score = 2
p2_score = 2

# Game Loop
while not game_over:
    # Updates
    delta_time = clock.tick() / 1000
    if current_turn == 2:
        ai_timer -= delta_time
    # ... make sure both players can move.  If not, the game is over
    if not util.does_player_have_move(board, 1) or not util.does_player_have_move(board, 2):
        current_turn = 3
    # ... make the ai move (if doing the bonus)
    if current_turn == 2:
        index = random.randint(0, 48)
        if state == "select start square" and util.is_valid_move_start(board, current_turn, index):
            if ai_timer <= 0:
                state = "select destination square"
                start_square = index
                ai_timer = random.uniform(1.0, 2.5)
        elif state == "select destination square" and util.is_valid_move_end(board, start_square, index):
            if ai_timer <= 0:
                util.make_move(board, current_turn, start_square, index)
                current_turn = 3 - current_turn        # <= neat trick to change to the other player, huh?
                start_square = None
                state = "select start square"
                ai_timer = random.uniform(1.0, 2.5)

    # Input
    evt = pygame.event.poll()
    # ... event-handling
    if evt.type == pygame.QUIT:
        game_over = True
    if evt.type == pygame.MOUSEBUTTONDOWN and current_turn == 1:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        row = util.pixel_to_row(win, mouse_y)
        col = util.pixel_to_column(win, mouse_x)
        index = util.get_square_index(col, row)
        if state == "select start square" and util.is_valid_move_start(board, current_turn, index):
            state = "select destination square"
            start_square = index
        elif state == "select destination square" and util.is_valid_move_end(board, start_square, index):
            util.make_move(board, current_turn, start_square, index)
            current_turn = 3 - current_turn
            start_square = None
            state = "select start square"
        else:
            start_square = None
            state = "select start square"
    # ... device-polling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        game_over = True

    # Drawing
    util.draw_board(board, win, start_square)
    if current_turn != 3:
        temps = font.render("Player" + str(current_turn) + ": " + state, False, (255, 255, 255))
        win.blit(temps, (0, 0))
    p1_score, p2_score = util.get_scores(board)
    temps = font.render("Player 1 (human): " + str(p1_score), False, (255, 0, 0), (0, 0, 0))
    win.blit(temps, (0, win_h - 16))
    temps = font.render("Player 2 (ai): " + str(p2_score), False, (255, 255, 0), (0, 0, 0))
    win.blit(temps, (400, win_h - 16))
    if current_turn == 3:
        if p1_score > p2_score:
            text = "Human (Player1) wins!"
            color = (255, 0, 0)
        elif p2_score > p1_score:
            text = "AI (Player2) wins!"
            color = (255, 255, 0)
        else:
            text = "It's a Draw!"
            color = (255, 255, 255)
        temps = font.render(text, False, color, (0, 0, 0))
        win.blit(temps, ((win_w - temps.get_width()) // 2, (win_h - temps.get_height()) // 2))
    pygame.display.flip()

# Shutdown
pygame.quit()