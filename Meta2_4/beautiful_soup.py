#Daniel Jimenez Manrique
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import time

# Configurar opciones de Chrome
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-infobars')

# Ruta al chromedriver
driver_path = 'C:\\Users\\Dell\\Desktop\\Ciencia_Datos\\Selenium\\chromedriver-win64\\chromedriver.exe'

# Crear un objeto Service con la ruta del driver
service = Service(driver_path)

# Iniciar el navegador con las opciones y el servicio
driver = webdriver.Chrome(service=service, options=options)

# Lista para almacenar los resultados
productos = []

try:
    # Abrir el sitio de Amazon
    driver.get('https://www.amazon.com.mx')

    # Esperar hasta que el input sea clickable y enviar el texto 'proteina'
    search_box = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input#twotabsearchtextbox'))
    )
    search_box.send_keys('proteina')
    
    # Simular la presión de la tecla Enter
    search_box.send_keys(Keys.RETURN)

    # Navegar entre 5 páginas
    for page in range(5):  # Cambia a 5 para navegar por 5 páginas
        # Esperar un poco para que se carguen los resultados
        time.sleep(5)

        # Obtener el HTML de la página cargada
        page_source = driver.page_source

        # Usar BeautifulSoup para procesar el HTML
        soup = BeautifulSoup(page_source, 'html.parser')

        # Extraer los resultados de búsqueda usando BeautifulSoup
        results = soup.select('span.a-size-medium')

        # Guardar los resultados en la lista de productos
        for result in results:
            productos.append(result.text)

        # Intentar ir a la siguiente página usando el enlace "Siguiente"
        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.s-pagination-next'))
            )
            next_button.click()
        except Exception as e:
            print("No se pudo ir a la siguiente página:", e)
            break

finally:
    driver.quit()

# Crear un DataFrame con los resultados
df = pd.DataFrame(productos, columns=['Producto'])

# Guardar el DataFrame en un archivo CSV
df.to_csv('productos_amazon.csv', index=False, encoding='utf-8')

print("Archivo CSV creado exitosamente.")
