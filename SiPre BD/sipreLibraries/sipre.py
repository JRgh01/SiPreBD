from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
import json
import logging
from . import utils
from . import constantes

def pideImgDeCaptcha(driver):
    response = None
    try:
        id_Sesion = 5
        strCaptcha =  utils.encontrarControlByXPath(driver, constantes.strImgCaptcha)
        if strCaptcha != None:
            jasonCap = {
                "url": strCaptcha.get_attribute("src"),
                "id": id_Sesion
            }
        else:
            jasonCap = {
                "Error": "Sin CAPTCHA",
                "id": id_Sesion
            }
        response = jasonCap
    except Exception as error:
        logging.error(error)
        response = {"error": error}
    return response

def moveFromWelcomePageToNSSForm(driver):
    inputErr = utils.encontrarControlByXPath(driver,constantes.strXpathError)
    if inputErr == None:                
        navMenu = utils.encontrarControlByXPath(driver, constantes.strXpathMenu)
        if navMenu != None:
            response = {"activeSession": True}
            goToNSS_CURP_form(driver)
        else:
            response = {
                "activeSession": False,
                "Error": "No se encontró el objeto navMenu"
                }
    else:
        response = {"activeSession": True}
    return response

#AGREGAR LA RUTA DE BIENVENIDA SI ES CORRECTO
def checkCorrectLogin(driver):
    if driver.current_url[:49] == constantes.strURL_Login:
        driver.get(constantes.strURL_Login)
        result = False
    else:
        result = True
    return result
    
def iniciarSesion(driver, strCaptcha, strUsuario, strPassword):
    response = None
    try:
        inputUser = utils.encontrarControlByXPath(driver,constantes.strXpathUsr)
        if inputUser != None:
            inputUser.clear()            
            inputUser.send_keys(strUsuario)

        inputPswd = utils.encontrarControlByXPath(driver,constantes.strXpathPswd)        
        if inputPswd != None:        
            inputPswd.clear()            
            inputPswd.send_keys(strPassword)

        inputCaptcha = utils.encontrarControlByXPath(driver,constantes.strXpathCaptcha)        
        if inputCaptcha != None:                
            inputCaptcha.clear()
            inputCaptcha.send_keys(strCaptcha)
            inputCaptcha.send_keys(Keys.ENTER)

        time.sleep (3)
        response = {"activeSession": checkCorrectLogin(driver)} 
        
    except Exception as error:
        logging.error(error)
        response = {
            "activeSession": False,
            "Error": str(error)
        }
    return response

"""
The next function surfs to the nss page using the navmenu, is it think to use it when you have the menu in that page
"""
def goToNSS_CURP_form(driver):
    navMenu = utils.encontrarControlByXPath(driver, constantes.strXpathMenu)
    navMenu.click()
    navPrestamos = utils.encontrarControlByXPath(driver,constantes.strXpathPrestamos)
    navPrestamos.click()

def goToWelcomeFromNSS_CURP(driver):
    btnRegresar = utils.encontrarControlByXPath(driver,constantes.strBtnRegresar)
    response = False
    if btnRegresar != None:
        btnRegresar.send_keys(Keys.ENTER)
        response = True
        #JR
        response = moveFromWelcomePageToNSSForm(driver)

    return response

def ObtenerDatos(driver, paramJSON):
    response = None
    try:
        strParam = json.loads(paramJSON)
        NSS = strParam["NSS"]
        CURP = strParam["CURP"]

        wait = WebDriverWait(driver, 20)        
        
        """
        if driver.current_url == constantes.strURL_RESULT:
            clickMenu(driver,wait) # cambiar por goToNSS_CURP_form
            navPrestamos = utils.encontrarControlByXPath(driver, constantes.strXpathPrestamos)
            navPrestamos.click()
        elif driver.current_url != constantes.strURL_NSSCURP:
            goToNSS_CURP_form(driver)
        """
        
        strError, strURLNavegacion = fillNSS_CURP_AndClick(driver, NSS, CURP)
        
        
        if strURLNavegacion == "":
                jsonPersona = { "Error": strError }
        elif strURLNavegacion == constantes.strURL_RESULT:
            #escribir a db con objeto jsonPersona
            jsonPersona = getDatosFromConsulta(driver,wait)
            goToNSS_CURP_form(driver)
        response = jsonPersona

    except Exception as error:
        logging.error(error)
        response = { "Error": str(error)}
    return response

