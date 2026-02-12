import streamlit as st
from services.api_service import ApiService

def render_chat():
    st.title(f"{st.session_state.get('page_title', 'Asistan')}")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Mesajınızı yazın..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Asistan düşünüyor..."):
                response_text = ApiService.send_message(
                    message=prompt, 
                    thread_id=st.session_state.thread_id
                )
                st.markdown(response_text)
                
                st.session_state.messages.append({"role": "assistant", "content": response_text})