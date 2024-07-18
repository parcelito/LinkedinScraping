#funciona pero no obtiene datos de los empleados resultantes

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

def linkedin_login(driver, username, password):
    driver.get("https://www.linkedin.com/login")
    time.sleep(5)
    username_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")
    username_input.send_keys(username)
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)
    time.sleep(5)  # Espera adicional para asegurar que la página se cargue completamente

def search_profiles(driver, organization):
    search_url = f"https://www.linkedin.com/search/results/people/?keywords={organization}"
    driver.get(search_url)
    time.sleep(10)  # Espera adicional para asegurar que la página de resultados se cargue completamente
    print("Página de búsqueda cargada")
    time.sleep(2)
    profiles = driver.find_elements(By.CSS_SELECTOR, "div.entity-result__item")
    time.sleep(5)
    print(f"Se encontraron {len(profiles)} perfiles")
    time.sleep(2)
    results = []
    for profile in profiles:
        try:
            name = profile.find_element(By.CSS_SELECTOR, "span.entity-result__title-text > a > span").text
            title = profile.find_element(By.CSS_SELECTOR, "div.entity-result__primary-subtitle").text
            results.append({'name': name, 'title': title})
        except Exception as e:
            print(f"Error al obtener perfil: {e}")
    return results

if __name__ == "__main__":
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    
    username = input("Enter your LinkedIn username: ")
    password = input("Enter your LinkedIn password: ")
    organization = input("Enter the organization name: ")

    try:
        linkedin_login(driver, username, password)
        print("Login successful. Searching for profiles...")
        profiles = search_profiles(driver, organization)
        for profile in profiles:
            print(profile)
    except Exception as e:
        print(f"An error occurred: {e}")
    # finally:
    #     driver.quit()  # Comentar esta línea para mantener el navegador abierto
