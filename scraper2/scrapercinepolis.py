from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager # pip install webdriver-manager
import firebase_admin
from firebase_admin import credentials, db
from collections import defaultdict
from selenium.common.exceptions import StaleElementReferenceException
from datetime import datetime

# Inicializar la app de Firebase con las credenciales y la URL de la base de datos
cred = credentials.Certificate("prueba1.json")  
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://prueba-d306f-default-rtdb.firebaseio.com/'  
})



opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
#opts.add_argument("--headless")


driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=opts
)  

# Navegar a la URL de Cinepolis
driver.get("https://cinepolis.com.co/cartelera/bogota-colombia/")

# Esperar a que la página cargue completamente
sleep(0.5)
data_final = {}
cine_index = 1 
t = 0
def upload_movie(movie_data):
    ref = db.reference('movie_titles')
    
    # Buscar si el título ya existe
    all_movies = ref.get()  # Obtén todos los datos en 'movie_titles'
    
    for key, movie in all_movies.items():
        if movie['title'] == movie_data['title']:
            print(f"El título '{movie_data['title']}' ya existe en la base de datos.")
            return  # Salir si el título ya existe
    
    # Si el título no existe, subir los nuevos datos
    new_movie_ref = ref.push()  # Crear una nueva entrada
    new_movie_ref.set(movie_data)
    print(f"Datos subidos para '{movie_data['title']}'.")

try:
    wait = WebDriverWait(driver, 10)  # Espera hasta 10 segundos        
    # Espera a que el div con las clases específicas se encuentre en la página
    div_element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/form/div[2]/div[2]/section[2]/section[2]/div[5]")))
    a_elements = div_element.find_elements(By.CSS_SELECTOR, "h3 a.datalayer-movie.ng-binding")
    for a in a_elements:
        print(a_elements[t].text.lower().replace(":", ""))
        times = []
        driver.execute_script("arguments[0].click();", a_elements[t])
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".duracion")))
        current_url = driver.current_url
        print("Current URL:", current_url)
        driver.back()
        
        wait = WebDriverWait(driver, 10)  # Espera hasta 10 segundos
        # Espera a que el div con las clases específicas se encuentre en la página
        div_element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/form/div[2]/div[2]/section[2]/section[2]/div[5]")))
        a_elements = div_element.find_elements(By.CSS_SELECTOR, "h3 a.datalayer-movie.ng-binding")
        try:
            wait = WebDriverWait(driver, 10)  # Espera hasta 10 segundos
            macro_check = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/form/div[2]/div[2]/section[2]/div/div/div/div/div[4]/div/div[1]/p[3]/div/span/input")))
            macro_check.click()
            d4_check = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/form/div[2]/div[2]/section[2]/div/div/div/div/div[4]/div/div[1]/p[2]/div/span/input")))
            d4_check.click()
        except:
            print()
        
        articles = WebDriverWait(div_element, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article.row.tituloPelicula.ng-scope"))
        )
        time_elements = articles[t].find_elements(By.CSS_SELECTOR, "time.btn.btnhorario.ng-scope")
        
        # Extraer y guardar los valores en una lista
        time_values = [element.get_attribute("value") for element in time_elements]
        formatted_times = [datetime.strptime(time_24, '%H:%M').strftime('%I:%M %p').replace(' ', '').lower() for time_24 in time_values]    # Imprimir las horas en formato 12 horas
        for formatted in formatted_times:
            times.append(formatted)
        print(times)
        # Dentro de cada fecha, buscar todos los elementos <a> que contienen imágenes
        img_elements = div_element.find_elements(By.CSS_SELECTOR, 'a img')
        img_src = img_elements[t].get_attribute('ng-src')
        print(f"  Imagen ng-src: {img_src}")
        movie_data = {
            "image": img_src,
            "title": a_elements[t].text.lower().replace(":", ""),
            "url": current_url
        }
        upload_movie(movie_data)
        data_final = {
            "cine": "Cinépolis VIP Plaza Claro",
            "horarios": " ".join(times),  # String de horarios concatenados
            "precio": "$22000"
        }
        ref = db.reference(a_elements[t].text.lower().replace(":", ""))
        # Usar set() para establecer todos los datos
        new_movie_ref = ref.push()
        new_movie_ref.update(data_final)
        t += 1

except:
    print("error")

driver.get("https://cinepolis.com.co/cartelera/bogota-colombia/")

# Esperar a que la página cargue completamente
sleep(0.5)

t = 0

