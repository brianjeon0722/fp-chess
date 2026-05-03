import chess
import random
from opening_lines import openings_list
from opening_only import openings_only

# get information on the number of games, variation vs. opening, and mcq vs. free response
def start():
    while True:
        try:
            games = int(input('How many times would you like to play? ').strip())
            break
        except ValueError:
            print("Please input a valid number.")

    while True:
        try:
            mode = int(input('Would you like to only guess openings or also variations? Type 1 for openings only and type 2 for openings and variations: '
            ' ').strip())

            if mode not in (1, 2):
                print('Please enter 1 or 2!')
                continue
            break

        except ValueError:
            print('Please input a valid number.')

    while True:
        try:
            answer_type = int(input('Type 1 for MCQ answers or 2 for short answer: '))

            if answer_type not in (1, 2):
                print('Please enter 1 or 2!')
                continue
            break
        except ValueError:
            print('Please input a valid number.')

    while True:
        try:
            difficulty = int(input('Type 1 for Hard difficulty. Type 2 for Medium difficulty. Type 3 for Easy difficulty. '))

            if answer_type not in (1, 2, 3):
                print('Please enter 1, 2, or 3!')
                continue
            break
        except ValueError:
            print('Please input a valid number.')

    if mode == 1:
        opening = openings_only
    else:
        opening = openings_list

    opening = opening[difficulty-1]

    return games, opening, answer_type


# clean the input
def get_guess(question):
    return str(input(question)).lower().strip()

# function to check the answer of free response
def check_guess_short(computer_opening, guesses):
    initial_guess = get_guess('What opening is this? ').lower()
    opening_name = computer_opening.get('name').lower()
    line_name = computer_opening.get('line_name')

    # if only opening name exists
    if line_name is None:
        full_name = computer_opening["name"]
        if opening_name in initial_guess:
            print(f'Correct! This is the {full_name}.\n')
            return True, guesses
        else:
            guesses += 1
            print(f'Not quite. You have {3 - guesses} more attempt(s).\n')
            if guesses >= 3:
                print(f'This is the {full_name}.\n')
            return False, guesses # thanks Chat for this idea

    # if opening name and variation / line name exists
    else:
        line_name = line_name.lower()
        full_name = f'{computer_opening["name"]} {computer_opening["line_name"]}'

        # if the variation is guessed (we assume if you say Accelerated Dragon, you know this is the Sicilian Accelerated Dragon)
        if line_name in initial_guess:
            print(f'Correct! This is the {full_name}.\n')
            return True, guesses

        # if you just guess the opening but not the variation, we prompt you to guess the variation
        elif opening_name in initial_guess:
            line_guess = get_guess(f'What line of the {computer_opening["name"]} is this? ')

            if line_name in line_guess:
                print(f'Correct! This is the {full_name}.\n')
                return True, guesses
            else:
                guesses += 1
                print(f'Not quite. You have {3 - guesses} more attempt(s).\n')
                if guesses >= 3:
                    print(f'This is the {full_name}.\n')
                return False, guesses # thanks Chat for this idea
        else:
            guesses += 1
            print(f'Not quite. You have {3 - guesses} more attempt(s).\n')
            if guesses >= 3:
                print(f'This is the {full_name}.\n')
            return False, guesses # thanks Chat for this idea


# Claude helped with formatting the MCQ (particularly for the variation version)
def check_guess_mcq(computer_opening, opening, guesses, opening_correct_answer, opening_solved, line_correct_answer=None, line_mcq_shown=False):
    opening_name = computer_opening.get('name').lower()
    line_name = computer_opening.get('line_name')

    # if no variation
    if line_name is None:
        full_name = computer_opening["name"]
        initial_guess = get_guess('What opening is this? ').lower().strip()

        # this handles responding either in a. (a) or a or saying the actual opening (ex: a. Sicilian vs. a vs. Sicilian)
        if opening_name in initial_guess or initial_guess == opening_correct_answer:
            print(f'Correct! This is the {full_name}.\n')
            return True, guesses, True, line_correct_answer, line_mcq_shown

        #if wrong
        else:
            guesses += 1
            print(f'Not quite. You have {3 - guesses} more attempt(s).\n')
            if guesses >= 3:
                print(f'This is the {full_name}.\n')
            return False, guesses, False, line_correct_answer, line_mcq_shown

    # if variation
    line_name = line_name.lower()
    full_name = f'{computer_opening["name"]} {computer_opening["line_name"]}'

    # Phase 1: opening not solved yet
    if not opening_solved:
        initial_guess = get_guess('What opening is this? ').lower().strip()

        # if you for some reason don't answer the MCQ and just say the variation from the start
        if line_name in initial_guess:
            print(f'Correct! This is the {full_name}.\n')
            return True, guesses, True, line_correct_answer, line_mcq_shown

        # if you got the first MCQ right
        elif opening_name in initial_guess or initial_guess == opening_correct_answer:
            opening_solved = True

            # if you haven't gotten the 2nd MCQ yet
            if not line_mcq_shown:
                print('\n')
                line_correct_answer = mcq(computer_opening, opening, 1) # the 2nd MCQ answer
                line_mcq_shown = True # you've been shown the 2nd MCQ

            # get your 2nd MCQ guess
            line_guess = get_guess(f'Correct! What line of the {computer_opening["name"]} is this? ').lower().strip()

            if line_name in line_guess or line_guess == line_correct_answer:
                print(f'Correct! This is the {full_name}.\n')
                return True, guesses, True, line_correct_answer, line_mcq_shown
            else:
                guesses += 1
                print(f'Not quite. You have {3 - guesses} more attempt(s).\n')
                if guesses >= 3:
                    print(f'This is the {full_name}.\n')
                return False, guesses, True, line_correct_answer, line_mcq_shown

        else:
            guesses += 1
            print(f'Not quite. You have {3 - guesses} more attempt(s).\n')
            if guesses >= 3:
                print(f'This is the {full_name}.\n')
            return False, guesses, False, line_correct_answer, line_mcq_shown

    # Phase 2: opening already solved, only ask line
    else:
        line_guess = get_guess(f'What line of the {computer_opening["name"]} is this? ').lower().strip()
        if not line_mcq_shown:
            line_correct_answer = mcq(computer_opening, opening, 1)
            line_mcq_shown = True

        if line_name in line_guess or line_guess == line_correct_answer:
            print(f'Correct! This is the {full_name}.\n')
            return True, guesses, True, line_correct_answer, line_mcq_shown
        else:
            guesses += 1
            print(f'Not quite. You have {3 - guesses} more attempt(s).\n')
            if guesses >= 3:
                print(f'This is the {full_name}.\n')
            return False, guesses, True, line_correct_answer, line_mcq_shown


