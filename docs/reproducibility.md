# Reproducibility notes

This repository is organized so that analysis steps can be inspected, repeated, and adapted.

## Recommended practices

1. Record the exact script command used for each analysis.
2. Keep raw simulation files separate from processed summaries.
3. Save intermediate CSV outputs before making figures.
4. Use versioned scripts for manuscript or poster figures.
5. Record software versions for Python, MDAnalysis, GROMACS, Open Babel, and any other external tools.
6. Keep replicate-level summaries separate before computing pooled averages.
7. Store figure-generation code next to the figure or in a clearly named notebook.

## Suggested output structure

```text
results/
├── radial_density/
│   ├── rep01.csv
│   ├── rep02.csv
│   ├── rep03.csv
│   └── summary.csv
├── hydration_counts/
│   ├── rep01.csv
│   └── summary.csv
└── figures/
    ├── radial_density.png
    └── hydration_counts.png
```

## Version capture

For reproducible records, save these outputs with each major analysis campaign:

```bash
python --version
pip freeze > requirements_freeze.txt
gmx --version > gromacs_version.txt
```

## Validation checklist

Before trusting a trajectory-analysis result:

- Confirm atom selections match the intended molecules.
- Confirm the reference center is physically meaningful.
- Confirm periodic boundary conditions were handled appropriately.
- Confirm distance bins and units are correct.
- Confirm replicate-level trends before pooling data.
- Confirm that plotted values match the saved CSV summaries.
