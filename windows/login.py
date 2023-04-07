import sys
import base64

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtGui import QImage, QPixmap

from new_ui.login import Ui_Form
from db.execute_sql import check_account


class LoginWindows(QMainWindow, Ui_Form):
    login_success = QtCore.pyqtSignal(int)  # 跳转信号
    switch_register = QtCore.pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.loginPushButton.clicked.connect(self.login)
        self.registerPushButton.clicked.connect(self.register)

    def login(self):
        try:
            username = self.usernameLineEdit.text()
            password = self.passwordLineEdit.text()
            uid = check_account(username, password)
            if uid:
                self.login_success.emit(uid)
            else:
                self.tipsLabel.setText('账号或密码错误！')
        except Exception as e:
            print(e)

    def register(self):
        self.switch_register.emit(True)  # 显示注册页面


if __name__ == "__main__":
    # 固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)
    # 初始化
    myWin = LoginWindows()
    # 将窗口控件显示在屏幕上
    myWin.show()
    # 程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec_())
