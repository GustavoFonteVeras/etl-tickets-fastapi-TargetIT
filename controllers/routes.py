from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.services import processar_excel

router = APIRouter()

@router.post("/upload", tags=["upload"])
async def upload_arquivo(file: UploadFile = File(...), db: Session = Depends(get_db)):

    # endpoint pra fazer upload da planilha Excel

    # valida extensão
    if not file.filename.endswith((".xlsx",".xlsx")):
        raise HTTPException(status_code=400, detail="Arquivo precisa ser .xlsx ou .xls")

    try:
        #Lê o arquivo enviado
        conteudo = await file.read()

        #Processa
        resultado = processar_excel(db, conteudo)

        return{
            "mensagem": "Upload processado com sucesso!",
            "resumo": resultado
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro: {str(e)}")


