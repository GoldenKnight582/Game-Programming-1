# Tyler Cobb
# ETGG1801-05 Lab 07
import pygame

def create_board():
    """ The list created by this function are arranged as follows:

      0  | 1  | 2  | 3  | 4  | 5  | 6
      ---+----+----+----+----+----+----
      7  | 8  | 9  | 10 | 11 | 12 | 13
      ---+----+----+----+----+----+----
      14 | 15 | 16 | 17 | 18 | 19 | 20
      ---+-----+-----+----+----+----+----
      21 | 22 | 23 | 24 | 25 | 26 | 27
      ---+----+----+----+----+----+----
      28 | 29 | 30 | 31 | 32 | 33 | 34
      ---+----+----+----+----+----+----
      35 | 36 | 37 | 38 | 39 | 40 | 41
      ---+----+----+----+----+----+----
      42 | 43 | 44 | 45 | 46 | 47 | 48

      This method creates the initial board state (with the players owning two opposing corners)
    """
    state = [0] * 49
    state[0] = state[48] = 1
    state[6] = state[42] = 2
    return state



def get_square_index(col_num, row_num):
    """
    :param col_num: the column number (0 - 6)
    :param row_num: the row number (0 - 6)
    :return: the square index (as seen in the docstring for create_board)
    """
    square_index = 7 * row_num + col_num
    return square_index


def pixel_to_row(surf, pixel_y):
    """
    :param surf: the surface we'll be drawing to (possibly the window)
    :param pixel_y: a y-coordinate (possibly the mouse position)
    :return: The row number (0 - 6)
    """
    surf_height = surf.get_height()
    row_height = round(surf_height / 7, 0)

    if pixel_y <= row_height:
        row = 0
    elif pixel_y <= row_height * 2:
        row = 1
    elif pixel_y <= row_height * 3:
        row = 2
    elif pixel_y <= row_height * 4:
        row = 3
    elif pixel_y <= row_height * 5:
        row = 4
    elif pixel_y <= row_height * 6:
        row = 5
    elif pixel_y <= row_height * 7:
        row = 6

    return row


def pixel_to_column(surf, pixel_x):
    """
    :param surf: the surface we'll be drawing to (possibly the window)
    :param pixel_x: a x-coordinate (possibly the mouse position)
    :return: The column number (0 - 6)
    """
    surf_width = surf.get_width()
    col_width = round(surf_width / 7, 0)

    if pixel_x <= col_width:
        col = 0
    elif pixel_x <= col_width * 2:
        col = 1
    elif pixel_x <= col_width * 3:
        col = 2
    elif pixel_x <= col_width * 4:
        col = 3
    elif pixel_x <= col_width * 5:
        col = 4
    elif pixel_x <= col_width * 6:
        col = 5
    elif pixel_x <= col_width * 7:
        col = 6

    return col


def index_to_row(index):
    """
    :param index: a square index (0 - 48)
    :return: the row number (0 - 6)
    """
    if index <= 6:
        row = 0
    elif index <= 13:
        row = 1
    elif index <= 20:
        row = 2
    elif index <= 27:
        row = 3
    elif index <= 34:
        row = 4
    elif index <= 41:
        row = 5
    elif index <= 48:
        row = 6

    return row


def index_to_column(index):
    """
    :param index: a square index (0 - 48)
    :return: the column number (0 - 6)
    """
    if index % 7 == 0:
        col = 0
    elif index % 7 == 1:
        col = 1
    elif index % 7 == 2:
        col = 2
    elif index % 7 == 3:
        col = 3
    elif index % 7 == 4:
        col = 4
    elif index % 7 == 5:
        col = 5
    elif index % 7 == 6:
        col = 6

    return col


def get_available_start_moves(bstate, player_num):
    """
    :param bstate: the board state list
    :param player_num: usually 1 or 2
    :return: a list of square index numbers where the given player can start a move (which is equivalent to the
              spots where that player owns the token)
    """
    available_start_moves = []
    for i in range(len(bstate)):
        if bstate[i] == player_num:
            available_start_moves.append(i)

    return available_start_moves


