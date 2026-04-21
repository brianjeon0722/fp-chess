# fp-chess

# Description: creating a Worlde x Chess remix where you are given a series of ASCII chess board drawing and asked to guess the opening. the total openings are in a python dictionary and you are given 3 attempts to guess the name. fp_lines.py has you guess both the opening and line variation (Ex: Sicilian Dragon, King's Indian Averbakh, etc.). fp_opening.py only requires you to guess the opening (Ex: Sicilian, Carro-Kann)

# Instructions for running the code: Install the chess library, re library, and os library. Run python3 fp_openiing.py to play the easy version. Run python3 fp_lines.py to play the hard version. No need for any other API keys or hosting.

# External contributors: ChatGPT helped understand the libraries (chess, re, and os) and debug those unique errors. ChatGPT also helped format the regex since I wasn't 100% with all the formatting. These portions are noted in the .py documents explicitly. ChatGPT also gave me the idea of returning tuples with False or True + the number of guesses rather than only False or True from check_guess() and correct(). Shoutout Lichess.com for being my analysis board / dictionary so I could verify that my outputs were giving me the correct moves for certain variations.

# What's next: 1. Hint mode where if you guess the word 'hint' it'll give you 4 options to choose from. These options for hard mode will only give you hints on the opening or variation depending on where you are. 2. Combining fp_opening.py with fp_lines.py into 1 script where it asks you first whether you want to play opening or opening + variation mode then how many times you want to play. 3. Toggling more explicit difficulty for each opening or opening + variation mode. There is currently a minimum count for how many times an opening or variation must be in the eco library before I use it. You will be able to toggle this number between 10 20 or 30 for hard, medium, or easy.

# One problem I encountered: identical names for openings due to shortening names, identical move orders due to shortening moves
# Ex: Scotch Game, Scotch Opening, Scotch
