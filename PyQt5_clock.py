import sys
import os
import time
import pygame
import threading
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QPushButton, QRadioButton, QLineEdit, QHBoxLayout, QGridLayout
from PyQt5.QtCore import QTimer, QTime, Qt, pyqtSignal
from PyQt5.QtGui import QFont, QFontDatabase
import databases_module_for_alarms
#------------------------Imports------------------------

class AlarmRow(QWidget):

    def __init__(self, text, db, parent_window):
        super().__init__()

        self.db = db
        self.text = text
        self.parent_window = parent_window
        self.label = QLabel(self.text)
        self.button = QPushButton("Delete")
        
        self.label.setMinimumSize(100, 20)
        self.label.setMaximumSize(2000, 60)
        self.button.setMinimumSize(50, 20)
        self.button.setMaximumSize(100, 60)

        self.label.setStyleSheet("font-size: 10px; font-weight: bold; background-color: #f0eded; border: 2px solid; border-radius: 5px;")
        self.button.setStyleSheet("font-size: 10px; font-weight: bold; background-color: #f0eded; border: 2px solid; border-radius: 5px;")

        layout = QHBoxLayout()

        layout.addWidget(self.label)
        layout.addWidget(self.button)

        self.setLayout(layout)
        self.button.clicked.connect(self.delete_self)


    def enterEvent(self, event):
        
        super().enterEvent(event)
        self.label.setStyleSheet("""
            background-color: #969292;
            color: white;
            font-size: 10px; 
            font-weight: bold;
            border: 2px solid;
            border-radius: 5px;
        """)
        self.button.setStyleSheet("""
            background-color: #ff4040;  
            color: white;
            font-size: 10px; 
            font-weight: bold;
            border: 2px solid;
            border-radius: 5px;
        """)


    def leaveEvent(self, event):
        super().leaveEvent(event)

        self.label.setStyleSheet("font-size: 10px; font-weight: bold; background-color: #f0eded; border: 2px solid; border-radius: 5px;")
        self.button.setStyleSheet("font-size: 10px; font-weight: bold; background-color: #f0eded; border: 2px solid; border-radius: 5px;")


    def delete_self(self):
        self.db.delete_value(self.text)
        # self.deleteLater()
        self.parent_window.refresh()
        self.parent_window.adjustSize()




class AlarmsWindow(QWidget):

    def __init__(self, db):
        super().__init__()
        self.setWindowTitle("List of Alarms")
        self.resize(200, 50)
        self.db = db
        self.initUI()
    

    def initUI(self):
        # print(self.db.count_values())  testing
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        for y, x in enumerate(self.db.read_all()):
            alarm_row = AlarmRow(x, self.db, self)
            # alarm_row.mouse_entered.connect(self.on_hover_enter)
            # alarm_row.mouse_left.connect(self.on_hover_leave)

            self.grid.addWidget(alarm_row, y, 0)


    def refresh(self):

        while self.grid.count():
            item = self.grid.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        for y, x in enumerate(self.db.read_all()):
            alarm_row = AlarmRow(x, self.db, self)
            self.grid.addWidget(alarm_row, y, 0)



