# chemistry-analysis-tools

`chemistry-analysis-tools` is a lightweight collection of small Python utilities for molecule-file cleanup and partial-charge analysis. The current repository is centered on practical MOL2-oriented helpers rather than a fully packaged software library.

## Current scripts
### `mol2_formatter.py`
Formats a MOL2 file using the Open Babel command-line tool and writes a cleaned output MOL2 file.

Typical use:

```bash
python mol2_formatter.py input.mol2 -o output_formatted.mol2
```

### `mol2_charge_diff.py`
Computes per-atom charge differences between metal-bound, metal-unbound, and metal-only MOL2 files using the Open Babel Python bindings.

Typical use:

```bash
python mol2_charge_diff.py bound.mol2 unbound.mol2 metal.mol2
```

By default, the script writes a text report named `charge_difference.txt`.

## Requirements
- Python 3
- Open Babel command-line tool (`obabel`) for `mol2_formatter.py`
- Open Babel Python bindings for `mol2_charge_diff.py`

## Repository scope
This repository is intended as a practical utility collection for small chemistry file-manipulation tasks. It is most useful for focused command-line workflows where a full package would be unnecessary overhead.

## Notes
- These tools assume MOL2 inputs with atom and residue information compatible with the current parsing logic.
- Users may need to adapt the scripts for project-specific naming conventions or atom-selection schemes.

## Contributing
Small, focused pull requests are preferred. Good contributions include bug fixes, clearer error handling, usage examples, and lightweight refactoring that improves script reliability without overcomplicating the repository.

## Citation
If this repository contributes to published work, please cite the repository and the version used.

## License
This project is released under the MIT License. See [`LICENSE`](LICENSE) for details.
