
import requests
from flask_restx import Resource

from services.iphone_service import buscar_iphone_por_id
from services.currency_service import converter_iphone_para_real


def registrar_rotas_classificacao(api):

    @api.route("/classificar-preco/<int:id>")
    class ClassificarPreco(Resource):

        def get(self, id):
            try:
                iphone = buscar_iphone_por_id(id)

                if not iphone:
                    return {
                        "mensagem": "iPhone não encontrado."
                    }, 404

                resultado = converter_iphone_para_real(iphone)
                preco = resultado["preco_em_reais"]

                if preco < 5000:
                    classificacao = "Preço baixo"
                elif preco < 8000:
                    classificacao = "Preço intermediário"
                else:
                    classificacao = "Preço alto"

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
                    "mensagem": "Erro ao classificar preço.",
                    "erro": str(erro)
                }, 502
