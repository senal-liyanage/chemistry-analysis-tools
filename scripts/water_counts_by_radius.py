#!/usr/bin/env python3
"""Count selected atoms or molecule centers within radial cutoffs.

This template is useful for hydration, ion-localization, or ligand-proximity
analysis around a nanoparticle, protein, or molecular aggregate.

Example
-------
python scripts/water_counts_by_radius.py \
    --topology system.gro \
    --trajectory traj.xtc \
    --reference "resname PLG" \
    --selection "resname SOL and name OW" \
    --radii 20 30 40 50 \
    --output water_counts.csv
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

try:
    import MDAnalysis as mda
except ImportError as exc:  # pragma: no cover
    raise SystemExit("MDAnalysis is required. Install with `pip install MDAnalysis`.") from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Count selected atoms within one or more radii of a reference COM.")
    parser.add_argument("--topology", required=True, help="Topology/structure file")
    parser.add_argument("--trajectory", required=True, help="Trajectory file")
    parser.add_argument("--reference", required=True, help="MDAnalysis selection for reference COM")
    parser.add_argument("--selection", required=True, help="MDAnalysis selection to count")
    parser.add_argument("--radii", nargs="+", type=float, required=True, help="One or more cutoff radii")
    parser.add_argument("--start", type=int, default=None, help="First frame index")
    parser.add_argument("--stop", type=int, default=None, help="Final frame index, exclusive")
    parser.add_argument("--step", type=int, default=1, help="Frame stride")
    parser.add_argument("--output", default="counts_by_radius.csv", help="Output CSV path")
    return parser.parse_args()


def counts_by_radius(
    topology: str,
    trajectory: str,
    reference_selection: str,
    target_selection: str,
    radii: list[float],
    start: int | None,
    stop: int | None,
    step: int,
) -> pd.DataFrame:
    universe = mda.Universe(topology, trajectory)
    reference = universe.select_atoms(reference_selection)
    target = universe.select_atoms(target_selection)

    if reference.n_atoms == 0:
        raise ValueError(f"Reference selection matched zero atoms: {reference_selection!r}")
    if target.n_atoms == 0:
        raise ValueError(f"Target selection matched zero atoms: {target_selection!r}")

    radii_array = np.array(sorted(radii), dtype=float)
    rows = []

    for ts in universe.trajectory[start:stop:step]:
        ref_com = reference.center_of_mass()
        distances = np.linalg.norm(target.positions - ref_com, axis=1)
        row = {"frame": int(ts.frame), "time": float(getattr(ts, "time", np.nan))}
        for radius in radii_array:
            row[f"count_within_{radius:g}"] = int(np.count_nonzero(distances <= radius))
        rows.append(row)

    if not rows:
        raise ValueError("No trajectory frames were processed. Check start/stop/step options.")

    return pd.DataFrame(rows)


def main() -> None:
    args = parse_args()
    df = counts_by_radius(
        topology=args.topology,
        trajectory=args.trajectory,
        reference_selection=args.reference,
        target_selection=args.selection,
        radii=args.radii,
        start=args.start,
        stop=args.stop,
        step=args.step,
    )
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output, index=False)
    print(f"Wrote radius-count table to {output}")


if __name__ == "__main__":
    main()