def get_available_moves(bstate, start_index):
    """
    :param bstate: the board state list
    :param start_index: The square index (0 - 48) where the player has initiated a move
    :return: a list of square indicies (0 - 48) where the player can move two (+/- 2 squares)
    """
    available_moves = []
    row = index_to_row(start_index)
    col = index_to_column(start_index)
    c = -2

    while c <= 2:
        if 0 <= col + c <= 6:
            if bstate[get_square_index(col + c, row - 2)] == 0:
                available_moves.append(get_square_index(col + c, row - 2))
            if bstate[get_square_index(col + c, row - 1)] == 0:
                available_moves.append(get_square_index(col + c, row - 1))
            if bstate[get_square_index(col + c, row)] == 0:
                available_moves.append(get_square_index(col + c, row))
            if row + 1 <= 6:
                if bstate[get_square_index(col + c, row + 1)] == 0:
                    available_moves.append(get_square_index(col + c, row + 1))
            if row + 2 <= 6:
                if bstate[get_square_index(col + c, row + 2)] == 0:
                    available_moves.append(get_square_index(col + c, row + 2))

        c += 1

    for i in range(len(available_moves) - 1, -1, -1):
        if available_moves[i] < 0:
            del available_moves[i]

    return available_moves


def make_move(bstate, player_num, start_index, end_index):
    """
    Actually makes the move given.  Infects tokens near the destination and hops the starting token (if applicable)
    :param bstate: the board state list
    :param player_num: usually 1 or 2
    :param start_index: The square index (0 - 48) where the current player is starting their move
    :param end_index: The square index (0 - 48) where the current player is moving that token to
    :return: None.
    """
    col = index_to_column(start_index)
    row = index_to_row(start_index)
    endcol = index_to_column(end_index)
    endrow = index_to_row(end_index)
    one_step_range = []
    infect_range = []
    two_step_range = []

    c = -1
    while c <= 1:
        if 0 <= col + c <= 6:
            if bstate[get_square_index(col + c, row - 1)] == 0:
                one_step_range.append(get_square_index(col + c, row - 1))
            if bstate[get_square_index(col + c, row)] == 0:
                one_step_range.append(get_square_index(col + c, row))
            if row + 1 <= 6:
                if bstate[get_square_index(col + c, row + 1)] == 0:
                    one_step_range.append(get_square_index(col + c, row + 1))
        c += 1

    for i in range(len(one_step_range) - 1, -1, -1):
        if one_step_range[i] < 0:
            del one_step_range[i]

    c = -1
    if player_num == 1:
        # Player 2 owned spaces enter the range
        while c <= 1:
            if 0 <= endcol + c <= 6:
                if bstate[get_square_index(endcol + c, endrow - 1)] == 2:
                    infect_range.append(get_square_index(endcol + c, endrow - 1))
                if bstate[get_square_index(endcol + c, endrow)] == 2:
                    infect_range.append(get_square_index(endcol + c, endrow))
                if endrow + 1 <= 6:
                    if bstate[get_square_index(endcol + c, endrow + 1)] == 2:
                        infect_range.append(get_square_index(endcol + c, endrow + 1))
            c += 1
    if player_num == 2:
        # Player 1 owned spaces enter the range
        while c <= 1:
            if 0 <= endcol + c <= 6:
                if bstate[get_square_index(endcol + c, endrow - 1)] == 1:
                    infect_range.append(get_square_index(endcol + c, endrow - 1))
                if bstate[get_square_index(endcol + c, endrow)] == 1:
                    infect_range.append(get_square_index(endcol + c, endrow))
                if endrow + 1 <= 6:
                    if bstate[get_square_index(endcol + c, endrow + 1)] == 1:
                        infect_range.append(get_square_index(endcol + c, endrow + 1))
            c += 1

    for i in range(len(infect_range) - 1, -1, -1):
        if infect_range[i] < 0:
            del infect_range[i]

    c = -2
    while c <= 2:
        if 0 <= col + c <= 6:
            if c == -2 or c == 2:
                if bstate[get_square_index(col + c, row - 2)] == 0:
                    two_step_range.append(get_square_index(col + c, row - 2))
                if bstate[get_square_index(col + c, row - 1)] == 0:
                    two_step_range.append(get_square_index(col + c, row - 1))
                if bstate[get_square_index(col + c, row)] == 0:
                    two_step_range.append(get_square_index(col + c, row))
                if row + 1 <= 6:
                    if bstate[get_square_index(col + c, row + 1)] == 0:
                        two_step_range.append(get_square_index(col + c, row + 1))
                if row + 2 <= 6:
                    if bstate[get_square_index(col + c, row + 2)] == 0:
                        two_step_range.append(get_square_index(col + c, row + 2))
            else:
                if bstate[get_square_index(col + c, row - 2)] == 0:
                    two_step_range.append(get_square_index(col + c, row - 2))
                if 0 <= row + 2 <= 6:
                    if bstate[get_square_index(col + c, row + 2)] == 0:
                        two_step_range.append(get_square_index(col + c, row + 2))
        c += 1

    for i in range(len(two_step_range) - 1, -1, -1):
        if two_step_range[i] < 0:
            del two_step_range[i]

    if player_num == 1:
        # Determine if the move is one step
        for i in range(len(one_step_range)):
            # If it is, then place a token on that spot
            if end_index == one_step_range[i]:
                bstate[end_index] = 1
            # And flip any of the other player's tokens around it
            for i in range(len(infect_range)):
                infect_square = infect_range[i]
                if bstate[infect_square] == 2:
                    bstate[infect_square] = 1
        # Determine if the move is two steps
        for i in range(len(two_step_range)):
            # If it is, pick up the token and move it to that spot
            if end_index == two_step_range[i]:
                bstate[start_index] = 0
                bstate[end_index] = 1
            # And flip any of the other player's tokens around it
            for i in range(len(infect_range)):
                infect_square = infect_range[i]
                if bstate[infect_square] == 2:
                    bstate[infect_square] = 1
    # Case for if it's Player Two's move
    elif player_num == 2:
        # Determine if the move is one step
        for i in range(len(one_step_range)):
            # If it is, then place a token on that spot
            if end_index == one_step_range[i]:
                bstate[end_index] = 2
            # And flip any of the other player's tokens around it
            for i in range(len(infect_range)):
                infect_square = infect_range[i]
                if bstate[infect_square] == 1:
                    bstate[infect_square] = 2
        # Determine if the move is two steps
        for i in range(len(two_step_range)):
            # If it is, pick up the token and move it to that spot
            if end_index == two_step_range[i]:
                bstate[start_index] = 0
                bstate[end_index] = 2
            # And flip any of the other player's tokens around it
            for i in range(len(infect_range)):
                infect_square = infect_range[i]
                if bstate[infect_square] == 1:
                    bstate[infect_square] = 2


