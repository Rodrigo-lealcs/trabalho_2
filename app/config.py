"""Configuração: onde ficam os dados e em qual porta o serviço responde.

Tudo pode ser trocado por variável de ambiente, sem mexer no código. Isso é o
que permite ao container usar uma pasta de dados diferente (um volume Docker).
"""

import os

_PASTA_DO_CODIGO = os.path.dirname(os.path.abspath(__file__))

DIR_DADOS = os.environ.get("DADOS_DIR", os.path.join(_PASTA_DO_CODIGO, "data"))
ARQ_EQUIPAMENTOS = os.path.join(DIR_DADOS, "inventario.json")
ARQ_VULNERABILIDADES = os.path.join(DIR_DADOS, "vulnerabilidades.json")

PORTA = int(os.environ.get("PORTA", "8000"))
