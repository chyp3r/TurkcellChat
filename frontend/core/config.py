import os

class AppConfig:
    PAGE_TITLE = "Turkcell Asistan"
    PAGE_ICON = "🟡"
    LAYOUT = "wide"
    
    BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:5050/api/v1")
    
    LOGO_URL = "https://ffo3gv1cf3ir.merlincdn.net/SiteAssets/Hakkimizda/genel-bakis/logolarimiz/AMBLEM_SARI.png?20260127_03"
    
    ENDPOINT_UPLOAD = "/ingest/upload-pdf"
    ENDPOINT_CHAT = "/agent/master-agent"