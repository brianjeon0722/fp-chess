from Openix import ChessOpeningsLibrary
import re
import os

library = ChessOpeningsLibrary()
loaded_count = library.load_builtin_openings()

all_openings = library.get_all_openings()

print(f"Total openings: {len(all_openings)}")

# for opening in all_openings[500:530]:
#     print(opening.name)
#     print(opening.eco_code)

openings = {}

openings = {}

for a in range(20, 100):
    for opening in library.find_by_eco(f'B{a}'):
        opening_name = opening.name
        if opening.name[0:opening.name.find(':')] == 'Sicilian Defense':
            opening_name = opening_name.replace("Sicilian Defense", "Sicilian")
        if opening.name[0:opening.name.find(':')] == 'Sicilian':
            if re.search(r"[1234567890]", opening_name) != None:
                opening_name = opening_name[:re.search(r"[1234567890]", opening_name).start()-1]
            if re.search(r"[,]", opening_name) != None:
                opening_name = opening_name[:re.search(r"[,]", opening_name).start()]
            # CLEAN: remove vs. artifacts
            if re.search(r'\bvs\.?$', opening_name):
                opening_name = re.sub(r'\s*vs\.?$', '', opening_name).strip()
            # CLEAN: collapse slash variants to first name
            if '/' in opening_name:
                opening_name = opening_name[:opening_name.find('/')].strip()
            if opening_name not in openings:
                openings[opening_name] = set()
            openings[opening_name].add(opening.moves_str)

# CLEAN: remove names that are prefixes of other names (handles Sozin, Prins, Smith-Morra, etc.)
names = list(openings.keys())
for name in names:
    if any(other != name and other.startswith(name) for other in names):
        del openings[name]

for opening_name, variations in openings.items():
    common = os.path.commonprefix(list(variations)).rstrip()
    common = common.strip()
    common = re.sub(r'\s*\d+\.(?=\s|$)', '', common).strip()
    openings[opening_name] = common.split(' ')

openings_list = []

for opening_name, moves in openings.items():
    parts = opening_name.split(': ', 1)
    entry = {
        'name': parts[0],
        'line_name': parts[1] if len(parts) > 1 else None,
        'moves': moves
    }
    openings_list.append(entry)




