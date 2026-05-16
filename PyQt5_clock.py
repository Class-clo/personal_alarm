import sys
import os
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QPushButton, QRadioButton, QLineEdit, QHBoxLayout
from PyQt5.QtCore import QTimer, QTime, Qt
from PyQt5.QtGui import QFont, QFontDatabase

class DigitalClock(QWidget):
    def __init__(self):
        super().__init__()
        self.time_label = QLabel("12:00:00", self)
        self.alarms_label = QLabel("No alarms", self)
        self.alarms_label.hide()
        self.alarms_button = QPushButton("Alarms", self)

        self.set_alarm_lineedit = QLineEdit(self)
        self.set_alarm_lineedit.hide()
        self.set_alarm_button = QPushButton("Set alarm")
        self.set_alarm_button.hide()
        self.alarms = []
        self.timer = QTimer(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Digital Clock")
        self.setGeometry(700, 400, 300, 100)
        self.set_alarm_lineedit.setPlaceholderText("hh:mm AM/PM")
        self.time_label.setObjectName("time_label")
        self.alarms_button.setObjectName("alarms_button")
        self.set_alarm_button.setObjectName("set_alarm_button")
        self.alarms_button.clicked.connect(self.open_alarms)
        self.set_alarm_button.clicked.connect(self.set_alarm_buttonfunc)

        self.opened = False
        self.layouts()
        self.styles()
        self.clock_functionality()

    def layouts(self):
        vbox = QVBoxLayout(self)
        hbox = QHBoxLayout()
        vbox.addWidget(self.alarms_label)
        hbox.addWidget(self.set_alarm_lineedit)
        hbox.addWidget(self.set_alarm_button)
        vbox.addLayout(hbox)
        vbox.addWidget(self.alarms_button)
        vbox.addWidget(self.time_label)
        self.setLayout(vbox)

    def styles(self):
        self.time_label.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("""
                            QLabel#time_label{
                                font-size: 150px;
                                color: #5CA904;
                                border-radius: 10px;
                                background-color: black;
                            }

                            QPushButton#set_alarm_button{
                                border: 3px solid;
                                font-size: 30px;
                                font-weight: bold;
                                background-color: #adadac;
                                border-radius: 7px;
                                padding: 10px 10px;
                            }
                            
                            QPushButton#alarms_button{
                                border: 3px solid;
                                font-size: 30px;
                                font-weight: bold;
                                background-color: #adadac;
                                border-radius: 7px;
                            }
                            
                            QLineEdit{
                                border: 3px solid;
                                font-size: 30px;
                                font-weight: bold;
                                border-radius: 7px;
                                padding: 5px 10px;
                            }
                            
                        """)
                                      
        self.font_id = QFontDatabase.addApplicationFont("games/gud/DS-DIGIT.TTF")
        self.font_family = QFontDatabase.applicationFontFamilies(self.font_id)[0]
        self.my_font = QFont(self.font_family, 150)
        self.time_label.setFont(self.my_font)

    def clock_functionality(self):
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()

    def open_alarms(self):
        if self.opened == False and self.alarms_button.clicked:
            self.alarms_label.show()
            self.set_alarm_button.show()
            self.set_alarm_lineedit.show()
            self.alarms_button.setText("Hide alarms")
            self.opened = True
        elif self.opened == True and self.alarms_button.clicked:
            self.alarms_label.hide()
            self.set_alarm_button.hide()
            self.set_alarm_lineedit.hide()
            self.alarms_button.setText("Alarms")
            self.opened = False

    def set_alarm_buttonfunc(self):
        alarm_time = self.set_alarm_lineedit.text().strip()    #       By AI start

        # Simple validation: Ensure field isn't empty and alarm is unique    
        if alarm_time and alarm_time not in self.alarms:
            self.alarms.append(alarm_time)
            
            # Rebuild the full text display from the updated list
            full_alarm_text = "\n".join(self.alarms)
            self.alarms_label.setText(full_alarm_text)
            
            # Optional: Clear the input box after adding the alarm 
            self.set_alarm_lineedit.clear()        #                    By AI  end

    def alarm_functionality(self):
        time_now = QTime.currentTime().toString("hh:mm AP")
        if time_now in self.alarms:
            os.system('spd-say "Wake up"')

    def update_time(self):
        current_time = QTime.currentTime().toString("hh:mm:ss AP")
        self.time_label.setText(current_time)
        self.alarm_functionality()
        



if __name__ == '__main__':
    app = QApplication(sys.argv)
    clock = DigitalClock()
    clock.show()
    sys.exit(app.exec_())