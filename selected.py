from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Create a new browser instance (make sure you have ChromeDriver installed)
driver = webdriver.Chrome()

# Open a website
driver.get("https://kleinanzeigen.de")

# Wait for it to load
time.sleep(2)

# Click a button (by its XPath, ID, or CSS selector)
#button = driver.find_element(By.XPATH, '//*[@id="my-button"]')
#button.click()

wait = WebDriverWait(driver, 10)

try:
    # Wait until the cookie banner button appears (max 10 sec)
    accept_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div[1]/div/div/dialog/div/div[2]/div[1]/button[1]'))
        )
    # Click the button
    accept_button.click()
    print("? Cookies accepted successfully!")

    # --- 2. Wait and click next button ---
    next_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/header/div[1]/div/span/astro-island/div/ul[2]/li[2]/a'))
    )
    next_button.click()
    print("? Login button clicked!")

    username_field = wait.until(EC.element_to_be_clickable((By.ID, "login-email")))
    username_field.clear()                    # optional: clear any existing text
    username_field.send_keys("youremail")   # type into the input box
    print("? Email entered successfully!")

    # Same for password field
    password_field = wait.until(EC.element_to_be_clickable((By.ID, "login-password")))
    password_field.send_keys("yourpassword")
    print("? Password entered successfully!")

    submit_button = wait.until(EC.element_to_be_clickable((By.ID, "login-submit")))
    submit_button.click()

except Exception as e:
    print("?? Could not find or click the cookie button:", e)


# Fill an input field
#input_box = driver.find_element(By.ID, "username")
#input_box.send_keys("myusername")

# Submit with Enter
#input_box.send_keys(Keys.RETURN)

# Wait a bit and close
time.sleep(3)
#driver.quit()
