from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from webdriver_manager.utils import ChromeType
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from chromedriver_py import binary_path # this will get you the path variable
import time
import logging
from datetime import datetime

def getFechaHoy():
    fecha_hoy = datetime.now()
    strFecHoy = str(fecha_hoy.year) + "-" + str(fecha_hoy.month) + "-" + str(fecha_hoy.day)
    return (strFecHoy)

def abreNavegador(isServer):
    driver = None
    try:

        if isServer:
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox") 
            options.add_argument("--remote-debugging-port=9222")  # this
            options.add_argument("--disable-dev-shm-using") 
            print(binary_path)
            #driver = webdriver.Chrome(options=options, executable_path='/home/jose_reyes/.wdm/drivers/chromedriver/linux64/109.0.5414.74/chromedriver')
            driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
        else:    
            chromedriver = ChromeDriverManager(chrome_type=ChromeType.GOOGLE, 
                                            log_level='0', 
                                            print_first_line=False).install()
            driver = webdriver.Chrome(chromedriver, service_log_path=None)

        #strURL='https://mclprestamos.imss.gob.mx/mclpe/auth/login'        
        wait = WebDriverWait(driver, 20)
        #driver.get(strURL)
    except Exception as error:
        logging.error(error)
    return driver

def encontrarControlByXPath(driver,selector):
    # COntrol vars
    #selector = ""
    time_out = 5
        
    # Seconds counter
    total_time = 0
    elem = None
    # Main loop for get element
    while True: 

        # Valide time
        if total_time < time_out: 
            total_time += 1

            # Catch error to get text
            try: 
                elem = driver.find_element_by_xpath (selector)
                #link = driver.find_element_by_xpath("//*[@id='add-to-cart-or-refresh']/div[2]/div/div[2]/button")
                elem.text
                break
            except:

                # Wait time
                time.sleep (1) 
                continue
        # Raise and error when time exceeds the limit
        else: 
            #raise Exception ("Time out exeded. The element {} is not in the page".format (selector))
             break
    
    return (elem)

def encontrarControlByClassName(driver,selector):
    # COntrol vars
    #selector = ""
    time_out = 10
        
    # Seconds counter
    total_time = 0

    # Main loop for get element
    while True: 

        # Valide time
        if total_time < time_out: 
            total_time += 1

            # Catch error to get text
            try: 
                elem = driver.find_elements_by_class_name (selector)
                
                break
            except:

                # Wait time
                time.sleep (1) 
                continue
        # Raise and error when time exceeds the limit
        else: 
            raise Exception ("Time out exeded. The element {} is not in the page".format (selector))
    
    return (elem)

