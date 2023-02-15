import logging
import json
from . import sipre
from . import constantes
from . import utils


def estadoSesionyBienvenida(driver, strCaptcha, strUsuario, strPassword):
    response = sipre.iniciarSesion(driver, strCaptcha, strUsuario, strPassword)
    if response["activeSession"]:
        #Case where the init was succesful
        nextState = constantes.BIENVENIDA
        nextState, response = estadoBienvenida(driver)
    else:
        nextState = constantes.ERROR
    return nextState, response
        
def estadoBienvenida(driver):
    response = sipre.moveFromWelcomePageToNSSForm(driver)
    if response["activeSession"]:
        nextState = constantes.INFO_NSS_CURP
    else:
        nextState = constantes.ERROR
    return nextState, response    

def estadoInicio(visible):
    driver =  utils.abreNavegador(not visible)
    if driver != None:
        driver.get(constantes.strURL_Login)
        estado = constantes.SESION    
    else:
        estado = constantes.TERMINA
    return estado, driver

def estadoTermina(driver):
    try:
        driver.quit()
        nextState = constantes.INICIO
        response = {"success" : True}
    except Exception as error:
        nextState = constantes.FINAL
        reponse =  {"Error" : "Requiere reinicio de servidor o servicio"}
    return nextState, response

#revisar con la consutlta de backend getDatosDeConsulta
def estadoError(driver):
    response = None
    nextState = constantes.TERMINA
    try:
        #Si puede recuperarse de alguna inconsistencia, continúa el proceso, sino pide nueva sesion
        if driver.current_url == constantes.strURL_NSSCURP:
            if sipre.goToWelcomeFromNSS_CURP(driver):
                nextState = constantes.INFO_NSS_CURP
        elif driver.current_url == constantes.strURL_RESULT:
            sipre.goToNSS_CURP_form(driver)
            nextState = constantes.INFO_NSS_CURP
        else: 
            response = {"Error": "El sistema no pudo continuar con el proceso de consulta, se reiniciará. Intente de nuevo"}
            nextState = constantes.TERMINA
    except Exception as error:
        logging.error(error)
        response = {"Error": str(error)}
        nextState = constantes.TERMINA
    return nextState, response

def estadoINFO_NSS_CURP(driver, NSS, CURP):
    print(CURP)
    paramJSON = {
                "NSS":      NSS,
                "CURP":     CURP
                }
    response =  sipre.ObtenerDatos(driver, json.dumps(paramJSON))
    
    if "Error" in response:
        nextState = constantes.ERROR
    else:
        nextState = constantes.INFO_NSS_CURP
    
    return nextState, response