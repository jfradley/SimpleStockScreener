import os
import sys
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QTableWidget,\
    QTableWidgetItem, QDateEdit, QLabel, QListWidget, QCheckBox, QTabWidget, \
    QMessageBox, QWidget, QFileDialog, QHBoxLayout
from PyQt5.QtCore import QDateTime, Qt
import pandas as pd
from DataExtraction import stock_check, PriceAnalysis, VolumeAnalysis,\
    DailyPriceAnalysis, errorRemove, PriceAnalysis1

# ----------------------------------------------------------------------------
stylesheet = ("background-color:rgb(134,194,50);"
              "color:rgb(255,255,255);"
              "border-radius:100;"
              "border-right:5px solid rgb(97,137,47);"
              "border-top:5px solid rgb(97,137,47);"
              "border-bottom:5px solid rgb(97,137,47);"
              "border-left:5px solid rgb(97,137,47);")

stylesheet1 = ("background-color:rgb(134,194,50);"
               "color:rgb(0,0,0);"
               "border-radius:26;"
               "border-right:2.5px solid rgb(97,137,47);"
               "border-top:2.5px solid rgb(97,137,47);"
               "border-bottom:2.5px solid rgb(97,137,47);"
               "border-left:2.5px solid rgb(97,137,47);")


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setGeometry(50, 50, 800, 700)  # x, y, w, h
        self.setWindowTitle("Simplified Stock Checker")
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QIcon(scriptDir + os.path.sep + 'Drawing1.png'))
        self.setStyleSheet("background-color: rgb(71,75,79)")

        size = [200, 200]
        # --------------------------------------------------------------------
        #  Push buttons

        b3 = QPushButton('World \n Markets', self)
        b3.setFont(QFont("Open Sans Bold", 14))
        b3.move(300, 50)
        b3.resize(size[0], size[1])
        b3.setStyleSheet(stylesheet)
        b3.clicked.connect(self.page2)

        b1 = QPushButton('UK \n Market Sectors ', self)
        b1.setFont(QFont("Open Sans Bold", 14))
        b1.move(300, 200)
        b1.resize(size[0], size[1])
        b1.setStyleSheet(stylesheet)
        b1.clicked.connect(self.page3)

        b2 = QPushButton('UK Individual \nSector Components', self)
        b2.setFont(QFont("Open Sans Bold", 14))
        b2.move(300, 350)
        b2.resize(size[0], size[1])
        b2.setStyleSheet(stylesheet)
        b2.clicked.connect(self.page4)

        #b4 = QPushButton('Edit Sectors', self)
        #b4.setFont(QFont("Times", 14))
        #b4.move(300, 500)
        #b4.resize(size[0], size[1])
        #b4.setStyleSheet(stylesheet)
        #b2.clicked.connect(self.down)

    def page2(self):
        self.SW2 = SecondWindow()
        self.SW2.show()
        self.hide()

    def page3(self):
        self.SW3 = ThirdWindow()
        self.SW3.show()
        self.hide()

    def page4(self):
        self.SW4 = FourthWindow()
        self.SW4.show()
        self.hide()


