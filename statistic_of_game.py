import sqlite3
import sys
from PyQt5 import QtWidgets


# данный класс выплняет задачу вывода статистики об рекордах игроков из базы game.sqlite
class Stat_Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(300, 400)
        self.setWindowTitle('Scores')
        # создание таблицы
        self.table = QtWidgets.QTableWidget(self)
        self.table.setGeometry(10, 10, 280, 380)
        with sqlite3.connect('game.db') as con:
            cur = con.cursor()
        scores = cur.execute('SELECT * FROM score').fetchall()
        self.table.setRowCount(len(scores))
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['id', 'name', 'score'])
        # отрисовка таблицы
        for i in range(len(scores)):
            for j in range(len(scores[i])):
                self.table.setItem(i, j, QtWidgets.QTableWidgetItem(str(scores[i][j])))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = Stat_Window()
    ex.show()
    sys.exit(app.exec())