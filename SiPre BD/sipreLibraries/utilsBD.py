import mysql.connector
import json
import logging

def AbreBD (jsonParam):
    try:        
        jsonDB = json.loads(jsonParam)
        strUser = jsonDB["Usuario"]
        strPass = jsonDB["Password"]
        strHost = jsonDB["Host"]
        strDB = jsonDB["DB"]
#        cnxDB = mysql.connector.connect(user='root', password='',
#                                        host='127.0.0.1',
#                                        database='base2')
        cnxDB = mysql.connector.connect(user     = strUser,
                                        password = strPass,
                                        host     = strHost,
                                        database = strDB)

        return cnxDB
    except mysql.connector.Error as error:
        logging.error("DB AbreBD: ", error)
    except Exception as excep:
        logging.error("AbreBD: ", excep)

def CierraBD (cnxDB):
    try:        
        cnxDB.commit()
        cnxDB.close()
    except mysql.connector.Error as error:
        logging.error("DB CierraBD: ", error)
    except Exception as excep:
        logging.error("CierraBD: ", excep)
 