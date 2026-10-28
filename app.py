from flask import Flask
from flask_restx import Api, Resource

from routes.conversao_routes import registrar_rotas_conversao
from routes.classificacao_routes import registrar_rotas_classificacao
from routes.economia_routes import registrar_rotas_economia
from routes.comparacao_routes import registrar_rotas_comparacao
from routes.ranking_routes import registrar_rotas_ranking

# ============================================================
# FLASK
# ============================================================

app = Flask(__name__)

# ============================================================
# SWAGGER
# ============================================================

api = Api(
    app,
    version="1.0",
    title="GlobalPhone Compare Service - API Secundária",
    description=(
        "API secundária responsável por conversão, comparação, "
        "classificação, economia e ranking de preços de iPhones."
    )
)

registrar_rotas_conversao(api)
registrar_rotas_classificacao(api)
registrar_rotas_economia(api)
registrar_rotas_comparacao(api)
registrar_rotas_ranking(api)

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
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    )