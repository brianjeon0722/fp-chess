import chess
import random

openings = [{
    'name': 'Sicilian',
    'line_name': 'Smith-Morra',
    'moves': ['e4', 'c5', 'd4', 'cxd4', 'c3']},
    {
    'name': 'Sicilian',
    'line_name': 'Accelerated Dragon',
    'moves': ['e4', 'c5', 'Nf3', 'Nc6' 'd4', 'cxd4', 'Nxd4', 'g6']},
    {
    'name': 'Sicilian',
    'line_name': 'Dragon',
    'moves': ['e4', 'c5', 'Nf3', 'd6', 'd4', 'cxd4', 'Nxd4', 'Nf6', 'Nc3', 'g6']},
    {
    'name': 'Sicilian',
    'line_name': 'Grand Prix',
    'moves': ['e4', 'c5', 'Nc3', 'Nc6' 'f4']},
    {
    'name': 'Ruy Lopez',
    'moves': ['e4', 'e5', 'Nf3', 'Nc6', 'Bb5']},
    {
    'name': 'Scotch',
    'moves': ['e4', 'e5', 'Nf3', 'Nc6', 'd4']
    }
]


def get_guess(question):
    return str(input(question)).lower().strip()

def correct(full_name, guesses):
    print(f'Correct! This is the {full_name}.\n')
    return True, guesses

def correct(full_name, guesses):
    print(f'Correct! This is the {full_name}.\n')
    return True, guesses  # already does this, good

def check_guess(computer_opening, guesses):
    initial_guess = get_guess('What opening is this? ')
    opening_name = computer_opening.get('name')
    line_name = computer_opening.get('line_name')

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
        full_name = f'{computer_opening["name"]} {line_name}'
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

    while times_played < games:
        guesses = 0
        solved = False
        computer_opening = random.choice(openings)

        print(f'### Game {times_played + 1} ###')  # ← +1 so it starts at 1
        board = chess.Board()
        for move in computer_opening['moves']:
            board.push_san(move)
            print(board)
            print('\n')

        while not solved and guesses < 3:  # ← keep asking until solved or out of guesses
            solved, guesses = check_guess(computer_opening, guesses)

        times_played += 1

def main():
    games = int(input('How many times would you like to play? ').strip())
    play_game(games)

main()