def get_scores(bstate):
    """
    :param bstate: the board state list
    :return: a tuple of the score of each player (player1_score, player2_score)
    """
    player1_score = 0
    player2_score = 0

    for i in range(len(bstate)):
        if bstate[i] == 1:
            player1_score += 1
        elif bstate[i] == 2:
            player2_score += 1

    return player1_score, player2_score




def does_player_have_move(bstate, player_num):
    """
    :param bstate: the board state list
    :param player_num: usually 1 or 2
    :return: True if the given player can make a move
    """
    # Begin by assuming the player has no tokens
    has_token = False

    if player_num == 1:
        # Look at each state on the board
        for i in range(len(bstate)):
            # See if there are any red pieces
            if bstate[i] == 1:
                has_token = True
                break
    elif player_num == 2:
        for i in range(len(bstate)):
            # See if there are any yellow pieces
            if bstate[i] == 2:
                has_token = True
                break

    # If the loop determines that one of the players is out of tokens, no more moves can be made.
    if has_token:
        can_move = True
    else:
        can_move = False

    return can_move


def is_valid_move_start(bstate, player_num, square_index):
    """
    :param bstate: the board state list
    :param player_num: usually 1 or 2
    :param square_index: Can the current player start a move at the given square index (0 - 48).  In other words, does
                    the player own that square?
    :return:
    """
    if bstate[square_index] == player_num:
        valid_start = True
    else:
        valid_start = False

    return valid_start


