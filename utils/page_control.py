import streamlit as st
from streamlit_extras.switch_page_button import switch_page

def check_prev_step(step_uri:str, step_var:str):
    if not st.session_state.get(step_var, False):
        st.warning("Please complete the previous step to continue.", icon="⚠️")
        if st.button(f"Go to {step_uri.replace('_', ' ')}"):
            switch_page(step_uri,)
        st.stop()