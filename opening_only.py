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

        # extract the base opening name (everything before the first colon)
        if ':' in opening_name:
            opening_name = opening_name.split(':')[0].strip()

        # remove numbers and everything after them
        if re.search(r"[1234567890]", opening_name) != None:
            opening_name = opening_name[:re.search(r"[1234567890]", opening_name).start()-1]

        # remove everything after comma
        if re.search(r"[,]", opening_name) != None:
            opening_name = opening_name[:re.search(r"[,]", opening_name).start()]

        # remove 'vs.' or 'vs' at the end
        if re.search(r'\bvs\.?$', opening_name):
            opening_name = re.sub(r'\s*vs\.?$', '', opening_name).strip()

        # remove everything after /
        if '/' in opening_name:
            opening_name = opening_name[:opening_name.find('/')].strip()

        # Remove generic terms
        generic_terms = ['Variation', 'Defense', 'Defence', 'System', 'Opening', 'Attack']
        for term in generic_terms:
            opening_name = re.sub(rf'\b{term}\b', '', opening_name, flags=re.IGNORECASE).strip()

        # clean extra spaces
        opening_name = re.sub(r'\s+', ' ', opening_name).strip()
        opening_name = opening_name.strip(':,').strip()

        # add moves to this opening
        if opening_name not in openings:
            openings[opening_name] = set()
        openings[opening_name].add(opening.moves_str)

# remove names that are prefixes of other names
names = list(openings.keys())
for name in names:
    if name in openings and any(other != name and other.startswith(name) for other in names):
        del openings[name]

# for each opening + line combination, find the common  moves across ALL variations
openings_dict = {}
for opening_name, variations in openings.items():
    # Find common prefix across all variations
    common = os.path.commonprefix(list(variations)).rstrip()
    common = common.strip()

    # Remove trailing incomplete move numbers (e.g., "1. e4 2." -> "1. e4")
    common = re.sub(r'\s*\d+\.$', '', common).strip()

    # Convert to list of moves
    moves = common.split()

    openings_dict[opening_name] = {
        'name': opening_name,
        'moves': moves
    }

# Print results
for opening_name, data in openings_dict.items():
    print(f"Opening: {data['name']}")
    print(f"Moves: {' '.join(data['moves'])}")
    print()