class SecondWindow(QMainWindow):
    def __init__(self, parent=None):
        super(SecondWindow, self).__init__(parent)

        self.setGeometry(20, 30, 800, 680)  # x, y, w, h
        self.setWindowTitle("Edit")
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        #self.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + 'Drawing1.png'))
        self.setStyleSheet("background-color: rgb(71,75,79)")

        label1 = QLabel('World Market Sectors', self)
        label1.setFont(QFont("Open Sans Bold", 12))
        label1.setStyleSheet("color:rgb(255,255,255);")
        label1.resize(285, 30)
        label1.move(20, 5)

        b1 = QPushButton('Home', self)
        b1.setFont(QFont("Open Sans Bold", 12))
        b1.setStyleSheet(stylesheet1)
        b1.move(720, 620)
        b1.resize(55, 55)
        b1.setToolTip('Back to home page')
        b1.clicked.connect(self.home)

        b2 = QPushButton('Run Analysis...', self)
        b2.setFont(QFont("Open Sans Bold", 12))
        b2.setStyleSheet("background-color:rgb(134,194,50);"
                             "color:rgb(0,0,0);")
        b2.move(140, 330)
        b2.resize(160, 25)
        b2.clicked.connect(self.stock)

        self.datepicker = dateWidget(parent=self)
        self.datepicker.show()
        self.datepicker.d1.dateChanged.connect(self.datepicker.date_change)
        self.datepicker.d2.dateChanged.connect(self.datepicker.date_change)

        # --------------------------------------------------------------------
        # Tab widget
        self.tab1 = MyTabWidget(self)
        self.tabwidget = QTabWidget(self)
        self.tabwidget.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.tabwidget.setGeometry(340, 50, 360, 600)  # x,y,w,h
        self.tabwidget.addTab(self.tab1, 'Price change')
        self.tabwidget.show()

        self.tab1.tw.itemSelectionChanged.connect(lambda: self.tab1.col_select())

        # --------------------------------------------------------------------

        # --------------------------------------------------------------------
        # Sector loader

        self.file_name = None
        parent_fldr = (os.path.dirname(os.getcwd()))
        self.file_name = parent_fldr + "/Data/SectorsExample.xlsx"

        with pd.ExcelFile(self.file_name) as file:
            self.sheet_names = file.sheet_names

            #for i, sheet in enumerate(self.sheet_names):
                #if sheet[:6] == 'sector':
                    #self.lw.insertItem(i, sheet[6:])

    def stock(self):
        df_list = []
        #tick_list = []

        df = pd.read_excel(self.file_name, sheet_name='World', usecols="A:E")
        tick_list = list(df['Code'])
        print('h')
        print(df)
        area_list = list(df['Area'])
        print('a')

        start = self.datepicker.start
        end = self.datepicker.end

        for tick in tick_list:
            result_df = stock_check(tick, start, end)
            df_list.append(result_df)

        self.price_df = PriceAnalysis1(df_list, tick_list, area_list)
        self.tab1.table_set(self.price_df)


    def home(self):

        self.SW = MainWindow()
        self.SW.show()
        self.close()









# ----------------------------------------------------------------------------
# For UK sectors


class ThirdWindow(QMainWindow):
    def __init__(self, parent=None):

        super(ThirdWindow, self).__init__(parent)

        self.setGeometry(50, 50, 800, 700)  # x, y, w, h
        self.setWindowTitle("Edit")
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QIcon(scriptDir + os.path.sep + 'Drawing1.png'))
        self.setStyleSheet("background-color: rgb(71,75,79)")

        label1 = QLabel('UK Market Sectors', self)
        label1.setFont(QFont("Open Sans Bold",12))
        label1.setStyleSheet("color:rgb(255,255,255);")
        label1.resize(285, 30)
        label1.move(20, 5)

        b1 = QPushButton('Home', self)
        b1.setFont(QFont("Open Sans Bold", 12))
        b1.setStyleSheet(stylesheet1)
        b1.move(720, 620)
        b1.resize(55, 55)
        b1.setToolTip('Back to home page')
        b1.clicked.connect(self.home)

        self.datepicker = dateWidget(parent=self)
        self.datepicker.show()
        self.datepicker.d1.dateChanged.connect(self.datepicker.date_change)
        self.datepicker.d2.dateChanged.connect(self.datepicker.date_change)

    def home(self):
        self.SW = MainWindow()
        self.SW.show()
        self.close()

# ----------------------------------------------------------------------------
# For Individual sector overview


