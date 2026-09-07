# Travel Planner Service

API Secundária do MVP **Travel Planner**, responsável pelos cálculos e regras de planejamento das viagens.

A API é consumida pela **Travel Planner API (API Principal)** através de comunicação REST.

## Funcionalidades

- Cálculo do gasto médio por dia
- Classificação do orçamento
- Cálculo da quantidade de dias da viagem
- Geração de informações de planejamento
- Comunicação REST com a API Principal
- Documentação interativa com Swagger
- Execução em container Docker

## Tecnologias

- Python 3.11
- Flask
- Flask-RESTX
- Swagger
- Docker

## Estrutura do Projeto

```text
travel-planner-service/
├── app.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── README.md
└── services/
    └── planejamento.py
```

## Rotas da API

| Método | Endpoint | Descrição |
|---|---|---|
| `GET` | `/` | Verifica se a API Secundária está funcionando |
| `POST` | `/planejamento` | Calcula informações do planejamento da viagem |
| `GET` | `/classificar-orcamento/{orcamento}` | Classifica o orçamento da viagem |
| `POST` | `/calcular-dias` | Calcula a quantidade de dias entre duas datas |

## Planejamento

### POST /planejamento

Recebe informações de uma viagem e calcula o gasto médio por dia.

Exemplo de requisição:

```json
{
  "destino": "Roma",
  "dias": 10,
  "orcamento": 14000
}
```

Exemplo de resposta:

```json
{
  "destino": "Roma",
  "dias": 10,
  "orcamento": 14000,
  "gasto_por_dia": 1400
}
```

## Classificação do Orçamento

### GET /classificar-orcamento/{orcamento}

Classifica o orçamento informado.

Exemplo:

```text
GET /classificar-orcamento/12000
```

Exemplo de resposta:

```json
{
  "orcamento": 12000,
  "classificacao": "Confortável"
}
```

## Cálculo de Dias

### POST /calcular-dias

Calcula a quantidade de dias entre a data de início e a data de fim da viagem.

Exemplo:

```json
{
  "data_inicio": "2027-05-10",
  "data_fim": "2027-05-20"
}
```

Exemplo de resposta:

```json
{
  "data_inicio": "2027-05-10",
  "data_fim": "2027-05-20",
  "quantidade_dias": 10
}
```

## Swagger UI

Com a API em execução, acesse:

```text
http://127.0.0.1:5001/
```

O Swagger permite visualizar e testar os endpoints da API.

## Como Executar Localmente

Ative o ambiente virtual:

```powershell
.venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute:

```bash
python app.py
```

A API estará disponível em:

```text
http://127.0.0.1:5001
```

## Docker

Construa a imagem:

```bash
docker build -t travel-planner-service .
```

Execute o container:

```bash
docker run -p 5001:5001 travel-planner-service
```

A API estará disponível em:

```text
http://127.0.0.1:5001
```

## Integração com a API Principal

A **Travel Planner API** utiliza esta API para obter informações de planejamento.

A comunicação é realizada através de requisições REST.

No Docker Compose, a API Principal acessa este serviço utilizando:

```text
http://api-secundaria:5001
```

## Arquitetura

```text
Travel Planner API
    API Principal
         |
         | REST
         v
Travel Planner Service
    API Secundária
```

## Objetivo

Esta API representa um componente independente da arquitetura do MVP, concentrando as regras e cálculos relacionados ao planejamento das viagens.