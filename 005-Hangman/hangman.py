import random
import string
from words import words
from hangman_visual import lives_visual_dict  # make sure this file exists and is updated

def get_valid_word(words):
    word = random.choice(words)
    while '-' in word or ' ' in word:
        word = random.choice(words)
    return word.upper()

def hangman():
    word = get_valid_word(words)
    word_letters = set(word)
    alphabet = set(string.ascii_uppercase)
    used_letters = set()

    lives = 7

    while len(word_letters) > 0 and lives > 0:
        print("\nYou have", lives, "lives left and have used these letters:", ' '.join(sorted(used_letters)))
        print(lives_visual_dict[lives])

        # Current guessed word display
        word_list = [letter if letter in used_letters else '-' for letter in word]
        print("Current word:", ' '.join(word_list))

        user_letter = input("Guess a letter: ").upper()

        if user_letter in alphabet - used_letters:
            used_letters.add(user_letter)
            if user_letter in word_letters:
                word_letters.remove(user_letter)
                print("Good guess!")
            else:
                lives -= 1
                print("Wrong guess. The letter", user_letter, "is not in the word.")
        elif user_letter in used_letters:
            print("You have already used that letter. Try a different one.")
        else:
            print("Invalid character. Please enter a letter (A-Z).")

    if lives == 0:
        print(lives_visual_dict[lives])
        print("You died! The word was:", word)
    else:
        print("Congratulations! You guessed the word:", word)

if __name__ == '__main__':
    hangman()
