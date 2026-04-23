"""Compute per-atom charge differences across related MOL2 files.

This script compares metal-bound, metal-unbound, and metal-only MOL2 files and
writes a per-atom charge-difference report.

Usage:
    python mol2_charge_diff.py bound.mol2 unbound.mol2 metal.mol2
"""

import argparse
import logging
import sys

from openbabel import openbabel as ob

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_mol2(path):
    conv = ob.OBConversion()
    conv.SetInFormat("mol2")
    mol = ob.OBMol()
    if not conv.ReadFile(mol, path):
        raise ValueError(f"Failed to read MOL2 file: {path}")
    return mol


def extract_residue_charges(mol):
    charges = {}
    for res in ob.OBResidueIter(mol):
        res_id = res.GetNum()
        for atom in ob.OBResidueAtomIter(res):
            atom_name = res.GetAtomID(atom).strip()
            charges[f"{res_id}_{atom_name}"] = atom.GetPartialCharge()
    return charges


def write_charge_difference_report(bound_mol, bound_charges, unbound_charges, metal_charges, output_path):
    with open(output_path, "w") as handle:
        handle.write(
            f"{'Residue ID':<10} {'Atom Name':<10} {'Bound Charge':<15} "
            f"{'Unbound Charge':<15} {'Metal Charge':<15} {'Charge Difference':<18}\n"
        )

        for res in ob.OBResidueIter(bound_mol):
            res_id = res.GetNum()
            for atom in ob.OBResidueAtomIter(res):
                atom_name = res.GetAtomID(atom).strip()
                key = f"{res_id}_{atom_name}"
                if key not in bound_charges or key not in unbound_charges or key not in metal_charges:
                    continue

                bound_charge = bound_charges[key]
                unbound_charge = unbound_charges[key]
                metal_charge = metal_charges[key]
                diff = bound_charge - (unbound_charge + metal_charge)

                line = (
                    f"{res_id:<10} {atom_name:<10} {bound_charge:<15.4f} "
                    f"{unbound_charge:<15.4f} {metal_charge:<15.4f} {diff:<18.4f}"
                )
                handle.write(line + "\n")
                print(line)


def main():
    parser = argparse.ArgumentParser(description="Calculate charge differences from related MOL2 files.")
    parser.add_argument("bound", help="Path to the metal-bound MOL2 file.")
    parser.add_argument("unbound", help="Path to the metal-unbound MOL2 file.")
    parser.add_argument("metal", help="Path to the metal-only MOL2 file.")
    parser.add_argument(
        "-o",
        "--output",
        default="charge_difference.txt",
        help="Output text file for the charge-difference report.",
    )
    args = parser.parse_args()

    try:
        bound_mol = load_mol2(args.bound)
        unbound_mol = load_mol2(args.unbound)
        metal_mol = load_mol2(args.metal)

        bound_charges = extract_residue_charges(bound_mol)
        unbound_charges = extract_residue_charges(unbound_mol)
        metal_charges = extract_residue_charges(metal_mol)

        common_atoms = set(bound_charges).intersection(unbound_charges, metal_charges)
        if not common_atoms:
            raise ValueError("No common residue/atom identifiers were found across the three MOL2 files.")

        logger.info("Writing charge-difference report for %d common atoms.", len(common_atoms))
        write_charge_difference_report(
            bound_mol,
            bound_charges,
            unbound_charges,
            metal_charges,
            args.output,
        )
    except Exception as exc:
        logger.error("%s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
