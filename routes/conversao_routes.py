
import requests
from flask import request
from flask_restx import Resource

from services.iphone_service import buscar_iphone_por_id
from services.currency_service import converter_iphone_para_real


def registrar_rotas_conversao(api):

    # GET - Converter preço pelo ID
    @api.route("/converter-preco/<int:id>")
    class ConverterPreco(Resource):

        def get(self, id):
            try:
                iphone = buscar_iphone_por_id(id)

                if not iphone:
                    return {
                        "mensagem": "iPhone não encontrado."
                    }, 404

                resultado = converter_iphone_para_real(iphone)

                return resultado, 200

            except ValueError as erro:
                return {
                    "mensagem": str(erro)
                }, 404

            except requests.RequestException as erro:
                return {
                    "mensagem": "Erro ao consultar a API principal ou a cotação.",
                    "erro": str(erro)
                }, 502

    # POST - Conversão interna utilizada pela API principal
    @api.route("/converter-preco")
    class ConverterPrecoInterno(Resource):

        @api.doc(False)
        def post(self):
            dados = request.get_json(silent=True) or {}

            if any(
                campo not in dados
                for campo in ("preco", "cotacao", "moeda")
            ):
                return {
                    "mensagem": "Dados de conversão inválidos."
                }, 400

            preco = float(dados["preco"])
            cotacao = float(dados["cotacao"])
            moeda = dados["moeda"].upper()

            preco_em_reais = round(preco * cotacao, 2)

            return {
                "preco_original": preco,
                "moeda": moeda,
                "cotacao": cotacao,
                "preco_em_reais": preco_em_reais
            }, 200