def is_valid_move_end(bstate, start_square_index, end_square_index):
    """
    :param bstate: the board state list
    :param player_num: usually 1 or 2
    :param start_square_index: A square index (0 - 48) where the move would start
    :param end_square_index: A square index (0 - 48) where the move would end
    :return: True if the player could make that move.  This method does not actually make that move (use make_move)
                for that.
    """
    available_moves = get_available_moves(bstate, start_square_index)
    for i in range(len(available_moves)):
        if end_square_index == available_moves[i]:
            valid_move_end = True
            break
        else:
            valid_move_end = False

    return valid_move_end


def draw_board(bstate, surf, selected_square=None):
    """
    Erases and draws the board to the given surface
    :param bstate: the board state list
    :param surf: the surface to draw to
    :param selected_square: If None, just draw the board as normal.  If selected_square is a square index (0 - 48),
                   highlight the squares we could move to from selected_square
    :return: None
    """
    surf.fill((0, 0, 0))
    surf_width = surf.get_width()
    surf_height = surf.get_height()

    xlist = []
    ylist = []
    circ_xlist = []
    circ_ylist = []

    if selected_square is None:
        pass
    else:
        available_moves = get_available_moves(bstate, selected_square)

    column_width = round(surf_width / 7, 0)
    row_height = round(surf_height / 7, 0)

    for cur_row in range(7):
        # Create a single row of tokens
        y = cur_row * row_height
        for cur_col in range(7):
            x = cur_col * column_width
            xlist.append(x)
            ylist.append(y)

    for cur_row in range(7):
        # Create a single row of tokens
        y = (cur_row + 0.5) * row_height
        for cur_col in range(7):
            x = (cur_col + 0.5) * column_width
            circ_xlist.append(x)
            circ_ylist.append(y)

    for i in range(len(bstate)):
        if i % 2 == 0:
            if selected_square is not None:
                if i in available_moves:
                    if bstate[selected_square] == 1:
                        pygame.draw.rect(surf, (140, 100, 100), (xlist[i], ylist[i], column_width, row_height))
                    elif bstate[selected_square] == 2:
                        pygame.draw.rect(surf, (140, 140, 100), (xlist[i], ylist[i], column_width, row_height))
                else:
                    pygame.draw.rect(surf, (100, 100, 100), (xlist[i], ylist[i], column_width, row_height))
            else:
                pygame.draw.rect(surf, (100, 100, 100), (xlist[i], ylist[i], column_width, row_height))
        elif i % 2 > 0:
            if selected_square is not None:
                if i in available_moves:
                    if bstate[selected_square] == 1:
                        pygame.draw.rect(surf, (90, 50, 50), (xlist[i], ylist[i], column_width, row_height))
                    elif bstate[selected_square] == 2:
                        pygame.draw.rect(surf, (90, 90, 50), (xlist[i], ylist[i], column_width, row_height))
                else:
                    pygame.draw.rect(surf, (50, 50, 50), (xlist[i], ylist[i], column_width, row_height))

            else:
                pygame.draw.rect(surf, (50, 50, 50), (xlist[i], ylist[i], column_width, row_height))
        if bstate[i] == 1:
            pygame.draw.circle(surf, (255, 0, 0), (int(circ_xlist[i]), int(circ_ylist[i])), min(int(row_height / 2), int(column_width / 2)))
        elif bstate[i] == 2:
            pygame.draw.circle(surf, (255, 255, 0), (int(circ_xlist[i]), int(circ_ylist[i])), min(int(row_height / 2), int(column_width / 2)))

