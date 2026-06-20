# Methods overview

This document describes the scientific intent behind the analysis scaffold in this repository.

## Scope

The analysis templates are intended for atomistic molecular simulation projects where the main questions involve molecular organization around a reference object such as a polymer nanoparticle, protein, ligand, ion cluster, or molecular aggregate.

## Typical inputs

- GROMACS-compatible topology/structure files such as `.gro`, `.pdb`, or `.tpr`
- Trajectory files such as `.xtc` or `.trr`
- Atom selections defined using MDAnalysis selection syntax
- Optional CSV files containing precomputed centers of mass, distance shells, or summary statistics

## Analysis concepts

### Radial density

Radial density analysis bins atoms, residues, molecules, or centers of mass by distance from a reference center. For nanoparticle systems, the reference center is commonly the nanoparticle center of mass.

Typical outputs:

- distance-bin centers
- raw counts per shell
- shell volumes
- number density or mass density

### Distance-shell counts

Distance-shell counts summarize how many atoms, residues, molecules, or molecular centers fall within a defined radius or radial interval. This is useful for hydration, ion localization, or ligand proximity analysis.

Typical outputs:

- count within each radius
- count per frame
- mean, standard deviation, and replicate-level summaries

### Interfacial orientation

Orientation analysis compares a molecular vector with a radial vector from the reference center. For ion pairs or amphiphilic molecules, this can test whether one group preferentially points toward or away from an interface.

Typical outputs:

- radial position of the molecular center
- signed radial displacement between two molecular groups
- cosine of the angle between a molecular vector and the radial vector
- shell-averaged orientation statistics

## Portfolio note

The files in this repository are designed to demonstrate reproducible analysis structure and scientific interpretation. They should be adapted and validated before use in a production manuscript workflow.
