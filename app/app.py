import sys

from configs.config import Config as C
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


class Test(QPushButton):

    test_info = {
        'birth_day': 'TEST',
        'birth_place': 'TEST',
        'constellation': 'TEST',
        'contract': 'TEST',
        'education': 'TEST',
        'gender': 'TEST',
        'height': 'TEST',
        'hobbies': 'TEST',
        'marriage': 'TEST',
        'name': 'TEST',
        'profession': 'TEST',
        'requirements': 'TEST',
        'self_introduction': 'TEST',
    }

    def __init__(self, *args, **kwargs):
        super().__init__("打印测试", *args, **kwargs)
        self.clicked.connect(self.print_test)

    def print_test(self):
        from scripts.printer import print_pipline
        from scripts.render import render_docx
        out_put = render_docx(self.test_info)
        print_pipline(out_put.as_posix(), times=C.get_config("times"), sleep=C.get_config("sleep"))


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("自动打印服务")
        layout = QVBoxLayout()
        self.log_button = Start()
        self.config_button = Config()
        self.test_button = Test()
        layout.addWidget(self.log_button)
        layout.addWidget(self.config_button)
        layout.addWidget(self.test_button)
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