try:
    wait = WebDriverWait(driver, 10)  # Espera hasta 10 segundos
    
    # Espera a que el div con las clases específicas se encuentre en la página
    div_element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/form/div[2]/div[2]/section[2]/section[2]/div[6]")))
    a_elements = div_element.find_elements(By.CSS_SELECTOR, "h3 a.datalayer-movie.ng-binding")
    for a in a_elements:
        print(a_elements[t].text.lower().replace(":", ""))
        times = []
        driver.execute_script("arguments[0].click();", a_elements[t])
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".duracion")))
        current_url = driver.current_url
        print("Current URL:", current_url)
        driver.back()
        
        wait = WebDriverWait(driver, 10)  # Espera hasta 10 segundos
        # Espera a que el div con las clases específicas se encuentre en la página
        div_element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/form/div[2]/div[2]/section[2]/section[2]/div[6]")))
        a_elements = div_element.find_elements(By.CSS_SELECTOR, "h3 a.datalayer-movie.ng-binding")
        try:
            wait = WebDriverWait(driver, 10)  # Espera hasta 10 segundos
            macro_check = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/form/div[2]/div[2]/section[2]/div/div/div/div/div[4]/div/div[1]/p[3]/div/span/input")))
            macro_check.click()
            d4_check = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/form/div[2]/div[2]/section[2]/div/div/div/div/div[4]/div/div[1]/p[2]/div/span/input")))
            d4_check.click()
        except:
            print()
        
        articles = WebDriverWait(div_element, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article.row.tituloPelicula.ng-scope"))
        )
        time_elements = articles[t].find_elements(By.CSS_SELECTOR, "time.btn.btnhorario.ng-scope")
        
        # Extraer y guardar los valores en una lista
        time_values = [element.get_attribute("value") for element in time_elements]
        formatted_times = [datetime.strptime(time_24, '%H:%M').strftime('%I:%M %p').replace(' ', '').lower() for time_24 in time_values]    # Imprimir las horas en formato 12 horas
        for formatted in formatted_times:
            times.append(formatted)
        print(times)
        # Dentro de cada fecha, buscar todos los elementos <a> que contienen imágenes
        img_elements = div_element.find_elements(By.CSS_SELECTOR, 'a img')
        img_src = img_elements[t].get_attribute('ng-src')
        print(f"  Imagen ng-src: {img_src}")
        movie_data = {
            "image": img_src,
            "title": a_elements[t].text.lower().replace(":", ""),
            "url": current_url
        }
        upload_movie(movie_data)
        data_final = {
            "cine": "Cinépolis Diverplaza",
            "horarios": " ".join(times),  # String de horarios concatenados
            "precio": "$9900"
        }
        ref = db.reference(a_elements[t].text.lower().replace(":", ""))
        # Usar set() para establecer todos los datos
        new_movie_ref = ref.push()
        new_movie_ref.update(data_final)
        t += 1
except:
    print("error")
driver.get("https://cinepolis.com.co/cartelera/bogota-colombia/")

# Esperar a que la página cargue completamente
sleep(0.5)
t = 0

try:
    wait = WebDriverWait(driver, 10)  # Espera hasta 10 segundos
    
    # Espera a que el div con las clases específicas se encuentre en la página
    div_element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/form/div[2]/div[2]/section[2]/section[2]/div[7]")))
    a_elements = div_element.find_elements(By.CSS_SELECTOR, "h3 a.datalayer-movie.ng-binding")
    for a in a_elements:
        print(a_elements[t].text.lower().replace(":", ""))
        times = []
        driver.execute_script("arguments[0].click();", a_elements[t])
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".duracion")))
        current_url = driver.current_url
        print("Current URL:", current_url)
        driver.back()
        
        wait = WebDriverWait(driver, 10)  # Espera hasta 10 segundos
        # Espera a que el div con las clases específicas se encuentre en la página
        div_element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/form/div[2]/div[2]/section[2]/section[2]/div[7]")))
        
        a_elements = div_element.find_elements(By.CSS_SELECTOR, "h3 a.datalayer-movie.ng-binding")
        try:
            wait = WebDriverWait(driver, 10)  # Espera hasta 10 segundos
            macro_check = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/form/div[2]/div[2]/section[2]/div/div/div/div/div[4]/div/div[1]/p[3]/div/span/input")))
            macro_check.click()
            d4_check = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/form/div[2]/div[2]/section[2]/div/div/div/div/div[4]/div/div[1]/p[2]/div/span/input")))
            d4_check.click()
        except:
            print()
        
        articles = WebDriverWait(div_element, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article.row.tituloPelicula.ng-scope"))
        )
        time_elements = articles[t].find_elements(By.CSS_SELECTOR, "time.btn.btnhorario.ng-scope")
        
        # Extraer y guardar los valores en una lista
        time_values = [element.get_attribute("value") for element in time_elements]
        formatted_times = [datetime.strptime(time_24, '%H:%M').strftime('%I:%M %p').replace(' ', '').lower() for time_24 in time_values]    # Imprimir las horas en formato 12 horas
        for formatted in formatted_times:
            times.append(formatted)
        print(times)
        # Dentro de cada fecha, buscar todos los elementos <a> que contienen imágenes
        img_elements = div_element.find_elements(By.CSS_SELECTOR, 'a img')
        img_src = img_elements[t].get_attribute('ng-src')
        print(f"  Imagen ng-src: {img_src}")
        movie_data = {
            "image": img_src,
            "title": a_elements[t].text.lower().replace(":", ""),
            "url": current_url
        }
        upload_movie(movie_data)
        data_final = {
            "cine": "Cinépolis Mallplaza",
            "horarios": " ".join(times),  # String de horarios concatenados
            "precio": "$12700"
        }
        ref = db.reference(a_elements[t].text.lower().replace(":", ""))
        # Usar set() para establecer todos los datos
        new_movie_ref = ref.push()
        new_movie_ref.update(data_final)
        t += 1
        
