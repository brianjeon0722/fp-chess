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

def check_guess(computer_opening):
    initial_guess = get_guess('What opening is this? ')
    opening_name = computer_opening['name'].lower()
    line_name = computer_opening['line_name'].lower()

    if opening_name in initial_guess or line_name in initial_guess:
        if line_name in initial_guess:
            print(f'Correct! This is the {full_name}.\n')
        if opening_name in initial_guess:
            line_guess = get_guess(f'What line of the {opening_name} is this? ')
            if line_name in line_guess:
                print(f'Correct! This is the {full_name}.\n')
    else:
        guesses += 1
        print(f'Not quite. You have {3 - guesses} more attempt(s).\n')
        if guesses >= 3:
            print(f'This is the {full_name}.\n')




# Sicilian Accelerated Dragon
# The Sicilian Accelerated Dragon

# sicilian

# accelerated


def play_game(games):
    times_played = 0

    while times_played < games:
        computer_opening = random.choice(openings)
        print(f'### Game {times_played} ###')
        board = chess.Board()
        for move in computer_opening['moves']:
            board.push_san(move)
            print(board)
            print('\n')



def main():
    games = int(input('How many times would you like to play? ').strip())
    play_game(games)

games = int(input('How many times would you like to play? ').strip())

times_played = 0
wins = 0

while times_played < games:

    times_played += 1

    computer_opening = random.choice(openings)

    print(f'### Game {times_played} ###')
    board = chess.Board() # reset chess board

    for i in computer_opening['moves']:
        board.push_san(i)
        print(board)
        print('\n')

    guesses = 0

    while guesses < 3:
        initial_guess = str(input('What opening is this? ')).lower().strip()

        if computer_opening.get('line_name') is not None:

            if computer_opening['line_name'].lower().strip() == initial_guess:
                print(f'Correct! This is the {computer_opening["name"]} {computer_opening["line_name"]}.\n')
                wins += 1
                break

            elif computer_opening['name'].lower().strip() == initial_guess:
                line_guess = str(input(f'What line of the {computer_opening["name"]} is this? ')).lower().strip()

                if computer_opening['line_name'].lower().strip() == line_guess:
                    print(f'Correct! This is the {computer_opening["name"]} {computer_opening["line_name"]}.\n')
                    wins += 1
                    break

                else:
                    guesses += 1
                    print(f'Not quite. You have {3 - guesses} more attempt(s).\n')
                    if guesses >= 3:
                        print(f'This is the {computer_opening["name"]} {computer_opening["line_name"]}.\n')

            else:
                guesses += 1
                print(f'Not quite. You have {3 - guesses} more attempt(s).\n')
                if guesses >= 3:
                    print(f'This is the {computer_opening["name"]} {computer_opening["line_name"]}.\n')

        else:
            if computer_opening['name'].lower().strip() == initial_guess:
                print(f'Correct! This is the {computer_opening["name"]}.\n')
                wins += 1
                break
            else:
                guesses += 1
                print(f'Not quite. You have {3 - guesses} more attempt(s).\n')
                if guesses >= 3:
                    print(f'This is the {computer_opening["name"]}.\n')


print(f'You got {wins}/{games} correct!')
