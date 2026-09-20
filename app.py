import os

from flask import Flask, request
from flask_restx import Api, Resource
import requests


# ============================================================
# FLASK
# ============================================================

app = Flask(__name__)


# ============================================================
# API PRINCIPAL
# ============================================================

API_PRINCIPAL_URL = os.getenv(
    "API_PRINCIPAL_URL",
    "http://127.0.0.1:5000"
)


# ============================================================
# SWAGGER
# ============================================================

api = Api(
    app,
    version="1.0",
    title="GlobalPhone Compare Service",
    description=(
        "API secundária responsável por conversão, comparação, "
        "classificação, economia e ranking de preços de iPhones."
    )
)


# ============================================================
# FUNÇÃO - BUSCAR TODOS OS IPHONES DA API PRINCIPAL
# ============================================================

def buscar_iphones():

    resposta = requests.get(
        f"{API_PRINCIPAL_URL}/iphones",
        timeout=10
    )

    resposta.raise_for_status()

    dados = resposta.json()

    return dados.get(
        "iphones",
        []
    )


# ============================================================
# FUNÇÃO - BUSCAR IPHONE PELO ID
# ============================================================

def buscar_iphone_por_id(iphone_id):

    iphones = buscar_iphones()

    for iphone in iphones:

        if iphone["id"] == iphone_id:

            return iphone

    return None


# ============================================================
# FUNÇÃO - BUSCAR COTAÇÃO PARA BRL
# ============================================================

def buscar_cotacao(moeda):

    moeda = moeda.upper()

    # Real não precisa de conversão
    if moeda == "BRL":

        return 1.0


    resposta = requests.get(
        "https://api.frankfurter.dev/v2/rates",
        params={
            "base": moeda,
            "quotes": "BRL"
        },
        timeout=10
    )

    resposta.raise_for_status()

    dados = resposta.json()


    if not dados:

        raise ValueError(
            "Cotação não encontrada."
        )


    return float(
        dados[0]["rate"]
    )


# ============================================================
# FUNÇÃO - CONVERTER UM IPHONE PARA REAL
# ============================================================

def converter_iphone_para_real(iphone):

    preco_original = float(
        iphone["preco"]
    )

    moeda = (
        iphone["moeda"]
        .upper()
    )

    cotacao = buscar_cotacao(
        moeda
    )

    preco_em_reais = round(
        preco_original * cotacao,
        2
    )


    return {
        "id": iphone["id"],
        "modelo": iphone["modelo"],
        "armazenamento": iphone["armazenamento"],
        "cor": iphone["cor"],
        "pais": iphone["pais"],
        "moeda": moeda,
        "preco_original": preco_original,
        "cotacao": cotacao,
        "preco_em_reais": preco_em_reais
    }


# ============================================================
# ROTA INICIAL
# ============================================================

@api.route("/")
class Home(Resource):

    def get(self):

        return {
            "mensagem": (
                "GlobalPhone Compare Service funcionando!"
            )
        }, 200


# ============================================================
# CONVERTER PREÇO PELO ID
#
# EXEMPLO:
# GET /converter-preco/1
#
# VOCÊ DIGITA SOMENTE O ID.
# ============================================================

@api.route("/converter-preco/<int:id>")
class ConverterPreco(Resource):

    def get(self, id):

        try:

            iphone = buscar_iphone_por_id(
                id
            )


            if not iphone:

                return {
                    "mensagem": (
                        "iPhone não encontrado."
                    )
                }, 404


            resultado = converter_iphone_para_real(
                iphone
            )


            return resultado, 200


        except ValueError as erro:

            return {
                "mensagem": str(erro)
            }, 404


        except requests.RequestException as erro:

            return {
                "mensagem": (
                    "Erro ao consultar a API "
                    "principal ou a cotação."
                ),
                "erro": str(erro)
            }, 502


# ============================================================
# CONVERSOR INTERNO
#
# NÃO APARECE NO SWAGGER.
#
# Mantém compatibilidade com a API principal atual,
# que envia preço + cotação + moeda por POST.
# ============================================================

@api.route("/converter-preco")
class ConverterPrecoInterno(Resource):

    @api.doc(False)
    def post(self):

        dados = request.get_json(
            silent=True
        ) or {}


        if (
            "preco" not in dados
            or "cotacao" not in dados
            or "moeda" not in dados
        ):

            return {
                "mensagem": (
                    "Dados de conversão inválidos."
                )
            }, 400


        preco = float(
            dados["preco"]
        )

        cotacao = float(
            dados["cotacao"]
        )

        moeda = (
            dados["moeda"]
            .upper()
        )


        preco_em_reais = round(
            preco * cotacao,
            2
        )


        return {
            "preco_original": preco,
            "moeda": moeda,
            "cotacao": cotacao,
            "preco_em_reais": preco_em_reais
        }, 200


