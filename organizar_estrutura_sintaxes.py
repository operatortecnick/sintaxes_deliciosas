from pathlib import Path
"""Utilities to create the project folder tree."""


def criar_arquivo_if_needed(caminho: Path, created: list[str]):
    """Create an empty file if it does not exist."""
    if not caminho.exists():
        caminho.parent.mkdir(parents=True, exist_ok=True)
        caminho.touch()
        created.append(str(caminho.relative_to(Path(__file__).resolve().parent)))


def main(log: bool = False):
    """Create the expected directory layout."""
    base = Path(__file__).resolve().parent
    created: list[str] = []

    arquivos_topo = [
        "start_services.bat",
        "abrir_reciclador_scanner.bat",
        "organizar_estrutura_sintaxes.bat",
        "painel_visual_completo.py",
        "reciclador_inteligente_scanner.py",
    ]
    for nome in arquivos_topo:
        criar_arquivo_if_needed(base / nome, created)

    src = base / "src"
    diretorios = [
        src / "funcoes",
        src / "modulos",
        src / "logs",
        src / "__pycache__",
    ]
    for d in diretorios:
        d.mkdir(parents=True, exist_ok=True)

    arquivos_src = [
        src / "bot.py",
        src / "main.py",
        src / "funcoes" / "utils.py",
        src / "modulos" / "watchdog_module.py",
        src / "modulos" / "telegram_module.py",
        src / "logs" / "registro.log",
        src / "logs" / "screenshot.png",
    ]
    for caminho in arquivos_src:
        criar_arquivo_if_needed(caminho, created)

    (base / "monitora").mkdir(exist_ok=True)

    if log:
        log_path = base / "src" / "logs" / "estrutura.log"
        with log_path.open("a", encoding="utf-8") as f:
            for item in created:
                f.write(f"{item}\n")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Create project folders")
    parser.add_argument("--log", action="store_true", help="write created files to log")
    args = parser.parse_args()

    main(log=args.log)
