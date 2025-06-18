import random

def play():
    user = input("What's your choice? 'r' for rock, 'p' for paper, 's' for scissors:\n ")
    computer = random.choice(['r', 'p', 's'])

    if user ==computer:
        return "It's a tie! You both chose " + user + "."
    
    if is_win(user, computer):
        return "You win! " + user + " beats " + computer + "."
    
    if is_win(computer, user):
        return "You lose! " + computer + " beats " + user + "."
    
def is_win(player, opponent):
    if (player == 'r' and opponent == 's') or \
            (player == 'p' and opponent == 'r') or \
            (player == 's' and opponent == 'p'):
        return True
    
print(play())