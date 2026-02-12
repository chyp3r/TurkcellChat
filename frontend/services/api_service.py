import requests
from core.config import AppConfig

class ApiService:
    @staticmethod
    def upload_pdf(file,category):
        try:
            files = {"file": (file.name, file, "application/pdf")}
            data = {"kategori": category}
            url = f"{AppConfig.BACKEND_URL}{AppConfig.ENDPOINT_UPLOAD}"
            response = requests.post(url, files=files, data=data, timeout=300)
            return response
        except requests.exceptions.RequestException:
            return None

    @staticmethod
    def send_message(message: str, thread_id: str):
        try:
            payload = {"question": message, "thread_id": thread_id}
            url = f"{AppConfig.BACKEND_URL}{AppConfig.ENDPOINT_CHAT}"
            response = requests.post(url, json=payload, timeout=300)
            
            if response.status_code == 200:
                return response.json().get("answer")
            else:
                return f"Hata: {response.text}"
        except Exception as e:
            return f"Bağlantı Hatası: {str(e)}"