import logging
from datetime import datetime

# Arquivo que ficará os logs
log_file = "tickets.log"

def registrar_log(acao: str, ticket_id: int = None, descricao: str = None):
    # Aqui elle registra uma ação no arquivo tickets.log e no console

    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    if acao == "inserido":
        mensagem = f"[{timestamp}] -- Novo ticket inserido | id = {ticket_id} | desc = {descricao}"
    elif acao == "atualizado":
        mensagem = f"[{timestamp}] -- Ticket atualizado | id = {ticket_id}"
    elif acao == "nao_atualizado":
        mensagem = f"[{timestamp}] -- Ticket não atuallizado (sem alteração) | id = {ticket_id}"

    else: mensagem = f"[{timestamp}] | {acao} | {descricao}"

    # Salva no arquivo
    with open(log_file, "a",encoding="utf-8") as f:
        f.write(mensagem + "\n")

    # Mostar no console
    print(mensagem)