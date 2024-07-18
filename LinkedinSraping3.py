# funciona!! obtiene los nombres de empleados de la primera hoja de resultados 
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
    time.sleep(5)  # Espera adicional para asegurar que la página de resultados se cargue completamente
    print("Página de búsqueda cargada")

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
            break  # Salir del bucle cuando no se encuentren más perfiles

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
    finally:
        driver.quit()  # Cerrar el navegador al final
