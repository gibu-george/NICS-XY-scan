## NICS-XY Scan and ICSS Plotting Tools

This repository contains two Python scripts to automate NICS-XY / ICSS analyses using Gaussian and post-processing of NMR shielding tensors.

The workflow consists of:

1. Generating Gaussian input files with Bq probe atoms positioned along selected bonds.
2. Extracting magnetic shielding tensors from Gaussian NMR outputs and plotting NICS-XY curves.

These tools are useful for aromaticity and magnetic response analyses.

---

## 1. NICS-XY Input Generator

### Purpose

Generates Gaussian input files by inserting Bq (ghost) atoms at regular intervals along a user-defined path between bond midpoints.  
This enables automated NICS-XY or ICSS scans.

### How it works

- Reads an input structure file containing atomic coordinates.
- User selects bonds by atomic indices.
- Computes midpoints of selected bonds.
- Places Bq atoms along the path connecting these midpoints.
- Writes a Gaussian `.com` input file including the Bq atoms and connectivity section.

### Required input

- A Gaussian-style coordinate file containing atomic symbols and Cartesian coordinates.

### Running the script

The script will interactively ask for:

- Input filename (tab completion enabled)
- Height of Bq atoms above the molecular plane
- Bond pairs defining the scan path
- Distance interval between Bq points

### Output

- Gaussian input file:  
  `input_with_Bq_<height>.com`

Ready for Gaussian NMR calculations.

---
