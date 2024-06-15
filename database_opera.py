import sqlite3

class Db_insertion:
    def __init__(self,venv,path,version):
        print("Insertion des données")
        self.venv = venv
        self.path = path
        self.version = version
        conn = sqlite3.connect("databases/venv.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO venvs VALUES(?,?,?)",(self.venv,self.path,self.version))
        conn.commit()
        conn.close()
        
class Db_deletion:
    def __init__(self,table):
        print("Suppression des données")
        self.table = table
        conn = sqlite3.connect("databases/venv.db")
        cur = conn.cursor()
        cur.execute(f"DELETE FROM {self.table}")
        conn.commit()
        conn.close()
        
class Data_collection:
    def __init__(self):
        print("Data Collection")
        conn = sqlite3.connect("databases/venv.db")
        cur = conn.cursor()
        req = "SELECT * FROM venvs"
        self.data = cur.execute(req)
        self.data = self.data.fetchall()
        conn.commit()
        conn.close()
    def data_result(self):
        return self.data