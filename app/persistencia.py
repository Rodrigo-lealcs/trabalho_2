"""Salvar e ler os dados nos arquivos JSON.

Cada arquivo é uma lista de objetos: [ {...}, {...} ].
Aqui só se lê e se grava; as regras ficam no inventario.py.
"""

import json
import os

from erros import ErroInventario
from modelos import (BancoDeDados, Notebook, Outro, Roteador, Servidor, Severidade,
                     Status, Vulnerabilidade)


def _salvar_json(lista, caminho):
    os.makedirs(os.path.dirname(os.path.abspath(caminho)), exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(lista, arquivo, indent=4, ensure_ascii=False)


def _ler_json(caminho):
    """Devolve a lista do arquivo. Se o arquivo não existe, devolve lista vazia."""
    if not os.path.exists(caminho):
        return []
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            lista = json.load(arquivo)
    except json.JSONDecodeError:
        raise ErroInventario(f"O arquivo '{caminho}' está com o JSON quebrado.")
    if not isinstance(lista, list):
        raise ErroInventario(f"O arquivo '{caminho}' deveria conter uma lista.")
    return lista


def equipamento_de_dicionario(dados):
    """Cria o objeto da classe certa olhando o campo 'tipo' (como no trabalho anterior)."""
    base = (dados["id_ativo"], dados["nome"], dados["ip"],
            dados["responsavel"], dados["setor"])
    tipo = dados["tipo"]
    if tipo == "ROTEADOR":
        equipamento = Roteador(*base, dados["quantidade_portas"])
    elif tipo == "SERVIDOR":
        equipamento = Servidor(*base, dados["sistema_operacional"])
    elif tipo == "NOTEBOOK":
        equipamento = Notebook(*base, dados["patrimonio"])
    elif tipo == "BANCO_DE_DADOS":
        equipamento = BancoDeDados(*base, dados["sgbd"])
    elif tipo == "OUTRO":
        equipamento = Outro(*base, dados["descricao_tipo"])
    else:
        raise ErroInventario(f"Tipo desconhecido no arquivo: {tipo}")
    equipamento.vulnerabilidades = list(dados["vulnerabilidades"])
    for dep in dados["dependencias"]:
        equipamento.dependencias[dep["depende_de"]] = dep["fracao"]
    return equipamento


def vulnerabilidade_de_dicionario(dados):
    return Vulnerabilidade(dados["id_vuln"], dados["descricao"], dados["categoria"],
                           Severidade[dados["severidade"]], Status[dados["status"]])


def salvar_equipamentos(equipamentos, caminho):
    _salvar_json([e.para_dicionario() for e in equipamentos], caminho)


def carregar_equipamentos(caminho):
    resultado = []
    for dados in _ler_json(caminho):
        try:
            resultado.append(equipamento_de_dicionario(dados))
        except (KeyError, TypeError):
            raise ErroInventario(f"Um registro de '{caminho}' está incompleto ou inválido.")
    return resultado


def salvar_vulnerabilidades(vulnerabilidades, caminho):
    _salvar_json([v.para_dicionario() for v in vulnerabilidades], caminho)


def carregar_vulnerabilidades(caminho):
    resultado = []
    for dados in _ler_json(caminho):
        try:
            resultado.append(vulnerabilidade_de_dicionario(dados))
        except (KeyError, TypeError):
            raise ErroInventario(f"Um registro de '{caminho}' está incompleto ou inválido.")
    return resultado
