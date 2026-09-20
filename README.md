# GlobalPhone Compare Service

API Secundária do MVP **GlobalPhone Compare**, responsável pelas regras de negócio relacionadas à conversão, comparação, classificação, cálculo de economia e ranking de preços de iPhones.

A API trabalha integrada à **GlobalPhone Compare API (API Principal)**, buscando os iPhones previamente cadastrados e utilizando seus identificadores (`id`) para realizar as operações.

Também é utilizada a API externa **Frankfurter** para obtenção das taxas de câmbio e conversão dos preços para Real (BRL).

---

## Funcionalidades

- Busca de iPhones cadastrados na API Principal
- Conversão automática de preços para Real (BRL)
- Consulta automática da cotação da moeda
- Comparação entre dois iPhones
- Identificação da opção mais econômica
- Cálculo da economia entre dois iPhones
- Cálculo percentual da economia
- Classificação de preços
- Ranking automático do mais barato ao mais caro
- Comunicação REST entre API Principal e API Secundária
- Integração com API externa de câmbio
- Documentação interativa com Swagger
- Execução em container Docker

---

## Tecnologias

- Python 3.11
- Flask
- Flask-RESTX
- Requests
- Swagger
- Docker
- REST API
- Frankfurter API

---

## Estrutura do Projeto

```text
globalphone-compare-service/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
└── README.md
```

### Descrição dos Arquivos

- `app.py`: implementação da API Secundária e suas regras de negócio.
- `requirements.txt`: dependências Python utilizadas pelo projeto.
- `Dockerfile`: configuração da imagem Docker da API.
- `.dockerignore`: arquivos ignorados durante a construção da imagem Docker.
- `.gitignore`: arquivos e diretórios que não devem ser versionados.
- `README.md`: documentação do projeto.

---

# Rotas da API

| Método | Endpoint | Descrição |
|---|---|---|
| `GET` | `/` | Verifica se o Service está funcionando |
| `GET` | `/converter-preco/{id}` | Converte automaticamente o preço de um iPhone para BRL |
| `GET` | `/classificar-preco/{id}` | Classifica o preço do iPhone |
| `GET` | `/comparar-precos/{id1}/{id2}` | Compara dois iPhones cadastrados |
| `GET` | `/calcular-economia/{id1}/{id2}` | Calcula a economia entre dois iPhones |
| `GET` | `/ranking-precos` | Gera um ranking automático dos iPhones por preço em BRL |

Os iPhones utilizados nessas operações são buscados automaticamente na **API Principal**.

---

# Conversão de Preço

## GET `/converter-preco/{id}`

Realiza a conversão do preço de um iPhone cadastrado na API Principal.

É necessário informar apenas o `id`.

Exemplo:

```text
GET /converter-preco/1
```

O Service:

1. Busca o iPhone de ID `1` na API Principal.
2. Obtém o preço e a moeda cadastrados.
3. Consulta a cotação da moeda.
4. Converte automaticamente o valor para Real (BRL).

Exemplo de resposta:

```json
{
  "id": 1,
  "modelo": "iPhone 17 Pro",
  "armazenamento": "256 GB",
  "cor": "Prata",
  "pais": "Estados Unidos",
  "moeda": "USD",
  "preco_original": 1099.0,
  "cotacao": 5.1,
  "preco_em_reais": 5604.9
}
```

Os valores apresentados são exemplos e podem variar conforme a cotação atual.

---

# Classificação de Preço

## GET `/classificar-preco/{id}`

Busca o iPhone pelo ID, converte o preço para Real e classifica o valor.

Exemplo:

```text
GET /classificar-preco/1
```

Exemplo de resposta:

```json
{
  "id": 1,
  "modelo": "iPhone 17 Pro",
  "pais": "Estados Unidos",
  "preco_em_reais": 5604.9,
  "classificacao": "Preço intermediário"
}
```

As classificações utilizadas são:

