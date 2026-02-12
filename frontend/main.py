import streamlit as st
from core.config import AppConfig
from utils.session import init_session_state
from ui.sidebar import render_sidebar
from ui.chat import render_chat

st.set_page_config(
    page_title=AppConfig.PAGE_TITLE,
    page_icon=AppConfig.PAGE_ICON,
    layout=AppConfig.LAYOUT
)

init_session_state()

def main():
    st.session_state.page_title = AppConfig.PAGE_TITLE
    
    render_sidebar()
    render_chat()

if __name__ == "__main__":
    main()