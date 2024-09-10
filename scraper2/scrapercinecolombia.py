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

try: 
    driver.get('https://www.cinecolombia.com/bogota/cartelera')


    sleep(1)

    #dar click a aceptar cookies
    wait = WebDriverWait(driver, 3)
    cookies_button = wait.until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[1]/div/div/div/div[3]/button")))

    cookies_button.click()
            # Esperar a que el elemento SVG sea clickeable
    wait = WebDriverWait(driver, 10)
    svg_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='account-dropdown-button']")))

    svg_element.click()
            
            
            # Esperar a que el campo de correo electrónico esté visible y luego llenarlo
    email_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@id='username']"))  # Cambia "email" por el nombre o identificador correcto
    )
    email_field.send_keys("snehidersalas@gmail.com")

            # Esperar a que el campo de contraseña esté visible y luego llenarlo
    password_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@id='password']"))  # Cambia "password" por el nombre o identificador correcto
    )
    password_field.send_keys("Relampag0*")

                # Esperar a que el botón de iniciar sesión esté clickeable y luego hacer clic
    wait = WebDriverWait(driver, 10)
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/header/div/div/div[3]/div[3]/div/div/div/div[1]/div[2]/div[2]/div/div[1]/form/div[3]/div/button")))

    login_button.click()
    sleep(3.2)
except Exception as e:
    print(f"Ocurrió un error cinecolombia: {e}")
    
z = 0
try:
    


    # Buscar todos los enlaces <a> con la clase "movie-item"
    a_elements = driver.find_elements(By.XPATH, "//a[@class='movie-item']")

    # Extraer los href de los enlaces y almacenarlos en una lista
    links = [a.get_attribute('href') for a in a_elements]
    
    # Buscar todas las etiquetas <figure> con la clase "movie-item__image" y luego las imágenes
    figure_elements = driver.find_elements(By.XPATH, "//figure[@class='movie-item__image']//img")

    # Extraer los data-src de las imágenes y almacenarlos en una lista
    image_links = [img.get_attribute('data-src') for img in figure_elements]


    # Recorrer cada enlace almacenado
    for link in links:
        # Navegar al enlace
        driver.get(link)
        
        
        # Esperar explícitamente a que los elementos <h3> sean visibles
        wait = WebDriverWait(driver, 10)
        h3_elements = wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//h3[@class='show-times-collapse__title']")))

        try: 
            title = driver.find_elements(By.XPATH, "//span[@class='ezstring-field']")
            if len(title) > 2:
                title_name = title[1].text

            else:
                eee
        except Exception as e:
            title = driver.find_element(By.XPATH, "//span[@class='ezstring-field']")
            title_name = title.text.lower().replace(":", "")
        # Referencia a la base de datos
        ref = db.reference('movie_titles')
        # Subir datos a Firebase
        movie_data = {
            'image': image_links[z],
            'title': title_name.lower().replace(":", ""),
            'url': link
        }
        ref.child(f'movie_{z}').set(movie_data)
        print("firebase")
        z += 1

        # Recopilar y mostrar el texto de los elementos encontrados
        cines_list = [h3.text for h3 in h3_elements]
        print(f"Resultados para {title_name}: {cines_list}")
        n = 0
        # Construir la estructura final
        data_final = {}
        cine_index = 1  #"cine1", "cine2", etc.    
        try:
            
            
            # Esperar a que los botones con la clase 'boton' estén visibles
            try:
                button_elements = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".collapsible.show-times-collapse"))
                )
                
                
            except Exception as e:
                print(f"No se encontraron los botones: {e}")
                driver.quit()
                exit()

            # Iterar sobre los botones y hacer clic en cada uno
            for button in button_elements:
                try:
                    newlist = []
                    newlist2 = []
                    # Hacer clic en el botón
                    button.click()
                    sleep(0.7)
                    parent_div = WebDriverWait(driver, 2).until(
                        EC.visibility_of_element_located(
                            (By.CSS_SELECTOR, ".collapse.is-open")
                        )
                    )
                    #buscar horarios
                    
                    child_div = parent_div.find_element(By.CSS_SELECTOR, ".show-times-group__times")
                    span_elements = child_div.find_elements(By.TAG_NAME, "span")
                    for span in span_elements:
                        span_text = span.text.replace(" ", "").lower()
                        
                        try: 
                            
                            driver.execute_script("arguments[0].click();", span)
                            print("Haciendo clic en un enlace")
                            # Espera un poco para que la página o el contenido se cargue (ajusta según sea necesario)
                            # Esperar y hacer clic en el primer elemento
                            pse = WebDriverWait(driver, 15).until(
                                EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/section/div[2]/div/div[2]/section/div/div/div[3]/label/div"))
                            )
                            pse.click()
                            # Esperar y hacer clic en el botón de continuar
                            continuar_boton = WebDriverWait(driver, 15).until(
                                EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/section/div[2]/div/div[2]/section/div/div/div[5]/div/a"))
                            )
                            continuar_boton.click()

                            # Esperar a que el botón plus esté clickeable
                            plus_button = WebDriverWait(driver, 15).until(
                                EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/section/div[2]/div/div[2]/section/div[2]/div/div[1]/div/div[1]/div/div/button[2]"))
                            )
                            plus_button.click()

                            continuar2 = WebDriverWait(driver, 15).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.button.is-uppercase.has-shadow.is-primary'))
                            )
                            continuar2.click()
                            
                            
                            segundo_span = WebDriverWait(driver, 15).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.tickets-summary__total span:nth-of-type(2)'))
                            )
                            print(span_text)
                            print(segundo_span.text)
                            newlist2.append(segundo_span.text)
                            newlist.append(span_text)
                        
                                
                            
                            # Regresar a la página anterior
                            driver.back()
                            driver.back()
                            driver.back()

                            
                        except Exception as e:
                            driver.back()
                            
                    
                    # Agrupar horarios por precio
                    precio_horarios = defaultdict(list)
                    for i, precio in enumerate(newlist2):
                        precio_horarios[precio].append(newlist[i])
                        
                    for precio, horarios_list in precio_horarios.items():
                        key = f"cine{cine_index}"
                        # Convertir la lista de horarios en un string concatenado
                        horarios_str = ", ".join(horarios_list)
                        
                        data_final[key] = {
                            "cine": cines_list[n],
                            "horarios": horarios_str,  # String de horarios concatenados
                            "precio": precio
                        }
                        cine_index += 1
                    
                    print("hecho")
                        
                    n += 1
                    times_div = driver.find_element(By.CSS_SELECTOR, ".show-times-group__times")
                    elements = times_div.find_elements(By.CSS_SELECTOR, ".button.is-primary.is-outlined.is-small")

                    
                    
                    
                        
                    
                except Exception as e:
                    print(f"Error al hacer clic en el botón: {e}")

        except Exception as e:
            print(f"Error general: {e}")
            
            

        # Esperar a que la página cargue
        sleep(0.5)
        # Referencia a la ubicación en Firebase donde quieres subir los datos
        ref = db.reference(title_name.lower().replace(":", ""))
        # Usar set() para establecer todos los datos
        ref.set(data_final)

        print("Datos subidos exitosamente a Firebase.")
            
except Exception as e:
    print(f"Ocurrió un error cinecolombia: {e}")

     
    
    
    
    
    
    



# Cerrar el navegador
driver.quit()