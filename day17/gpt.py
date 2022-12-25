def simulate_rock_fall(chamber_width, chamber_height, rock_types, jet_patterns):
    # Initialize the chamber and the list of fallen rocks
    chamber = [['.' for _ in range(chamber_width)] for _ in range(chamber_height)]
    fallen_rocks = []

    # Initialize the counter for the current rock and jet pattern
    counter = 0

    # Keep simulating until there are no more rocks falling
    while True:
        # Get the current rock and jet pattern using the counter modulo the length of the lists
        rock_type = rock_types[counter % len(rock_types)]
        jet_pattern = jet_patterns[counter % len(jet_patterns)]

        # Create a new rock using the current rock type, and place it at the top of the chamber
        rock = [['#' if c == '#' else '.' for c in row] for row in rock_type]
        x = chamber_width // 2 - len(rock[0]) // 2
        y = 0

        # While the rock has not landed, apply the jet pattern and move the rock down one unit
        while y + len(rock) < chamber_height:
            # Apply the jet pattern to the rock
            for i, direction in enumerate(jet_pattern):
                if direction == '<':
                    x -= 1
                elif direction == '>':
                    x += 1
                if x < 0 or x + len(rock[0]) > chamber_width:
                    x -= direction
                    jet_pattern = jet_pattern[i+1:] + jet_pattern[:i+1]
                    break

            # Move the rock down one unit
            y += 1

            # Check for collisions with other rocks or the floor
            for i in range(len(rock)):
                for j in range(len(rock[0])):
                    if chamber[y+i][x+j] == '#' or rock[i][j] == '#':
                        y -= 1
                        break
                else:
                    continue
                break
            else:
                continue
            break

        # Add the rock to the list of fallen rocks and update the chamber
        fallen_rocks.append((y, x, rock))
        for i in range(len(rock)):
            for j in range(len(rock[0])):
                chamber[y+i][x+j] = rock[i][j]

        # Increment the counter and check if there are any more rocks falling
        counter += 1
        if counter >= len(rock_types):
            break

    return chamber, fallen_rocks


chamber_width = 7
chamber_height = 7

rock_types = [
    [['#', '#', '#', '#'],
     ['#', '#', '#', '#']],
    [['.', '.', '#', '#'],
     ['.', '.', '#', '#'],
     ['#', '#', '#', '#']],
    [['.', '#'],
     ['.', '#'],
     ['.', '#'],
     ['.', '#']],
    [['#', '#'],
     ['#', '#']],
    [['#', '#', '#'],
     ['.', '.', '#'],
     ['#', '#', '#']]
]
jet_patterns = ['>>><<<>><>>><<<>>><<<><<<>><>><<>>']

chamber, fallen_rocks = simulate_rock_fall(chamber_width, chamber_height, rock_types, jet_patterns)

for row in chamber:
    print(''.join(row))