# Goal: start with MCQ of JUST OPENINGS (random). then, when prompted to guess the variation, only randomly pull the variations with the same base opening
# Ex: if the opening is the Sicilian, the 2nd MCQ should be variations of the Sicilian (when possible).
def mcq(computer_opening, opening, need_line):
    correct_answer = None
    notation = ['a. ', 'b. ', 'c. ', 'd. ']
    order = random.sample(range(0, 4), 4)

    # only need to guess opening
    if need_line == 0:
        options = [computer_opening]
        used_names = {computer_opening['name']}

        # generate 3 unique random openings
        while len(options) < 4:
            choice = random.choice(opening)
            if choice['name'] not in used_names:
                options.append(choice)
                used_names.add(choice['name'])

        i = 0
        for a in range(len(order)):
            if options[order[a]] == computer_opening:
                correct_answer = notation[i][0]
            print(f'{notation[i]}{options[order[a]]['name']}\n')
            i += 1

    # need to guess variation
    else:
        all_options = []
        options = [computer_opening]

        # filter for all the openings with the same starting name as the computer's opening
        for o in opening:
            if o['name'] == computer_opening['name'] and o != computer_opening:
                all_options.append(o)

        # if there's less than 3 of these, fill the remainder with other openings
        if len(all_options) < 3:
            while len(all_options) < 3:
               choice = random.choice(opening)
               if choice not in all_options and choice != computer_opening:
                   all_options.append(choice)

        # pick 3 openings randomly
        choices = random.sample(all_options, 3)
        for c in choices:
            options.append(c)

        # print 4 openings randomly
        i = 0
        for a in range(len(order)):
            if options[order[a]] == computer_opening:
                correct_answer = notation[i][0]
            print(f"{notation[i]}{options[order[a]]['line_name']}\n")
            i += 1

    return correct_answer



def play_game(games, opening, answer_type):
    times_played = 0
    wins = 0
    losses = 0

    # play until the number of games
    while times_played < games:

        guesses = 0 # not guessed yet
        solved = False # haven't solved anything yet
        opening_solved = False # haven't solved opening yet
        line_correct_answer = None # correct answer of the 2nd MCQ
        line_mcq_shown = False # haven't gotten the first MCQ right
        computer_opening = random.choice(opening)

        print(f'### Game {times_played + 1} ###')
        board = chess.Board()

        # print the chess board
        for move in computer_opening['moves']:
            board.push_san(move)
            print(board)
            print()

        # if you chose MCQ
        if answer_type == 1:
            # correct answer of first MCQ
            correct_answer = mcq(computer_opening, opening, 0)

        # while you haven't solved ir or run out of guesses
        while not solved and guesses < 3:
            # if MCQ
            if answer_type == 1:
                solved, guesses, opening_solved, line_correct_answer, line_mcq_shown = check_guess_mcq(computer_opening, opening, guesses, correct_answer, opening_solved, line_correct_answer, line_mcq_shown)
            # if free response
            else:
                solved, guesses = check_guess_short(computer_opening, guesses)

        if solved:
            wins += 1
        else:
            losses += 1

        times_played += 1

    print(f'### Results ###')
    print(f'You won {wins}/{wins + losses}')



def main():
    games, opening, answer_type = start()
    play_game(games, opening, answer_type)

if __name__ == '__main__':
    main()