# ============================================================
# CLASSIFICAR PREÇO PELO ID
#
# EXEMPLO:
# GET /classificar-preco/1
# ============================================================

@api.route("/classificar-preco/<int:id>")
class ClassificarPreco(Resource):

    def get(self, id):

        try:

            iphone = buscar_iphone_por_id(
                id
            )


            if not iphone:

                return {
                    "mensagem": (
                        "iPhone não encontrado."
                    )
                }, 404


            resultado = converter_iphone_para_real(
                iphone
            )


            preco = resultado[
                "preco_em_reais"
            ]


            if preco < 5000:

                classificacao = (
                    "Preço baixo"
                )


            elif preco < 8000:

                classificacao = (
                    "Preço intermediário"
                )


            else:

                classificacao = (
                    "Preço alto"
                )


            return {
                "id": iphone["id"],
                "modelo": iphone["modelo"],
                "pais": iphone["pais"],
                "preco_em_reais": preco,
                "classificacao": classificacao
            }, 200


        except ValueError as erro:

            return {
                "mensagem": str(erro)
            }, 404


        except requests.RequestException as erro:

            return {
                "mensagem": (
                    "Erro ao classificar preço."
                ),
                "erro": str(erro)
            }, 502


# ============================================================
# CALCULAR ECONOMIA ENTRE DOIS IPHONES
#
# EXEMPLO:
# GET /calcular-economia/1/2
#
# VOCÊ DIGITA SOMENTE:
# id1 = 1
# id2 = 2
# ============================================================

@api.route(
    "/calcular-economia/<int:id1>/<int:id2>"
)
class CalcularEconomia(Resource):

    def get(self, id1, id2):

        try:

            iphone1 = buscar_iphone_por_id(
                id1
            )

            iphone2 = buscar_iphone_por_id(
                id2
            )


            if not iphone1 or not iphone2:

                return {
                    "mensagem": (
                        "Um dos iPhones "
                        "não foi encontrado."
                    )
                }, 404


            resultado1 = (
                converter_iphone_para_real(
                    iphone1
                )
            )

            resultado2 = (
                converter_iphone_para_real(
                    iphone2
                )
            )


            preco1 = resultado1[
                "preco_em_reais"
            ]

            preco2 = resultado2[
                "preco_em_reais"
            ]


            diferenca = round(
                abs(
                    preco1 - preco2
                ),
                2
            )


            menor_preco = min(
                preco1,
                preco2
            )


            maior_preco = max(
                preco1,
                preco2
            )


            if maior_preco > 0:

                percentual = round(
                    (
                        diferenca
                        / maior_preco
                    ) * 100,
                    2
                )

            else:

                percentual = 0


            if preco1 < preco2:

                mais_barato = {
                    "id": iphone1["id"],
                    "modelo": iphone1["modelo"],
                    "pais": iphone1["pais"]
                }


            elif preco2 < preco1:

                mais_barato = {
                    "id": iphone2["id"],
                    "modelo": iphone2["modelo"],
                    "pais": iphone2["pais"]
                }


            else:

                mais_barato = {
                    "mensagem": (
                        "Os dois possuem "
                        "o mesmo preço."
                    )
                }


            return {
                "iphone_1": {
                    "id": iphone1["id"],
                    "modelo": iphone1["modelo"],
                    "pais": iphone1["pais"],
                    "preco_em_reais": preco1
                },
                "iphone_2": {
                    "id": iphone2["id"],
                    "modelo": iphone2["modelo"],
                    "pais": iphone2["pais"],
                    "preco_em_reais": preco2
                },
                "mais_barato": mais_barato,
                "economia": diferenca,
                "economia_percentual": percentual
            }, 200


        except ValueError as erro:

            return {
                "mensagem": str(erro)
            }, 404


        except requests.RequestException as erro:

            return {
                "mensagem": (
                    "Erro ao calcular economia."
                ),
                "erro": str(erro)
            }, 502


# ============================================================
# COMPARAR DOIS IPHONES PELO ID
#
# EXEMPLO:
# GET /comparar-precos/1/2
#
# VOCÊ DIGITA SOMENTE:
# id1 = 1
# id2 = 2
# ============================================================

