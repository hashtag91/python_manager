import subprocess
import sys
import sqlite3

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
    def __init__(self,path):
        super().__init__()
        self.path = path
        # Commande pour lister les packages installés dans l'environnement virtuel
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
        self.data_list = []
        
        for i in range(0,len(result_splitted),2):
            self.data_list.append(result_splitted[i-2:i])
    def data(self):
        return self.data_list