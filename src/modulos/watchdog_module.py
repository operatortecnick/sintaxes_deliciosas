from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging
from pathlib import Path


class MonitorHandler(FileSystemEventHandler):
    def __init__(self, callback=None):
        self.callback = callback

    def on_any_event(self, event):
        logging.info('Evento %s em %s', event.event_type, event.src_path)
        if self.callback:
            self.callback(event)


def start_monitor(path: Path, callback=None) -> Observer:
    handler = MonitorHandler(callback)
    observer = Observer()
    observer.schedule(handler, str(path), recursive=True)
    observer.start()
    logging.info('Monitorando %s', path)
    return observer
