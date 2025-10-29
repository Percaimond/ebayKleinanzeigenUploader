import streamlit as st
import subprocess

st.title("Article upload Automation Bot ?")

url = st.text_input("Enter website URL:")
selector = st.text_input("Enter button selector (XPath or CSS):")

if st.button("Run Bot"):
    cmd = f"python automate.py --url '{url}' --selector '{selector}'"
    subprocess.run(cmd, shell=True)
    st.success("Automation complete!")
