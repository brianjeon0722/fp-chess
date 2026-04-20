from Openix import ChessOpeningsLibrary
import re
import os

library = ChessOpeningsLibrary()
loaded_count = library.load_builtin_openings()

all_openings = library.get_all_openings()

openings = {}


for a in range(0, 100):
    for opening in library.find_by_eco(f'B{a}'):
        opening_name = opening.name

        if re.search(r"[1234567890]", opening_name) != None: # if there are numbers
            opening_name = opening_name[:re.search(r"[1234567890]", opening_name).start()-1] # remove everything after the numbers

        if re.search(r"[,]", opening_name) != None: # if there is a comma
            opening_name = opening_name[:re.search(r"[,]", opening_name).start()] # remove everything after the coma

        if re.search(r'\bvs\.?$', opening_name): # if there are any vs. or vs
            opening_name = re.sub(r'\s*vs\.?$', '', opening_name).strip() # remove them

        if '/' in opening_name: # if there is a / in the name
            opening_name = opening_name[:opening_name.find('/')].strip() # remove it

        generic_terms = ['Variation', 'Defense', 'Defence', 'System', 'Opening', 'Attack'] # different ways of saying an opening
        for term in generic_terms: # for each of these
            opening_name = re.sub(rf'\b{term}\b', '', opening_name).strip() # remove them

        opening_name = re.sub(r'\s+', ' ', opening_name).strip() # turn any double spaces we created about into a single one

        opening_name = opening_name.strip(':,').strip() # remove trailing , or :

        if opening_name not in openings: # if this is a new opening,
            openings[opening_name] = set() # create a set
        openings[opening_name].add(opening.moves_str) # add the moves (a string with the moves '1. e4 c5 2. ...')

# CLEAN: remove names that are prefixes of other names
names = list(openings.keys())
for name in names:
    if any(other != name and other.startswith(name) for other in names):
        del openings[name]

openings_filtered = {}

# filter: only keep openings that appear 10+ times
for openings, moves in openings.items():
    if len(moves) >= 3:
        openings_filtered[openings] = moves

for opening_name, moves in openings_filtered.items():
    common = os.path.commonprefix(list(moves)).rstrip()
    common = common.strip()
    common = re.sub(r'\s*\d+\.(?=\s|$)', '', common).strip()
    openings_filtered[opening_name] = common.split(' ')

openings_list = []

for opening_name, moves in openings_filtered.items():
    parts = re.split(r'\s*:\s*|\s*-\s*', opening_name, maxsplit=1)
    entry = {
        'name': parts[0],
        'line_name': parts[1] if len(parts) > 1 else None,
        'moves': moves
    }
    openings_list.append(entry)

for i in openings_list:
    print(i.get('name'))
    print(i.get('line_name'))
