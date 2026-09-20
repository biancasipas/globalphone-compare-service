# GlobalPhone Compare Service

API Secundária do MVP **GlobalPhone Compare**, responsável pelos cálculos de conversão, comparação e classificação de preços de iPhones.

A API é consumida pela **GlobalPhone Compare API (API Principal)** através de comunicação REST.

## Funcionalidades

- Conversão de preços para Real (BRL)
- Comparação de preços entre dois países
- Identificação da opção mais econômica
- Cálculo da economia entre dois preços
- Classificação de preços
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
globalphone-compare-service/
├── app.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
└── README.md
```

### Descrição dos Arquivos

- `app.py`: contém a implementação da API Secundária e suas rotas.
- `requirements.txt`: contém as dependências Python utilizadas pelo projeto.
- `Dockerfile`: define a imagem Docker da API Secundária.
- `.dockerignore`: define os arquivos e diretórios ignorados durante a construção da imagem Docker.
- `.gitignore`: define os arquivos e diretórios que não devem ser versionados no Git.
- `README.md`: contém a documentação do componente.

## Rotas da API

| Método | Endpoint | Descrição |
|---|---|---|
| `GET` | `/` | Verifica se a API Secundária está funcionando |
| `POST` | `/converter-preco` | Converte um preço utilizando a cotação recebida |
| `POST` | `/comparar-precos` | Compara dois preços e identifica a melhor opção |
| `GET` | `/classificar-preco/{preco}` | Classifica o preço informado |

## Conversão de Preço

### POST /converter-preco

Recebe o preço, a moeda e a cotação fornecidos pela API Principal.

Exemplo:

```json
{
  "preco": 1099,
  "cotacao": 5.1053,
  "moeda": "USD"
}
```

Exemplo de resposta:

```json
{
  "preco_original": 1099,
  "moeda": "USD",
  "cotacao": 5.1053,
  "preco_em_reais": 5610.72
}
```

Os valores apresentados são apenas exemplos utilizados para demonstração do MVP.

## Comparação de Preços

### POST /comparar-precos

Compara dois preços já convertidos para Real.

Exemplo:

```json
{
  "pais_1": "Estados Unidos",
  "preco_1": 5610.72,
  "pais_2": "Brasil",
  "preco_2": 11999
}
```

Exemplo de resposta:

```json
{
  "pais_1": "Estados Unidos",
  "preco_1": 5610.72,
  "pais_2": "Brasil",
  "preco_2": 11999,
  "melhor_opcao": "Estados Unidos",
  "economia": 6388.28
}
```

Os valores apresentados são apenas exemplos utilizados para demonstração do MVP.

## Classificação de Preço

### GET /classificar-preco/{preco}

Classifica o preço informado como baixo, intermediário ou alto.

Exemplo:

```text
GET /classificar-preco/5610.72
```

Exemplo de resposta:

```json
{
  "preco": 5610.72,
  "classificacao": "Preço intermediário"
}
```

## Swagger UI

Com a API Secundária em execução, o Swagger estará disponível em:

```text
http://127.0.0.1:5001/
```

O Swagger permite visualizar e testar diretamente todas as rotas da API Secundária.

## Como Executar Localmente

### Pré-requisitos

- Python 3.11
- pip

Crie o ambiente virtual:

```powershell
python -m venv .venv
```

Ative o ambiente virtual:

```powershell
.venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute a aplicação:

```bash
python app.py
```

A API estará disponível em:

```text
http://127.0.0.1:5001
```

## Docker

A API Secundária possui seu próprio `Dockerfile`, permitindo sua execução em container independente.

Construa a imagem:

```bash
docker build -t globalphone-service .
```

Execute o container:

```bash
docker run -p 5001:5001 globalphone-service
```

A API estará disponível em:

```text
http://127.0.0.1:5001
```

## Integração com a API Principal

A **GlobalPhone Compare API** utiliza esta API para realizar os cálculos de conversão e comparação de preços.

A comunicação entre os componentes é realizada através de requisições REST.

Durante a execução com Docker Compose, a API Principal acessa a API Secundária através do endereço:

```text
http://api-secundaria:5001
```

O arquivo `docker-compose.yml` responsável pela orquestração dos dois serviços está localizado no repositório da **API Principal**.

## Arquitetura

A API Secundária faz parte do **Cenário 2** utilizado no MVP.

```text
                    GlobalPhone Compare

Frankfurter API
  API Externa
       |
       | HTTPS / REST
       v
GlobalPhone Compare API
     API Principal
       |       |
       |       └──── SQLite
       |
       | REST
       v
GlobalPhone Compare Service
     API Secundária
```

A consulta à API externa de câmbio é responsabilidade da **API Principal**.

A API Secundária recebe os valores necessários e executa as regras de negócio relacionadas à conversão, comparação e classificação dos preços.

## Repositórios do Projeto

### API Principal — GlobalPhone Compare API

https://github.com/biancasipas/globalphone-compare-api

### API Secundária — GlobalPhone Compare Service

https://github.com/biancasipas/globalphone-compare-service

## Objetivo

Esta API representa um componente independente da arquitetura do MVP, concentrando as regras de conversão, comparação e classificação de preços.

A separação das responsabilidades permite demonstrar a comunicação REST entre componentes independentes da aplicação.

## Autora

**Bianca Maria Fernandes Alves**

Projeto desenvolvido como MVP da Pós-Graduação em Desenvolvimento Full Stack da PUC-Rio.
