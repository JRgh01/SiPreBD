import json
import logging
import mysql.connector

#Abre BD y consulta Persona
#def ObtenerIDPersona(cnxDB, NPer):
def ObtenerIDPersona(cnxDB, NPer):
    try:
        strSQL = "LOCK TABLES Persona WRITE"
        cnxDB.cmd_query(strSQL)

        dbCursor = cnxDB.cursor()  
        #strSQL = "Select ID_Persona, NSS, CURP From Persona Where Proceso = 0 LIMIT " + str(NPer)
        #strSQL = "Select ID_Persona, NSS, CURP From Persona Where ID_Persona = 393 LIMIT " + str(NPer)
        strSQL = "Select ID_Persona, NSS, CURP From Persona Where Proceso = 0 LIMIT 1"
        
        dbCursor.execute(strSQL)
        auxCur = dbCursor
        lisIDPersona = []
        lisNSS = []
        lisCURP = []

        for resultado in auxCur:
            lisIDPersona.append(resultado[0])
            lisNSS.append(resultado[1])
            lisCURP.append(resultado[2])

        dbCursor.close()

        intAux = 0
        for actualizar in lisIDPersona:
            strSQL = "Update Persona Set Proceso = 1 Where ID_Persona = " + str(lisIDPersona[intAux])
            cnxDB.cmd_query(strSQL)
            intAux = intAux + 1

        strSQL = "UNLOCK TABLES"
        cnxDB.cmd_query(strSQL)

        return (lisIDPersona, lisNSS, lisCURP, intAux)

    except mysql.connector.Error as error:
        print("DB subObtenerPersona: ", error)
    except Exception as excep:
        print("subObtenerPersona: ", excep)

#Abre BD y ACTUALIZA Persona
def Actualiza_BD_Persona(cnxDB, IDPer, jsonParam, Fecha):
    try:
        jsonResul = json.loads(jsonParam)
        if "Error" in jsonResul:
            #Si ocurrio un error
            intComent = 0
            strError = jsonResul["Error"]
            if strError[1] == '\n':
                jsonResul["Error"] = strError[2:100]
            intComent = setTablaComentario(cnxDB, IDPer, jsonResul["Error"])
            intProceso = 3
            strSQL = "Update Persona Set Proceso = " + str(intProceso) + ",  ID_Comentario = " + str(intComent) + " Where ID_Persona = " + str(IDPer)            
            cnxDB.cmd_query(strSQL)
        else:
            Prov = 2
            if jsonResul["strTelefono"] != "":
                setTablaTelefono(cnxDB, IDPer, jsonResul["strTelefono"], Prov)

            if jsonResul["strTelefonoMovil"] != "":
                setTablaTelefono(cnxDB, IDPer, jsonResul["strTelefonoMovil"], Prov)
            
            if jsonResul["strCorreo"] != "":
                setTablaCorreo(cnxDB, IDPer, jsonResul["strCorreo"], Prov)

            if jsonResul["strCapacidad"] != "":
                    setTablaCapPago(cnxDB, IDPer, jsonResul["strCapacidad"], Fecha)

            if jsonResul["PrestamosVigentes"] != None:
                intAux = 0
                strParam = ""
                for aux in jsonResul["PrestamosVigentes"]:
                    strParam = jsonResul["PrestamosVigentes"][intAux]["strEntidadFinanciera"] + " - CAT: "
                    strParam = strParam + jsonResul["PrestamosVigentes"][intAux]["strCAT"] + " - Monto: "
                    strParam = strParam + jsonResul["PrestamosVigentes"][intAux]["strMonto"] + " - Descuento: "
                    strParam = strParam + jsonResul["PrestamosVigentes"][intAux]["strDescuento"] + " - Plazo: "
                    strParam = strParam + jsonResul["PrestamosVigentes"][intAux]["strPlazos"] + " - Saldo: "
                    strParam = strParam + jsonResul["PrestamosVigentes"][intAux]["strSaldo"]

                    setTablaPrestamoVig(cnxDB, IDPer, strParam)
                    intAux = intAux + 1
            
            intComent = 0
            intProceso = 2
            strSQL = "Update Persona Set Proceso = " + str(intProceso) + ",  ID_Comentario = " + str(intComent) + " Where ID_Persona = " + str(IDPer)            
            cnxDB.cmd_query(strSQL)
    
    except mysql.connector.Error as error:
        print("DB subActualizaPersona: ", error)
    except Exception as excep:
        print("subActualizaPersona: ", excep)