class FourthWindow(QMainWindow):
    def __init__(self, parent=None):
        super(FourthWindow, self).__init__(parent)

        self.setGeometry(20, 30, 800, 680)  # x, y, w, h
        self.setWindowTitle("Edit")
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        #self.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + 'Drawing1.png'))
        self.setStyleSheet("background-color: rgb(71,75,79)")

        self.sheet_names = None

        label1 = QLabel('UK Individual Sector Components', self)
        label1.setFont(QFont("Open Sans Bold",12))
        label1.setStyleSheet("color:rgb(255,255,255);")
        label1.resize(285, 30)
        label1.move(20, 5)

        b1 = QPushButton('Home', self)
        b1.setFont(QFont("Open Sans Bold", 12))
        b1.setStyleSheet(stylesheet1)
        b1.move(720, 620)
        b1.resize(55, 55)
        b1.setToolTip('Back to home page')
        b1.clicked.connect(self.home)

        b2 = QPushButton('Run Analysis...', self)
        b2.setFont(QFont("Open Sans Bold", 12))
        b2.setStyleSheet("background-color:rgb(134,194,50);"
                             "color:rgb(0,0,0);")
        b2.move(140, 330)
        b2.resize(160, 25)
        b2.clicked.connect(self.stock)

        #b3 = QPushButton('select file', self)
        #b3.move(50, 700)
        #b3.resize(70, 25)
        #b3.clicked.connect(self.file_select)

        b4 = QPushButton('Sort Asc.', self)
        b4.setStyleSheet("background-color:rgb(134,194,50);"
                             "color:rgb(0,0,0);")
        b4.move(710, 350)
        b4.resize(70, 25)
        b4.clicked.connect(self.sort_ascending)

        b4 = QPushButton('Sort Desc.', self)
        b4.setStyleSheet("background-color:rgb(134,194,50);"
                             "color:rgb(0,0,0);")
        b4.move(710, 380)
        b4.resize(70, 25)
        b4.clicked.connect(self.sort_descending)

        b_save = QPushButton('Save table', self)
        b_save.setStyleSheet("background-color:rgb(134,194,50);"
                             "color:rgb(0,0,0);")
        b_save.move(710, 410)
        b_save.resize(70, 25)
        b_save.clicked.connect(self.save_table)

        self.cb1 = QCheckBox('Main', self)
        self.cb1.setFont(QFont("Open Sans Bold", 12))
        self.cb1.setStyleSheet("background-color:rgb(134,194,50);"
                               "color: rgb(255,255,255);")
        self.cb1.move(20,130)

        self.cb2 = QCheckBox('Aim', self)
        self.cb2.setFont(QFont("Open Sans Bold", 12))
        self.cb2.move(20, 160)
        self.cb2.setStyleSheet("background-color:rgb(134,194,50);"
                               "color: rgb(255,255,255);")
        # --------------------------------------------------------------------
        # List widget
        label_lw = QLabel('Sectors', self)
        label_lw.setAlignment(Qt.AlignCenter)
        label_lw.setFont(QFont("Open Sans Bold",12))
        label_lw.setStyleSheet("background-color:rgb(134,194,50);"
                               "color: rgb(255,255,255);")
        label_lw.resize(160, 20)
        label_lw.move(140, 130)

        self.lw = QListWidget(self)
        self.lw.setFont(QFont("Open Sans Bold", 12))
        self.lw.setStyleSheet("background-color:rgb(255,255,255);")
        self.lw.resize(160, 150)
        self.lw.move(140, 150)
        value = self.lw.currentRow()
        self.lw.itemSelectionChanged.connect(self.list_select_change)

        self.label_lw2 = QLabel("Selected = Empty", self)
        self.label_lw2.setFont(QFont("Open Sans Bold",12))
        self.label_lw2.setStyleSheet("background-color:rgb(134,194,50);"
                                     "color:rgb(255,255,255);")
        self.label_lw2.resize(160, 25)
        self.label_lw2.move(140, 300)

        # --------------------------------------------------------------------
        # Sector loader

        self.file_name = None
        parent_fldr = (os.path.dirname(os.getcwd()))
        self.file_name = parent_fldr + "/Data/SectorsExample.xlsx"

        with pd.ExcelFile(self.file_name) as file:
            self.sheet_names = file.sheet_names

            for i, sheet in enumerate(self.sheet_names):
                if sheet[:6] == 'sector':
                    self.lw.insertItem(i, sheet[6:])

        # --------------------------------------------------------------------
        # Date picker
        self.datepicker = dateWidget(parent=self)
        self.datepicker.show()
        self.datepicker.d1.dateChanged.connect(self.datepicker.date_change)
        self.datepicker.d2.dateChanged.connect(self.datepicker.date_change)

        # --------------------------------------------------------------------

        self.price_df = None
        self.volume_df = None
        self.dailyprice_df = None
        self.error_df = None

        # --------------------------------------------------------------------
        # Tab widget
        self.tab1 = MyTabWidget(self)
        self.tab2 = MyTabWidget(self)
        self.tab3 = MyTabWidget(self)
        self.tab4 = MyTabWidget(self)
        self.tabwidget = QTabWidget(self)
        self.tabwidget.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.tabwidget.setGeometry(340, 50, 360, 600)  # x,y,w,h
        self.tabwidget.addTab(self.tab1, 'Price change')
        self.tabwidget.addTab(self.tab2, 'Volume')
        self.tabwidget.addTab(self.tab3, 'Daily Price difference')
        self.tabwidget.addTab(self.tab4, 'Error Frames')
        self.tabwidget.show()

        self.tab1.tw.itemSelectionChanged.connect(lambda: self.tab1.col_select())
        self.tab2.tw.itemSelectionChanged.connect(lambda: self.tab2.col_select())
        self.tab3.tw.itemSelectionChanged.connect(lambda: self.tab3.col_select())
        # --------------------------------------------------------------------

        self.labeldyn = QLabel('Select sector, dates and market', self)
        self.labeldyn.setAlignment(Qt.AlignCenter)
        self.labeldyn.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.labeldyn.setFont(QFont('Times', 12))
        self.labeldyn.resize(340, 100)
        self.labeldyn.move(355, 100)

        # --------------------------------------------------------------------
        msg_btn = QPushButton('Table\n Info', self)
        msg_btn.setFont(QFont("Open Sans Bold", 12))
        msg_btn.setStyleSheet(stylesheet1)
        msg_btn.move(720, 40)
        msg_btn.resize(55, 55)
        msg_btn.clicked.connect(self.msg)

        # --------------------------------------------------------------------
    def save_table(self):

        tab_index = self.tabwidget.currentIndex()
        if tab_index == 0 and self.price_df is not None:  # price tab
            self.tab1.tab_save(self.price_df)
        if tab_index == 1 and self.volume_df is not None:  # volume tab
            self.tab2.tab_save(self.volume_df)
        if tab_index == 2 and self.dailyprice_df is not None:  # volatility tab
            self.tab3.tab_save(self.dailyprice_df)

    def msg(self):
        msg = QMessageBox()
        text = 'Price Tab:\n' \
               'Last Price - Last price\n' \
               'Avg. - Average price over the time frame\n' \
               'Avg. Adj. - avergae price with FTSE movement removed\n\n' \
               'Volume Tab:\nMin. - Minimum volume\nMax. - Maximum volume\n' \
               'Avg. - Average volume\n\n' \
               'Daily price difference tab:\n' \
               'Avg. Pct. - Average daily price percentage change\n' \
               'Min. Pct. - Minimum daily price percentage change\n' \
               'Max. Pct. - Maximum daily price percentage change'

        msg.setText(text)
        msg.setWindowTitle("Table Label Key")
        #msg.setWindowIcon(QtGui.QIcon("black tic.png"))
        msg.setIcon(QMessageBox.Information)
        msg.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0)")
        msg.exec_()

    def sort_ascending(self):
        tab_index = self.tabwidget.currentIndex()
        tab_col_no1 = self.tab1.num
        tab_col_no2 = self.tab2.num
        tab_col_no3 = self.tab3.num

        if tab_index == 0 and self.price_df is not None:  # price tab
            self.price_df = self.price_df.sort_values(self.price_df.columns[tab_col_no1])
            self.tab1.table_set(self.price_df)
        if tab_index == 1 and self.volume_df is not None:  # volume tab
            self.volume_df = self.volume_df.sort_values(self.volume_df.columns[tab_col_no2])
            self.tab2.table_set(self.volume_df)
        if tab_index == 2 and self.dailyprice_df is not None:  # volatility tab
            self.dailyprice_df = self.dailyprice_df.sort_values(self.dailyprice_df.columns[tab_col_no3])
            self.tab3.table_set(self.dailyprice_df)

    def sort_descending(self):
        tab_index = self.tabwidget.currentIndex()
        tab_col_no1 = self.tab1.num
        tab_col_no2 = self.tab2.num
        tab_col_no3 = self.tab3.num

        if tab_index == 0 and self.price_df is not None:  # price tab
            self.price_df = self.price_df.sort_values(self.price_df.columns[tab_col_no1], ascending=False)
            self.tab1.table_set(self.price_df)
        if tab_index == 1 and self.volume_df is not None:  # volume tab
            self.volume_df = self.volume_df.sort_values(self.volume_df.columns[tab_col_no2], ascending=False)
            self.tab2.table_set(self.volume_df)
        if tab_index == 2 and self.dailyprice_df is not None:  # volatility tab
            self.dailyprice_df = self.dailyprice_df.sort_values(self.dailyprice_df.columns[tab_col_no3], ascending=False)
            self.tab3.table_set(self.dailyprice_df)

    def home(self):
        self.SW = MainWindow()
        self.SW.show()
        self.close()


    # file picker and get sheet names
    def file_select(self):
        self.file_name, _ = QFileDialog.getOpenFileName(self, 'Open File')
        with pd.ExcelFile(self.file_name) as file:
            self.sheet_names = file.sheet_names

            for i, sheet in enumerate(self.sheet_names):
                self.lw.insertItem(i, sheet)

    def list_select_change(self):
        self.label_lw2.setText('Selected = ' + (self.lw.currentItem().text()))

    def stock(self):

        df_list = []
        tick_list = []
        sheet = 'sector' + self.lw.currentItem().text()
        df = pd.read_excel(self.file_name, sheet_name=sheet, usecols="A,C")
        market_list = list(df['Market'])

        for i, market_type in enumerate(market_list):
            if self.cb1.isChecked() and market_type == 'Main':
                tick_list.append(df.at[i,'Code'])
            if self.cb2.isChecked() and market_type == 'Aim':
                tick_list.append(df.at[i, 'Code'])
        start = self.datepicker.start
        end = self.datepicker.end

        for tick in tick_list:
            ticker = tick + '.L'
            result_df = stock_check(ticker, start, end)
            df_list.append(result_df)
        self.labeldyn.setHidden(True)

        df_list, self.error_df, tick_list = errorRemove(df_list, tick_list)

        self.price_df = PriceAnalysis(df_list, start, end, tick_list)
        self.volume_df = VolumeAnalysis(df_list, tick_list)
        self.dailyprice_df = DailyPriceAnalysis(df_list, tick_list)

        self.tab1.table_set(self.price_df)
        self.tab2.table_set(self.volume_df)
        self.tab3.table_set(self.dailyprice_df)
        self.tab4.table_set(self.error_df)


