import sys

from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QBoxLayout,
    QPushButton,
    QWidget,
)

from widgets.log_widget import Logger


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("print worker")
        # Create a QHBoxLayout instance
        layout = QHBoxLayout()
        self.resize(1080, 720)
        # Add widgets to the layout
        layout.addWidget(Logger())
        # layout.addWidget(QPushButton("Center"), 1)
        # layout.addWidget(QPushButton("Right-Most"), 2)
        # Set the layout on the application's window
        self.setLayout(layout)
        print(self.children())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = Window()
    window.show()
    sys.exit(app.exec_())
