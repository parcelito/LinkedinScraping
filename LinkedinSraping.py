from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

def linkedin_login(driver, username, password):
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)
    username_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")
    username_input.send_keys(username)
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)
    time.sleep(2)

def search_profiles(driver, organization):
    search_url = f"https://www.linkedin.com/search/results/people/?keywords={organization}"
    driver.get(search_url)
    time.sleep(2)
    profiles = driver.find_elements(By.CSS_SELECTOR, "div.search-result__info")
    results = []
    for profile in profiles:
        name = profile.find_element(By.CSS_SELECTOR, "span.name.actor-name").text
        title = profile.find_element(By.CSS_SELECTOR, "p.subline-level-1").text
        results.append({'name': name, 'title': title})
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
        profiles = search_profiles(driver, organization)
        for profile in profiles:
            print(profile)
    finally:
        driver.quit()
