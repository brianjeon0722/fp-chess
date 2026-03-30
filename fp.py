import chess
import random

board = chess.Board()

openings = [{
    'name': 'Sicilian',
    'line_name': 'Smith-Morra',
    'moves': ['e4', 'c5', 'd4', 'cxd4', 'c3']},
    {
    'name': 'Sicilian',
    'line_name': 'Nimzowitsch',
    'moves': ['e4', 'c5', 'Nf3', 'Nf6']},
    {
    'name': 'Sicilian',
    'line_name': 'Grand Prix',
    'moves': ['e4', 'c5', 'Nc3', 'Nc6', 'f4']},
    {
    'name': 'Scotch',
    'line_name': 'Traditional',
    'moves': ['e4', 'e5', 'Nf3', 'Nc6', 'd4']
    }
]

computer_opening = random.choice(openings)

for i in computer_opening['moves']:
    board.push_san(i)
    print(board)
    print('\n')
guesses = 0
while guesses < 3:
    initial_guess = str(input('What opening is this? ').lower().strip())
    if computer_opening['line_name'].lower().strip() == initial_guess:
        print(f'Correct! This is the {computer_opening['name']} {computer_opening['line_name']}.')
        break
    elif computer_opening['name'].lower().strip() == initial_guess:
        print(f'Correct! This is the {computer_opening['name']}.')
        line_guess = str(input(f'What line of the {computer_opening['name']} is this? ').lower().strip())
        if computer_opening['line_name'].lower().strip() == line_guess:
            print(f'Correct! This is the {computer_opening['name']} {computer_opening['line_name']}')
            break
        else:
            guesses += 1
            print(f'Not quite. You have {3 - guesses} more attempt(s).')
    else:
         guesses += 1
         print(f'Not quite. You have {3 - guesses} more attempt(s).')


