import requests


def buscar_cotacao(moeda):
    moeda = moeda.upper()

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
        raise ValueError("Cotação não encontrada.")

    return float(dados[0]["rate"])


def converter_iphone_para_real(iphone):
    preco_original = float(iphone["preco"])
    moeda = iphone["moeda"].upper()

    cotacao = buscar_cotacao(moeda)

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