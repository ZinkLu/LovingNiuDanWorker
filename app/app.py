import sys

from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget

from .widgets.config_widget import ConfigView
from .widgets.log_widget import LogWindow


class Start(QPushButton):

    def __init__(self, *args, **kwargs):
        super(Start, self).__init__("开始", *args, **kwargs)
        self.log_window = LogWindow()
        self.clicked.connect(self.show_log_view)

    def show_log_view(self):
        self.log_window.show()


class Config(QPushButton):

    def __init__(self, *args, **kwargs):
        super(Config, self).__init__("配置", *args, **kwargs)
        self.config_view = ConfigView()
        self.clicked.connect(lambda: self.config_view.show())


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("自动打印服务")
        layout = QVBoxLayout()
        layout.addWidget(Start())
        layout.addWidget(Config())
        self.resize(400, 400)
        self.setLayout(layout)


class App(QApplication):
    ...


app = App(sys.argv)
window = Window()


def run():
    app.setStyle('Fusion')
    window.show()
    sys.exit(app.exec())
