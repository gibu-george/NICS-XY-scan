#!/usr/bin/env python
import readline
import matplotlib.pyplot as plt

print("\nPRESS Ctrl+c to exit the program.\n")

# Enable tab-completion for file selection
readline.set_completer_delims('\t\n')
readline.parse_and_bind("tab: complete")

def elementNo(element):
    eleNumber = 6.000000
    periodTable = ['Bq', 'H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', \
                    'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', \
                    'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe', \
                    'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta', \
                    'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th', 'Pa', 'U', \
                    'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', \
                    'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og']
    eleNumber = periodTable.index(element)
    return eleNumber

# ========================== Read original output file ==========================
print("Please specify the Gaussian output file path of NMR:")

fileName = input("(e.g.: /home/system/nmr.log)\n")
if fileName.strip()[0] == '\'' and fileName.strip()[-1] == '\'':
    fileName = fileName.strip()[1:-1]

print("\nPlease wait...")
print("The magnetic shielding tensor is extracting from the output file...\n")

shieldTensorIso = []
shieldTensorAni = []
shieldTensorXX = []
shieldTensorYX = []
shieldTensorZX = []
shieldTensorXY = []
shieldTensorYY = []
shieldTensorZY = []
shieldTensorXZ = []
shieldTensorYZ = []
shieldTensorZZ = []
atomicLabels = []
xCoordinates = []
zCoordinates = []

with open(fileName, 'r') as icssOut:
    outputLines = icssOut.readlines()

print(f"Processing {fileName}...")

tensorCount = 0

for outputLine in outputLines:
    if ' NumDoF:  NAt=' in outputLine:
        sysAtomNumbers = int(outputLine.split()[2])
        bqAtomNumbers = int(outputLine.split()[4]) - int(outputLine.split()[2])
    elif 'Isotropic =' in outputLine:
        tensorCount += 1
        if tensorCount > sysAtomNumbers:
            atomicLabels.append(outputLine.split()[0])
            shieldTensorIso.append(- float(outputLine.split()[4]))
            shieldTensorAni.append(- float(outputLine.split()[7]))
    elif ('XX=  ' in outputLine) and ('YX=  ' in outputLine) and ('ZX=  ' in outputLine) and (tensorCount > sysAtomNumbers):
        shieldTensorXX.append(- float(outputLine.split()[1]))
        shieldTensorYX.append(- float(outputLine.split()[3]))
        shieldTensorZX.append(- float(outputLine.split()[5]))
    elif ('XY=  ' in outputLine) and ('YY=  ' in outputLine) and ('ZY=  ' in outputLine) and (tensorCount > sysAtomNumbers):
        shieldTensorXY.append(- float(outputLine.split()[1]))
        shieldTensorYY.append(- float(outputLine.split()[3]))
        shieldTensorZY.append(- float(outputLine.split()[5]))
    elif ('XZ=  ' in outputLine) and ('YZ=  ' in outputLine) and ('ZZ=  ' in outputLine) and (tensorCount > sysAtomNumbers):
        shieldTensorXZ.append(- float(outputLine.split()[1]))
        shieldTensorYZ.append(- float(outputLine.split()[3]))
        shieldTensorZZ.append(- float(outputLine.split()[5]))

for line1 in outputLines:
    if 'Bq              ' in line1:
        xCoordinates.append(float(line1.split()[1]))
        zCoordinates.append(float(line1.split()[3]))

print("Processing finished!\n")

print("Choose shielding tensor for the NICS-XY plot:")
print("      1 - Isoptropic       2 - Anisotropy")
print("      3 - XX component     4 - YX component     5 - ZX component")
print("      6 - XY component     7 - YY component     8 - ZY component")
print("      9 - XZ component    10 - YZ component    11 - ZZ component")
nicsTensor = input('Please input the No.: ')
tensorType = ''
tensorLabel = ''

if nicsTensor == '1':
    mapValue = shieldTensorIso
    tensorType = 'iso'
    tensorLabel = 'iso'
elif nicsTensor == '2':
    mapValue = shieldTensorAni
    tensorType = 'ani'
    tensorLabel = 'ani'
elif nicsTensor == '3':
    mapValue = shieldTensorXX
    tensorType = 'xx'
    tensorLabel = 'xx'
elif nicsTensor == '4':
    mapValue = shieldTensorYX
    tensorType = 'yx'
    tensorLabel = 'yx'
elif nicsTensor == '5':
    mapValue = shieldTensorZX
    tensorType = 'zx'
    tensorLabel = 'zx'
elif nicsTensor == '6':
    mapValue = shieldTensorXY
    tensorType = 'xy'
    tensorLabel = 'xy'
elif nicsTensor == '7':
    mapValue = shieldTensorYY
    tensorType = 'yy'
    tensorLabel = 'yy'
elif nicsTensor == '8':
    mapValue = shieldTensorZY
    tensorType = 'zy'
    tensorLabel = 'zy'
elif nicsTensor == '9':
    mapValue = shieldTensorXZ
    tensorType = 'xz'
    tensorLabel = 'xz'
elif nicsTensor == '10':
    mapValue = shieldTensorYZ
    tensorType = 'yz'
    tensorLabel = 'yz'
elif nicsTensor == '11':
    mapValue = shieldTensorZZ
    tensorType = 'zz'
    tensorLabel = 'zz'

# Plotting the graph
plt.figure(figsize=(10, 6))
plt.plot(xCoordinates, mapValue, marker='o', linestyle='-', color='b', label=f'NICS({zCoordinates[0]:.1f})$_{{\mathrm{{{tensorLabel}}}}}$')
plt.xlabel('Distance / Å', fontsize=14, fontweight='bold')
plt.ylabel('Chemical Shift / ppm', fontsize=14, fontweight='bold')

# Configure ticks
plt.xticks(fontsize=12, fontweight='bold')
plt.yticks(fontsize=12, fontweight='bold')
plt.minorticks_on()
plt.tick_params(axis='x', which='both', direction='in', top=True)
plt.tick_params(axis='y', which='both', direction='in', right=True)
plt.tick_params(axis='x', which='minor', length=4)
plt.tick_params(axis='x', which='major', length=7)
plt.grid(False)  # Disable the grid

# Add legend with font properties
plt.legend(prop={'size': 14, 'weight': 'bold'})

# Save the plot before showing it
plt.savefig(f"{fileName.strip()[:-4]}_XY_{tensorType}.png", dpi=300)
plt.show()