def setTablaCorreo(cnxDB, IdPer, Correo, Prov):
    curPersona = cnxDB.cursor()
    
    strSQL = "Select ID_Persona, Correo From Correo Where ID_Persona = " + str(IdPer) + " AND Correo = '" + Correo + "'"
    curPersona.execute(strSQL)
    resSQL = curPersona
    idxErr = 0
    for valores in resSQL:
        idxErr  = valores[0]
        break

    if idxErr == 0:
        strINSCorr = "INSERT INTO Correo (ID_Persona, Correo, Procedencia) VALUES ("
        strSQL = strINSCorr + str(IdPer) + ", '" + Correo + "', " + str(Prov) + ")"
        curPersona.execute(strSQL)
    
    curPersona.close()

def setTablaDomicilio(cnxDB, IdPer, Calle, Colonia, DomMun, DomEdo):
    strINSDom = "INSERT INTO Domicilio (ID_Persona, DomCalle, DomColonia, DomMun, DomEdo) VALUES ("
    curPersona = cnxDB.cursor()
    strSQL = strINSDom + str(IdPer) + ", '" + Calle + "', '" + Colonia + "', '" + DomMun + "', '" + DomEdo + "')"
    curPersona.execute(strSQL)
    curPersona.close()

def setTablaTelefono(cnxDB, IdPer, Telefono, Prov):
    curPersona = cnxDB.cursor()
    
    strSQL = "Select ID_Persona, Telefono From Telefono Where ID_Persona = " + str(IdPer) + " AND Telefono = '" + Telefono + "'"
    curPersona.execute(strSQL)
    resSQL = curPersona
    idxErr = 0
    for valores in resSQL:
        idxErr  = valores[0]
        break

    if idxErr == 0:
        strINSTel = "INSERT INTO Telefono (ID_Persona, Telefono, Procedencia) VALUES ("
        strSQL = strINSTel + str(IdPer) + ", '" + Telefono + "', " + str(Prov) + ")"
        curPersona.execute(strSQL)
    
    curPersona.close()

def setTablaCapPago(cnxDB, IdPer, Monto, Fecha):
    curPersona = cnxDB.cursor()
    
    strSQL = "Select ID_Persona, Monto From CapacidadPago Where ID_Persona = " + str(IdPer) + " AND Monto = '" + str(Monto) + "'"
    curPersona.execute(strSQL)
    resSQL = curPersona
    idxErr = 0
    for valores in resSQL:
        idxErr  = valores[0]
        break

    if idxErr == 0:
        strSQL = "INSERT INTO CapacidadPago (ID_Persona, Monto, Fecha) VALUES ("
        strSQL = strSQL + str(IdPer) + ", '" + str(Monto) + "', '" + Fecha + "')"
        curPersona.execute(strSQL)

    curPersona.close()

def setTablaPrestamoVig(cnxDB, IdPer, PreVig):
    curPersona = cnxDB.cursor()
    
    strSQL = "Select ID_Persona, PrestamoVig From PrestamoVig Where ID_Persona = " + str(IdPer) + " AND PrestamoVig = '" + PreVig + "'"
    curPersona.execute(strSQL)
    resSQL = curPersona
    idxErr = 0
    for valores in resSQL:
        idxErr  = valores[0]
        break

    if idxErr == 0:
        strINSCapP = "INSERT INTO PrestamoVig (ID_Persona, PrestamoVig) VALUES ("
        strSQL = strINSCapP + str(IdPer) + ", '" + PreVig + "')"
        curPersona.execute(strSQL)

    curPersona.close()

def setTablaComentario(cnxDB, IdPer, strError):
    curPersona = cnxDB.cursor()
    
    intLargo = len(strError)
    strSQL = "Select ID_Comentario, Comentario From Comentario Where Comentario = '" + strError + "'"
    curPersona.execute(strSQL)
    resSQL = curPersona
    idxErr = 0
    for valores in resSQL:
        idxErr  = valores[0]
        break
    
    if idxErr == 0:
        strSQL = "Insert into Comentario (Comentario) Values ('" + strError + "')"
        curPersona.execute(strSQL)
        idxErr = 0
        idxErr = curPersona.lastrowid

    curPersona.close()

    return(idxErr)
