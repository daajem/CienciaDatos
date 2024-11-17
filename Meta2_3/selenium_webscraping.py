#Daniel Jimenez Manrique 382
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#Configurar el chromedriver
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')

#Ruta del chromedriver
driver_path = 'C:\\Users\\Dell\\Desktop\\Ciencia_Datos\\Selenium\\chromedriver-win64\\chromedriver.exe'
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

#Abrir el navegador para ir a amazon
driver.get('https://www.amazon.com')


search_box = driver.find_element(By.ID, 'twotabsearchtextbox')
search_box.send_keys('laptop' + Keys.RETURN) #Buscar la palabra clave en amazon


num_paginas = 2 #El numero de paginas que se quieren ver

for _ in range(num_paginas):
    #Esperar a que se carguen los resultados
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.s-main-slot'))
    )

    #Obtener los nombresde los productos 
    productos = driver.find_elements(By.CSS_SELECTOR, '.s-main-slot .s-title')
    for producto in productos:
        print(producto.text)

    
    try: #Ir a la siguiente pagina
        siguiente_btn = driver.find_element(By.CSS_SELECTOR, '.s-pagination-next')
        siguiente_btn.click()
    except:
        print("No hay más páginas.")
        break

