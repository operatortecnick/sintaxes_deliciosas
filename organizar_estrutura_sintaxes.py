import argparse
import logging
from pathlib import Path
from typing import Iterable

# Conteúdo padrao para arquivos gerados
FILE_CONTENT = {
    "start_services.bat": "@echo off\nREM Start the bot and main process\npython src/main.py\n",
    "abrir_reciclador_scanner.bat": "@echo off\nREM Start the scanner/recycler\npython reciclador_inteligente_scanner.py\n",
    "organizar_estrutura_sintaxes.bat": "@echo off\npython organizar_estrutura_sintaxes.py\n",
    "painel_visual_completo.py": "from tkinter import Tk, Button\nfrom reciclador_inteligente_scanner import scan\n\n\ndef main():\n    root = Tk()\n    Button(root, text='Executar Scanner', command=scan).pack(padx=20, pady=20)\n    root.mainloop()\n\n\nif __name__ == '__main__':\n    main()\n",
    "reciclador_inteligente_scanner.py": "from pathlib import Path\nimport logging\n\n\ndef scan(base: str = 'monitora') -> Path:\n    path = Path(base)\n    report = Path('relatorio_reciclagem.txt')\n    with report.open('w', encoding='utf-8') as f:\n        for item in path.rglob('*'):\n            if item.is_file():\n                f.write(str(item.resolve()) + '\n')\n    logging.info('Relat\u00f3rio salvo em %s', report)\n    return report\n\n\nif __name__ == '__main__':\n    scan()\n",
    "src/bot.py": "import os\nimport requests\nimport time\nimport logging\n\nTOKEN = os.getenv('TELEGRAM_TOKEN')\nCHAT_ID = os.getenv('TELEGRAM_CHAT_ID')\nOFFSET = 0\n\n\ndef send_message(text: str):\n    if not TOKEN or not CHAT_ID:\n        logging.warning('Telegram n\u00e3o configurado.')\n        return\n    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'\n    requests.post(url, data={'chat_id': CHAT_ID, 'text': text})\n\n\ndef handle_update(update):\n    message = update.get('message', {}).get('text', '')\n    if message == '/start':\n        send_message('Bot iniciado!')\n    elif message == '/print':\n        send_message('Comando /print recebido.')\n\n\ndef bot_loop(stop_event):\n    global OFFSET\n    while not stop_event.is_set():\n        url = f'https://api.telegram.org/bot{TOKEN}/getUpdates'\n        resp = requests.get(url, params={'timeout': 30, 'offset': OFFSET + 1})\n        if resp.ok:\n            for update in resp.json().get('result', []):\n                OFFSET = update['update_id']\n                handle_update(update)\n        time.sleep(1)\n",
    "src/main.py": "import logging\nfrom pathlib import Path\nfrom threading import Event, Thread\nfrom time import sleep\nfrom funcoes.utils import setup_logging\nfrom modulos.watchdog_module import start_monitor\nfrom bot import bot_loop\n\n\ndef main():\n    log_file = Path('src/logs/registro.log')\n    setup_logging(log_file)\n    stop_event = Event()\n    observer = start_monitor(Path('monitora'))\n    bot_thread = Thread(target=bot_loop, args=(stop_event,), daemon=True)\n    bot_thread.start()\n    try:\n        while True:\n            logging.info('Heartbeat')\n            sleep(10)\n    except KeyboardInterrupt:\n        logging.info('Encerrando...')\n    finally:\n        stop_event.set()\n        observer.stop()\n        observer.join()\n        bot_thread.join()\n\n\nif __name__ == '__main__':\n    main()\n",
    "src/funcoes/utils.py": "import logging\nfrom pathlib import Path\n\n\ndef setup_logging(log_file: Path, level: int = logging.INFO) -> None:\n    log_file.parent.mkdir(parents=True, exist_ok=True)\n    fmt = '%(asctime)s [%(levelname)s] %(message)s'\n    handlers = [logging.FileHandler(log_file), logging.StreamHandler()]\n    logging.basicConfig(level=level, format=fmt, handlers=handlers)\n",
    "src/modulos/watchdog_module.py": "from watchdog.observers import Observer\nfrom watchdog.events import FileSystemEventHandler\nimport logging\nfrom pathlib import Path\n\n\nclass MonitorHandler(FileSystemEventHandler):\n    def __init__(self, callback=None):\n        self.callback = callback\n\n    def on_any_event(self, event):\n        logging.info('Evento %s em %s', event.event_type, event.src_path)\n        if self.callback:\n            self.callback(event)\n\n\ndef start_monitor(path: Path, callback=None) -> Observer:\n    handler = MonitorHandler(callback)\n    observer = Observer()\n    observer.schedule(handler, str(path), recursive=True)\n    observer.start()\n    logging.info('Monitorando %s', path)\n    return observer\n",
    "src/modulos/telegram_module.py": "import os\nimport logging\nimport requests\n\nTOKEN = os.getenv('TELEGRAM_TOKEN')\nCHAT_ID = os.getenv('TELEGRAM_CHAT_ID')\n\n\ndef send_message(text: str) -> None:\n    if not TOKEN or not CHAT_ID:\n        logging.warning('Credenciais do Telegram ausentes.')\n        return\n    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'\n    resp = requests.post(url, data={'chat_id': CHAT_ID, 'text': text})\n    if not resp.ok:\n        logging.error('Falha ao enviar mensagem: %s', resp.text)\n",
}

# Diret\u00f3rios necess\u00e1rios
DIRS = [
    Path('src/funcoes'),
    Path('src/modulos'),
    Path('src/logs'),
    Path('monitora'),
]

FILES = list(FILE_CONTENT.keys()) + [
    'src/logs/registro.log',
    'src/logs/screenshot.png',
    'relatorio_reciclagem.txt',
]


def write_file(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8') as f:
        f.write(content)


def create_structure(base: Path, force: bool = False) -> None:
    for d in DIRS:
        (base / d).mkdir(parents=True, exist_ok=True)
    for name in FILES:
        content = FILE_CONTENT.get(name, '')
        write_file(base / name, content, force)


def check_structure(base: Path) -> Iterable[str]:
    missing = []
    for d in DIRS:
        if not (base / d).exists():
            missing.append(str(base / d))
    for f in FILES:
        if not (base / f).exists():
            missing.append(str(base / f))
    return missing


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description='Gerencia a estrutura do projeto')
    parser.add_argument('--base', type=Path, default=Path('.'), help='Diretorio base')
    parser.add_argument('--force', action='store_true', help='Sobrescreve arquivos existentes')
    parser.add_argument('--check', action='store_true', help='Apenas verifica a estrutura')
    parser.add_argument('--log', type=Path, help='Arquivo de log')
    args = parser.parse_args(argv)

    if args.log:
        logging.basicConfig(level=logging.INFO, filename=args.log, filemode='w',
                            format='%(asctime)s [%(levelname)s] %(message)s')
    else:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

    if args.check:
        missing = check_structure(args.base)
        if missing:
            print('Itens ausentes:')
            for item in missing:
                print('-', item)
        else:
            print('Estrutura completa.')
        return

    create_structure(args.base, args.force)
    logging.info('Estrutura criada em %s', args.base.resolve())


if __name__ == '__main__':
    main()
