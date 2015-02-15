__author__ = 'Youcef'
import sqlite3 as lite
import sys,re
class DBHandler:
    connect = None
    db = None

    def __init__(self,database):
        self.db = database

    def getFromTable(self,table,attribute=None,condition=None):
        try:
            cur = self.connect.cursor()
            request = 'SELECT '
            if attribute: request += attribute
            else : request += '* '
            request +=  ' FROM '+table
            if condition: request += ' WHERE '+condition
            cur.execute(request)
            return cur.fetchall()
        except Exception as exception :
            print("#Error : %s " % exception.args[0])
            sys.exit(1)

    def execute(self,query):
        try:
            cur = self.connect.cursor()
            cur.execute(query)
            self.connect.commit()
            return cur.fetchall()
        except Exception as exception :
            print("#Error : %s " % exception.args[0])
            sys.exit(1)

    def updateRow(self,table,values,condition=None):
        try:
            cur = self.connect.cursor()
            query = 'UPDATE '+table+' SET '+','.join(values)
            if condition : query += ' WHERE '+condition
            cur.execute(query)
            self.connect.commit()
        except Exception as exception :
            print("#Error : %s " % exception.args[0])
            sys.exit(1)

    def insertIntoTable(self,table,data):
        cur = self.connect.cursor()
        val = '('
        cur.execute('PRAGMA table_info('+table+')')
        rows = cur.fetchall()
        l = len(rows)
        i = 0
        for r in rows:
            if i > 0:
                if i != l-1: val += r[1]+','
                else : val += r[1]+')'
            i+=1
        for tuple in data:
            try: cur.execute('INSERT INTO '+table+val+ " VALUES('"+tuple[0]+"','"+str(tuple[1])+"');")
            except Exception as exception : print("#Error : %s " % exception.args[0] + " => VALUES('"+tuple[0]+"','"+str(tuple[1])+"');")

        self.connect.commit()
    """
    def insertIntoTable(self,table,data):
        cur = self.connect.cursor()
        val = '('
        cur.execute('PRAGMA table_info('+table+')')
        rows = cur.fetchall()
        l = len(rows)
        i = 0
        for r in rows:
            if i > 0:
                if i != l-1: val += r[1]+','
                else : val += r[1]+')'
            i+=1
        l = len(data[0])
        for tuple in data:
            valide = True
            a =  'VALUES('
            i = 0
            for v in tuple:
                if v == "":
                    valide = False
                    break
                else :
                    ### Pour le netoyage des chaine de caractére
                    if type(v)==str : v =  re.sub("[\d|\{|\}|\(|\)|\-|\[|\]|\?|\؟|\!|\"|\']", "", v)
                    ###
                    if i != l-1: a+= "'"+str(v)+"',"
                    else : a+= "'"+str(v)+"')"
                    i+=1
            if valide == True:
                try: cur.execute('INSERT INTO '+table+val+ " "+a+";")
                except Exception as exception : print("#Error : %s " % exception.args[0] + " => " + a)
        self.connect.commit()
    """
    def updateOrinsert(self,table,exist_condition,attributes,values,set):
        if self.exist(table,exist_condition):
            self.updateRow(table,values,condition=None)

    #Vérifié si il existe et il le retourne

    def SelectOne(self,table,condition,attribute=None):
        try:
            cur = self.connect.cursor()
            request = 'SELECT '
            if attribute: request += attribute
            else : request += '* '
            request +=  ' FROM '+table
            request += ' WHERE '+condition
            cur.execute(request)
            return cur.fetchone()
        except Exception as exception :
            print("#Error : %s " % exception.args[0])
            sys.exit(1)

    def exist(self,table,condition):
        try:
            cur = self.connect.cursor()
            cur.execute('SELECT * FROM '+table+' WHERE '+condition)
            data = cur.fetchone()
            if data : return True
            else : return False
        except Exception as exception :
            print("#Error : %s " % exception.args[0])
            sys.exit(1)

    def connect(self):
        try:
            self.connect = lite.connect(self.db)
            #self.connect.row_factory = lite.Row
        except Exception as exception :
            print("#Error : %s " % exception.args[0])
            sys.exit(1)

    def close(self):
        if self.connect : self.connect.close()
        else : print("Cette connexion n'existe pas.")