def fillNSS_CURP_AndClick(driver, NSS, CURP):
    strError = ""
    strUrl=""

    try:
        inputCurp = utils.encontrarControlByXPath(driver, constantes.strXpathCurp)
        if inputCurp != None:
            inputCurp.clear()
            #inputCurp = utils.encontrarControlByXPath(driver,strXpathCurp)
            inputCurp.send_keys(CURP)

        
        inputNss = utils.encontrarControlByXPath(driver, constantes.strXpathNss)        
        if inputNss != None:
            inputNss.clear()
            #inputNss = utils.encontrarControlByXPath(driver,strXpathNss)
            inputNss.send_keys(NSS)
        time.sleep(1)
        
        #Cambio versión JR  21-Ene-2023
        btnContinuar = utils.encontrarControlByXPath(driver, constantes.strBtnContinua)        
        if btnContinuar.is_enabled():
            btnContinuar.send_keys(Keys.ENTER)
    
        time.sleep(2)

        if driver.current_url == constantes.strURL_RESULT:
            strUrl = constantes.strURL_RESULT
        else:
            objError = utils.encontrarControlByXPath(driver, constantes.strMensajeError)
            if objError != None:
                strError = objError.text
            elif driver.current_url == constantes.strURL_RESULT:
                strUrl = constantes.strURL_RESULT
            else:    
                strError ="No se realizó la consulta, intente nuevamente"
    except Exception as error:
        strError = str(error)
        logging.error(error)
        
    return strError,strUrl

