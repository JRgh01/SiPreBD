import sipreLibraries.constantes as constantes
import sipreLibraries.estados as estados
import sipreLibraries.sipre as sipre
import sipreLibraries.utils as utils                #JR
import sipreLibraries.utilsBD as utilsBD            #JR
import sipreLibraries.datosBD as datosBD            #JR
import json

#Rutina Principal
try:
    driver = None
    cnxDB = None
    lisIDPersona = []
    lisNSS = []
    lisCURP = [] 
    intReg = 0
    strCaptcha = ""
    estado = constantes.INICIO
    intNumProc = 0
    while estado != constantes.FINAL:
        if estado == constantes.INFO_NSS_CURP:
            intNumProc = intNumProc + 1
            #Prepara registro de persona a consultar            
            lisIDPersona, lisNSS, lisCURP, intReg = datosBD.ObtenerIDPersona(cnxDB, 1)            
            if intReg > 0:
                estado, response = estados.estadoINFO_NSS_CURP(driver, lisNSS[intReg-1], lisCURP[intReg-1])
                if response != None or response != "":
                    
                    datosBD.Actualiza_BD_Persona(cnxDB, lisIDPersona[0], json.dumps(response), strFecha)
            else:
                estado = constantes.TERMINA

        elif estado == constantes.TERMINA:
            estado = constantes.FINAL
            utilsBD.CierraBD(cnxDB)
            print("Termina Proceso ... Llevo: ", intNumProc)

        elif estado == constantes.INICIO:
            visibleActual = True
            estado, driver = estados.estadoInicio(visible = visibleActual)
            response = json.dumps({"Error": "No existia captcha, favor de solicitar primero el CAPTCHA"})
            reintentar = False
            jsonDB = {
                "Usuario": "root",
                "Password": "",
                "Host": "127.0.0.1",
                "DB": "SiPre"
            }
            cnxDB = utilsBD.AbreBD(json.dumps(jsonDB))
            if cnxDB == None:
                estado = constantes.TERMINA
            #Falta checar el estado
            strFecha = utils.getFechaHoy()
        elif estado == constantes.SESION:
            strCaptcha = ""
            while strCaptcha == "" or len(strCaptcha) != 7:
                strCaptcha = input('Favor de teclear el CAPTCHA (7 caracteres): ')
            estado, response = estados.estadoSesionyBienvenida(driver, strCaptcha, "fernando.salazar.cue@gmail.com", "Viraal2023**")
            print("Llevo: ", intNumProc-1)
        elif  estado == constantes.ERROR:
            estado, response = estados.estadoError(driver)
            response = json.dumps(response)
        else:
            print("ESTATUS: ", estado)
            estado = constantes.TERMINA

except Exception as error:
    print(error)
