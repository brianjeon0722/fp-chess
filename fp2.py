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

def check_guess(computer_opening, guesses):
    initial_guess = get_guess('What opening is this? ')
    opening_name = computer_opening.get('name')
    line_name = computer_opening.get('line_name')

    if line_name == None: # if no lines
        full_name = computer_opening["name"]
        if opening_name in initial_guess:
            correct(full_name, guesses)
        else:
            guesses += 1
            print(f'Not quite. You have {3 - guesses} more attempt(s).\n')
            if guesses >= 3:
                print(f'This is the {full_name}.\n')
            return False, guesses

    else: # if lines exist
        full_name = f'{computer_opening["name"]} {line_name}'
        if opening_name in initial_guess or line_name in initial_guess:
            if line_name in initial_guess:
                correct(full_name, guesses)
            elif opening_name in initial_guess:
                line_guess = get_guess(f'What line of the {opening_name} is this? ')
                if line_name in line_guess:
                    correct(full_name, guesses)
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
        computer_opening = random.choice(openings)

        print(f'### Game {times_played} ###')
        board = chess.Board()
        for move in computer_opening['moves']:
            board.push_san(move)
            print(board)
            print('\n')

        check_guess(computer_opening, guesses)
        times_played += 1

def main():
    games = int(input('How many times would you like to play? ').strip())
    play_game(games)

main()
