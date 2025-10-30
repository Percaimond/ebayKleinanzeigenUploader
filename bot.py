# bot.py
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def _wait_clickable(wait, by, value, click=True, label="element"):
    el = wait.until(EC.element_to_be_clickable((by, value)))
    if click:
        el.click()
    return el

def _find(wait, by, value):
    return wait.until(EC.presence_of_element_located((by, value)))

def _upload_folder_through_input(input_element, folder_path):
    """
    Many file inputs accept multiple files by sending a newline-separated list of paths.
    If the site supports directory upload (webkitdirectory), that also works by passing the folder.
    """
    files = []
    for root, _, names in os.walk(folder_path):
        for n in names:
            files.append(os.path.abspath(os.path.join(root, n)))
    if not files:
        raise RuntimeError(f"No files found under folder: {folder_path}")
    input_element.send_keys("\n".join(files))

def run_bot(
    url: str,
    folder_path: str,
    email: str = "",
    password: str = "",
    # selectors (defaults filled for kleinanzeigen.de based on your script)
    cookie_accept_xpath: str = '/html/body/div[1]/div/div/dialog/div/div[2]/div[1]/button[1]',
    login_button_xpath: str = '/html/body/header/div[1]/div/span/astro-island/div/ul[2]/li[2]/a',
    email_id: str = 'login-email',
    password_id: str = 'login-password',
    submit_id: str = 'login-submit',
    # selector for the file input where we send paths:
    upload_selector: str = 'input[type="file"]',
    upload_selector_is_css: bool = True,
    headless: bool = False,
    timeout: int = 20
):
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Folder does not exist: {folder_path}")

    # --- browser options ---
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, timeout)

    try:
        driver.get(url)

        # 1) Accept cookies (if selector present)
        if cookie_accept_xpath:
            try:
                _wait_clickable(wait, By.XPATH, cookie_accept_xpath, click=True, label="cookie-accept")
                print("? Cookies accepted")
            except Exception:
                print("?? Cookie banner not found or already accepted; continuing.")

        # 2) Click login (optional)
        if login_button_xpath:
            try:
                _wait_clickable(wait, By.XPATH, login_button_xpath, click=True, label="login-button")
                print("? Login button clicked")
            except Exception:
                print("?? Login button not found; continuing.")

        # 3) Fill credentials (optional)
        if email:
            try:
                email_el = _wait_clickable(wait, By.ID, email_id, click=False, label="email")
                email_el.clear()
                email_el.send_keys(email)
                print("? Email entered")
            except Exception:
                print("?? Could not fill email")

        if password:
            try:
                pw_el = _wait_clickable(wait, By.ID, password_id, click=False, label="password")
                pw_el.send_keys(password)
                print("? Password entered")
            except Exception:
                print("?? Could not fill password")

        if email and password:
            try:
                _wait_clickable(wait, By.ID, submit_id, click=True, label="submit")
                print("? Login submitted")
            except Exception:
                print("?? Could not click submit")

        # 4) Find the file input and upload the folder's files
        try:
            if upload_selector_is_css:
                file_input = _find(wait, By.CSS_SELECTOR, upload_selector)
            else:
                file_input = _find(wait, By.XPATH, upload_selector)

            # Make it visible/focused (some sites hide it)
            driver.execute_script("arguments[0].style.display='block'; arguments[0].focus();", file_input)

            _upload_folder_through_input(file_input, folder_path)
            print("? Files sent to file-input")
        except Exception as e:
            raise RuntimeError(f"Could not locate or use the upload input. Detail: {e}")

        # give some time to process uploads on site
        time.sleep(5)
    finally:
        # Keep browser open if you want to continue manually; otherwise uncomment:
        # driver.quit()
        pass
