from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

def amazon_scraper(search_query, num_pages):
    # Configurar el chromedriver
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    driver_path = 'C:/Users/jimen/Document/GitHub/CienciaDatos/chromedriver/chromedriver.exe'
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    driver.get('https://www.amazon.com')
    search_box = driver.find_element(By.ID, 'twotabsearchtextbox')
    search_box.send_keys(search_query + Keys.RETURN)

    data = []

    for page in range(num_pages):
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.s-main-slot'))
            )
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            results = soup.select('.s-main-slot .s-result-item')

            for result in results:
                name = result.select_one('.a-text-normal')
                price = result.select_one('.a-price .a-offscreen')
                delivery = result.select_one('.a-text-bold + span')
                rating = result.select_one('.a-icon-alt')

                product_name = name.text.strip() if name else 'Producto desconocido'
                product_price = price.text.strip() if price else 'Precio no disponible'
                product_delivery = delivery.text.strip() if delivery else 'Fecha de entrega no disponible'
                product_rating = rating.text.split(' ')[0] if rating else 'Rating no disponible'

                data.append({
                    'Nombre': product_name,
                    'Precio': product_price,
                    'Fecha de entrega': product_delivery,
                    'Rating': product_rating
                })

            next_btn = driver.find_element(By.CSS_SELECTOR, '.s-pagination-next')
            next_btn.click()
            time.sleep(2)

        except Exception as e:
            print(f"No se pudo procesar la página {page + 1}: {e}")
            break

    # Cerrar el navegador
    driver.quit()

    # Crear un DataFrame y guardar en CSV
    df = pd.DataFrame(data)
    df.to_csv('amazon_scraping_results.csv', index=False)
    return df

# Uso de la función
resultados = amazon_scraper('laptop', 2)
print(resultados)
