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

            # Skip if opening name is empty or too short after cleaning
            if not opening_name or len(opening_name) < 2:
                continue

            # Add to dictionary - store the move string
            if opening_name not in openings:
                openings[opening_name] = []
            openings[opening_name].append(opening.moves_str)

# Filter: only keep openings that appear 10+ times
filtered_openings = {name: moves_list for name, moves_list in openings.items() if len(moves_list) >= 10}

print(f"Total unique opening names: {len(openings)}")
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

# Print results
for opening_name, moves in sorted(final_openings.items()):
    print(f"Opening: {opening_name}")
    print(f"Count: {len(filtered_openings[opening_name])} variations")
    print(f"Moves: {moves}")
    print(f"Moves string: {' '.join(moves)}")
    print()
