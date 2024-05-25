import os
import sqlite3

def find_virtual_envs():
    virtual_envs = {}
    # Récupérer le répertoire personnel de l'utilisateur
    home_dir = os.path.expanduser("~")
    # Parcourir les répertoires pour rechercher les environnements virtuels
    for root, dirs, files in os.walk(home_dir):
        #root: contient le chemin du dossier courant
        #dirs: contient le nom des sous-dossiers du dossier courant
        #files: contient les fichiers du dossier courant
        for dir in dirs:
            #Vérifier s'il y a un dossier du nom de "Scripts" et qui contient un fichier "activate"
            #pour s'assurer qu'il s'agit d'un environnement virtuel
            if dir == "Scripts" and "activate" in os.listdir(os.path.join(root, dir)):
                root_path = root.replace('\\','/')
                #Splitter le chemin pour extraire le nom de l'environnement virtuel
                #Stocker un dict key=venv_name value=venvpath
                virtual_envs[root_path.split("/")[-1]] = root_path
    return virtual_envs

def read_cfg(path):
    if "pyvenv.cfg" in os.listdir(path):
        with open(f"{path}/pyvenv.cfg") as f:
            lignes = f.readlines()[2]
            words = lignes.split(" ")
            version = words[-1].split(".")[0:3]
            return ".".join(version)
    else:
        return "N/A"

class Venv_found:
    def __init__(self):
        envs = find_virtual_envs()
        self.venvs_dict = {}
        Db_deletion("./databases/venv.db",'venvs')
        if envs:
            for env,path in envs.items():
                version = read_cfg(path)
                self.venvs_dict[env] = list((path,version))
                Db_insertion(env,path,version)
    def data_return(self):
        return self.venvs_dict

class Db_insertion:
    def __init__(self,venv,path,version):
        self.venv = venv
        self.path = path
        self.version = version
        conn = sqlite3.connect("databases/venv.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO venvs VALUES(?,?,?)",(self.venv,self.path,self.version))
        conn.commit()
        conn.close()
        
class Db_deletion:
    def __init__(self,db,table):
        self.db = db
        self.table = table
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()
        cur.execute(f"DELETE FROM {self.table}")
        conn.commit()
        conn.close()
        
class Data_collection:
    def __init__(self):
        conn = sqlite3.connect("./databases/venv.db")
        cur = conn.cursor()
        req = "SELECT * FROM venvs"
        self.data = cur.execute(req)
        self.data = self.data.fetchall()
        conn.commit()
        conn.close()
    def data_result(self):
        return self.data