INICIO = 1
SESION = 2
BIENVENIDA = 7
INFO_NSS_CURP = 3
RESULTS = 8
ERROR = 4
TERMINA = 5
FINAL = 6

strURL_Login = "https://mclprestamos.imss.gob.mx/mclpe/auth/login"
strURL_RESULT = "https://mclprestamos.imss.gob.mx/mclpe/promotor/registroPrestamoEditar"
strURL_NSSCURP = "https://mclprestamos.imss.gob.mx/mclpe/promotor/registroPrestamo"

#LOGIN PAGE
strXpathUsr = '/html/body/main/app-root/div/div/div/app-login/div[1]/div[2]/form/div[2]/div[1]/div/input'
strXpathPswd = '/html/body/main/app-root/div/div/div/app-login/div[1]/div[2]/form/div[2]/div[2]/div/input'
strXpathCaptcha = '/html/body/main/app-root/div/div/div/app-login/div[1]/div[2]/form/div[2]/div[5]/div/input'
strImgCaptcha = '/html/body/main/app-root/div/div/div/app-login/div[1]/div[2]/form/div[2]/div[4]/div[2]/img'

#WELCOME PAGE
strXpathError = '/html/body/main/app-root/div/div/div/app-login/div[1]/div[2]/form/div[2]/div[5]/div/div[2]'
strXpathMenu = '//*[@id="subenlaces"]/ul'


#CURP_NSS PAGE
strXpathCurp= '/html/body/main/app-root/div/div/div/app-registrar-prestamo/form/div[2]/div[1]/input'
strXpathNss= '/html/body/main/app-root/div/div/div/app-registrar-prestamo/form/div[2]/div[2]/input'
strBtnRegresar = '/html/body/main/app-root/div/div/div/app-registrar-prestamo/form/div[3]/div[2]/div/button[1]'
strBtnContinua = '/html/body/main/app-root/div/div/div/app-registrar-prestamo/form/div[3]/div[2]/div/button[2]'
strMensajeError = '/html/body/main/app-root/div/div/div/app-alertas[1]/div/div/div/div'

#RESULT PAGE
strPathName = "/html/body/main/app-root/div/div/div/app-registrar-prestamo-editar/form/div[1]/div[2]/div[2]/div[1]/label"
strPathCapacidad = '/html/body/main/app-root/div/div/div/app-registrar-prestamo-editar/form/div[3]/label[1]/strong'
strPathTelefono = '/html/body/main/app-root/div/div/div/app-registrar-prestamo-editar/form/div[1]/div[2]/div[3]/div[2]/div[2]/input'
strPathTelefonoMovil = '/html/body/main/app-root/div/div/div/app-registrar-prestamo-editar/form/div[1]/div[2]/div[3]/div[2]/div[3]/input'
strPathCorreo = '/html/body/main/app-root/div/div/div/app-registrar-prestamo-editar/form/div[1]/div[2]/div[3]/div[4]/div[1]/input'
strXpathPrestamos = '//*[@id="subenlaces"]/ul/li[2]/ul/li[2]'