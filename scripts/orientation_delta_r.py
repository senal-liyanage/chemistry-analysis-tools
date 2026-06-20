#!/usr/bin/env python3
"""Analyze molecular-vector orientation relative to a radial reference direction.

This script is written for pair/group orientation questions such as whether an
anion group is radially outward or inward relative to a nanoparticle center of
mass. The user supplies two atom selections that define the molecular vector
A -> B and a reference selection that defines the system center.

Example
-------
python scripts/orientation_delta_r.py \
    --topology system.gro \
    --trajectory traj.xtc \
    --reference "resname PLG" \
    --group-a "resname CHOL and name N" \
    --group-b "resname BUT and name C1 C2 O1 O2" \
    --output orientation_delta_r.csv

Interpretation
--------------
- delta_r = r_B - r_A
- positive delta_r means group B is farther from the reference COM than group A
- cos_theta compares vector A->B with the radial vector from reference COM to midpoint(A,B)
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
    parser = argparse.ArgumentParser(description="Compute delta-r and radial orientation of two molecular groups.")
    parser.add_argument("--topology", required=True, help="Topology/structure file")
    parser.add_argument("--trajectory", required=True, help="Trajectory file")
    parser.add_argument("--reference", required=True, help="MDAnalysis selection for reference COM")
    parser.add_argument("--group-a", required=True, help="Selection for vector start group A")
    parser.add_argument("--group-b", required=True, help="Selection for vector end group B")
    parser.add_argument("--start", type=int, default=None, help="First frame index")
    parser.add_argument("--stop", type=int, default=None, help="Final frame index, exclusive")
    parser.add_argument("--step", type=int, default=1, help="Frame stride")
    parser.add_argument("--output", default="orientation_delta_r.csv", help="Output CSV path")
    return parser.parse_args()


def safe_cosine(vector_1: np.ndarray, vector_2: np.ndarray) -> float:
    norm_1 = np.linalg.norm(vector_1)
    norm_2 = np.linalg.norm(vector_2)
    if norm_1 == 0.0 or norm_2 == 0.0:
        return np.nan
    return float(np.dot(vector_1, vector_2) / (norm_1 * norm_2))


def orientation_delta_r(
    topology: str,
    trajectory: str,
    reference_selection: str,
    group_a_selection: str,
    group_b_selection: str,
    start: int | None,
    stop: int | None,
    step: int,
) -> pd.DataFrame:
    universe = mda.Universe(topology, trajectory)
    reference = universe.select_atoms(reference_selection)
    group_a = universe.select_atoms(group_a_selection)
    group_b = universe.select_atoms(group_b_selection)

    if reference.n_atoms == 0:
        raise ValueError(f"Reference selection matched zero atoms: {reference_selection!r}")
    if group_a.n_atoms == 0:
        raise ValueError(f"Group A selection matched zero atoms: {group_a_selection!r}")
    if group_b.n_atoms == 0:
        raise ValueError(f"Group B selection matched zero atoms: {group_b_selection!r}")

    rows = []

    for ts in universe.trajectory[start:stop:step]:
        ref_com = reference.center_of_mass()
        a_com = group_a.center_of_mass()
        b_com = group_b.center_of_mass()
        midpoint = 0.5 * (a_com + b_com)

        r_a = np.linalg.norm(a_com - ref_com)
        r_b = np.linalg.norm(b_com - ref_com)
        molecular_vector = b_com - a_com
        radial_vector = midpoint - ref_com

        rows.append(
            {
                "frame": int(ts.frame),
                "time": float(getattr(ts, "time", np.nan)),
                "r_a": float(r_a),
                "r_b": float(r_b),
                "delta_r_b_minus_a": float(r_b - r_a),
                "cos_theta_radial": safe_cosine(molecular_vector, radial_vector),
            }
        )

    if not rows:
        raise ValueError("No trajectory frames were processed. Check start/stop/step options.")

    return pd.DataFrame(rows)


def main() -> None:
    args = parse_args()
    df = orientation_delta_r(
        topology=args.topology,
        trajectory=args.trajectory,
        reference_selection=args.reference,
        group_a_selection=args.group_a,
        group_b_selection=args.group_b,
        start=args.start,
        stop=args.stop,
        step=args.step,
    )
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output, index=False)
    print(f"Wrote orientation table to {output}")


if __name__ == "__main__":
    main()
