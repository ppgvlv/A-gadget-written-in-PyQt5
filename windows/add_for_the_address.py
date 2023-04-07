import sys
import base64

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtGui import QImage, QPixmap

from new_ui.add_for_the_address import Ui_Xbox

from db.execute_sql import save_mail_list_data, update_mail_list

class AddInfoWindows(QMainWindow, Ui_Xbox):
    user_define = QtCore.pyqtSignal(dict)  # 跳转信号
    current_upload_image = ''

    change_data = False
    change_id = None

    def __init__(self, uid, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.uid = uid
        self.phototPushButton.clicked.connect(self.openfile)
        self.okButton.clicked.connect(self.save_data)
        self.cancelButton.clicked.connect(self.cancel)

    def set_data(self, data):
        self.SnameEdit.setText(data['name'])
        self.LnoEdit.setText(data['phone'])
        self.SnoEdit.setText(data['qq'])
        self.MIDEdit.setText(data['address'])
        self.MnameEdit.setText(data['relation'])
        pic = base64.b64decode(data['photo'])
        picture = QImage.fromData(pic)
        pixmap = QPixmap.fromImage(picture)
        self.photoLabel.setPixmap(pixmap)
        self.photoLabel.setScaledContents(True)  # 让图片自适应label大小

        if data['sex'] == '男':
            self.nanButton.setChecked(True)
        else:
            self.nvButton.setChecked(True)
        self.change_data = True
        self.change_id = data['id']
        self.current_upload_image = data['photo']

    def openfile(self):
        openfile_name = QFileDialog.getOpenFileName(self, '选择文件', '', 'Image files(*.png , *.jpg)')
        if not openfile_name[0]:
            return
        with open(openfile_name[0], 'rb') as f:
            pic = f.read()
            self.current_upload_image = base64.b64encode(pic)  # 图片转base64存在MySQL中
        picture = QImage.fromData(pic)
        pixmap = QPixmap.fromImage(picture)
        self.photoLabel.setPixmap(pixmap)
        self.photoLabel.setScaledContents(True)  # 让图片自适应label大小

    def save_data(self):

        sex = '女' if self.nvButton.isChecked() is True else '男'
        data = {'name': self.SnameEdit.text(), 'sex': sex,
                'phone': self.LnoEdit.text(), 'qq': self.SnoEdit.text(),
                'address': self.MIDEdit.text(), 'relation': self.MnameEdit.text(),
                'photo': self.current_upload_image}
        for k, v in data.items():
            if not v:
                print(k)
                self.msg.setText('数据不完整，请检查再提交')
                return
        if self.change_data is True:
            data['id'] = self.change_id
            update_mail_list(data)
        else:
            data['uid'] = self.uid
            save_mail_list_data(data)

        self.user_define.emit(data)

        self.change_data = False
        self.change_id = None
        self.close()

        self.SnameEdit.setText('')
        self.LnoEdit.setText('')
        self.SnoEdit.setText('')
        self.MIDEdit.setText('')
        self.MnameEdit.setText('')
        self.current_upload_image = None
        self.photoLabel.clear()

    def closeEvent(self, event):
        self.change_data = False
        self.change_id = None
        self.SnameEdit.setText('')
        self.LnoEdit.setText('')
        self.SnoEdit.setText('')
        self.MIDEdit.setText('')
        self.MnameEdit.setText('')
        self.current_upload_image = None
        self.photoLabel.clear()
        super(AddInfoWindows, self).closeEvent(event)

    def cancel(self):
        self.close()


if __name__ == "__main__":
    # 固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)
    # 初始化
    myWin = AddInfoWindows()
    # 将窗口控件显示在屏幕上
    myWin.show()
    # 程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec_())
