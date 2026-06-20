# Data policy

This repository is intended to be public-facing portfolio material. It should demonstrate technical competence without exposing restricted research material.

## Do not commit

- Full unpublished molecular dynamics trajectories
- Collaborator-owned raw data without permission
- Manuscript-sensitive intermediate results
- Proprietary input structures or force-field files
- Personal data, credentials, tokens, passwords, or private cluster paths
- Large binary outputs that cannot be inspected in GitHub

## Safe to commit

- Toy example inputs
- Sanitized CSV summary tables
- Small demonstration files created only for documentation
- Generic Slurm or Bash workflow templates
- Python scripts without hard-coded private paths
- Figures approved for public portfolio use

## Recommended approach

Use this repository for methods, scripts, examples, and public summaries. Keep production data in private storage or institutional storage, and only move sanitized derivatives into this public repository.

## File-size note

Large scientific data files should usually be excluded from Git. If a public example dataset is needed, use a small toy dataset or provide instructions for downloading a public dataset from an appropriate source.
