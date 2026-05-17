import sys
import subprocess
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QPushButton, QRadioButton, QLineEdit, QHBoxLayout
from PyQt5.QtCore import QTimer, QTime, Qt
from PyQt5.QtGui import QFont, QFontDatabase
import time
import threading
#------------------------Imports------------------------


class DigitalClock(QWidget):
    def __init__(self):
        super().__init__()
        self.time_label = QLabel("--:--:-- --", self) #If this gets deleted, changes have been undone.
        self.alarms_label = QLabel("No alarms", self)
        self.alarms_label.hide()
        self.stop_alarm_button = QPushButton("Stop alarm", self)
        self.stop_alarm_button.hide()
        self.alarms_button = QPushButton("Alarms", self)

        self.set_alarm_lineedit = QLineEdit(self)
        self.set_alarm_lineedit.hide()
        self.set_alarm_button = QPushButton("Set alarm")
        self.set_alarm_button.hide()
        self.alarms = []
        self.clock_timer = QTimer(self)
        self.alarm_timer = QTimer(self)
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
        vbox.addWidget(self.stop_alarm_button)
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
        self.clock_timer.timeout.connect(self.thread1.start())
        self.clock_timer.start(1000)
        self.thread1 = threading.Thread(target=self.update_time, )
        self.thread2 = threading.Thread(target=self.alarm_functionality, )
        self.thread1.start()
        self.thread2.start()
        #here

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
        time_obj = QTime.fromString(alarm_time, "hh:mm AP")

        # Simple validation: Ensure field isn't empty and alarm is unique
        if time_obj.isValid():
            alarm_time = time_obj.toString("hh:mm AP")  # Standardize format
            if alarm_time and alarm_time not in self.alarms:
                # if self.alarms_label.text() ==
                self.alarms.append(alarm_time)
                full_alarm_text = "\n".join(self.alarms)            # Rebuild the full text display from the updated list
                self.alarms_label.setText(full_alarm_text)
                self.set_alarm_lineedit.clear()            # Optional: Clear the input box after adding the alarm
            else:
                self.set_alarm_lineedit.clear()
                self.set_alarm_lineedit.setPlaceholderText("You already set that alarm")  # Feedback for duplicate alarm
        else:
            self.set_alarm_lineedit.clear()
            self.set_alarm_lineedit.setPlaceholderText("Enter a valid time (hh:mm AP)")                    #                    By AI  end


    def alarm_functionality(self):
        alarm_time = self.current_time[0:5] + self.current_time[-3:]
        print("Checking alarm:", alarm_time)  # Debug print to verify the alarm time being checked
        if alarm_time in self.alarms:
            subprocess.run(['spd-say', 'Wake up'])
            self.stop_alarm_button.show()
            self.stop_alarm_button.clicked.connect(self.stop_alarm)
    
    def stop_alarm(self):
        self.clock_seconds = QTime.currentTime().second()
        subprocess.run(['pkill', 'spd-say " Wake up"'])
        self.stop_alarm_button.hide()
        time.sleep(60 - int(self.clock_seconds))  # Prevents the alarm from immediately going off again if the user stops it within the same minute

    def update_time(self):
        self.current_time = QTime.currentTime().toString("hh:mm:ss AP")
        self.time_label.setText(self.current_time)
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    clock = DigitalClock()
    clock.show()
    sys.exit(app.exec_())