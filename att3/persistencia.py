import json

def salvar_equipamentos(equipamentos, caminho):
    dados = []
    for equipamento in equipamentos:
        dados.append(equipamento.para_dicionario())

    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)