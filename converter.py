#!/usr/bin/env python3
"""Merge multiple text files into a single output file."""

import argparse
from pathlib import Path


def merge_files(input_files: list[str], output_file: Path) -> None:
    """Merge the contents of *input_files* into *output_file*."""
    with output_file.open('w', encoding='utf-8') as dest:
        for index, name in enumerate(input_files):
            path = Path(name)
            with path.open('r', encoding='utf-8') as src:
                dest.write(src.read())
            if index < len(input_files) - 1:
                dest.write("\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Merge multiple text files into one file.")
    parser.add_argument(
        'files', nargs='+', help='Input files to merge')
    parser.add_argument(
        '-o', '--output', default='merged.txt', help='Output filename')
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    merge_files(args.files, Path(args.output))
    print(f"Merged {len(args.files)} files into '{args.output}'.")


if __name__ == '__main__':
    main()
