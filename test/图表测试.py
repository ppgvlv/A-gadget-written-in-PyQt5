
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QFrame
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys


class Stacked(QWidget):
    def __init__(self):
        super(Stacked, self).__init__()
        self.initData()
        self.initUI()
        self.mainLayout()

    def initUI(self):
        self.setGeometry(400, 400, 800, 600)
        self.setWindowTitle(" ")

    def db_connect(self):
        import pymysql
        self.db = pymysql.connect(host='localhost',
                             user='root',
                             password='123456',
                             port=3306,
                             database='mail_list_sys')

    def initData(self):
        from pyecharts import options as opts
        from pyecharts.charts import Pie
        from pyecharts.faker import Faker

        self.db_connect()
        cursor = self.db.cursor()
        sql = "select * from account_book;"
        cursor.execute(sql)
        results = cursor.fetchall()

        c = (
            Pie(init_opts=opts.InitOpts(width="431x",
                                height="261px"))
            .add("", [list(z) for z in zip(Faker.choose(), Faker.values())])
            .set_colors(["blue", "green", "yellow", "red", "pink", "orange", "purple"])
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
            .render("pie_set_color.html")
        )

    def mainLayout(self):
        self.mainhboxLayout = QHBoxLayout(self)
        self.frame = QFrame(self)
        self.mainhboxLayout.addWidget(self.frame)
        self.hboxLayout = QHBoxLayout(self.frame)
        self.myHtml = QWebEngineView()
        # 打开本地html文件
        self.myHtml.load(QUrl("file:///pie_set_color.html"))
        self.hboxLayout.addWidget(self.myHtml)
        self.setLayout(self.mainhboxLayout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Stacked()
    ex.show()
    sys.exit(app.exec_())