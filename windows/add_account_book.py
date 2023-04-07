import sys
import base64

from datetime import datetime

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtGui import QImage, QPixmap

from new_ui.add_account_book import Ui_Sbox
from db.execute_sql import save_account_book, update_account_book


class AddAccountBookWindows(QMainWindow, Ui_Sbox):
    switch_refresh = QtCore.pyqtSignal(bool)
    in_types = ('工资', '兼职', '理财', '礼金', '其他')
    out_types = ('餐饮', '购物', '交通', '零食', '运动', '娱乐', '通讯', '服饰', '美容', '住房')

    change_data = False
    change_id = None

    def __init__(self, uid, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.uid = uid
        self.comboBox.currentIndexChanged.connect(self.change_type)
        self.current_type = self.comboBox.currentText()
        self.change_type(1)
        self.okButton.clicked.connect(self.save_data)
        self.cancelButton.clicked.connect(self.cancel)
        _start = datetime.now()
        self.dateEdit.setDate(QtCore.QDate(_start.year, _start.month, _start.day))

    def set_data(self, data):
        try:
            self.comboBox.setCurrentText(data['a_type'])
            self.dateEdit.setDate(QtCore.QDate(*[int(_) for _ in data['record_time'].split('-')]))
            self.comboBox_2.setCurrentText(data['type'])
            self.moneyDoubleSpinBox.setValue(float(data['money']))
            self.markTextEdit.setText(data['mark'])
            self.change_data = True
            self.change_id = data['id']
        except Exception as e:
            print(e)

    def change_type(self, index):
        self.current_type = self.comboBox.currentText()
        self.comboBox_2.clear()
        if self.current_type == '收入':
            types = self.in_types
        else:
            types = self.out_types
        for typ in types:
            self.comboBox_2.addItem(typ)

    def save_data(self):

        record_time = self.dateEdit.date().getDate()
        record_time = f'{record_time[0]}-{record_time[1]}-{record_time[2]}'
        data = {
            'a_type': self.comboBox.currentText(),
            'record_time': record_time,
            'type': self.comboBox_2.currentText(),
            'money': self.moneyDoubleSpinBox.value(),
            'mark': self.markTextEdit.toPlainText()
        }

        if self.change_data is True:
            data['id'] = self.change_id
            update_account_book(data)
        else:
            data['uid'] = self.uid
            save_account_book(data)
        self.switch_refresh.emit(True)

        self.change_data = False
        self.change_id = None
        self.close()

        self.markTextEdit.setText('')
        self.moneyDoubleSpinBox.setValue(0)

    def cancel(self):
        self.close()

    def closeEvent(self, event):
        print('点击关闭')
        self.comboBox.setCurrentText('收入')
        # self.dateEdit.setDate(QtCore.QDate(*[int(_) for _ in data['record_time'].split('-')]))
        self.comboBox_2.setCurrentText('工资')
        self.moneyDoubleSpinBox.clear()
        self.markTextEdit.clear()
        self.change_data = False
        self.change_id = None
        super(AddAccountBookWindows, self).close()


if __name__ == "__main__":
    # 固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)
    # 初始化
    myWin = AddAccountBookWindows()
    # 将窗口控件显示在屏幕上
    myWin.show()
    # 程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec_())
