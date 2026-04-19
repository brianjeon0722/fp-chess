from Openix import ChessOpeningsLibrary
import re
import os

library = ChessOpeningsLibrary()
loaded_count = library.load_builtin_openings()

openings = {}

# Generic terms to remove
generic_terms = ['Variation', 'Defense', 'Defence', 'System', 'Opening', 'Attack', 'Gambit', 'Game']

for a in range(0, 100):
    for opening in library.find_by_eco(f'B{a}'):
        opening_name = opening.name

        # Extract first few words before ':' or ',' (whichever comes first)
        if ':' in opening_name:
            opening_name = opening_name.split(':')[0].strip()
        if ',' in opening_name:
            opening_name = opening_name.split(',')[0].strip()

        # Remove generic terms
        for term in generic_terms:
            opening_name = re.sub(rf'\b{term}\b', '', opening_name, flags=re.IGNORECASE).strip()

        # Clean up extra spaces
        opening_name = re.sub(r'\s+', ' ', opening_name).strip()

        # Add to dictionary
        if opening_name not in openings:
            openings[opening_name] = set()
        openings[opening_name].add(opening.moves_str)

# Find common prefix for each opening
final_openings = {}
for opening_name, variations in openings.items():
    # Find common prefix across all variations
    common = os.path.commonprefix(list(variations)).strip()

    # Remove trailing incomplete move numbers or periods
    common = re.sub(r'\s*\d+\.\s*$', '', common).strip()

    # Extract only the actual moves (remove move numbers)
    # Pattern: remove "1." "2." etc. and keep only the moves
    moves = re.findall(r'(?:\d+\.\s*)?([a-hNBRQKO][\w\-+=#]*)', common)

    # Only keep if there are 2 or more moves
    if len(moves) >= 2:
        # Check if this move sequence already exists
        moves_tuple = tuple(moves)
        if moves_tuple not in [tuple(v) for v in final_openings.values()]:
            final_openings[opening_name] = moves

# Print results
for opening_name, moves in sorted(final_openings.items()):
    print(f"Opening: {opening_name}")
    print(f"Moves: {moves}")
    print(f"Moves string: {' '.join(moves)}")
    print()
