def draw_board(spots):
    board = (f"| {spots[1]} | {spots[2]} | {spots[3]} |\n"
             f"| {spots[4]} | {spots[5]} | {spots[6]} |\n"
             f"| {spots[7]} | {spots[8]} | {spots[9]} |\n")
    print(board)
def check_turn(turn):
    if turn % 2 == 0:
        return " X"
    else:
        return "    O"
def check_for_win(spots):
    win_conditions = [
        (1, 2, 3), (4, 5, 6), (7, 8, 9),  # Horizontal
        (1, 4, 7), (2, 5, 8), (3, 6, 9),  # Vertical
        (1, 5, 9), (3, 5, 7)              # Diagonal
    ]
    
    for a, b, c in win_conditions:
        if spots[a] == spots[b] == spots[c] and spots[a] not in {'1', '2', '3', '4', '5', '6', '7', '8', '9'}:
            return True
    return False
    