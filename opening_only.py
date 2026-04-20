from Openix import ChessOpeningsLibrary
import re
import os

library = ChessOpeningsLibrary()
loaded_count = library.load_builtin_openings()

openings = {}

# Generic terms to remove
generic_terms = ['Variation', 'Defense', 'Defence', 'System', 'Opening', 'Attack', 'Gambit', 'Game']

for a in range(0, 100):
    for opening in library.find_by_eco(f'C{a}'):
        opening_name = opening.name
        original_name = opening_name  # Store for debugging

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

        # Remove "The " at the beginning (more aggressively)
        opening_name = re.sub(r'^\s*[Tt]he\s+', '', opening_name).strip()

        # Remove generic terms - do this AFTER removing "The"
        for term in generic_terms:
            opening_name = re.sub(rf'\b{term}\b', '', opening_name, flags=re.IGNORECASE).strip()

        # Clean up extra spaces
        opening_name = re.sub(r'\s+', ' ', opening_name).strip()

        # Final cleanup - remove any leading non-letter characters
        opening_name = re.sub(r'^[^a-zA-Z]+', '', opening_name).strip()

        # DEBUG: Print if it contains "talian"
        if 'talian' in opening_name.lower():
            print(f"DEBUG - Original: '{original_name}' -> Cleaned: '{opening_name}'")

        # Skip if opening name is empty or too short after cleaning
        if not opening_name or len(opening_name) < 2:
            continue

        # Add to dictionary
        if opening_name not in openings:
            openings[opening_name] = set()
        openings[opening_name].add(opening.moves_str)

# Find common prefix for each opening
final_openings = {}
for opening_name, variations in openings.items():
    common = os.path.commonprefix(list(variations)).strip()
    common = re.sub(r'\s*\d+\.\s*$', '', common).strip()
    moves = re.findall(r'(?:\d+\.\s*)?([a-hNBRQKO][\w\-+=#]*)', common)

    if len(moves) >= 2:
        moves_tuple = tuple(moves)
        if moves_tuple not in [tuple(v) for v in final_openings.values()]:
            final_openings[opening_name] = moves

# Print results
for opening_name, moves in sorted(final_openings.items()):
    print(f"Opening: {opening_name}")
    print(f"Moves: {moves}")
    print()
