import logging
from pathlib import Path
from threading import Event, Thread
from time import sleep
from funcoes.utils import setup_logging
from modulos.watchdog_module import start_monitor
from bot import bot_loop


def main() -> None:
    log_file = Path('src/logs/registro.log')
    setup_logging(log_file)
    stop_event = Event()
    observer = start_monitor(Path('monitora'))
    bot_thread = Thread(target=bot_loop, args=(stop_event,), daemon=True)
    bot_thread.start()
    try:
        while True:
            logging.info('Heartbeat')
            sleep(10)
    except KeyboardInterrupt:
        logging.info('Encerrando...')
    finally:
        stop_event.set()
        observer.stop()
        observer.join()
        bot_thread.join()


if __name__ == '__main__':
    main()
