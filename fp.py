import chess
import random
from openings import openings_list

openings = openings_list

def get_guess(question):
    return str(input(question)).lower().strip()

def correct(full_name, guesses):
    print(f'Correct! This is the {full_name}.\n')
    return True, guesses

def correct(full_name, guesses):
    print(f'Correct! This is the {full_name}.\n')
    return True, guesses  # already does this, good

def check_guess(computer_opening, guesses):
    initial_guess = get_guess('What opening is this? ').lower()
    opening_name = computer_opening.get('name').lower()
    line_name = computer_opening.get('line_name').lower()

    if line_name is None:
        full_name = computer_opening["name"]
        if opening_name in initial_guess:
            return correct(full_name, guesses)  # ← return the result
        else:
            guesses += 1
            print(f'Not quite. You have {3 - guesses} more attempt(s).\n')
            if guesses >= 3:
                print(f'This is the {full_name}.\n')
            return False, guesses

    else:
        full_name = f'{computer_opening["name"]} {computer_opening["line_name"]}'
        if line_name in initial_guess:
            return correct(full_name, guesses)  # ← return the result
        elif opening_name in initial_guess:
            line_guess = get_guess(f'What line of the {opening_name} is this? ')
            if line_name in line_guess:
                return correct(full_name, guesses)  # ← return the result
            else:
                guesses += 1
                print(f'Not quite. You have {3 - guesses} more attempt(s).\n')
                if guesses >= 3:
                    print(f'This is the {full_name}.\n')
                return False, guesses
        else:
            guesses += 1
            print(f'Not quite. You have {3 - guesses} more attempt(s).\n')
            if guesses >= 3:
                print(f'This is the {full_name}.\n')
            return False, guesses


def play_game(games):
    times_played = 0
    wins = 0
    losses = 0

    while times_played < games:
        guesses = 0
        solved = False
        computer_opening = random.choice(openings)

        print(f'### Game {times_played + 1} ###')
        board = chess.Board()
        for move in computer_opening['moves']:
            board.push_san(move)
            print(board)
            print()

        while not solved and guesses < 3:
            solved, guesses = check_guess(computer_opening, guesses)

        if solved:
            wins += 1
        else:
            losses += 1

        times_played += 1

    print(f'### Results ###')
    print(f'You won {wins}/{wins + losses}')

def main():
    games = int(input('How many times would you like to play? ').strip())
    play_game(games)

if __name__ == '__main__':
    main()
