import streamlit as st

def render_login():
    """Render login form and handle authentication"""
    st.title("\U0001f512 Inicio de Sesi\u00f3n")
    
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Contrase\u00f1a", type="password")
        submitted = st.form_submit_button("Ingresar")
        
        if submitted:
            # Simulated authentication
            if email == "admin@ciplas.com" and password == "admin123":
                st.session_state['authenticated'] = True
                st.session_state['user_email'] = email
                st.rerun()
            else:
                st.error("Credenciales incorrectas")

def check_auth():
    """Check if user is authenticated"""
    return st.session_state.get('authenticated', False)

def logout():
    """Clear session and logout"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()
