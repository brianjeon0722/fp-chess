from Openix import ChessOpeningsLibrary
import re
import os

library = ChessOpeningsLibrary()
loaded_count = library.load_builtin_openings()

all_openings = library.get_all_openings()

openings = {}

for a in range(0, 100):
    for opening in library.find_by_eco(f'C{a}'):
        print(opening.name)
