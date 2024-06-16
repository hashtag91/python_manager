from PyQt5.QtWidgets import (
    QScrollArea,QFrame, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, 
    QToolButton, QWidget, QTableWidget, QTableWidgetItem,QHeaderView, QDialog)
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QCursor, QFont, QIcon, QPixmap
from qtwidgets import AnimatedToggle
import venv_script
import os
import sys
from pywinauto import Application
import pywinauto
from package_list import Packages
import sqlite3

class Venv_details(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #e8e8e8;")
        self.main_layout = QVBoxLayout()
        self.setupUi()
        self.setLayout(self.main_layout)
    def setupUi(self):
        title_layout = QHBoxLayout()
        self.title = QLabel("Title")
        self.title.setStyleSheet("color: #363636")
        self.title.setFont(QFont("Arial Black",18,QFont.Bold))
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_layout.addWidget(self.title)
        self.main_layout.addLayout(title_layout)

        #PATH
        self.path_frame = QFrame()
        self.path_frame.setStyleSheet("border-radius: 15%")
        self.path_layout = QHBoxLayout()
        self.path_frame.setLayout(self.path_layout)
        path_ico = QLabel()
        path_ico.setPixmap(QPixmap("img/folder.svg").scaled(QSize(30,30),aspectRatioMode=Qt.AspectRatioMode.IgnoreAspectRatio, transformMode=Qt.TransformationMode.SmoothTransformation))
        self.path_layout.addWidget(path_ico)
        self.path_line = QLineEdit()
        self.path_line.setStyleSheet("background: transparent; border: none")
        self.path_line.setReadOnly(True)
        self.path_layout.addWidget(self.path_line)
        #Button panel
        btn_panel = QFrame()
        btn_panel.setStyleSheet("""
            QFrame{
                background: transparent;
            }
            QToolButton{
                background: transparent;
            }
                                """)
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(0)
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        btn_panel.setLayout(btn_layout)
        self.add_btn = QToolButton()
        self.add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_btn.setIcon(QIcon("img/plus-dark"))
        self.remove_btn = QToolButton()
        self.remove_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.remove_btn.setIcon(QIcon("img/trash-dark"))
        self.update_btn = QToolButton()
        self.update_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.update_btn.setIcon(QIcon("img/update"))
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.remove_btn)
        btn_layout.addWidget(self.update_btn)
        #Pyhon version
        self.python_frame = QFrame()
        self.python_frame.setStyleSheet("background: transparent; border: none")
        python_layout = QHBoxLayout()
        self.python_frame.setLayout(python_layout)
        python_ico =  QLabel()
        python_ico.setPixmap(QPixmap("img/python-dark1.png").scaled(QSize(15,15),aspectRatioMode=Qt.AspectRatioMode.IgnoreAspectRatio, transformMode=Qt.TransformationMode.SmoothTransformation))
        python_layout.addStretch()
        python_layout.addWidget(python_ico)
        self.python_line = QLineEdit()
        self.python_line.setMaximumWidth(100)
        self.python_line.setStyleSheet("background: transparent; border: none")
        self.python_line.setReadOnly(True)
        python_layout.addWidget(self.python_line)

        self.tableau = QTableWidget()
        self.tableau.setColumnCount(2)
        self.tableau.setColumnWidth(1,20)
        self.tableau.horizontalHeader().setSectionResizeMode(0,QHeaderView.Stretch)
        self.tableau.setColumnWidth(1,150)
        self.tableau.setHorizontalHeaderLabels(['Path','Version'])
        self.tableau.horizontalHeader().stretchLastSection()

        self.main_layout.addWidget(self.path_frame)
        self.main_layout.addWidget(btn_panel)
        self.main_layout.addWidget(self.tableau)
        self.main_layout.addWidget(self.python_frame)
        

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
        self.p_version_line = QLineEdit(f"Python {self.p_version}")
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
        self.details = QDialog()
        self.venv_details = Venv_details()
        detail_layout = QVBoxLayout()
        detail_layout.addWidget(self.venv_details)
        self.details.setLayout(detail_layout)
        
    def print_widget_position(self):
        for i in range(self.layout1.count()):
            widget = self.layout1.itemAt(i).widget() #Obtenir le objet widget du boutton eye clicqué
            if widget.name_label.text() == self.name_label.text():
                print(self.layout1.indexOf(widget)) # Avoir la position du widget dans le layout pour pouvoir le manipuler
                self.venv_details.title.setText(self.name_label.text())
                self.venv_details.path_line.setText(self.path_line.text())
                self.venv_details.python_line.setText(self.p_version_line.text())
                self.packages = Packages(widget.path_line.text(),self.name_label.text()).data()
                self.venv_details.tableau.setRowCount(len(self.packages))
                for row, row_data in enumerate(self.packages): #avoir l'indexe et les valeurs de chaque ligne
                    for column, values in enumerate(row_data): #avoir l'indexe la valeur de chaque colonne de la ligne
                        self.venv_details.tableau.setItem(row, column, QTableWidgetItem(values))
                self.details.exec()
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
            s.close()
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
        self.refresh_btn.clicked.connect(self.my_refresh)
        btn_frame_layout.addStretch()
        btn_frame_layout.addWidget(self.add_btn)
        btn_frame_layout.addWidget(self.refresh_btn)
        btn_frame.setLayout(btn_frame_layout)
        
        #Main Panel
        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("venv_scroll1")
        scroll_frame = QFrame()
        scroll_frame.setStyleSheet("background: transparent;")
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
        
    def my_refresh(self):
        venv_script.Venv_found()