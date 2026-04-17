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
            if opening_name not in openings:
                openings[opening_name] = set()
            openings[opening_name].add(opening.moves_str)

#{"Sicilian: Rossolimo": ['e4', 'c5', ...],
# "Sicilian: Kan: [],
# "Sicilian: Dragon: []}

for opening_name, variations in openings.items():
    common = os.path.commonprefix(list(variations)).rstrip()
    common = common.strip()
    if re.search(r'\d+\.', common):
        common = re.sub(r'\s*\d+\.(?=\s|$)', '', common).strip()
    openings[opening_name] = common.split(' ')

print(openings["Sicilian: Rossolimo"])



