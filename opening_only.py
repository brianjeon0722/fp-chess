from Openix import ChessOpeningsLibrary
import re
import os
from collections import Counter

library = ChessOpeningsLibrary()
load = library.load_builtin_openings()

# thank you claude for this function
# tldr: this function essentially finds the collection of prefix strings that are shared by 80% of the list of strings
# ex: 'e4 c5 d1' 'e4 c5 d2' 'e4 c2 d1' --> 'e4 c5' but only if its 80% of the list etc etc
def common_move_prefix(move_strings):
    split_lists = []
    for s in move_strings:
        # Extract moves using regex to avoid concatenation
        moves = re.findall(r'(?:\d+\.\s*)?([a-hNBRQKO][\w\-+=#]*)', s)
        split_lists.append(moves)

    if not split_lists:
        return []

    result = []
    max_len = max(len(m) for m in split_lists)

    for i in range(max_len):
        candidates = [m[i] for m in split_lists if i < len(m)]
        most_common, count = Counter(candidates).most_common(1)[0]
        if count / len(split_lists) >= 0.8:
            result.append(most_common)
        else:
            break

    return result

grouped = {}

# eco libraries are A1-100 to E1-100
for letter in ['A', 'B', 'C', 'D', 'E']:
    for num in range(0, 100):
        for opening in library.find_by_eco(f'{letter}{num}'):

            opening_name = opening.name # class for an opening

            if opening_name.startswith('talian'): # fix a minor typo i found
                opening_name = 'I' + opening_name

            # AI helped me with writing the regex and using re library
            # remove everything after the first ',' ' - ' ':' or '/'
            opening_name = re.sub(r'\s*(,|/|:|\s-\s).*$', '', opening_name).strip()

            # remove numbers +
            if re.search(r"[1234567890]", opening_name):
                opening_name = opening_name[:re.search(r"[1234567890]", opening_name).start()-1]

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

            # remove generic terms
            generic_terms = ['Variation', 'Defense', 'Defence', 'System', 'Opening', 'Attack', 'Game']
            for term in generic_terms:
                opening_name = re.sub(rf'\b{term}\b', '', opening_name).strip()

            # remove trailing spaces
            opening_name = re.sub(r'\s+', ' ', opening_name).strip()

            # remove trailing :
            opening_name = opening_name.strip(':,').strip()

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

            # if this opening is new, create new set
            if opening_name not in grouped:
                grouped[opening_name] = set()

            # add into new set
            grouped[opening_name].add(opening.moves_str)

for name, moves in grouped.items():
    if name == "Sicilian":
        for m in moves:
            cleaned = re.sub(r'\s*\d+\.\s*', '', m).strip()
            tokens = cleaned.split()
            if not tokens or tokens[0] != 'e4':
                print(f"ROGUE: {repr(m)}")
        break

openings_list = []

for name, moves in grouped.items():
    if len(moves) >= 10:

        common_moves = common_move_prefix(list(moves))

        # # removes numbers from the string '1. e4 c5 2. etc etc' --> 'e4 c5 etc etc'
        # common = re.sub(r'\s*\d+\.(?=\s|$)', '', common).strip()

        if len(common_moves) >= 2:
            already = False
            for item in openings_list:
                if item['moves'] == common_moves:
                    already = True
                    break

            if already == False:
                # transforms
                openings_list.append({
                'name': name,
                'moves': common_moves})

for i in openings_list:
    print(i['name'])

