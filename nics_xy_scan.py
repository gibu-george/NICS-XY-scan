#!/usr/bin/env python
import os
import readline
import numpy as np

print("\ncode for NICS-XY scan - by Gibu George\n")
print("\nPRESS Ctrl+c to exit the program.\n")

# Enable tab-completion for file selection
readline.set_completer_delims('\t\n')
readline.parse_and_bind("tab: complete")

# Prompt the user for the original input file path
file_prompt = "Please specify fileName (press Tab to autocomplete):\n"
fileName = input(file_prompt)

# Check if the file exists in the current directory
try:
    fileName = os.path.normpath(fileName)
    with open(fileName, 'r') as originalInput:
        inputLines = originalInput.readlines()
    print(f"Selected file: {fileName}")
except FileNotFoundError:
    print(f"File not found: {fileName}")
    exit()

# Extract atomic coordinates
atoms = []
coordinates = []

for line in inputLines:
    if len(line.split()) == 4:
        atom, x, y, z = line.split()
        atoms.append(atom)
        coordinates.append([float(x), float(y), float(z)])

# Convert to numpy array for easier manipulation
coordinates = np.array(coordinates)

# User specifies the height for Bq atoms
while True:
    try:
        height = float(input("\nPlease input the height at which to add Bq atoms (in angstrom):\n"))
        break
    except ValueError:
        print("\nInput error, please input a number!")
        continue

# Get the list of bonds from the user
bonds = []
print("\nPlease specify the bonds as pairs of atomic numbers (starting from 1). Type 'done' when finished:")
while True:
    bond_input = input("Enter bond (e.g., 1 2): ")
    if bond_input.lower() == 'done':
        break
    try:
        i, j = map(int, bond_input.split())
        i -= 1  # Convert to zero-based index
        j -= 1  # Convert to zero-based index
        if i >= 0 and j >= 0 and i < len(atoms) and j < len(atoms):
            bonds.append((i, j))
        else:
            print("Invalid indices. Please enter valid atomic numbers.")
    except ValueError:
        print("Input error. Please enter two integer indices separated by a space or type 'done'.")

# Calculate midpoints of the specified bonds and place Bq atoms at these midpoints
midpoints = []
for bond in bonds:
    i, j = bond
    midpoint = (coordinates[i] + coordinates[j]) / 2
    midpoints.append(midpoint)

# Convert midpoints to numpy array for easier manipulation
midpoints = np.array(midpoints)

# Ask the user for the distance between Bq atoms
while True:
    interval_input = input("\nPlease input the distance between Bq atoms (in angstrom, default is 0.2):\n")
    if interval_input == '':
        interval = 0.2
        break
    try:
        interval = float(interval_input)
        break
    except ValueError:
        print("\nInput error, please input a number!")
        continue

# Function to add Bq atoms at regular intervals along the path connecting midpoints
def add_bq_atoms_between_midpoints(midpoints, height, interval):
    bq_atoms = []
    for i in range(len(midpoints) - 1):
        start = midpoints[i]
        end = midpoints[i + 1]
        vector = end - start
        length = np.linalg.norm(vector)
        unit_vector = vector / length
        n_bq_atoms = int(length // interval)
        for k in range(n_bq_atoms + 1):
            position = start + k * interval * unit_vector
            bq_position = position + np.array([0, 0, height])
            bq_atoms.append(bq_position)
    return np.array(bq_atoms)

# Add Bq atoms at regular intervals along the path connecting the midpoints
bq_atoms = add_bq_atoms_between_midpoints(midpoints, height, interval)

# Write the output to a new file
output_file = os.path.splitext(fileName)[0] + f"_with_Bq_{str(height).replace('.', '_')}.com"
header = f"""%NProcShared=8
%mem=38Gb
%chk={os.path.splitext(fileName)[0]}.chk
#p LC-wPBE/def2TZVPP NMR=giao IOp(10/46=1) geom=connectivity

{os.path.splitext(fileName)[0]}

0 1
"""

with open(output_file, 'w') as f:
    for atom, coord in zip(atoms, coordinates):
        f.write(f"{atom:<3} {coord[0]:>10.6f} {coord[1]:>10.6f} {coord[2]:>10.6f}\n")
    for bq in bq_atoms:
        f.write(f"Bq  {bq[0]:>10.6f} {bq[1]:>10.6f} {bq[2]:>10.6f}\n")
    f.write('\n')
    for i in range(1, len(atoms) + len(bq_atoms) + 1):
        f.write(f"{i}\n")

print(f"\nOutput file '{output_file}' generated successfully.")
print("Submit the calculation")
