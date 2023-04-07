import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QCoreApplication, Qt

from windows.main import MainWindows
from windows.add_for_the_address import AddInfoWindows
from windows.add_account_book import AddAccountBookWindows
from windows.change_my_info import ChangeMyInfoWindows
from windows.login import LoginWindows


class Controller:

    def __init__(self):
        self.chang_my_info = ChangeMyInfoWindows()
        self.add_account_book = None
        self.add_for_the_address = None
        self.main_windows = None
        self.login_windows = LoginWindows()

        self.login_windows.login_success.connect(self.load_windows)  # 登录成功
        self.login_windows.switch_register.connect(self.register)

    def login(self, status=False):
        if status:
            self.log_off()
        self.login_windows.show()

    def register(self):
        self.chang_my_info.register = True
        self.chang_my_info.show()

    def log_off(self):
        self.main_windows.close()
        self.add_for_the_address.close()
        self.add_account_book.close()
        self.chang_my_info.close()

    def load_windows(self, uid):
        self.login_windows.close()
        print('登录账号的ID：', uid)
        self.main_windows = MainWindows(uid)
        self.add_for_the_address = AddInfoWindows(uid)
        self.add_account_book = AddAccountBookWindows(uid)
        self.add_account_book.switch_refresh.connect(self.refresh_add_account_book_page)
        self.add_for_the_address.user_define.connect(self.save_user)
        self.chang_my_info.switch_refresh.connect(self.refresh_my_info)
        self.main_windows.switch_login.connect(self.login)
        self.index_page()

    def index_page(self):
        self.main_windows.show()
        self.main_windows.switch_add.connect(self.show_pop_info)
        self.main_windows.switch_change.connect(self.change_mail_list)

    def show_pop_info(self, typ):
        if typ == 1:
            self.add_for_the_address.show()
        elif typ == 2:
            self.add_account_book.show()
        elif typ == 3:
            self.chang_my_info.show()

    def save_user(self, data):
        """
        保存填写的通讯录
        """
        print('调用回调')
        self.main_windows.refresh()

    def change_mail_list(self, data):
        """
        修改通讯录数据
        """
        _typ = data.pop('s_type')
        if _typ == 1:
            self.add_for_the_address.close()
            self.add_for_the_address.set_data(data)
            self.add_for_the_address.show()
        elif _typ == 2:
            self.add_account_book.close()
            self.add_account_book.set_data(data)
            self.add_account_book.show()
        elif _typ == 3:
            self.chang_my_info.close()
            self.chang_my_info.set_data(data)
            self.chang_my_info.show()

    def refresh_add_account_book_page(self):
        self.main_windows.refresh_account_book()

    def refresh_my_info(self, data):
        self.main_windows.refresh_my_info()


def main():
    try:
        QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
        app = QApplication(sys.argv)
        controller = Controller()
        controller.login()
        sys.exit(app.exec_())
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
