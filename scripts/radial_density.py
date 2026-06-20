#!/usr/bin/env python3
"""Compute a simple radial number-density profile from an MD trajectory.

Example
-------
python scripts/radial_density.py \
    --topology system.gro \
    --trajectory traj.xtc \
    --reference "resname PLG" \
    --selection "name OW" \
    --rmax 6.0 \
    --bin-width 0.05 \
    --output radial_density.csv

Notes
-----
Distances are reported in Angstrom when using MDAnalysis default coordinate units.
Convert to nm in downstream plotting if your manuscript workflow uses nm.
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
    parser = argparse.ArgumentParser(description="Compute radial number density around a reference COM.")
    parser.add_argument("--topology", required=True, help="Topology/structure file, e.g. .gro, .pdb, or .tpr")
    parser.add_argument("--trajectory", required=True, help="Trajectory file, e.g. .xtc or .trr")
    parser.add_argument("--reference", required=True, help="MDAnalysis selection for reference COM")
    parser.add_argument("--selection", required=True, help="MDAnalysis selection to bin radially")
    parser.add_argument("--rmax", type=float, default=60.0, help="Maximum radius in coordinate units; default 60 A")
    parser.add_argument("--bin-width", type=float, default=1.0, help="Radial bin width in coordinate units; default 1 A")
    parser.add_argument("--start", type=int, default=None, help="First frame index")
    parser.add_argument("--stop", type=int, default=None, help="Final frame index, exclusive")
    parser.add_argument("--step", type=int, default=1, help="Frame stride")
    parser.add_argument("--output", default="radial_density.csv", help="Output CSV path")
    return parser.parse_args()


def shell_volumes(edges: np.ndarray) -> np.ndarray:
    """Return spherical shell volumes for radial bin edges."""
    return (4.0 / 3.0) * np.pi * (edges[1:] ** 3 - edges[:-1] ** 3)


def radial_density(
    topology: str,
    trajectory: str,
    reference_selection: str,
    target_selection: str,
    rmax: float,
    bin_width: float,
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

    edges = np.arange(0.0, rmax + bin_width, bin_width)
    counts = np.zeros(len(edges) - 1, dtype=float)
    n_frames = 0

    for _ts in universe.trajectory[start:stop:step]:
        ref_com = reference.center_of_mass()
        distances = np.linalg.norm(target.positions - ref_com, axis=1)
        hist, _ = np.histogram(distances, bins=edges)
        counts += hist
        n_frames += 1

    if n_frames == 0:
        raise ValueError("No trajectory frames were processed. Check start/stop/step options.")

    volumes = shell_volumes(edges)
    mean_counts = counts / n_frames
    density = mean_counts / volumes
    centers = 0.5 * (edges[1:] + edges[:-1])

    return pd.DataFrame(
        {
            "r_inner": edges[:-1],
            "r_outer": edges[1:],
            "r_center": centers,
            "mean_count": mean_counts,
            "shell_volume": volumes,
            "number_density": density,
            "n_frames": n_frames,
        }
    )


def main() -> None:
    args = parse_args()
    df = radial_density(
        topology=args.topology,
        trajectory=args.trajectory,
        reference_selection=args.reference,
        target_selection=args.selection,
        rmax=args.rmax,
        bin_width=args.bin_width,
        start=args.start,
        stop=args.stop,
        step=args.step,
    )
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output, index=False)
    print(f"Wrote radial density profile to {output}")


if __name__ == "__main__":
    main()