```text
Preço abaixo de R$ 5.000
→ Preço baixo

Preço entre R$ 5.000 e R$ 7.999,99
→ Preço intermediário

Preço igual ou superior a R$ 8.000
→ Preço alto
```

---

# Comparação de Preços

## GET `/comparar-precos/{id1}/{id2}`

Compara dois iPhones cadastrados na API Principal.

É necessário informar somente os IDs.

Exemplo:

```text
GET /comparar-precos/1/2
```

O Service busca os dois registros, converte seus preços para Real e identifica qual possui o menor valor.

Exemplo de resposta:

```json
{
  "iphone_1": {
    "id": 1,
    "modelo": "iPhone 17 Pro",
    "pais": "Estados Unidos",
    "moeda": "USD",
    "preco_original": 1099.0,
    "preco_em_reais": 5604.9
  },
  "iphone_2": {
    "id": 2,
    "modelo": "iPhone 17 Pro",
    "pais": "Brasil",
    "moeda": "BRL",
    "preco_original": 11999.0,
    "preco_em_reais": 11999.0
  },
  "melhor_opcao": {
    "id": 1,
    "modelo": "iPhone 17 Pro",
    "pais": "Estados Unidos",
    "preco_em_reais": 5604.9
  },
  "economia": 6394.1
}
```

---

# Cálculo de Economia

## GET `/calcular-economia/{id1}/{id2}`

Calcula a diferença de preço entre dois iPhones.

Exemplo:

```text
GET /calcular-economia/1/2
```

Exemplo de resposta:

```json
{
  "iphone_1": {
    "id": 1,
    "modelo": "iPhone 17 Pro",
    "pais": "Estados Unidos",
    "preco_em_reais": 5604.9
  },
  "iphone_2": {
    "id": 2,
    "modelo": "iPhone 17 Pro",
    "pais": "Brasil",
    "preco_em_reais": 11999.0
  },
  "mais_barato": {
    "id": 1,
    "modelo": "iPhone 17 Pro",
    "pais": "Estados Unidos"
  },
  "economia": 6394.1,
  "economia_percentual": 53.29
}
```

---

# Ranking de Preços

## GET `/ranking-precos`

Não é necessário informar nenhum parâmetro.

O Service:

1. Busca todos os iPhones cadastrados na API Principal.
2. Obtém a moeda de cada registro.
3. Consulta a cotação quando necessário.
4. Converte todos os valores para BRL.
5. Ordena os iPhones do menor para o maior preço.

Exemplo:

```text
GET /ranking-precos
```

Exemplo de resposta:

```json
{
  "mais_barato": {
    "id": 1,
    "modelo": "iPhone 17 Pro",
    "pais": "Estados Unidos",
    "moeda": "USD",
    "preco_original": 1099.0,
    "preco_em_reais": 5604.9,
    "posicao": 1
  },
  "total_iphones": 2,
  "ranking": [
    {
      "id": 1,
      "modelo": "iPhone 17 Pro",
      "pais": "Estados Unidos",
      "preco_em_reais": 5604.9,
      "posicao": 1
    },
    {
      "id": 2,
      "modelo": "iPhone 17 Pro",
      "pais": "Brasil",
      "preco_em_reais": 11999.0,
      "posicao": 2
    }
  ]
}
```

---

# Swagger UI

Com a API Secundária em execução, o Swagger estará disponível em:

```text
http://127.0.0.1:5001/
```

O Swagger permite visualizar e testar todas as rotas públicas da API.

Na maior parte das operações é necessário informar apenas o ID do iPhone previamente cadastrado na API Principal.

No endpoint:

```text
GET /ranking-precos
```

não é necessário digitar nenhum parâmetro.

---

# Como Executar Localmente

## Pré-requisitos

- Python 3.11
- pip
- GlobalPhone Compare API em execução na porta `5000`

Crie o ambiente virtual:

```powershell
python -m venv .venv
```

Ative o ambiente virtual:

```powershell
.venv\Scripts\Activate.ps1
```

