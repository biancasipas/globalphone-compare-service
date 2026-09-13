from flask import Flask
from flask_restx import Api, Resource, fields


app = Flask(__name__)


api = Api(
    app,
    version="1.0",
    title="GlobalPhone Compare Service",
    description="API secundária responsável por conversão e comparação de preços de iPhones."
)


# Modelo para converter um preço
conversao_model = api.model(
    "ConversaoPreco",
    {
        "preco": fields.Float(required=True),
        "cotacao": fields.Float(required=True),
        "moeda": fields.String(required=True)
    }
)


# Modelo para comparar dois preços já convertidos para reais
comparacao_model = api.model(
    "ComparacaoPrecos",
    {
        "pais_1": fields.String(required=True),
        "preco_1": fields.Float(required=True),
        "pais_2": fields.String(required=True),
        "preco_2": fields.Float(required=True)
    }
)


# Rota inicial
@api.route("/")
class Home(Resource):

    def get(self):
        return {
            "mensagem": "GlobalPhone Compare Service funcionando!"
        }, 200


# Converte o preço utilizando uma cotação
@api.route("/converter-preco")
class ConverterPreco(Resource):

    @api.expect(conversao_model)
    def post(self):
        dados = api.payload

        preco = dados["preco"]
        cotacao = dados["cotacao"]

        preco_convertido = round(preco * cotacao, 2)

        return {
            "preco_original": preco,
            "moeda": dados["moeda"],
            "cotacao": cotacao,
            "preco_em_reais": preco_convertido
        }, 200


# Compara preços de dois países
@api.route("/comparar-precos")
class CompararPrecos(Resource):

    @api.expect(comparacao_model)
    def post(self):
        dados = api.payload

        pais_1 = dados["pais_1"]
        preco_1 = dados["preco_1"]

        pais_2 = dados["pais_2"]
        preco_2 = dados["preco_2"]

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


# Classifica o preço
@api.route("/classificar-preco/<preco>")
class ClassificarPreco(Resource):

    def get(self, preco):

        preco = float(preco)

        if preco < 5000:
            classificacao = "Preço baixo"

        elif preco < 8000:
            classificacao = "Preço intermediário"

        else:
            classificacao = "Preço alto"

        return {
            "preco": preco,
            "classificacao": classificacao
        }, 200


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    )