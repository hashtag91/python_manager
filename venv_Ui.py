from PyQt5.QtWidgets import (
    QScrollArea,QFrame, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, 
                            QToolButton, QMainWindow, QApplication)
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QCursor, QFont, QIcon
from qtwidgets import AnimatedToggle
import venv_script
import sys
import os
from pywinauto import Application
import pywinauto

class Venv(QFrame):
    def __init__(self, name:str, path:str, p_version:str,layout1:QVBoxLayout):
        super().__init__()
        self.setStyleSheet("""QFrame{
            background-color:rgba(255,255,255,80);
            border-radius: 10px;
        }""")
        self.setContentsMargins(0, 0, 0, 0)
        self.setMaximumHeight(40)
        self.name = name
        self.path = path
        self.p_version = p_version
        self.layout1 = layout1
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 15, 0)
        self.setupUi()
        self.setLayout(self.layout)
        self.toggler_state = 0
    def setupUi(self):
        self.name_label = QLabel(self.name)
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_label.setMinimumWidth(80)
        self.name_label.setFont(QFont("Arial", 12))
        self.name_label.setStyleSheet("color: #ffffff")
        self.path_line = QLineEdit(self.path)
        self.path_line.setStyleSheet("background: transparent; border:none; color: #ffffff")
        self.path_line.setReadOnly(True)
        self.p_version_line = QLineEdit(self.p_version)
        self.p_version_line.setStyleSheet("background: transparent; border:none; color: #ffffff")
        self.p_version_line.setReadOnly(True)
        self.switch_radio = AnimatedToggle(checked_color="#005dc7")
        self.switch_radio.toggled.connect(self.activate_venv)
        self.edit_btn = QToolButton()
        self.edit_btn.setIcon(QIcon("img/pencil.svg"))
        self.edit_btn.setStyleSheet("background:transparent; border:none")
        self.edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.delete_btn = QToolButton()
        self.delete_btn.setIcon(QIcon("img/garbage.svg"))
        self.delete_btn.setStyleSheet("background:transparent; border:none")
        self.delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.delete_btn.clicked.connect(self.terminate_process)
        self.eye_btn = QToolButton()
        self.eye_btn.setIcon(QIcon("img/eye.svg"))
        self.eye_btn.setStyleSheet("background:transparent; border:none")
        self.eye_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.eye_btn.clicked.connect(self.print_widget_position)
        self.layout.addWidget(self.name_label,1)
        self.layout.addWidget(self.path_line,2)
        self.layout.addWidget(self.p_version_line,1)
        self.layout.addWidget(self.switch_radio)
        self.layout.addWidget(self.edit_btn)
        self.layout.addWidget(self.delete_btn)
        self.layout.addWidget(self.eye_btn)
        
    def print_widget_position(self):
        for i in range(self.layout1.count()):
            widget = self.layout1.itemAt(i).widget()
            if widget.name_label.text() == self.name_label.text():
                print(self.layout1.indexOf(widget))
                break
    def activate_venv(self):
        for i in range(self.layout1.count()):
            widget = self.layout1.itemAt(i).widget()
            if widget.name_label.text() == self.name_label.text():
                title = f"{widget.name_label.text()}"
                #subprocess.Popen(['start cmd', '/k','title', title, '&', f"{widget.path_line.text()}/Scripts/activate"])
                if self.toggler_state == 0:
                    os.system(f"start cmd /k title {title} {widget.path_line.text()}/Scripts/activate")
                    self.toggler_state += 1
                    break
                else:
                    self.terminate_process()
                    self.toggler_state -= 1
                    break
    #Fonction permettant de fermer les fenêtres cmd en fonction de leur nom
    def close_window(self,title):
        windows = pywinauto.findwindows.find_windows(title_re=title)
        try:
            hwnd = windows[0]
            app = Application().connect(handle=hwnd)
            window = app.window(handle=hwnd)
            window.close()
        except IndexError:
            print("Cmd already closed !")
    #Fonction pour avoir le titre de la fenêtre cmd et application la fermeture (qtsignal)
    def terminate_process(self):
        for i in range(self.layout1.count()):
            widget = self.layout1.itemAt(i).widget()
            if widget.name_label.text() == self.name_label.text():
                self.close_window(widget.name_label.text())
                break

class Venv_frame(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("Ven_frame")
        with open('style.css','r') as s:
            self.setStyleSheet(s.read())
        self.layout = QVBoxLayout()
        self.setupUi()
        self.setLayout(self.layout)
    def setupUi(self):
        title = QLabel("Virtual Environment")
        title.setObjectName("title1")
        title.setFont(QFont("Arial Black", 13))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(title)
        
        #Buttons panel
        btn_frame = QFrame()
        btn_frame.setObjectName("venvUi_btn_frame")
        btn_frame_layout = QHBoxLayout()
        btn_frame_layout.setContentsMargins(9,0,20,0)
        self.add_btn = QToolButton()
        self.add_btn.setIcon(QIcon("img/plus.svg"))
        self.add_btn.setIconSize(QSize(30, 30))
        self.add_btn.setMinimumSize(QSize(35,35))
        self.add_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.add_btn.setToolTip("Create")
        self.refresh_btn = QToolButton()
        self.refresh_btn.setIcon(QIcon("img/refresh.svg"))
        self.refresh_btn.setIconSize(QSize(30, 30))
        self.refresh_btn.setMinimumSize(QSize(35,35))
        self.refresh_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.refresh_btn.setToolTip("Refresh")
        btn_frame_layout.addStretch()
        btn_frame_layout.addWidget(self.add_btn)
        btn_frame_layout.addWidget(self.refresh_btn)
        btn_frame.setLayout(btn_frame_layout)
        
        #Main Panel
        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("venv_scroll1")
        scroll_frame = QFrame()
        self.scroll_frame_layout = QVBoxLayout()
        self.data = venv_script.Data_collection().data_result()
        for i in self.data:
            self.scroll_frame_layout.addWidget(Venv(i[0],i[1],i[2],self.scroll_frame_layout))
        scroll_frame.setLayout(self.scroll_frame_layout)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(scroll_frame)
        
        self.layout.addWidget(btn_frame)
        self.layout.addWidget(self.scroll_area)
        self.layout.addStretch()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setStyleSheet("background-color: #0f0f0f")
    win.setCentralWidget(Venv_frame())
    win.show()
    sys.exit(app.exec_())