# ----------------------------------------------------------------------------
# Tab widget


class MyTabWidget(QWidget):

    def __init__(self, parent):
        super(MyTabWidget, self).__init__(parent=None)

        self.tw = QTableWidget(self)
        self.tw.resize(360, 600)
        self.num = 0

    def table_set(self,df):

        row = df.shape
        rowN = (row[0])
        colN = (row[1])

        self.tw.setRowCount(rowN)
        self.tw.setColumnCount(colN)
        width = self.tw.size().width()
        self.tw.setColumnWidth(0, width*0.23)
        self.tw.setColumnWidth(1, width*0.23)
        self.tw.setColumnWidth(2, width*0.23)
        self.tw.setColumnWidth(3, width*0.23)

        col_list = []
        for col in df.columns:
            col_list.append(col)
        self.tw.setHorizontalHeaderLabels(col_list)

        for i1 in range(0, rowN):
            for i in range(0, colN):
                cell_val = str(df.iat[i1, i])
                self.tw.setItem(i1, i, QTableWidgetItem(cell_val))
    def col_select(self):
        items = self.tw.selectedIndexes()
        self.num = (items[0].column())

    def tab_save(self, df):
        path = 'testsave.xlsx'
        df.to_excel(path)

# ----------------------------------------------------------------------------
# date widget


