from pathlib import Path
import logging


def scan(base: str = 'monitora') -> Path:
    """Escaneia arquivos dentro de ``base`` e salva relatorio_reciclagem.txt."""
    path = Path(base)
    report = Path('relatorio_reciclagem.txt')
    with report.open('w', encoding='utf-8') as f:
        for item in path.rglob('*'):
            if item.is_file():
                f.write(str(item.resolve()) + '\n')
    logging.info('Relat\u00f3rio salvo em %s', report)
    return report


if __name__ == '__main__':
    scan()
