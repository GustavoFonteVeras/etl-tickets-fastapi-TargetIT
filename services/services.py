import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session
from models.models import Ticket, TicketResponse
from utils.utils import registrar_log

COL = {
    "NUMERO"            : "Número",
    "SOLICITADO_PARA"   : "Solicitado(a) para",
    "EMAIL_SOL"         : "E-mail",
    "ABERTO_POR"        : "Aberto por",
    "ABERTO_EM"         : "Aberto",
    "ATUALIZADO_EM"     : "Atualizado em",
    "ITEM"              : "Item",
    "EMPRESA"           : "Empresa",
    "CANAL"             : "Canal",
    "LOCAL"             : "Local",
    "DESCRICAO"         : "Descrição",
    "STATUS"            : "Status",
    "GRUPO_ATRIB"       : "Grupo de atribuição",
    "ATRIBUIDO_A"       : "Atribuído a",
    "EMAIL_EXTRA"       : "E-mail",
    "COMENT"            : "Comentários adicionais",
}

COLUNAS_OBRIGATORIAS = [
    COL["NUMERO"],
    COL["DESCRICAO"],
    COL["ATUALIZADO_EM"],
]

# esta função lê o arquivo Excel, valida e insere/atualiza no banco
def processar_excel(db: Session, conteudo_arquivo: bytes) -> dict:
    """
        Lê o Excel enviado, valida colunas, e faz ETL simples:
        1. Se o 'Número' ainda não existe, insere novo ticket.
        2. Se já existe, atualiza apenas se 'Atualizado em' for mais recente.
        Retorna um resumo com quantos registros foram inseridos / atualizados / ignorados.
    """

    #Lê o arquivo em memória
    df = pd.read_excel(conteudo_arquivo)

    if not all(col in df.columns for col in COLUNAS_OBRIGATORIAS):
        raise ValueError(f"A planilha precisa ter as colunas: {COLUNAS_OBRIGATORIAS}")

    #Contadores para o resumo final
    inseridos = 0
    atualizados = 0
    nao_atualizados = 0

    #Percorre cada linha e aplica as regras de negócio
    for _,linha in df.iterrows():
        valores = {
            "numero": str(linha[COL["NUMERO"]]).strip(),
            "solicitado_para": str(linha.get(COL["SOLICITADO_PARA"], "")).strip(),
            "email_solicitado": str(linha.get(COL["EMAIL_SOL"], "")).strip(),
            "aberto_por": str(linha.get(COL["ABERTO_POR"], "")).strip(),
            "aberto_em": pd.to_datetime(linha.get(COL["ABERTO_EM"])) \
                if pd.notna(linha.get(COL["ABERTO_EM"])) else None,
            "atualizado_em": pd.to_datetime(linha[COL["ATUALIZADO_EM"]]),
            "item": str(linha.get(COL["ITEM"], "")).strip(),
            "empresa": str(linha.get(COL["EMPRESA"], "")).strip(),
            "canal": str(linha.get(COL["CANAL"], "")).strip(),
            "local": str(linha.get(COL["LOCAL"], "")).strip(),
            "descricao": str(linha[COL["DESCRICAO"]]).strip(),
            "status": str(linha.get(COL["STATUS"], "")).strip(),
            "grupo_atribuicao": str(linha.get(COL["GRUPO_ATRIB"], "")).strip(),
            "atribuido_a": str(linha.get(COL["ATRIBUIDO_A"], "")).strip(),
            "email_extra": str(linha.get(COL["EMAIL_EXTRA"], "")).strip(),
            "comentarios": str(linha.get(COL["COMENT"], "")).strip(),
        }

        #Verifica se já existe ticket com este Numero

        ticket = db.query(Ticket).filter(Ticket.numero == valores["numero"]).first()

        #se não existe, inser um novo
        if ticket is None:
            db.add(Ticket(**valores))

            registrar_log("inserido", descricao = valores["descricao"])
            inseridos += 1

        else:
            if valores["atualizado_em"] > ticket.atualizado_em:
                for campo, valor in valores.items():
                    setattr(ticket, campo, valor)

                registrar_log("atualizado", ticket_id=ticket.id)
                atualizados += 1

            else:
                registrar_log("nao inserido", ticket_id=ticket.id)
                nao_atualizados += 1


    #Retorna um resumo simples
    db.commit()
    return {
        "inseridos": inseridos,
        "atualizados": atualizados,
        "nao_atualizados": nao_atualizados
    }


