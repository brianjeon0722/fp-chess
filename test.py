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

all_sicilian_names = {}

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
            if opening_name not in all_sicilian_names:
                all_sicilian_names[opening_name] = set()
            all_sicilian_names[opening_name].add(opening.moves_str)

for opening_name, variations in all_sicilian_names.items():
    common = os.path.commonprefix(list(variations)).rstrip()
    all_sicilian_names[opening_name] = common.strip()

print(all_sicilian_names["Sicilian: Dragon"])



