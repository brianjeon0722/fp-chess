from Openix import ChessOpeningsLibrary
import re
import os

library = ChessOpeningsLibrary()
loaded_count = library.load_builtin_openings()

openings = {}

# Generic terms to remove
generic_terms = ['Variation', 'Defense', 'Defence', 'System', 'Opening', 'Attack', 'Gambit', 'Game']

for letter in ['A', 'B', 'C', 'D', 'E']:
    for a in range(0, 100):
        for opening in library.find_by_eco(f'{letter}{a}'):
            opening_name = opening.name

            if opening_name.startswith('talian'):
                opening_name = 'I' + opening_name

            if ':' in opening_name:
                opening_name = opening_name.split(':')[0].strip()
            if ',' in opening_name:
                opening_name = opening_name.split(',')[0].strip()
            if 'with' in opening_name:
                opening_name = opening_name.split('with')[0].strip()
            if ' - ' in opening_name:
                opening_name = opening_name.split(' - ')[0].strip()
            if re.search(r"[1234567890]", opening_name) != None:
                opening_name = opening_name[:re.search(r"[1234567890]", opening_name).start()-1]

            # Remove "The " at the beginning
            opening_name = re.sub(r'^\s*[Tt]he\s+', '', opening_name).strip()

            # Remove generic terms
            for term in generic_terms:
                opening_name = re.sub(rf'\b{term}\b', '', opening_name, flags=re.IGNORECASE).strip()

            # Clean up extra spaces
            opening_name = re.sub(r'\s+', ' ', opening_name).strip()

            # Final cleanup - remove any leading non-letter characters
            opening_name = re.sub(r'^[^a-zA-Z]+', '', opening_name).strip()

            # Remove "Old" from the beginning
            opening_name = re.sub(r'^\s*Old\s+', '', opening_name, flags=re.IGNORECASE).strip()

            # Normalize special characters to their ASCII equivalents
            # This handles ü->ue, é->e, etc.
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

            # Expand abbreviations
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

            # Skip if opening name is empty or too short after cleaning
            if not opening_name or len(opening_name) < 2:
                continue

            # Add to dictionary - store the move string
            if opening_name not in openings:
                openings[opening_name] = []
            openings[opening_name].append(opening.moves_str)

# Collapse similar names after abbreviation expansion
collapsed_openings = {}
for opening_name, moves_list in openings.items():
    if opening_name not in collapsed_openings:
        collapsed_openings[opening_name] = []
    collapsed_openings[opening_name].extend(moves_list)

# Filter: only keep openings that appear 10+ times
filtered_openings = {name: moves_list for name, moves_list in collapsed_openings.items() if len(moves_list) >= 10}

print(f"Total unique opening names: {len(openings)}")
print(f"After collapsing: {len(collapsed_openings)}")
print(f"Opening names with 10+ variations: {len(filtered_openings)}")
print()

# For each opening, find the shortest move string and convert to list
final_openings = {}
for opening_name, moves_list in filtered_openings.items():
    # Find the shortest move string
    shortest_moves_str = min(moves_list, key=len)

    # Remove trailing incomplete move numbers
    shortest_moves_str = re.sub(r'\s*\d+\.\s*$', '', shortest_moves_str).strip()

    # Extract only the actual moves (remove move numbers)
    moves = re.findall(r'(?:\d+\.\s*)?([a-hNBRQKO][\w\-+=#]*)', shortest_moves_str)

    # Only keep if there are 2 or more moves
    if len(moves) >= 2:
        final_openings[opening_name] = moves

# Remove openings that are just longer versions of shorter openings
openings_to_remove = set()
for name1, moves1 in final_openings.items():
    for name2, moves2 in final_openings.items():
        if name1 != name2:
            # Check if name1 starts with name2 (e.g., "Benko Accepted" starts with "Benko")
            if name1.startswith(name2 + ' '):
                # Check if moves2 is a prefix of moves1 (shorter base moves)
                if len(moves2) < len(moves1) and moves1[:len(moves2)] == moves2:
                    openings_to_remove.add(name1)
                    print(f"Removing '{name1}' (prefix of '{name2}')")

# Remove the identified openings
for name in openings_to_remove:
    del final_openings[name]

print(f"\nFinal openings after removing prefixes: {len(final_openings)}\n")

# Print results
for opening_name, moves in sorted(final_openings.items()):
    print(f"Opening: {opening_name}")
    print(f"Count: {len(filtered_openings[opening_name])} variations")
    print(f"Moves: {moves}")
    print(f"Moves string: {' '.join(moves)}")
    print()
