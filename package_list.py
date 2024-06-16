import subprocess
import sqlite3
import os
import getpass
import socket

# Chemin vers l'environnement virtuel
virtual_env_path = "D:/python_manager/venv"

class Packages:
    """
    Cette classe sert à recupérer les packages installés dans un envrrionnement virtuel.\n
    Elle prend en paramètre le chemin d'accès de l'environnement virtuel.\n
    On instanciéra cette classe dans la fonction 'print_widget_position' de la classe 'Venv' du fichier 'venv_Ui.py'.\n
    La fonction 'print_widget_position' est utiliser comme slot du button 'self.eye_btn' de sa classe.\n
    La fonction la fonction 'data' de cette classe (Packages)  retournera une liste des listes contenant le nom et la version de chaque packages installé dans l'environnement virtuel.\n
    Sa valeur de retour sera utilisée pour alimenter le tableau 'self.tableau' de la classe 'Venv_details' du fichier 'venv_Ui.py'.\n
    """
    def __init__(self,path, table):
        super().__init__()
        self.path = path
        if "-" in table:
            self.table = table.split("-")[0]
        else:
            self.table = table
        self.data_list = []
        self.my_data = []
        # Commande pour lister les packages installés dans l'environnement virtuel
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Changer le répertoire de travail
            os.chdir(current_dir)
            conn = sqlite3.connect("databases/venv.db")
            cur = conn.cursor()
            self.my_data = cur.execute(f"SELECT * FROM {self.table}").fetchall()
            conn.commit()
            conn.close()
        except:
            os.chdir(os.path.expanduser('~'))
            command = f"{self.path}/Scripts"
            with open(f"{command}/activate.bat",'r+') as f:
                if "pip list" not in f.readlines():
                    f.write("\npip list") #Ajout de la commande 'pip list dans le script activate de l'environnement pour lister les packages
                    f.close()
                else:
                    pass

            final_command = f"{command}/activate"

            # Exécution de la commande
            result = subprocess.run(final_command, shell=True, capture_output=True, text=True)
            # Affichage de la liste des packages
            result_splitted = result.stdout.split()
            
            for i in range(0,len(result_splitted),2):
                self.data_list.append(result_splitted[i-2:i])
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Changer le répertoire de travail
            os.chdir(current_dir)
            conn = sqlite3.connect("databases/venv.db")
            cur = conn.cursor()
            cur.execute(f"""CREATE TABLE IF NOT EXISTS {self.table} (
                        package TEXT,
                        version TEXT);
                        """)
            for d in self.data_list:
                if len(d) == 2:
                    cur.execute(f"INSERT INTO {self.table} (package, version) VALUES(?,?)",d)
            conn.commit()
            conn.close()

    def data(self):
        if len(self.my_data) != 0:
            return self.my_data
        else:
            return self.data_list