import streamlit as st
from core.config import AppConfig
from services.api_service import ApiService
from utils.session import reset_session

def render_sidebar():
    with st.sidebar:
        # st.image(AppConfig.LOGO_URL, width=180)        
        with st.container():
            st.markdown("#### 📂 Veri Yükleme Merkezi")
            st.info("Yüklediğiniz PDF'ler anında ilgili yapay zeka uzmanına iletilir.")

            category_options = {
                "tariff": "📱 Tarifeler & Paketler",
                "support": "🛠️ Teknik Destek & Arıza",
                "general": "ℹ️ Genel Bilgi"
            }
            
            selected_category = st.selectbox(
                label="Hangi uzmana bilgi eklenecek?", 
                options=list(category_options.keys()),
                format_func=lambda x: category_options[x]
            )
            
            uploaded_file = st.file_uploader("PDF Dosyanızı buraya bırakın", type=["pdf"])
            
            if uploaded_file:
                if st.button("🚀 Bilgiyi Sisteme İşle", use_container_width=True):
                    display_name = category_options[selected_category]
                    
                    progress_text = "Dosya okunuyor, vektörlere dönüştürülüyor..."
                    my_bar = st.progress(0, text=progress_text)
                    
                    try:
                        res = ApiService.upload_pdf(uploaded_file, selected_category)
                        
                        if res and res.status_code == 200:
                            my_bar.progress(100, text="İşlem Tamamlandı!")
                            st.success(f"✅ Başarılı! Veriler '{display_name}' hafızasına eklendi.")
                        else:
                            my_bar.empty()
                            st.error("❌ Bir hata oluştu. Lütfen tekrar deneyin.")
                    except Exception as e:
                        my_bar.empty()
                        st.error(f"Bağlantı hatası: {e}")

        st.markdown("---")
        
        with st.expander("⚙️ Sistem Ayarları", expanded=True):
            st.write("Mevcut sohbet geçmişini siler ve yapay zekayı sıfırlar.")
            
            if st.button("🗑️ Sohbeti Temizle", type="primary", use_container_width=True):
                reset_session()
                
            st.markdown("###") # Boşluk
            st.caption("Aktif Oturum ID:")
            st.code(st.session_state.thread_id, language=None)