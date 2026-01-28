## NICS-XY Scan

This repository contains two Python scripts to automate NICS-XY analyses and post-processing of NMR shielding tensors. The scripts are interactive by design to allow flexibility of the user.

The workflow consists of:

1. Generating Gaussian input files with Bq probe atoms positioned along selected bonds.
2. Extracting magnetic shielding tensors from Gaussian NMR outputs and plotting NICS-XY curves.

---

## 1. NICS-XY Input Generator (nics_xy_scan.py)

### Purpose

Generates Gaussian input files by inserting Bq (ghost) atoms at regular intervals along a user-defined path between bond midpoints.  
This enables automated NICS-XY scans.

### How it works

- Reads an input structure file containing just the cartesian coordinates.
- User selects bonds by atomic indices.
- Computes midpoints of selected bonds.
- Places Bq atoms along the path connecting these midpoints.
- Writes a Gaussian `.com` input file including the Bq atoms and connectivity section.

### Running the script

The script will interactively ask for:

- Height of Bq atoms above the molecular plane
- Bond pairs defining the scan path
- Distance interval between Bq points

### Output

- Gaussian input file:  
  `input_with_Bq_<height>.com`

Ready for Gaussian NMR calculations.

---

## 2. NICS-XY Plot (NICS_XY_plot.py)

### Purpose

Extracts NMR shielding tensors of Bq probe atoms from Gaussian output files and plots NICS-XY curves.

### How it works

- Reads Gaussian NMR output (`.log` or `.out`).
- Allows user to select tensor component (iso, xx, yy, zz, etc.) and the extracts the tensor components of shielding for Bq atoms.
- Plots NICS values along the scan coordinate.
- Saves the plots to PNG file.

### Running the script

The script interactively asks for:

- Gaussian output filename
- Tensor component to plot

### Output

- PNG figure:  
  `<outputname>_XY_<tensor>.png`

---
## How to cite this script

If you think this script contributed to your work, please consider citing this in your list of references.
You can navigate to Zenodo repository using the DOI below and export the citation in different styles and formats.

[![DOI](https://zenodo.org/badge/1143485919.svg)](https://doi.org/10.5281/zenodo.18402009)
