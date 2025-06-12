import os 
from helpers import check_turn, check_for_win, draw_board

spots = {
    1 : 'p1',2 :'p2', 3:'p3',4:'p4',5:'p5',6:'p6',7:'p7',8:'p8', 9:'p9'
}
playing, complete = True, False

turn = 0
prev_turn = -1

#Game Loop
while playing  :
    os.system('cls' if os.name =='nt' else 'clear')
    #Draw the current board
    draw_board (spots)
    if prev_turn == turn:
        print("Invalid spot selected, Choose another spot.")
    prev_turn = turn
    print("Players "+str((turn%2)+1)+ " 's turn:Pick your spot or press q to quit")
    
    choice = input()
    if choice == 'q':
        playing = False

    elif str.isdigit(choice) and int(choice) in spots:
        if not spots[int(choice)] in {" X","    O" }:
            turn +=1
            spots[int(choice)] = check_turn(turn)

    if check_for_win(spots): playing, complete =False, True
    if turn > 8: playing = False

os.system ('cls' if os.name =='nt' else 'clear')
draw_board(spots)

if complete :
    if check_turn(turn) =='X':print("Player 1 Wins!")
    else : print("Player 2 Wins!")

else:
    print("NO Winner")

print("Thanks for playing!")

