import os
import requests

API_PRINCIPAL_URL = os.getenv(
    "API_PRINCIPAL_URL",
    "http://127.0.0.1:5000"
)


def buscar_iphones():
    resposta = requests.get(
        f"{API_PRINCIPAL_URL}/iphones",
        timeout=10
    )

    resposta.raise_for_status()
    dados = resposta.json()

    return dados.get("iphones", [])


def buscar_iphone_por_id(iphone_id):
    iphones = buscar_iphones()

    for iphone in iphones:
        if iphone["id"] == iphone_id:
            return iphone

    return None