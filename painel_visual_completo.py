
"""Simple Tkinter interface to control the monitoring service."""

from pathlib import Path
from subprocess import Popen
import tkinter as tk


def start_scanner() -> None:
    """Launch the scanner script in a new process."""
    Popen(["python", "reciclador_inteligente_scanner.py"])


def main() -> None:
    """Run the basic GUI."""
    root = tk.Tk()
    root.title("Sintaxes Monitor")

    tk.Button(root, text="Executar Scanner", command=start_scanner).pack(padx=20, pady=10)
    tk.Button(root, text="Abrir Relatório", command=lambda: Popen(["notepad", str(Path("relatorio_reciclagem.txt"))])).pack(padx=20, pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
