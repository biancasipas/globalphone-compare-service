
import requests
from flask import request
from flask_restx import Resource

from services.iphone_service import buscar_iphone_por_id
from services.currency_service import converter_iphone_para_real


def registrar_rotas_comparacao(api):

    # =========================================
    # GET - COMPARAR DOIS IPHONES PELO ID
    # =========================================

    @api.route("/comparar-precos/<int:id1>/<int:id2>")
    class CompararPrecos(Resource):

        def get(self, id1, id2):
            try:
                iphone1 = buscar_iphone_por_id(id1)
                iphone2 = buscar_iphone_por_id(id2)

                if not iphone1 or not iphone2:
                    return {
                        "mensagem": "Um dos iPhones não foi encontrado."
                    }, 404

                resultado1 = converter_iphone_para_real(iphone1)
                resultado2 = converter_iphone_para_real(iphone2)

                preco1 = resultado1["preco_em_reais"]
                preco2 = resultado2["preco_em_reais"]

                if preco1 < preco2:
                    melhor_opcao = {
                        "id": iphone1["id"],
                        "modelo": iphone1["modelo"],
                        "pais": iphone1["pais"],
                        "preco_em_reais": preco1
                    }
                    economia = round(preco2 - preco1, 2)

                elif preco2 < preco1:
                    melhor_opcao = {
                        "id": iphone2["id"],
                        "modelo": iphone2["modelo"],
                        "pais": iphone2["pais"],
                        "preco_em_reais": preco2
                    }
                    economia = round(preco1 - preco2, 2)

                else:
                    melhor_opcao = {
                        "mensagem": "Os dois possuem o mesmo preço."
                    }
                    economia = 0

                return {
                    "iphone_1": resultado1,
                    "iphone_2": resultado2,
                    "melhor_opcao": melhor_opcao,
                    "economia": economia
                }, 200

            except ValueError as erro:
                return {"mensagem": str(erro)}, 404

            except requests.RequestException as erro:
                return {
                    "mensagem": "Erro ao comparar os iPhones.",
                    "erro": str(erro)
                }, 502

    # =========================================
    # POST - COMPARAÇÃO INTERNA
    # USADA PELA API PRINCIPAL
    # =========================================

    @api.route("/comparar-precos")
    class CompararPrecosInterno(Resource):

        @api.doc(False)
        def post(self):
            dados = request.get_json(silent=True) or {}

            campos = [
                "pais_1",
                "preco_1",
                "pais_2",
                "preco_2"
            ]

            for campo in campos:
                if campo not in dados:
                    return {
                        "mensagem": "Dados de comparação inválidos."
                    }, 400

            pais_1 = dados["pais_1"]
            preco_1 = float(dados["preco_1"])
            pais_2 = dados["pais_2"]
            preco_2 = float(dados["preco_2"])

            if preco_1 < preco_2:
                melhor_pais = pais_1
                economia = round(preco_2 - preco_1, 2)

            elif preco_2 < preco_1:
                melhor_pais = pais_2
                economia = round(preco_1 - preco_2, 2)

            else:
                melhor_pais = "Mesmo preço"
                economia = 0

            return {
                "pais_1": pais_1,
                "preco_1": preco_1,
                "pais_2": pais_2,
                "preco_2": preco_2,
                "melhor_opcao": melhor_pais,
                "economia": economia
            }, 200