class DigitalClock(QWidget):
    def __init__(self):
        super().__init__()
        self.time_label = QLabel("12:00:00", self)
        self.alarms_label = QLabel("No alarms", self)
        self.alarms_label.hide()
        self.alarms_button = QPushButton("Alarms", self)
        self.alarm_istriggered = None
        self.stop_alarm_button = QPushButton("Stop alarm", self)
        self.am_radio_button = QRadioButton("AM", self)
        self.pm_radio_button = QRadioButton("PM", self)
        self.am_radio_button.setChecked(True)
        self.am_radio_button.hide()
        self.pm_radio_button.hide()
        self.stop_alarm_button.hide()
        self.alarms_window_button = QPushButton("Show Alarms", self)
        self.alarms_window = None
        self.alarms_window_button.hide()
        self.set_alarm_lineedit = QLineEdit(self)
        self.set_alarm_lineedit.hide()
        self.set_alarm_button = QPushButton("Set alarm")
        self.set_alarm_button.hide()
        self.timer = QTimer(self)

        self.db = databases_module_for_alarms.Database("personal_alarms_db")
        self.alarms = []
        for value in self.db.read_all():
            self.alarms.append(value)
            self.alarms_label.setText("\n".join(self.alarms))

        self.initUI()


    def initUI(self):
        self.setWindowTitle("Digital Clock")
        self.setGeometry(700, 400, 300, 100)
        self.set_alarm_lineedit.setPlaceholderText("hh:mm")
        self.time_label.setObjectName("time_label")
        self.alarms_button.setObjectName("alarms_button")
        self.set_alarm_button.setObjectName("set_alarm_button")
        self.alarms_button.clicked.connect(self.open_alarms)
        self.set_alarm_button.clicked.connect(self.set_alarm_buttonfunc)
        self.stop_alarm_button.setObjectName("stop_alarm_button")
        self.am_radio_button.setObjectName("am_radio_button")
        self.pm_radio_button.setObjectName("pm_radio_button")
        self.alarms_window_button.setObjectName("Show_Alarms_button")
        self.alarms_window_button.clicked.connect(self.open_alarms_window)
        self.opened = False
        self.layouts()
        self.styles()
        self.clock_functionality()


    def layouts(self):
        vbox = QVBoxLayout(self)
        hbox = QHBoxLayout()
        # vbox.addWidget(self.alarms_label) for testing
        hbox.addWidget(self.set_alarm_lineedit)
        hbox.addWidget(self.am_radio_button)
        hbox.addWidget(self.pm_radio_button)
        hbox.addWidget(self.set_alarm_button)
        vbox.addLayout(hbox)
        vbox.addWidget(self.alarms_window_button)
        vbox.addWidget(self.alarms_button)
        vbox.addWidget(self.time_label)
        vbox.addWidget(self.stop_alarm_button)
        # vbox.addWidget(self.alarms_window_button)
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
                            QPushButton#stop_alarm_button{
                                border: 3px solid;
                                border-radius: 7px;
                                font-size: 20px;
                                font-weight: bold;
                                padding: 3px 5px;
                                background-color: #adadac;
                            }
                            QPushButton#Show_Alarms_button{
                                border: 3px solid;
                                background-color: #adadac;
                                font-size: 20px;
                                font-weight: bold;
                                padding: 2px 1px;
                                border-radius: 7px;
                            }
                        
                            QLineEdit{
                                border: 3px solid;
                                font-size: 20px;
                                font-weight: bold;
                                border-radius: 7px;
                                padding: 15px 10px;
                            }
                        
                            QRadioButton {
                                font-size: 20px;
                                font-weight: bold;
                                spacing: 10px;
                            }

                            QRadioButton:indicator{
                                width: 18px;
                                height: 18px;
                                border: 2px solid #444;
                                border-radius: 9px;
                            }

                            QRadioButton:indicator:checked{
                                background-color: #444;
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


    def open_alarms_window(self):
        if self.alarms_window is None:
            self.alarms_window = AlarmsWindow(self.db)
        self.alarms_window.show()
        self.alarms_window.raise_()
        self.alarms_window.activateWindow()


    def open_alarms(self):
        if self.opened == False and self.alarms_button.clicked:

            # self.alarms_label.show()      # for testing
            self.alarms_window_button.show()
            self.set_alarm_button.show()
            self.set_alarm_lineedit.show()
            self.am_radio_button.show()
            self.pm_radio_button.show()
            self.alarms_button.setText("Hide alarms")
            self.opened = True

        elif self.opened == True and self.alarms_button.clicked:

            self.alarms_window_button.hide()
            self.alarms_label.hide()
            self.set_alarm_button.hide()
            self.set_alarm_lineedit.hide()
            self.am_radio_button.hide()
            self.pm_radio_button.hide()
            self.alarms_button.setText("Alarms")
            self.opened = False


    def set_alarm_buttonfunc(self):
        self.refresh()
        alarm_text = self.set_alarm_lineedit.text().strip()
        # if not alarm_text:     #does not work if the user only enters spaces, so we strip the text first and then check if it's empty
        #     self.set_alarm_lineedit.setPlaceholderText("Enter a time like 07:30")
        #     return
        if self.am_radio_button.isChecked():
            ampm = "AM"
        elif self.pm_radio_button.isChecked():
            ampm = "PM"
        else:
            self.set_alarm_lineedit.setPlaceholderText("Choose AM or PM")
            return

        self.alarm_time = f"{alarm_text} {ampm}"
        time_obj = QTime.fromString(self.alarm_time, "hh:mm AP")

        if time_obj.isValid():
            self.alarm_time = time_obj.toString("hh:mm AP")

            if self.alarm_time not in self.alarms:

                # with databases_module_main.Database("school3") as db:

                self.alarms.append(self.alarm_time)
                self.db.add_value(self.alarm_time)
                if self.alarms_window is not None:
                    self.alarms_window.refresh()
                # self.alarms_window.show()
                # self.alarms_window.raise_()
                # self.alarms_window.activateWindow()
                self.alarms_label.setText("\n".join(self.alarms))
                self.set_alarm_lineedit.clear()
                    
            else:
                self.set_alarm_lineedit.clear()
                self.set_alarm_lineedit.setPlaceholderText("You already set that alarm")
        else:
            self.set_alarm_lineedit.clear()
            self.set_alarm_lineedit.setPlaceholderText("Enter a valid time (hh:mm)")

    def alarm_functionality(self):
        time_now = QTime.currentTime().toString("hh:mm AP")
        if time_now in self.alarms and time_now != self.alarm_istriggered:

            thread1 = threading.Thread(target=self.play_alarm_sound, daemon=True)
            thread1.start()
            self.alarm_istriggered = time_now
            self.stop_alarm_button.show()
            self.stop_alarm_button.clicked.connect(self.stop_alarm)

        elif time_now not in self.alarms:

            self.alarm_istriggered = None  # Reset the alarm trigger if the current time is not in the alarms list       
            self.stop_alarm_button.hide()


    def play_alarm_sound(self):
        pygame.mixer.init()
        pygame.mixer.music.load("games/gud/The Fog - Trey Xavier, Rod Kim.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)


    def stop_alarm(self):
        pygame.mixer.music.stop()
        self.stop_alarm_button.hide()


    def update_time(self):
        current_time = QTime.currentTime().toString("hh:mm:ss AP")
        self.time_label.setText(current_time)
        self.alarm_functionality()

    
    def refresh(self):
        self.alarms = []
        for alarm in self.db.read_all():
            self.alarms.append(alarm)



clock = None

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        clock = DigitalClock()
        clock.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Sorry, something went wrong. \n Error: \n \n {e}")
    finally:
        if clock is not None:
            clock.db.close_db()