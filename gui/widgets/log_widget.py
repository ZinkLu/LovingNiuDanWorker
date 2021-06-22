from PyQt5.QtWidgets import QTextBrowser
from PyQt5.QtCore import QUrl, pyqtSignal
from PyQt5 import QtGui
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class MyFileEvent(FileSystemEventHandler):
    def __init__(self, logger_view: "Logger") -> None:
        super().__init__()
        self.logger_view = logger_view

    def on_modified(self, event):
        self.logger_view.update.emit()
        return super().on_modified(event)


class Logger(QTextBrowser):
    update = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file = "logs\\log.log"
        self.setSource(QUrl(self.file))
        # self.worker = Worker(self)
        # self.thread = QThread()
        # self.worker.moveToThread(self.thread)

        # self.thread.started.connect(self.worker.run)
        # self.thread.start()
        self._observer()
        self.update.connect(self._update_view)

    def _observer(self):
        observer = Observer()
        observer.schedule(MyFileEvent(self), "logs")
        observer.start()

    def _update_view(self):
        self.reload()
        self.moveCursor(QtGui.QTextCursor.End)
        self.ensureCursorVisible()
