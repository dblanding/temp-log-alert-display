"""Show plot of temperatures by calendar date (starting 9/20/2020)"""

import matplotlib.pyplot as plt
from matplotlib import style
from pathlib import Path
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QApplication, QCalendarWidget, QWidget, QLabel
import sys

style.use('ggplot')

month_dict = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4,
              'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8,
              'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}

class Calendar(QWidget):
    def __init__(self):
        super(Calendar, self).__init__()
        self.initUI()
    def initUI(self):
        my_calendar = QCalendarWidget(self)
        my_calendar.setGridVisible(True)
        my_calendar.move(10, 20)
        my_calendar.clicked[QDate].connect(self.show_date)
        self.my_label = QLabel(self)
        date = my_calendar.selectedDate()
        self.my_label.setText(date.toString())
        self.my_label.move(10, 220)
        self.setGeometry(100,100,320,270)
        self.setWindowTitle('Calendar')
        self.show()
    def show_date(self, date):
        dow, mo, day, year = date.toString().split()
        month = month_dict[mo]
        date = date.toString()
        reply = plot_temp(year, month, day, date)
        self.my_label.setText(reply)
        self.my_label.adjustSize()
        
def plot_temp(y, m, d, date):
    file = Path(r'\\RASPI80\share', f"year{y}", f"month{m}", f"day{d}.csv")
    try:
        times = []
        temps = []
        for line in open(file):
            str_time, str_temp = line.strip().split()
            hr, mn = str_time.split(':')
            if mn == '00,':
                times.append(int(hr))
                temps.append(float(str_temp))
    except FileNotFoundError:
        return f"No data for {date}"
    plt.scatter(times, temps, color='#003F72', label = 'temp')
    plt.plot(times, temps)
    plt.title(date)
    plt.xticks([ 0., 3., 6., 9., 12., 15., 18., 21., 24.])
    plt.show()
    return f"Showing data for {date}"
    
def main():
    app = QApplication(sys.argv)
    ex = Calendar()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