#revisar la siguiente
def getDatosFromConsulta(driver,wait):
    response = None
    try:
        strNombre = ''
        strCapacidad = ''
        strTelefono=''
        strTelefonomovil=''
        strCorreo=''

        objName = utils.encontrarControlByXPath(driver,constantes.strPathName)
        if objName != None:
            strNombre = objName.text

        objCapacidad = utils.encontrarControlByXPath(driver,constantes.strPathCapacidad)
        if objCapacidad != None:
            strCapacidad = objCapacidad.text

        objTelefono = utils.encontrarControlByXPath(driver, constantes.strPathTelefono)
        if objTelefono != None:
            strTelefono = objTelefono.get_attribute('value')

        objTelefonoMovil = utils.encontrarControlByXPath(driver, constantes.strPathTelefonoMovil)
        if objTelefonoMovil != None:
            strTelefonomovil = objTelefonoMovil.get_attribute('value')

        objCorreo = utils.encontrarControlByXPath(driver, constantes.strPathCorreo)
        if objCorreo != None:
            strCorreo = str( objCorreo.get_attribute('value'))

        intPosicionPrestamos = 1
        objPrestamos = 'valida'
        strPrestamos = ''
        strPathPrestamos = '/html/body/main/app-root/div/div/div/app-registrar-prestamo-editar/form/app-prestamos-vigentes/div[' + str(intPosicionPrestamos)+']'
        strFinanciera = []
        strCAT= []
        strMonto=[]
        strDescuento=[]
        strPlazos=[]
        strSaldo=[]
        objPrestamos = utils.encontrarControlByXPath(driver,strPathPrestamos)

        while objPrestamos != None:
            if objPrestamos.text == 'No cuentas con préstamos vigentes.':
                break            
            else:
                strPathFinanciera = '/html/body/main/app-root/div/div/div/app-registrar-prestamo-editar/form/app-prestamos-vigentes/div[' + str(intPosicionPrestamos)+']/div/div/div[1]/div[1]'
                objFinanciera = utils.encontrarControlByXPath(driver,strPathFinanciera)
                if objFinanciera != None:
                    strFinanciera.append(objFinanciera.text)

                strPathCAT = '/html/body/main/app-root/div/div/div/app-registrar-prestamo-editar/form/app-prestamos-vigentes/div[' + str(intPosicionPrestamos)+']/div/div/div[3]/div[1]'
                objCAT = utils.encontrarControlByXPath(driver,strPathCAT)
                if objCAT != None:
                    strCAT.append(objCAT.text)

                strPathMonto = '/html/body/main/app-root/div/div/div/app-registrar-prestamo-editar/form/app-prestamos-vigentes/div[' + str(intPosicionPrestamos)+']/div/div/div[3]/div[2]'
                objMonto = utils.encontrarControlByXPath(driver,strPathMonto)
                if objMonto != None:
                    strMonto.append(objMonto.text)

                strPathDescuento = '/html/body/main/app-root/div/div/div/app-registrar-prestamo-editar/form/app-prestamos-vigentes/div[' + str(intPosicionPrestamos)+']/div/div/div[3]/div[3]'
                objDescuento = utils.encontrarControlByXPath(driver,strPathDescuento)
                if objDescuento != None:
                    strDescuento.append(objDescuento.text)

                strPathPlazos = '/html/body/main/app-root/div/div/div/app-registrar-prestamo-editar/form/app-prestamos-vigentes/div[' + str(intPosicionPrestamos)+']/div/div/div[3]/div[4]'
                objPlazos = utils.encontrarControlByXPath(driver,strPathPlazos)
                if objPlazos != None:
                    strPlazos.append(objPlazos.text)

                strPathSaldo = '/html/body/main/app-root/div/div/div/app-registrar-prestamo-editar/form/app-prestamos-vigentes/div[' + str(intPosicionPrestamos)+']/div/div/div[3]/div[5]'
                objSaldo = utils.encontrarControlByXPath(driver,strPathSaldo)
                if objSaldo != None:
                    strSaldo.append(objSaldo.text)

                intPosicionPrestamos = intPosicionPrestamos + 1

                strPathPrestamos = '/html/body/main/app-root/div/div/div/app-registrar-prestamo-editar/form/app-prestamos-vigentes/div[' + str(intPosicionPrestamos)+']'
                objPrestamos = utils.encontrarControlByXPath(driver,strPathPrestamos)
                if objPrestamos == None or objPrestamos.text == 'No cuentas con préstamos vigentes.':
                    objPrestamos = None

        data = {
            "strNombre": strNombre,
            "strCapacidad": strCapacidad,
            "strTelefono": strTelefono,
            "strTelefonoMovil":strTelefonomovil,
            "strCorreo":strCorreo,
            "PrestamosVigentes":[]
        }

        for intFila in range(0, len(strSaldo)):
            data["PrestamosVigentes"].append({
                "strEntidadFinanciera": strFinanciera[intFila],
                "strCAT": strCAT[intFila],
                "strMonto": strMonto[intFila],
                "strDescuento": strDescuento[intFila],
                "strPlazos": strPlazos[intFila],
                "strSaldo": strSaldo[intFila]
            })

        navMenu = None
        strXpathMenu = '//*[@id="subenlaces"]/ul/li[2]'

        navMenu = utils.encontrarControlByXPath(driver,strXpathMenu)
        if navMenu != None:
            navMenu.click()
            strXpathPrestamos = '//*[@id="subenlaces"]/ul/li[2]/ul/li[2]'
            navPrestamos = utils.encontrarControlByXPath(driver,strXpathPrestamos)        
            if navPrestamos != None:
                navPrestamos.click()

        response = data
    except Exception as error:
        logging.error(error)
        response = {"error": str(error)}
    return response
