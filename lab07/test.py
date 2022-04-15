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
        if col + c >= 0:
            if bstate[get_square_index(col + c, row - 2)] == 0:
                available_moves.append(get_square_index(col + c, row - 2))
            if bstate[get_square_index(col + c, row - 1)] == 0:
                available_moves.append(get_square_index(col + c, row - 1))
            if bstate[get_square_index(col + c, row)] == 0:
                available_moves.append(get_square_index(col + c, row))
            if bstate[get_square_index(col + c, row + 1)] == 0:
                available_moves.append(get_square_index(col + c, row + 1))
            if bstate[get_square_index(col + c, row + 2)] == 0:
                available_moves.append(get_square_index(col + c, row + 2))

        c += 1

    for i in range(len(available_moves) - 1, -1, -1):
        if available_moves[i] < 0:
            del available_moves[i]

    return row, col, available_moves

bstate = create_board()
row, col, available = get_available_moves(bstate, 25)
print("Row is " + str(row))
print("Col is " + str(col))
print(available)