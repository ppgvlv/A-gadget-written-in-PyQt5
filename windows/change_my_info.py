import sys
import base64

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtGui import QImage, QPixmap

from new_ui.my_page import Ui_Mbox
from db.execute_sql import update_user_info, add_account


class ChangeMyInfoWindows(QMainWindow, Ui_Mbox):
    switch_refresh = QtCore.pyqtSignal(dict)
    data = {}

    register = False

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.okButton.clicked.connect(self.click_ok)
        self.cancelButton.clicked.connect(self.cancel)

    def set_data(self, data):
        self.data = data
        self.usernameEdit.setText(data['username'])
        self.passwordEdit.setText(data['password'])
        self.nameEdit.setText(data['name'])
        self.universityEdit.setText(data['university'])
        self.textEdit.setText(data['personal_profile'])

    def click_ok(self):
        data = {
            'username': self.usernameEdit.text(),
            'password': self.passwordEdit.text(),
            'name': self.nameEdit.text(),
            'university': self.universityEdit.text(),
            'personal_profile': self.textEdit.toPlainText()
        }

        for k, v in data.items():
            if not v:
                self.msg.setText('数据不完整，请填写完整')
                return

        if not self.register:
            data['id'] = self.data['id']
            update_user_info(data)
            self.switch_refresh.emit(data)
        else:
            add_account(data)

        self.cancel()

    def cancel(self):
        self.usernameEdit.clear()
        self.passwordEdit.clear()
        self.nameEdit.clear()
        self.universityEdit.clear()
        self.textEdit.clear()
        self.register = False
        self.close()
