from PyQt5.QtWidgets import (
    QToolButton,
    QFrame,QWidget, QApplication, QMainWindow, QTabWidget, QHBoxLayout, 
    QVBoxLayout, QLabel, QLineEdit, QPushButton, QStackedWidget)
from PyQt5.QtGui import QIcon, QFont, QCursor
from PyQt5.QtCore import Qt, pyqtSignal, QSize
import sys
from venv_Ui import Venv_frame
from terminal import CMDWin

class MainWin(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("main")
        with open("style.css", "r") as f:
            self.setStyleSheet(f.read())
            f.close()
        self.layout = QVBoxLayout()
        self.setupUi()
        self.setLayout(self.layout)
    def setupUi(self):
        """La fonction qui contient tout les composants de la fênetre
        """
        title = QLabel("Python Manager")
        title.setObjectName("title") #cet id permet la stylisation dans le fichier style.css
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial black",18))
        self.layout.addWidget(title)
        
        #La frame pour les buttons des differentes pages
        self.nav = QFrame()
        self.nav.setObjectName("nav")
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(0)
        nav_layout.setContentsMargins(0,0,0,0)
        self.python_btn = QToolButton() #python page switch button
        self.python_btn.setObjectName("python_btn")
        self.python_btn.setIcon(QIcon("img/python-dark.png"))
        self.python_btn.setIconSize(QSize(45,25))
        self.python_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.python_btn.setToolTip("Python")
        self.pip_btn = QToolButton() #pip page switch button
        self.pip_btn.setObjectName("pip_btn")
        self.pip_btn.setIcon(QIcon("img/box-dark.png"))
        self.pip_btn.setIconSize(QSize(45,25))
        self.pip_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pip_btn.setToolTip("PIP")
        self.envir_btn = QToolButton()
        self.envir_btn.setObjectName("envir_btn")
        self.envir_btn.setIcon(QIcon("img/venv.svg"))
        self.envir_btn.setIconSize(QSize(45,25))
        self.envir_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.envir_btn.setToolTip("Venv")
        self.setting_btn = QToolButton() #setting page switch button
        self.setting_btn.setObjectName("setting_btn")
        self.setting_btn.setIcon(QIcon("img/settings-dark.png"))
        self.setting_btn.setIconSize(QSize(45,25))
        self.setting_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setting_btn.setToolTip("Setting")
        nav_layout.addWidget(self.python_btn)
        nav_layout.addWidget(self.pip_btn)
        nav_layout.addWidget(self.envir_btn)
        nav_layout.addWidget(self.setting_btn)
        self.nav.setLayout(nav_layout)
        nav_pos_layout = QHBoxLayout() #Ce layout permet de maintenir le navbar au milieu horizontalement
        nav_pos_layout.addStretch()
        nav_pos_layout.addWidget(self.nav)
        nav_pos_layout.addStretch()

        self.stack = QStackedWidget()
        self.stack.setObjectName("stackWidget")
        self.stack.addWidget(Venv_frame())
        
        self.layout.addLayout(nav_pos_layout)
        self.layout.addWidget(self.stack,2)
        self.layout.addWidget(CMDWin())

        
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setCentralWidget(MainWin())
    win.show()
    sys.exit(app.exec_())