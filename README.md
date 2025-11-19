# ETL de Tickets – FastAPI + SQLite

Projeto‐exemplo que implementa um fluxo **ETL** (Extract-Transform-Load) a partir de uma planilha Excel de chamados de TI.  
A API lê o arquivo, valida os dados, grava ou atualiza registros em banco e gera logs de todas as ações.

> **Objetivo** – entrega de teste prático (vaga Python/Back-end).

---

## Tecnologias

| Camada | Stack | Observações |
|--------|-------|-------------|
| API | FastAPI + Uvicorn | Swagger automático em `/docs` |
| ORM / DB | SQLAlchemy + SQLite | 100 % portável; nenhum servidor externo |
| ETL | pandas + openpyxl | Leitura de `.xlsx` |
| Logs | logging (Python) | Salvo em `tickets.log` |

---

## Estrutura do Projeto
```
.
├── controllers/
│   └── routes.py          # Endpoints da API
├── models/
│   └── models.py          # Modelos SQLAlchemy + Pydantic
├── services/
│   └── services.py        # Regras de negócio / ETL
├── utils/
│   └── utils.py           # Helpers (logs)
├── database.py            # Conexão + Base SQLAlchemy
├── main.py                # Ponto de entrada FastAPI
├── requirements.txt       # Dependências
└── README.md
```

Arquivos gerados em runtime  

tickets.db   → banco SQLite
tickets.log  → logs detalhados


---

## Como Executar

#### 1. Clone o repositório e acesse a pasta:

```
git clone https://github.com/<seu_user>/etl-tickets-fastapi.git
cd etl-tickets-fastapi
```

#### 2. Crie um ambiente virtuall (opcional) e instale as dependências:
    

```
python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
```

#### 3. Suba a API em modo desenvolvimento:

```
uvicorn main:app --reload
```
#### 4. Abra no navegador:

-  Documentação Swagger: http://localhost:8000/docs
-  Health check: http://localhost:8000/health

---

## Endpoints Principais

| Método | Rota | Descrição
|--------|-------|-------------|
|GET | / | Mensagem simples de “API funcionando”|
|GET | /health | Retorna {"status":"ok"}|
|POST | /upload | Upload de planilha Excel (campo file)|

#### Exemplo de Requisição POST /upload (curl)
```
curl -X POST http://localhost:8000/upload \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@planilha_tickets.xlsx"
```

Resposta esperada:
```
{
  "mensagem": "Upload processado com sucesso!",
  "resumo": {
    "inseridos": 10,
    "atualizados": 3,
    "nao_atualizados": 5
  }
}
```

Estrutura da Planilha

A planilha deve conter as colunas abaixo com estes cabeçalhos:

|Cabeçalho na planilha | Campo no banco|
|--------|-------------|
|Número | numero|
|Solicitado(a) para | solicitado_para|
|E-mail | email_solicitado|
|Aberto por | aberto_por|
|Aberto | aberto_em|
|Atualizado em | atualizado_em|
|Item | item|
|Empresa | empresa|
|Canal | canal|
|Local | local|
|Descrição | descricao|
|Status | status|
|Grupo de atribuição | grupo_atribuicao|
|Atribuído a | atribuido_a|
|E-mail | email_extra|
|Comentários adicionais | comentarios|

#### Regras implementadas

- Duplicidade → chave pelo campo Número.
- Atualização → só ocorre se Atualizado em da planilha for maior que o valor armazenado.
- Logs →
   - Novo ticket inserido
   - Ticket atualizado
   - Ticket não atualizado (sem alteração)


## Banco de Dados

 - Arquivo: tickets.db (SQLite)
 - Tabela: tickets
