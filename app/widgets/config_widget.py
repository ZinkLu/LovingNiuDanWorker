from configs.config import Config
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QListView, QPushButton, QTextEdit, QVBoxLayout, QWidget, QSizePolicy


class ConfigView(QWidget):

    def __init__(self, *args, **kwargs):
        super(ConfigView, self).__init__(*args, **kwargs)
        layout = QVBoxLayout(self)
        self.config_view = ConfigListView()
        layout.addWidget(self.config_view)
        # self.setLayout(layout)
        layout.addWidget(SaveButton(self.config_view))

    def sizeHint(self):
        return QSize(960, 720)


class SaveButton(QPushButton):

    def __init__(self, config_list: "ConfigListView", *args, **kwargs):
        self.config_list = config_list
        super(SaveButton, self).__init__("保存", *args, **kwargs)
        self.clicked.connect(self.save)

    def save(self):
        self.config_list.save_current_config()
        self.parent().close()


class ConfigListView(QListView):

    def __init__(self, *args, **kwargs):
        super(ConfigListView, self).__init__(*args, **kwargs)
        # self.setModel()
        self._model = QStandardItemModel(self)
        self.setModel(self._model)

        for config_key, config_value in Config.iter_config():
            item = QStandardItem()
            self._model.appendRow(item)  # 添加item

            # 得到索引
            index = self._model.indexFromItem(item)
            widget = ConfigItem(config_key, config_value)
            item.setSizeHint(widget.sizeHint())  # 主要是调整item的高度
            # 设置自定义的widget
            self.setIndexWidget(index, widget)
        # self.save_current_config()

    def save_current_config(self):
        for row in range(self._model.rowCount()):
            index = self._model.index(row, 0)
            self.indexWidget(index).save_config()


class ConfigItem(QWidget):

    def __init__(self, config_key, value_obj, *args, **kwargs):
        super(ConfigItem, self).__init__(*args, **kwargs)
        self.config_key = config_key
        self.value_obj = value_obj
        self.value_type = type(value_obj['value'])
        self._add_config_info()

    def _add_config_info(self):
        """
        |config_key|config_desc|config_value|
        |---|---|---|
        """
        layout = QHBoxLayout(self)

        self.key_item = QLabel(self.config_key)
        layout.addWidget(self.key_item)
        self.key_item.setFixedWidth(100)

        self.desc_item = QLabel(self.value_obj['desc'])
        self.desc_item.setFixedWidth(300)
        layout.addWidget(self.desc_item)

        self.value_item = QTextEdit(str(self.value_obj['value']))
        layout.addWidget(self.value_item)

    def save_config(self):
        Config.set_config(self.config_key, self.value_type(self.value_item.toPlainText()))

    def sizeHint(self):
        return QSize(100, 50)
