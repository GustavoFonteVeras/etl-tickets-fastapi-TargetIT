from fastapi import FastAPI
from database import Base, engine, get_db
from controllers.routes import router

#Cria as tabelas no banco
Base.metadata.create_all(bind=engine)

#Cria a apllicação
app = FastAPI(
    title="ETL Tickets API",
    description="API para processar os tickets de TI de uma planilha Excel",
)

# Adiciona as rotas
app.include_router(router)

# Rota de teste
@app.get("/")
def home():
    return {"mensagem": "API funcionando! Acesse o /docs para testar"}
@app.get("/health")
def health():
    return {"status": "ok"}