"""Format a MOL2 file using the Open Babel command-line tool.

Usage:
    python mol2_formatter.py input.mol2 -o output_formatted.mol2

If no output path is provided, the script writes `<input_stem>_formatted.mol2`.
"""

import argparse
import os
import subprocess
import sys


def format_mol2(input_file_path, output_file_path=None):
    """Run Open Babel to rewrite a MOL2 file in a normalized form."""
    if not os.path.isfile(input_file_path):
        raise FileNotFoundError(f"Input file not found: {input_file_path}")

    if output_file_path is None:
        file_name = os.path.splitext(os.path.basename(input_file_path))[0]
        output_file_path = f"{file_name}_formatted.mol2"

    obabel_cmd = ["obabel", "-imol2", input_file_path, "-omol2", "-O", output_file_path]
    subprocess.run(obabel_cmd, check=True)
    return output_file_path


def main():
    parser = argparse.ArgumentParser(description="Format a MOL2 file using Open Babel")
    parser.add_argument("input_file_path", help="Input MOL2 file path")
    parser.add_argument("-o", "--output_file_path", help="Output file path for formatted MOL2 file")
    args = parser.parse_args()

    try:
        output_path = format_mol2(args.input_file_path, args.output_file_path)
        print(f"Wrote formatted MOL2 file to {output_path}")
    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError:
        print("Error: Open Babel failed while formatting the MOL2 file.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
