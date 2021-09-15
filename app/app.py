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
        self.log_button = Start()
        self.config_button = Config()
        layout.addWidget(self.log_button)
        layout.addWidget(self.config_button)
        self.resize(400, 400)
        self.setLayout(layout)

    def closeEvent(self, a0) -> None:
        self.log_button.log_window.close()
        self.config_button.config_view.close()
        return super().closeEvent(a0)


class App(QApplication):
    ...


app = App(sys.argv)
window = Window()


def run():
    app.setStyle('Fusion')
    window.show()
    sys.exit(app.exec())
