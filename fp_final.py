import chess
import random
from opening_lines import openings_list
from opening_only import openings_only

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

    if mode == 1:
        opening = openings_only
    else:
        opening = openings_list

    return games, opening, answer_type



def get_guess(question):
    return str(input(question)).lower().strip()


def check_guess_short(computer_opening, guesses):
    initial_guess = get_guess('What opening is this? ').lower()
    opening_name = computer_opening.get('name').lower()
    line_name = computer_opening.get('line_name')

    # if initial guess is hint
        # note: add opening into check_guess()
        # randonchoice opening 3 times

    # else:

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

    else:
        line_name = line_name.lower()
        full_name = f'{computer_opening["name"]} {computer_opening["line_name"]}'
        if line_name in initial_guess:
            print(f'Correct! This is the {full_name}.\n')
            return True, guesses
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


def check_guess_mcq(computer_opening, opening, guesses, opening_correct_answer, opening_solved, line_correct_answer=None, line_mcq_shown=False):
    opening_name = computer_opening.get('name').lower()
    line_name = computer_opening.get('line_name')

    if line_name is None:
        full_name = computer_opening["name"]
        initial_guess = get_guess('What opening is this? ').lower().strip()

        if opening_name in initial_guess or initial_guess == opening_correct_answer:
            print(f'Correct! This is the {full_name}.\n')
            return True, guesses, True, line_correct_answer, line_mcq_shown
        else:
            guesses += 1
            print(f'Not quite. You have {3 - guesses} more attempt(s).\n')
            if guesses >= 3:
                print(f'This is the {full_name}.\n')
            return False, guesses, False, line_correct_answer, line_mcq_shown

    line_name = line_name.lower()
    full_name = f'{computer_opening["name"]} {computer_opening["line_name"]}'

    # Phase 1: opening not solved yet
    if not opening_solved:
        initial_guess = get_guess('What opening is this? ').lower().strip()

        if line_name in initial_guess:
            print(f'Correct! This is the {full_name}.\n')
            return True, guesses, True, line_correct_answer, line_mcq_shown

        elif opening_name in initial_guess or initial_guess == opening_correct_answer:
            opening_solved = True

            if not line_mcq_shown:
                print('\n')
                line_correct_answer = mcq(computer_opening, opening, 1)
                line_mcq_shown = True

            line_guess = get_guess(f'What line of the {computer_opening["name"]} is this? ').lower().strip()

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
        if not line_mcq_shown:
            line_correct_answer = mcq(computer_opening, opening, 1)
            line_mcq_shown = True

        line_guess = get_guess(f'What line of the {computer_opening["name"]} is this? ').lower().strip()

        if line_name in line_guess or line_guess == line_correct_answer:
            print(f'Correct! This is the {full_name}.\n')
            return True, guesses, True, line_correct_answer, line_mcq_shown
        else:
            guesses += 1
            print(f'Not quite. You have {3 - guesses} more attempt(s).\n')
            if guesses >= 3:
                print(f'This is the {full_name}.\n')
            return False, guesses, True, line_correct_answer, line_mcq_shown



def mcq(computer_opening, opening, need_line):
    correct_answer = None
    notation = ['a. ', 'b. ', 'c. ', 'd. ']
    order = random.sample(range(0, 4), 4)

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

    else:
        all_options = []
        options = [computer_opening]

        # filter for all the openings with the same starting name as the computer's opening
        for o in opening: # O(n) :(, maybe fix later?
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

    while times_played < games:
        guesses = 0
        solved = False
        opening_solved = False
        line_correct_answer = None
        line_mcq_shown = False
        computer_opening = random.choice(opening)

        print(f'### Game {times_played + 1} ###')
        board = chess.Board()
        for move in computer_opening['moves']:
            board.push_san(move)
            print(board)
            print()

        if answer_type == 1:
            correct_answer = mcq(computer_opening, opening, 0)

        while not solved and guesses < 3:
            if answer_type == 1:
                solved, guesses, opening_solved, line_correct_answer, line_mcq_shown = check_guess_mcq(computer_opening, opening, guesses, correct_answer, opening_solved, line_correct_answer, line_mcq_shown)
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

# if you haven't gotten the opening correct --> 4 random openings
# if you got the opening correct --> random variations WITH that opening
