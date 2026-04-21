from Openix import ChessOpeningsLibrary
import re
import os

library = ChessOpeningsLibrary()

grouped = {}

# eco libraries are A1-100 to E1-100
for letter in ['A', 'B', 'C', 'D', 'E']:
    for num in range(0, 100):
        for opening in library.find_by_eco(f'{letter}{num}'):

            opening_name = opening.name # class for an opening

            if opening_name.startswith('talian'): # fix a minor typo i found
                opening_name = 'I' + opening_name

            # remove numbers +
            if re.search(r"[1234567890]", opening_name):
                opening_name = opening_name[:re.search(r"[1234567890]", opening_name).start()-1]

            # remove everything after the first ,
            opening_name = opening_name.split(",", 1)[0]

            # AI helped me with writing the regex and using re library
            # remove 'The ' at the beginning
            opening_name = re.sub(r'^\s*[Tt]he\s+', '', opening_name).strip()

            # clean up extra spaces
            opening_name = re.sub(r'\s+', ' ', opening_name).strip()

            # remove any leading non-letter characters
            opening_name = re.sub(r'^[^a-zA-Z]+', '', opening_name).strip()

            # remove "Old" from the beginning
            opening_name = re.sub(r'^\s*Old\s+', '', opening_name, flags=re.IGNORECASE).strip()

            # remove trailing possessive "'s"
            opening_name = re.sub(r"'s$", "", opening_name, flags=re.IGNORECASE).strip()

            # remove trailing vs. or vs
            opening_name = re.sub(r'\s*vs\.?$', '', opening_name).strip()

            # remove everything after first /
            opening_name = opening_name.split('/', 1)[0].strip()

            # normalize special characters to their ASCII equivalents
            # openings like gruenfeld or reti
            char_replacements = {
                'ü': 'ue',
                'Ü': 'Ue',
                'ö': 'oe',
                'Ö': 'Oe',
                'ä': 'ae',
                'Ä': 'Ae',
                'é': 'e',
                'É': 'E',
                'è': 'e',
                'È': 'E',
                'á': 'a',
                'Á': 'A',
                'í': 'i',
                'Í': 'I',
                'ó': 'o',
                'Ó': 'O',
                'ú': 'u',
                'Ú': 'U',
            }

            for char, replacement in char_replacements.items():
                opening_name = opening_name.replace(char, replacement)

            abbreviations = {
                r'^QGD$': "Queen's Gambit Declined",
                r'^QGA$': "Queen's Gambit Accepted",
                r'^KGD$': "King's Gambit Declined",
                r'^KGA$': "King's Gambit Accepted",
                r"^Queen's Accepted$": "Queen's Gambit Accepted",
                r"^Queen's Declined$": "Queen's Gambit Declined",
                r"^King's Accepted$": "King's Gambit Accepted",
                r"^King's Declined$": "King's Gambit Declined"
            }

            for pattern, replacement in abbreviations.items():
                if re.match(pattern, opening_name, flags=re.IGNORECASE):
                    opening_name = replacement
                    break

            generic_terms = ['Variation', 'Defense', 'Defence', 'System', 'Opening', 'Attack']
            for term in generic_terms:
                opening_name = re.sub(rf'\b{term}\b', '', opening_name).strip()

            # remove trailing spaces
            opening_name = re.sub(r'\s+', ' ', opening_name).strip()

            # remove trailing :
            opening_name = opening_name.strip(':,').strip()

            # split by : or -
            parts = re.split(r'\s*:\s*|\s+-\s+', opening_name, maxsplit=1)
            name = parts[0].strip()

            if len(parts) > 1:
                line_name = parts[1].strip()
            else:
                line_name = None

            key = (name, line_name)

            if key not in grouped:
                grouped[key] = set()

            grouped[key].add(opening.moves_str)


openings_filtered = {}

for (name, line_name), moves in grouped.items():
    if len(moves) >= 10 and line_name != None:

        # AI helped me use os.path
        common = os.path.commonprefix(list(moves)).rstrip()

        # remove trailing spaces
        common = common.strip()

        common = re.sub(r'\s*\d+\.(?=\s|$)', '', common).strip()
        openings_filtered[(name, line_name)] = common.split()

openings_list = []

for name, line_name, moves in openings_filtered.items():
    openings_list.append({
        'name': name,
        'line_name': line_name,
        'moves': moves
    })

# for i in openings_list:
#     print(i['name'])
#     print(i['line_name'])
