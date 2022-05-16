import psycopg2
import sys 

from PyQt5.QtWidgets import (QApplication, QWidget,
                            QAbstractScrollArea,
                            QVBoxLayout, QHBoxLayout, QTabWidget,
                            QTableWidget, QGroupBox, 
                        QTableWidgetItem, QPushButton, QMessageBox)

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
    
        self._connect_to_db()

        self.setWindowTitle("TimeTable")

        self.vbox = QVBoxLayout(self)

        self.tabs = QTabWidget(self)
        self.vbox.addWidget(self.tabs)

        self._create_shedule_tab()

    def _connect_to_db(self):
        self.conn = psycopg2.connect(database="school_timetable",
                                    user="postgres",
                                    password="1111",
                                    host="localhost",
                                    port="5432")
        self.cursor = self.conn.cursor()

    def _create_shedule_tab(self):
        self.shedule_tab = QWidget()
        self.tabs.addTab(self.shedule_tab, "TimeTable")

        self.monday_gbox = QGroupBox("Расписание")

        self.svbox = QVBoxLayout()
        self.shbox1 = QVBoxLayout()
        self.shbox2 = QVBoxLayout()

        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)

        self.shbox1.addWidget(self.monday_gbox)

        self._create_monday_table()

        self.update_shedule_button = QPushButton("Update")
        self.shbox2.addWidget(self.update_shedule_button)
        self.update_shedule_button.clicked.connect(self._update_monday_table)

        self.shedule_tab.setLayout(self.svbox)

    def _create_monday_table(self):
        self.monday_table = QTableWidget()
        self.monday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.monday_table.setColumnCount(5)
        self.monday_table.setHorizontalHeaderLabels(["id", "day", "subject", "room_numb", "start_time"])

        self._update_monday_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.monday_table)
        self.monday_gbox.setLayout(self.mvbox)
    

    def _update_monday_table(self):
        self.monday_table.setRowCount(0)
        self.cursor.execute("SELECT * FROM timetable.timetable")
        records = list(self.cursor.fetchall())

        self.monday_table.setRowCount(len(records))

        for i, r in enumerate(records):
            r = list(r)

            self.monday_table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.monday_table.setItem(i, 1, QTableWidgetItem(str(r[1])))
            self.monday_table.setItem(i, 2, QTableWidgetItem(str(r[2])))
            self.monday_table.setItem(i, 3, QTableWidgetItem(str(r[3])))
            self.monday_table.setItem(i, 4, QTableWidgetItem(str(r[4])))
            
        self.monday_table.resizeRowsToContents()


app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())