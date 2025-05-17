
"""Scan the monitored folder and produce a simple report."""

from pathlib import Path


def scan_folder(folder: Path, report: Path) -> None:
    """Write a list of files under *folder* into *report*."""
    with report.open("w", encoding="utf-8") as f:
        for path in sorted(folder.rglob("*")):
            if path.is_file():
                size = path.stat().st_size
                f.write(f"{path.relative_to(folder)} - {size} bytes\n")


def main() -> None:
    base = Path(__file__).resolve().parent
    folder = base / "monitora"
    report = base / "relatorio_reciclagem.txt"
    folder.mkdir(exist_ok=True)
    scan_folder(folder, report)


if __name__ == "__main__":
    main()
