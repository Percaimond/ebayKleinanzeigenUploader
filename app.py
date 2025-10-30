# app.py
import streamlit as st
from bot import run_bot

st.set_page_config(page_title="Kleinanzeigen Uploader Bot", page_icon="?", layout="centered")
st.title("? Kleinanzeigen Uploader Bot")

st.markdown("Fill in the fields below and click **Run Bot**.")

with st.form("bot_form"):
    url = st.text_input("Website URL", value="https://kleinanzeigen.de")

    st.subheader("Login (optional)")
    email = st.text_input("Email (optional)", value="")
    password = st.text_input("Password (optional)", value="", type="password")

    st.subheader("Upload")
    folder_path = st.text_input("Local folder path to upload (absolute)", value="")

    st.subheader("Selectors (defaults for kleinanzeigen.de)")
    cookie_accept_xpath = st.text_input(
        "Cookie accept button XPath",
        value='/html/body/div[1]/div/div/dialog/div/div[2]/div[1]/button[1]'
    )
    login_button_xpath = st.text_input(
        "Login button XPath",
        value='/html/body/header/div[1]/div/span/astro-island/div/ul[2]/li[2]/a'
    )
    email_id = st.text_input("Email field ID", value="login-email")
    password_id = st.text_input("Password field ID", value="login-password")
    submit_id = st.text_input("Submit button ID", value="login-submit")

    st.subheader("File input selector")
    upload_selector = st.text_input('CSS selector or XPath for file input', value='input[type="file"]')
    selector_is_css = st.checkbox("Selector is CSS (uncheck for XPath)", value=True)

    headless = st.checkbox("Run headless", value=False)
    timeout = st.number_input("Timeout (seconds) for waits", min_value=5, max_value=60, value=20, step=1)

    submitted = st.form_submit_button("Run Bot ?")

if submitted:
    if not folder_path:
        st.error("Please enter a local folder path.")
    else:
        with st.spinner("Running Selenium?"):
            try:
                run_bot(
                    url=url,
                    folder_path=folder_path,
                    email=email,
                    password=password,
                    cookie_accept_xpath=cookie_accept_xpath,
                    login_button_xpath=login_button_xpath,
                    email_id=email_id,
                    password_id=password_id,
                    submit_id=submit_id,
                    upload_selector=upload_selector,
                    upload_selector_is_css=selector_is_css,
                    headless=headless,
                    timeout=int(timeout),
                )
                st.success("Done! Check the browser window.")
            except Exception as e:
                st.error(f"Error: {e}")
                st.exception(e)
