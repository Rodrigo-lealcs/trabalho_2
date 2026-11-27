"""Cria dados de exemplo se ainda não existir inventário (nunca apaga dados existentes).

Uso: python dados_exemplo.py
"""

import os

import config
from inventario import Inventario


def montar():
    inv = Inventario(config.ARQ_EQUIPAMENTOS, config.ARQ_VULNERABILIDADES)
    inv.cadastrar_equipamento("roteador", "Roteador-Borda", "10.0.0.1", "Ana", "TI", 24)
    inv.cadastrar_equipamento("servidor", "Servidor-Web", "10.0.0.10", "Bruno", "TI", "Ubuntu 22.04")
    inv.cadastrar_equipamento("banco_de_dados", "BD-Clientes", "10.0.0.20", "Bruno", "TI", "PostgreSQL 15")
    inv.cadastrar_equipamento("notebook", "Notebook-RH", "10.0.1.5", "Carla", "RH", "PAT-0042")

    inv.cadastrar_vulnerabilidade("Firmware desatualizado", "rede", "ALTA")
    inv.cadastrar_vulnerabilidade("SSH com senha fraca", "acesso", "CRITICA")
    inv.cadastrar_vulnerabilidade("Pacotes sem atualização", "SO", "MEDIA")
    inv.cadastrar_vulnerabilidade("Sem antivírus", "endpoint", "BAIXA")

    for ativo, vuln in [(1, 1), (2, 2), (2, 3), (3, 3), (4, 3), (4, 4)]:
        inv.associar_vulnerabilidade(ativo, vuln)

    inv.definir_dependencia(2, 1, 0.3)  # servidor web depende do roteador
    inv.definir_dependencia(3, 2, 0.2)  # banco depende do servidor
    inv.definir_dependencia(4, 1, 0.1)  # notebook depende do roteador
    return inv


if __name__ == "__main__":
    if os.path.exists(config.ARQ_EQUIPAMENTOS):
        print("Já existe inventário; nada foi alterado.")
    else:
        montar().salvar()
        print(f"Dados de exemplo gravados em {config.DIR_DADOS}")
