import streamlit as st
import uuid

def init_session_state():
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = str(uuid.uuid4())

    if "messages" not in st.session_state:
        st.session_state.messages = []

def reset_session():
    st.session_state.messages = []
    st.session_state.thread_id = str(uuid.uuid4())
    st.rerun()