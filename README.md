# chemistry-analysis-tools

`chemistry-analysis-tools` is a practical portfolio repository for lightweight computational chemistry, molecule-file, and molecular-simulation analysis utilities. The repository is designed to show clean command-line scripting, reproducible scientific analysis habits, and chemistry-aware data handling rather than a fully packaged software library.

## What this repository demonstrates

- Python command-line tools for chemistry file handling and analysis
- MOL2 formatting and partial-charge comparison workflows
- Molecular dynamics analysis scaffolds for radial, hydration, and interfacial metrics
- Reproducible project structure with documentation, example folders, and data-use notes
- Portfolio-ready scientific software practices: clear inputs, explicit outputs, and defensible assumptions

## Current utilities

### `mol2_formatter.py`
Formats a MOL2 file using the Open Babel command-line tool and writes a cleaned output MOL2 file.

```bash
python mol2_formatter.py input.mol2 -o output_formatted.mol2
```

### `mol2_charge_diff.py`
Computes per-atom charge differences between metal-bound, metal-unbound, and metal-only MOL2 files using the Open Babel Python bindings.

```bash
python mol2_charge_diff.py bound.mol2 unbound.mol2 metal.mol2
```

By default, the script writes a text report named `charge_difference.txt`.

## Molecular simulation analysis scaffold

The `scripts/` and `docs/` folders add a portfolio-grade scaffold for molecular dynamics analysis workflows, including:

- radial density and mass-envelope analysis
- solvent or ion counts within distance shells
- interfacial orientation metrics relative to a nanoparticle center of mass
- data-policy notes for using toy or sanitized data when full trajectories are unpublished or too large

These scripts are intentionally written as clear starting points. They are suitable for adapting to GROMACS-compatible trajectories using tools such as MDAnalysis.

## Suggested repository layout

```text
chemistry-analysis-tools/
├── mol2_formatter.py
├── mol2_charge_diff.py
├── scripts/
│   ├── radial_density.py
│   ├── water_counts_by_radius.py
│   └── orientation_delta_r.py
├── docs/
│   ├── methods.md
│   ├── reproducibility.md
│   └── data_policy.md
├── examples/
│   └── toy_system/
├── environment.yml
└── requirements.txt
```

## Requirements

Core utilities:

- Python 3.10+
- Open Babel command-line tool (`obabel`) for `mol2_formatter.py`
- Open Babel Python bindings for `mol2_charge_diff.py`

MD-analysis scaffold:

- NumPy
- pandas
- matplotlib
- MDAnalysis

Install the Python-only analysis dependencies with:

```bash
pip install -r requirements.txt
```

or create the conda environment:

```bash
conda env create -f environment.yml
conda activate chemistry-analysis-tools
```

## Data policy

This repository should not contain unpublished production trajectories, collaborator-owned datasets, proprietary simulation inputs, or manuscript-sensitive raw results. Use toy data, public data, or sanitized examples that demonstrate the analysis logic without exposing restricted research material.

## Portfolio relevance

This repository supports computational chemistry and scientific-computing job applications by demonstrating:

- molecular file manipulation
- chemistry-aware parsing and comparison
- trajectory-analysis workflow design
- reproducible documentation
- responsible separation of code from sensitive research data

## Citation

If this repository contributes to published work, cite the repository and the version or commit hash used.

## License

This project is released under the MIT License. See [`LICENSE`](LICENSE) for details.
