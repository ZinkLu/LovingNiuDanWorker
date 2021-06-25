from pathlib import Path
from typing import Optional

from configs.config import Config
from PyQt5 import QtGui
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QHBoxLayout, QPlainTextEdit, QPushButton, QWidget
from utils.logger import logger
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from workers.providers.redis_provider import RedisProvider
from workers.worker import Worker


class QueueThread(QThread):
    worker = None
    inited = False

    def run(self):
        self.worker = Worker.from_config(
            RedisProvider,
            Config.get_config("host"),
            Config.get_config("port"),
            Config.get_config("password"),
            Config.get_config("db"),
        )
        self.worker.start(Config.get_config("channel"))
        return super().run()

    def stop(self):
        if self.worker is not None:
            self.worker.stop()
        if self.isRunning():
            self.terminate()
            self.quit()
            self.wait()


class MyFileEvent(FileSystemEventHandler):

    def __init__(self, logger_view: "Logger") -> None:
        super().__init__()
        self.logger_view = logger_view

    def on_modified(self, event):
        self.logger_view.update.emit()
        return super().on_modified(event)


class ClearScreen(QPushButton):

    def __init__(self, logger_view: "Logger", *args, **kwargs):
        self.logger_view = logger_view
        super(ClearScreen, self).__init__("清屏", *args, **kwargs)
        self.clicked.connect(self.clear)

    def clear(self) -> bool:
        self.logger_view.clear()
        logger.info("clear log")
        self.logger_view.update.emit()
        return True


class ClearLog(QPushButton):

    def __init__(self, logger_view: "Logger", *args, **kwargs):
        self.logger_view = logger_view
        super(ClearLog, self).__init__("删除日志", *args, **kwargs)
        self.clicked.connect(self.clear)

    def clear(self) -> bool:
        self.logger_view.clear_log()
        self.logger_view.setPlainText("")
        return True


class Logger(QPlainTextEdit):
    LOGDIR = Path("logs")
    LOGFILE = LOGDIR / 'log.log'
    update = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, readOnly=True, **kwargs)
        if not self.LOGFILE.exists():
            self.LOGFILE.open('w').close()

        self.file = self.LOGFILE.as_posix()
        self.fp = self.LOGFILE.open('r+')
        self.setPlainText(self.fp.read())
        self._observer()
        self.update.connect(self._update_view)

    def _observer(self):
        observer = Observer()
        observer.schedule(MyFileEvent(self), self.LOGDIR.as_posix())
        observer.start()

    def _update_view(self):
        self.appendPlainText(self.fp.read())
        self.moveCursor(QtGui.QTextCursor.End)
        self.ensureCursorVisible()

    def clear_log(self):
        """最多保证10个log文件"""
        with self.LOGFILE.open('w') as t:
            t.write('')
        self.fp.seek(0)


class LogWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super(LogWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("日志")
        layout = QHBoxLayout()
        self.resize(1080, 720)
        logger_view = Logger()
        self.logger_view = logger_view
        layout.addWidget(logger_view)
        layout.addWidget(ClearScreen(logger_view))
        layout.addWidget(ClearLog(logger_view))
        self.setLayout(layout)

        self.q_thread: Optional[QueueThread] = None

    def closeEvent(self, QCloseEvent):
        print("quit thread", self.q_thread)
        if self.q_thread is not None:
            self.q_thread.stop()
        res = super(LogWindow, self).closeEvent(QCloseEvent)
        return res

    def show(self):
        print("show!")
        if self.q_thread is None:
            self.q_thread = QueueThread()

        self.logger_view.moveCursor(QtGui.QTextCursor.End)
        self.logger_view.ensureCursorVisible()
        self.q_thread.start()
        res = super(LogWindow, self).show()
        return res
