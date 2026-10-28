
import requests
from flask_restx import Resource

from services.iphone_service import buscar_iphone_por_id
from services.currency_service import converter_iphone_para_real


def registrar_rotas_economia(api):

    @api.route("/calcular-economia/<int:id1>/<int:id2>")
    class CalcularEconomia(Resource):

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

                diferenca = round(abs(preco1 - preco2), 2)
                maior_preco = max(preco1, preco2)

                if maior_preco > 0:
                    percentual = round(
                        (diferenca / maior_preco) * 100, 2
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
                        "mensagem": "Os dois possuem o mesmo preço."
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
                    "mensagem": "Erro ao calcular economia.",
                    "erro": str(erro)
                }, 502
