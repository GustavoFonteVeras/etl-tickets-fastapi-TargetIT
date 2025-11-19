from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from pydantic import BaseModel
from datetime import datetime
from database import Base

####### MODELO DO BANCO (SQLAlchemy) #######

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    numero = Column(String, unique=True, index=True)
    numero = Column(String, unique=True, index=True)
    solicitado_para = Column(String)
    email_solicitado = Column(String)
    aberto_por = Column(String)
    aberto_em = Column(DateTime)
    atualizado_em = Column(DateTime)
    item = Column(String)
    empresa = Column(String)
    canal = Column(String)
    local = Column(String)
    descricao = Column(String)
    status = Column(String)
    grupo_atribuicao = Column(String)
    atribuido_a = Column(String)
    email_extra = Column(String)
    comentarios = Column(String)

    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

####### MODELOS DO PYDANTIC (validação) #######

class TicketBase(BaseModel):
    numero: str
    solicitado_para: str | None = None
    email_solicitado: str | None = None
    aberto_por: str | None = None
    aberto_em: datetime | None = None
    atualizado_em: datetime
    item: str | None = None
    empresa: str | None = None
    canal: str | None = None
    local: str | None = None
    descricao: str
    status: str | None = None
    grupo_atribuicao: str | None = None
    atribuido_a: str | None = None
    email_extra: str | None = None
    comentarios: str | None = None

class TicketResponse(BaseModel):
    id:int
    numero: str
    descricao: str
    responsavel: str
    data_atualizacao: datetime
    created_at: datetime
    updated_at: datetime

    class config:
        orm_mode = True