@api.route(
    "/comparar-precos/<int:id1>/<int:id2>"
)
class CompararPrecos(Resource):

    def get(self, id1, id2):

        try:

            iphone1 = buscar_iphone_por_id(
                id1
            )

            iphone2 = buscar_iphone_por_id(
                id2
            )


            if not iphone1 or not iphone2:

                return {
                    "mensagem": (
                        "Um dos iPhones "
                        "não foi encontrado."
                    )
                }, 404


            resultado1 = (
                converter_iphone_para_real(
                    iphone1
                )
            )

            resultado2 = (
                converter_iphone_para_real(
                    iphone2
                )
            )


            preco1 = resultado1[
                "preco_em_reais"
            ]

            preco2 = resultado2[
                "preco_em_reais"
            ]


            if preco1 < preco2:

                melhor_opcao = {
                    "id": iphone1["id"],
                    "modelo": iphone1["modelo"],
                    "pais": iphone1["pais"],
                    "preco_em_reais": preco1
                }

                economia = round(
                    preco2 - preco1,
                    2
                )


            elif preco2 < preco1:

                melhor_opcao = {
                    "id": iphone2["id"],
                    "modelo": iphone2["modelo"],
                    "pais": iphone2["pais"],
                    "preco_em_reais": preco2
                }

                economia = round(
                    preco1 - preco2,
                    2
                )


            else:

                melhor_opcao = {
                    "mensagem": (
                        "Os dois possuem "
                        "o mesmo preço."
                    )
                }

                economia = 0


            return {
                "iphone_1": resultado1,
                "iphone_2": resultado2,
                "melhor_opcao": melhor_opcao,
                "economia": economia
            }, 200


        except ValueError as erro:

            return {
                "mensagem": str(erro)
            }, 404


        except requests.RequestException as erro:

            return {
                "mensagem": (
                    "Erro ao comparar os iPhones."
                ),
                "erro": str(erro)
            }, 502


# ============================================================
# COMPARAÇÃO INTERNA
#
# NÃO APARECE NO SWAGGER.
#
# Mantém compatibilidade com a API principal atual.
# ============================================================

@api.route("/comparar-precos")
class CompararPrecosInterno(Resource):

    @api.doc(False)
    def post(self):

        dados = request.get_json(
            silent=True
        ) or {}


        campos = [
            "pais_1",
            "preco_1",
            "pais_2",
            "preco_2"
        ]


        for campo in campos:

            if campo not in dados:

                return {
                    "mensagem": (
                        "Dados de comparação "
                        "inválidos."
                    )
                }, 400


        pais_1 = dados["pais_1"]

        preco_1 = float(
            dados["preco_1"]
        )

        pais_2 = dados["pais_2"]

        preco_2 = float(
            dados["preco_2"]
        )


        if preco_1 < preco_2:

            melhor_pais = pais_1

            economia = round(
                preco_2 - preco_1,
                2
            )


        elif preco_2 < preco_1:

            melhor_pais = pais_2

            economia = round(
                preco_1 - preco_2,
                2
            )


        else:

            melhor_pais = (
                "Mesmo preço"
            )

            economia = 0


        return {
            "pais_1": pais_1,
            "preco_1": preco_1,
            "pais_2": pais_2,
            "preco_2": preco_2,
            "melhor_opcao": melhor_pais,
            "economia": economia
        }, 200


# ============================================================
# RANKING DE PREÇOS
#
# NÃO PRECISA DIGITAR NADA.
#
# O SERVICE BUSCA AUTOMATICAMENTE TODOS OS IPHONES
# CADASTRADOS NA API PRINCIPAL.
# ============================================================

@api.route("/ranking-precos")
class RankingPrecos(Resource):

    def get(self):

        try:

            iphones = buscar_iphones()


            if not iphones:

                return {
                    "mensagem": (
                        "Nenhum iPhone cadastrado."
                    )
                }, 404


            ranking = []

            nao_convertidos = []


            for iphone in iphones:

                try:

                    resultado = (
                        converter_iphone_para_real(
                            iphone
                        )
                    )

                    ranking.append(
                        resultado
                    )


                except (
                    requests.RequestException,
                    ValueError
                ):

                    nao_convertidos.append({
                        "id": iphone["id"],
                        "modelo": iphone["modelo"],
                        "pais": iphone["pais"],
                        "moeda": iphone["moeda"]
                    })


            if not ranking:

                return {
                    "mensagem": (
                        "Não foi possível converter "
                        "nenhum iPhone."
                    )
                }, 502


            # Ordena do mais barato
            # para o mais caro
            ranking = sorted(
                ranking,
                key=lambda item: (
                    item["preco_em_reais"]
                )
            )


            # Adiciona posição
            for posicao, item in enumerate(
                ranking,
                start=1
            ):

                item["posicao"] = posicao


            return {
                "mais_barato": ranking[0],
                "total_iphones": len(ranking),
                "ranking": ranking,
                "nao_convertidos": nao_convertidos
            }, 200


        except requests.RequestException as erro:

            return {
                "mensagem": (
                    "Erro ao buscar os iPhones "
                    "na API principal."
                ),
                "erro": str(erro)
            }, 502


# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    )