except:
    print("error")
    
driver.get("https://cinepolis.com.co/cartelera/bogota-colombia/")

# Esperar a que la página cargue completamente
sleep(0.5)
t = 0

try:
    wait = WebDriverWait(driver, 10)  # Espera hasta 10 segundos
    
    # Espera a que el div con las clases específicas se encuentre en la página
    div_element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/form/div[2]/div[2]/section[2]/section[2]/div[8]")))
    a_elements = div_element.find_elements(By.CSS_SELECTOR, "h3 a.datalayer-movie.ng-binding")
    for a in a_elements:
        print(a_elements[t].text.lower().replace(":", ""))
        times = []
        driver.execute_script("arguments[0].click();", a_elements[t])
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".duracion")))
        current_url = driver.current_url
        print("Current URL:", current_url)
        driver.back()
        
        wait = WebDriverWait(driver, 10)  # Espera hasta 10 segundos
        
        # Espera a que el div con las clases específicas se encuentre en la página
        div_element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/form/div[2]/div[2]/section[2]/section[2]/div[8]")))
        
        a_elements = div_element.find_elements(By.CSS_SELECTOR, "h3 a.datalayer-movie.ng-binding")
        try:
            wait = WebDriverWait(driver, 10)  # Espera hasta 10 segundos
            macro_check = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/form/div[2]/div[2]/section[2]/div/div/div/div/div[4]/div/div[1]/p[3]/div/span/input")))
            macro_check.click()
            d4_check = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/form/div[2]/div[2]/section[2]/div/div/div/div/div[4]/div/div[1]/p[2]/div/span/input")))
            d4_check.click()
        except:
            print()
        
        articles = WebDriverWait(div_element, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article.row.tituloPelicula.ng-scope"))
        )
        time_elements = articles[t].find_elements(By.CSS_SELECTOR, "time.btn.btnhorario.ng-scope")
        
        # Extraer y guardar los valores en una lista
        time_values = [element.get_attribute("value") for element in time_elements]
        formatted_times = [datetime.strptime(time_24, '%H:%M').strftime('%I:%M %p').replace(' ', '').lower() for time_24 in time_values]    # Imprimir las horas en formato 12 horas
        for formatted in formatted_times:
            times.append(formatted)
        print(times)
        # Dentro de cada fecha, buscar todos los elementos <a> que contienen imágenes
        img_elements = div_element.find_elements(By.CSS_SELECTOR, 'a img')
        img_src = img_elements[t].get_attribute('ng-src')
        print(f"  Imagen ng-src: {img_src}")
        movie_data = {
            "image": img_src,
            "title": a_elements[t].text.lower().replace(":", ""),
            "url": current_url
        }
        upload_movie(movie_data)
        data_final = {
            "cine": "Cinépolis Hayuelos Colombia",
            "horarios": " ".join(times),  # String de horarios concatenados
            "precio": "$11900"
        }
        ref = db.reference(a_elements[t].text.lower().replace(":", ""))
        # Usar set() para establecer todos los datos
        new_movie_ref = ref.push()
        new_movie_ref.update(data_final)
        t += 1
        
except:
    print("error")
driver.quit()