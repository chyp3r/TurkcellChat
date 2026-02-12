from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.rag_service import RagService
from pypdf import PdfReader
from app.constants.db_collections import DBCollections
import io

router = APIRouter()

@router.post("/upload-pdf")
async def pdf_yukle(file: UploadFile = File(...), db_name = DBCollections.GENERAL):
    rag_service = RagService(db_name)
    try:
        print("Document upload started")
        if not file.filename.endswith(".pdf"):
            raise HTTPException(status_code=400)
        
        content = await file.read()
        pdf_file = io.BytesIO(content)
        reader = PdfReader(pdf_file)
        
        full_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
        
        if not full_text.strip():
            raise HTTPException(status_code=400)

        parca_sayisi = rag_service.belge_yukle(metin=full_text, kaynak_adi=file.filename)
        
        return {
            "status": "success",
            "filename": file.filename,
            "chunks_created": parca_sayisi,
            "message": "Document uploaded"
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))