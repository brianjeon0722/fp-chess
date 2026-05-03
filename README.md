# fp-chess

# description: creating a Chess quiz where you are given a series of ASCII chess board drawing and asked to guess the opening / variation. the total openings are in a python dictionary and you are given 3 attempts to guess the name. fp_lines.py has you guess both the opening and line variation (Ex: Sicilian Dragon, King's Indian Averbakh, etc.). fp_opening.py only requires you to guess the opening (Ex: Sicilian, Carro-Kann)

# instructions for running the code: install the chess library, Openix library, and collections library. Run python3 fp_final.py to play. You will be asked to select your game mode: just openings vs. openings and variations, MCQ vs. short response, and easy, medium vs. hard mode.

# external contributors: ChatGPT helped understand the libraries (chess, re, and os) and debug those unique errors. ChatGPT also helped format the regex since I wasn't 100% with all the formatting. These portions are noted in the .py documents explicitly. ChatGPT also gave me the idea of returning tuples with False or True + the number of guesses rather than only False or True from check_guess() and correct(). Shoutout Lichess.com for being my analysis board / dictionary so I could verify that my outputs were giving me the correct moves for certain variations. Claude helped write the majority base string function common_move_prefix() in opening_only.py since I was new to the collections library. it also helped me write the check_mcq_guess() function, particularly parsing multiple variables into the function for certain game states (getting the 1st vs. 2nd MCQ right).



# any changes in scope from last time: rather than typing 'hint' and bringing up MCQ, I just created a separate game mode for MCQ since it was really annoying to keep typing hint.

