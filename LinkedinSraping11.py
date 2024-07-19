from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def linkedin_login(driver, username, password):
    print("Abriendo LinkedIn...")
    driver.get("https://www.linkedin.com/login")
    time.sleep(5)
    username_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")
    print("Ingresando credenciales...")
    username_input.send_keys(username)
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)
    print("Esperando para asegurar que la página se cargue completamente...")
    time.sleep(5)

def search_company(driver, organization):
    print(f"Buscando la empresa {organization}...")
    search_url = f"https://www.linkedin.com/search/results/people/?keywords={organization}"
    driver.get(search_url)
    print("Esperando para cargar la página de resultados...")
    time.sleep(5)

def scroll_to_bottom(driver):
    print("Desplazándose hasta el final de la página...")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

def extract_profiles(driver):
    results = []
    index = 1
    while True:
        try:
            name_xpath = f"/html/body/div[5]/div[3]/div[2]/div/div[1]/main/div/div/div[2]/div/ul/li[{index}]/div/div/div/div[2]/div[1]/div[1]/div/span[1]/span/a/span/span[1]"
            name = driver.find_element(By.XPATH, name_xpath).text
            results.append({'name': name})
            index += 1
        except Exception as e:
            print(f"Error al obtener perfil {index}: {e}")
            break  # Salir del bucle cuando no se encuentren más perfiles en la página actual
    return results

def go_to_next_page(driver):
    next_button_xpath = "//button[@class='artdeco-button artdeco-button--muted artdeco-button--icon-right artdeco-button--1 artdeco-button--tertiary ember-view artdeco-pagination__button artdeco-pagination__button--next']"
    attempts = 3
    for attempt in range(attempts):
        try:
            print(f"Intento {attempt + 1}: Esperando que el botón 'Siguiente' esté presente...")
            scroll_to_bottom(driver)
            next_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, next_button_xpath))
            )
            print("Botón 'Siguiente' encontrado, haciendo clic...")
            driver.execute_script("arguments[0].click();", next_button)
            print("Esperando para cargar la nueva página...")
            time.sleep(10)
            print("Avanzando a la siguiente página")
            return True
        except Exception as e:
            print(f"Error en el intento {attempt + 1}: {e}")
            if attempt < attempts - 1:
                print("Reintentando...")
                driver.refresh()
                time.sleep(5)
            else:
                print("No se pudo hacer clic en el botón de siguiente o no hay más páginas.")
                return False

if __name__ == "__main__":
    print("Configurando el servicio del navegador...")
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    
    username = input("Enter your LinkedIn username: ")
    password = input("Enter your LinkedIn password: ")
    organization = input("Enter the organization name: ")

    try:
        linkedin_login(driver, username, password)
        print("Login successful. Buscando perfiles de la empresa...")
        search_company(driver, organization)
        print("esperando 5 segundos")
        time.sleep(5)
        
        all_results = []
        #results = extract_profiles(driver)
        #all_results.extend(results)


        # Ejemplo de cómo utilizar la función go_to_next_page en un bucle
        while True:
            results = extract_profiles(driver)
            all_results.extend(results)
            print("Nombres de los perfiles encontrados:")
            for result in all_results:
                print(result)
            if not go_to_next_page(driver):
                break
            print("Página avanzada con éxito")
        
        #print("Nombres de los perfiles encontrados:")
        #for result in all_results:
        #    print(result)
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Cerrando el navegador...")
        driver.quit()  # Cerrar el navegador al final
