import streamlit as st
from utils import auth_utils

def login_page():
    st.title("🔐 Login Sistem AHP")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = auth_utils.authenticate_user(username, password)
        if user:
            token = auth_utils.generate_token(username)
            auth_utils.save_user_token(username, token)
            st.query_params.update(token=token)  # set token ke URL
            st.rerun()
        else:
            st.error("Username atau password salah")
