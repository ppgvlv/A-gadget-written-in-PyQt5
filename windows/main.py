import sys
import json

import base64

from datetime import datetime
from datetime import timedelta

from PyQt5 import QtCore
# PyQt5中使用的基本控件都在PyQt5.QtWidgets模块中
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidgetItem, QHBoxLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWebEngineWidgets import *

from pyecharts.charts import Pie, Bar
from pyecharts import options as opts

from new_ui._mainUI import Ui_MainWindow
from db.execute_sql import get_all_mail_list, delete_mail, get_all_account_book, delete_account_book, get_my_info


class MainWindows(QMainWindow, Ui_MainWindow):
    switch_add = QtCore.pyqtSignal(int)  # 跳转信号
    switch_change = QtCore.pyqtSignal(dict)  # 跳转信号
    switch_login = QtCore.pyqtSignal(bool)

    all_mail_list = {}
    current_choice_mail = {}

    all_account_book = {}
    current_choice_account_book = {}

    current_user_info = {}

    def __init__(self, uid, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.browser = QWebEngineView()
        self.browser2 = QWebEngineView()

        self.Table.tabBarClicked.connect(self.change_tab_index)

        self.uid = uid
        self.set_default()
        self.groupBox_2.setHidden(True)
        self.actionEdit_1.clicked.connect(self.pop_info)
        self.studentTable.itemSelectionChanged.connect(self.on_select_mail)
        self.ShusheTable.itemSelectionChanged.connect(self.on_select_account_book)
        self.DeleteButton_1.clicked.connect(self.delete_mail)
        self.editButton_1.clicked.connect(self.show_change_pop)
        self.addEdit_2.clicked.connect(self.show_add_account_book)
        self.changeEditButton_2.clicked.connect(self.show_change_pop_2)
        self.deleteButton_2.clicked.connect(self.delete_account_mail)
        self.editButton_3.clicked.connect(self.show_change_my_info)
        self.DeleteButton_3.clicked.connect(self.log_off)
        self.searchPushButton.clicked.connect(self.search_account_book)
        self.ShusheTable.activated.connect(self.show_change_pop_2)
        self.studentTable.activated.connect(self.show_change_pop)

        self.inPushButton.clicked.connect(self.show_income)
        self.outPushButton.clicked.connect(self.show_pay)

        self.refresh()
        # self.refresh_account_book()
        self.refresh_my_info()

    def change_tab_index(self, index):
        print("Tab changed to:", index)
        if index == 1:
            self.refresh_account_book()

    def set_default(self):
        """
        设置默认值
        """
        self.SID.setText('')
        self.Sname.setText('')
        self.Ssex.setText('')
        self.Lno.setText('')
        self.Sno.setText('')
        self.MID.setText('')

        pic = base64.b64decode(
            """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""")

        picture = QImage.fromData(pic)
        pixmap = QPixmap.fromImage(picture)
        self.label.setPixmap(pixmap)
        self.label.setScaledContents(True)  # 让图片自适应label大小
        self.editButton_1.setEnabled(False)
        self.DeleteButton_1.setEnabled(False)
        self.changeEditButton_2.setEnabled(False)
        self.deleteButton_2.setEnabled(False)
        _now = datetime.now()
        _start = _now - timedelta(days=30)
        self.startDateEdit.setDate(QtCore.QDate(_start.year, _start.month, _start.day))
        self.endDateEdit.setDate(QtCore.QDate(_now.year, _now.month, _now.day))

    def refresh(self):
        """
        刷新这个表格数据
        """
        self.all_mail_list = {}
        self.studentTable.clear()
        datas = get_all_mail_list(self.uid)
        print('刷新通讯录')
        for row, data in enumerate(datas):
            new_item = QTreeWidgetItem([data[key] if key != 'photo' else data[key][:100] for key in
                                        ('name', 'sex', 'phone', 'qq', 'address', 'relation', 'photo')])
            self.all_mail_list[json.dumps(data)] = new_item
            self.studentTable.addTopLevelItem(new_item)

    def show_income(self):
        self.refresh_account_book(a_type='收入')

    def show_pay(self):
        self.refresh_account_book(a_type='支出')

    def refresh_account_book(self, start=None, end=None, a_type='收入'):
        self.browser.setHtml('')
        self.browser2.setHtml('')
        if not start:
            start = self.startDateEdit.date().getDate()
            end = self.endDateEdit.date().getDate()
            start = datetime.strptime(f'{start[0]}-{start[1]}-{start[2]}', '%Y-%m-%d')
            end = datetime.strptime(f'{end[0]}-{end[1]}-{end[2]}', '%Y-%m-%d')
            end = end.replace(hour=23, minute=59, second=59)
            start = start.strftime('%Y-%m-%d %H:%M:%S')
            end = end.strftime('%Y-%m-%d %H:%M:%S')

        self.all_account_book = {}
        self.ShusheTable.clear()
        datas = get_all_account_book(self.uid, start=start, end=end, a_type=a_type)
        for row, data in enumerate(datas):
            data['record_time'] = str(data['record_time'])
            data['money'] = str(data['money'])
            new_item = QTreeWidgetItem([data[key] for key in ('a_type', 'record_time', 'type', 'money', 'mark')])
            self.all_account_book[json.dumps(data)] = new_item
            self.ShusheTable.addTopLevelItem(new_item)
        print(datas)

        self.show_pie_images(datas)
        self.show_histogram_images(datas)

    def show_pie_images(self, data):
        if not data:
            return

        echarts_data = {}
        for row in data:
            if row['type'] not in echarts_data:
                echarts_data[row['type']] = float(row['money'])
            else:
                echarts_data[row['type']] += float(row['money'])

        c = (
            Pie(init_opts=opts.InitOpts(width="431x",
                                        height="261px"))
            .add("", [[k, v] for k, v in echarts_data.items()])
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        )
        html_path = c.render()
        with open(html_path, 'r', encoding='utf-8') as f:
            _html = f.read()
        # 显示HTML
        self.browser.setHtml(_html)
        hboxLayout = QHBoxLayout(self.leftFrame)
        hboxLayout.addWidget(self.browser)
        self.setLayout(hboxLayout)

    def show_histogram_images(self, data):
        if not data:
            return
        echarts_data = {}
        for row in data:
            if row['record_time'] not in echarts_data:
                echarts_data[row['record_time']] = float(row['money'])
            else:
                echarts_data[row['record_time']] += float(row['money'])
        echarts_data = {row[0]: row[1] for row in sorted(echarts_data.items(), key=lambda x:x[0])}
        bar = (
            Bar(init_opts=opts.InitOpts(width="800x",
                                        height="261px"))
            .add_xaxis(list(echarts_data.keys()))
            .add_yaxis("", list(echarts_data.values()))
            # .set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本示例", subtitle="我是副标题"))
        )

        html_path = bar.render('render_2.html')
        with open(html_path, 'r', encoding='utf-8') as f:
            _html = f.read()
        # 显示HTML
        self.browser2.setHtml(_html)
        hboxLayout = QHBoxLayout(self.bottomFrame)
        hboxLayout.addWidget(self.browser2)
        self.setLayout(hboxLayout)

    def refresh_my_info(self):
        datas = get_my_info(self.uid)[0]
        self.username.setText(datas['username'])
        self.password.setText(datas['password'])
        self.sex.setText(datas['name'])
        self.school.setText(datas['university'])
        self.personalProfile.setText(datas['personal_profile'])
        self.current_user_info = datas

    def pop_info(self):
        self.switch_add.emit(1)

    def on_select_mail(self):
        item = self.studentTable.selectedItems()
        print(item)
        if not item:
            return
        selected = True if item else False
        selection = None
        if selected:
            for k, v in self.all_mail_list.items():
                if v == item[0]:
                    selection = k
                    break
            else:
                selected = False
        self.editButton_1.setEnabled(selected)
        self.DeleteButton_1.setEnabled(selected)
        self.set_rigth_data(selection)

    def on_select_account_book(self):
        item = self.ShusheTable.selectedItems()
        print(item)
        if not item:
            return
        selected = True if item else False
        selection = None
        if selected:
            for k, v in self.all_account_book.items():
                if v == item[0]:
                    selection = k
                    break
            else:
                selected = False
        self.changeEditButton_2.setEnabled(selected)
        self.deleteButton_2.setEnabled(selected)
        self.set_rigth_data(selection, 2)

    def set_rigth_data(self, data: str, typ=1):
        data = json.loads(data)
        if typ == 1:
            self.current_choice_mail = data
            self.SID.setText(data['name'])
            self.Sname.setText(data['sex'])
            self.Ssex.setText(data['phone'])
            self.Lno.setText(data['qq'])
            self.Sno.setText(data['address'])
            self.MID.setText(data['relation'])

            pic = base64.b64decode(data['photo'])

            picture = QImage.fromData(pic)
            pixmap = QPixmap.fromImage(picture)
            self.label.setPixmap(pixmap)
            self.label.setScaledContents(True)  # 让图片自适应label大小
        elif typ == 2:
            self.current_choice_account_book = data
            self.messageLabel_4.setText(data['a_type'])
            self.rightTimeLabel.setText(data['record_time'])
            self.rightTypeLabel.setText(data['type'])
            self.rightMoneyLabel.setText(data['money'])
            self.rightMarkLabel.setText(data['mark'])

    def delete_mail(self):
        try:
            delete_mail(self.current_choice_mail['id'])
            self.set_default()
            self.refresh()
        except Exception as e:
            print(e)

    def delete_account_mail(self):
        try:
            delete_account_book(self.current_choice_account_book['id'])
            self.set_default()
            self.refresh_account_book()
        except Exception as e:
            print(e)

    def show_change_pop(self):
        self.switch_change.emit({**{'s_type': 1}, **self.current_choice_mail})

    def show_change_pop_2(self):
        self.switch_change.emit({**{'s_type': 2}, **self.current_choice_account_book})

    def show_add_account_book(self):
        self.switch_add.emit(2)

    def show_change_my_info(self):
        self.switch_change.emit({**{'s_type': 3}, **self.current_user_info})

    def log_off(self):
        self.close()
        self.switch_login.emit(True)

    def search_account_book(self):
        _start = self.startDateEdit.date().getDate()
        _end = self.endDateEdit.date().getDate()

        _start = datetime.strptime(f'{_start[0]}-{_start[1]}-{_start[2]}', '%Y-%m-%d')
        _end = datetime.strptime(f'{_end[0]}-{_end[1]}-{_end[2]}', '%Y-%m-%d')
        _end = _end.replace(hour=23, minute=59, second=59)
        if _start > _end:
            self.errMsglabel.setText('开始时间不能大于结束时间')
            return

        self.refresh_account_book(_start.strftime('%Y-%m-%d %H:%M:%S'), _end.strftime('%Y-%m-%d %H:%M:%S'))


if __name__ == "__main__":
    # 固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)
    # 初始化
    myWin = MainWindows(1)
    # 将窗口控件显示在屏幕上
    myWin.show()
    # 程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec_())
