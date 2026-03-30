import chess
import random

board = chess.Board()

openings = [{
    'name': 'Sicilian',
    'line_name': 'Najdorf',
    'moves': ['e4', 'c5', 'Nf3']}, {
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
    guess = str(input('What opening is this? ').lower().strip())
    if computer_opening['name'].lower().strip() in guess.split(' '):
        print('Correct!')
        break
    else:
         guesses += 1
         print(f'Not quite. You have {3 - guesses} more attempt(s)')


