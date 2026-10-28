
import requests
from flask_restx import Resource

from services.iphone_service import buscar_iphones
from services.currency_service import converter_iphone_para_real


def registrar_rotas_ranking(api):

    @api.route("/ranking-precos")
    class RankingPrecos(Resource):

        def get(self):
            try:
                iphones = buscar_iphones()

                if not iphones:
                    return {
                        "mensagem": "Nenhum iPhone cadastrado."
                    }, 404

                ranking = []
                nao_convertidos = []

                for iphone in iphones:
                    try:
                        resultado = converter_iphone_para_real(iphone)
                        ranking.append(resultado)

                    except (requests.RequestException, ValueError):
                        nao_convertidos.append({
                            "id": iphone["id"],
                            "modelo": iphone["modelo"],
                            "pais": iphone["pais"],
                            "moeda": iphone["moeda"]
                        })

                if not ranking:
                    return {
                        "mensagem": (
                            "Não foi possível converter nenhum iPhone."
                        )
                    }, 502

                # Ordena do mais barato para o mais caro
                ranking = sorted(
                    ranking,
                    key=lambda item: item["preco_em_reais"]
                )

                # Adiciona a posição no ranking
                for posicao, item in enumerate(ranking, start=1):
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
                        "Erro ao buscar os iPhones na API principal."
                    ),
                    "erro": str(erro)
                }, 502
