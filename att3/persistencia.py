"""Leitura e gravação dos equipamentos em um arquivo JSON."""

import json
import os

from modelos import Roteador, Servidor


def salvar_equipamentos(equipamentos, caminho):
    """Grava a lista de equipamentos no arquivo, como uma lista de objetos JSON."""
    dados = [equipamento.para_dicionario() for equipamento in equipamentos]

    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)


def _criar_equipamento(item):
    """Cria o objeto da classe certa a partir de um dicionário lido do JSON."""
    tipo = item["tipo"]

    if tipo == "ROTEADOR":
        equipamento = Roteador(
            item["id_ativo"], item["nome"], item["ip"], item["quantidade_portas"]
        )
    elif tipo == "SERVIDOR":
        equipamento = Servidor(
            item["id_ativo"], item["nome"], item["ip"], item["sistema_operacional"]
        )
    else:
        raise ValueError(f"Tipo de equipamento desconhecido: {tipo}")

    equipamento.vulnerabilidades = list(item.get("vulnerabilidades", []))
    return equipamento


def carregar_equipamentos(caminho):
    """Lê o arquivo e recria os objetos. Se o arquivo não existir, devolve lista vazia."""
    if not os.path.exists(caminho):
        return []

    with open(caminho, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    return [_criar_equipamento(item) for item in dados]