Instale as dependências:

```powershell
pip install -r requirements.txt
```

Execute a aplicação:

```powershell
python app.py
```

A API Secundária estará disponível em:

```text
http://127.0.0.1:5001
```

---

# Dependências

Exemplo de `requirements.txt`:

```text
Flask
flask-restx
requests
```

---

# Docker

A API Secundária possui seu próprio `Dockerfile`.

Construa a imagem:

```bash
docker build -t globalphone-compare-service .
```

Execute o container:

```bash
docker run -p 5001:5001 globalphone-compare-service
```

A API estará disponível em:

```text
http://127.0.0.1:5001
```

---

# Integração com a API Principal

A API Secundária consulta os iPhones cadastrados na **GlobalPhone Compare API** através de comunicação REST.

Em ambiente local, por padrão:

```text
API Principal
http://127.0.0.1:5000

API Secundária
http://127.0.0.1:5001
```

O endereço da API Principal pode ser configurado através da variável de ambiente:

```text
API_PRINCIPAL_URL
```

Valor padrão:

```text
http://127.0.0.1:5000
```

---

# Integração com a Frankfurter API

Para preços cadastrados em moedas diferentes de `BRL`, o Service consulta a API externa **Frankfurter**.

Exemplo de fluxo:

```text
USD
↓
Consulta da cotação
↓
BRL
```

Quando o preço já está cadastrado em:

```text
BRL
```

não é necessária conversão e a cotação utilizada é:

```text
1.0
```

---

# Arquitetura

```text
                    GlobalPhone Compare

                       Usuário
                          |
                          v
              GlobalPhone Compare API
                   API Principal
                          |
                          |
                       SQLite
                          |
                          |
                          v
             GlobalPhone Compare Service
                  API Secundária
                          |
                          |
                       HTTPS
                          |
                          v
                  Frankfurter API
                     API Externa
```

Fluxo simplificado:

```text
Cadastro do iPhone
        ↓
GlobalPhone Compare API
        ↓
SQLite
        ↓
GlobalPhone Compare Service
        ↓
Busca pelo ID
        ↓
Consulta da cotação
        ↓
Conversão para BRL
        ↓
Comparação / Economia / Classificação / Ranking
```

---

# Comunicação Entre os Componentes

O projeto demonstra comunicação entre componentes independentes através de APIs REST.

A **API Principal** é responsável principalmente por:

- cadastro de iPhones;
- consulta dos registros;
- alteração dos registros;
- exclusão dos registros;
- persistência dos dados no SQLite.

A **API Secundária** concentra regras de negócio relacionadas a:

- conversão;
- classificação;
- comparação;
- cálculo de economia;
- ranking de preços.

A **Frankfurter API** fornece as taxas de câmbio utilizadas nas conversões.

---

# Endpoints Internos

O Service também mantém endpoints internos utilizados para compatibilidade com a comunicação da API Principal.

Essas rotas não são exibidas no Swagger público.

Elas permitem que a API Principal envie dados para operações internas de:

- conversão de preço;
- comparação de preços.

---

# Repositórios do Projeto

## API Principal — GlobalPhone Compare API

https://github.com/biancasipas/globalphone-compare-api

## API Secundária — GlobalPhone Compare Service

https://github.com/biancasipas/globalphone-compare-service

---

# Objetivo

O **GlobalPhone Compare Service** representa um componente independente da arquitetura do MVP.

O objetivo é concentrar regras de negócio relacionadas à análise de preços de iPhones em diferentes países, demonstrando:

- desenvolvimento de APIs REST;
- comunicação entre APIs;
- consumo de API externa;
- conversão de moedas;
- separação de responsabilidades;
- arquitetura com múltiplos serviços;
- utilização de Docker;
- documentação com Swagger.

---

# Autora

**Bianca Maria Fernandes Alves**

Projeto desenvolvido como MVP da Pós-Graduação em Desenvolvimento Full Stack da PUC-Rio.