class dateWidget(QWidget):

    def __init__(self, parent):
        super(dateWidget, self).__init__(parent=parent)
        self.start = 0
        self.end = 0
        # --------------------------------------------------------------------
        # Date picker
        self.label_from = QLabel('From',parent)
        self.label_from.setAlignment(Qt.AlignCenter)
        self.label_from.setFont(QFont("Open Sans Bold", 12))
        self.label_from.setStyleSheet("background-color: rgb(134,194,50);"
                                 "color: rgb(255,255,255);")
        self.label_from.resize(100, 20)
        self.label_from.move(20, 60)

        self.d1 = QDateEdit(parent, calendarPopup=True)
        self.d1.setDateTime(QDateTime.currentDateTime())
        self.d1.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.d1.setGeometry(20, 80, 100, 25)
        #self.d1.dateChanged.connect(self.date_change)

        label_to = QLabel('To', parent)
        label_to.setAlignment(Qt.AlignCenter)
        label_to.setFont(QFont("Open Sans Bold",12))
        label_to.setStyleSheet("background-color: rgb(134,194,50);"
                               "color: rgb(255,255,255);")
        label_to.resize(100, 20)
        label_to.move(140, 60)

        self.d2 = QDateEdit(parent, calendarPopup=True)
        self.d2.setDateTime(QDateTime.currentDateTime())
        self.d2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.d2.setGeometry(140, 80, 100, 25)

    def date_change(self):

        self.start = self.d1.dateTime().toString('yyyy-MM-dd')
        self.end = self.d2.dateTime().toString('yyyy-MM-dd')

        # --------------------------------------------------------------------


# ----------------------------------------------------------------------------
# MAIN


if __name__ == '__main__':

    app = QApplication(sys.argv)
    MW = MainWindow()
    MW.show()
    sys.exit(app.exec_())
