import time
from pathlib import Path
from typing import Optional

from configs.config import Config
from PyQt5 import QtGui
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QHBoxLayout, QPlainTextEdit, QPushButton, QWidget
from utils.logger import logger
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
        print('正在关闭worker线程')
        if self.isRunning():
            print('正在 terminate worker线程')
            self.terminate()
            print('terminate worker线程结束')
            print('正在 quit worker线程')
            # self.quit()
            print('quit worker线程结束')
            # self.wait(5)
        print('worker线程关闭完毕')


class ClearScreen(QPushButton):

    def __init__(self, logger_view: "Logger", *args, **kwargs):
        self.logger_view = logger_view
        super(ClearScreen, self).__init__("清屏", *args, **kwargs)
        self.clicked.connect(self.clear)

    def clear(self) -> bool:
        self.logger_view.clear()
        logger.info("clear log")
        self.logger_view.update_file_signal.emit()
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


class WatchFile(QueueThread):

    def __init__(self, lg: "Logger"):
        self.lg = lg
        super(WatchFile, self).__init__()

    def run(self):
        with open(self.lg.LOGFILE, encoding='utf8') as self.lg.watch_fp:
            while True:
                if self.lg.watch_fp.read():
                    self.lg.update_file_signal.emit()
                else:
                    time.sleep(0.1)


class Logger(QPlainTextEdit):
    LOGDIR = Path("logs")
    LOGFILE = LOGDIR / 'log.log'
    update_file_signal = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, readOnly=True, **kwargs)
        if not self.LOGFILE.exists():
            self.LOGFILE.open('w', encoding='utf8').close()

        self.file = self.LOGFILE.as_posix()
        self.fp = self.LOGFILE.open('r+', encoding='utf8')
        self.watch_fp = self.LOGFILE.open('r', encoding='utf8')
        self.setPlainText(self.fp.read())
        self.update_file_signal.connect(self._update_view)

    def _update_view(self):
        self.appendPlainText(self.fp.read())
        self.moveCursor(QtGui.QTextCursor.End)
        self.ensureCursorVisible()

    def clear_log(self):
        """最多保证10个log文件"""
        with self.LOGFILE.open('w') as t:
            t.write('')
        self.fp.seek(0)
        self.watch_fp.seek(0)


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

        self.q_thread: Optional[QueueThread] = QueueThread()
        self.watch_thread = WatchFile(logger_view)

    def closeEvent(self, QCloseEvent):
        print("quit thread", self.q_thread)
        if self.q_thread is not None:
            self.q_thread.stop()
        self.watch_thread.terminate()
        res = super(LogWindow, self).closeEvent(QCloseEvent)
        return res

    def show(self):
        print("show!")
        if self.q_thread is None:
            self.q_thread = QueueThread()

        self.watch_thread.start()
        self.logger_view.moveCursor(QtGui.QTextCursor.End)
        self.logger_view.ensureCursorVisible()
        self.q_thread.start()
        res = super(LogWindow, self).show()
        return res
