import os
import sys

import pytest

# permite importar os módulos da pasta app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inventario import Inventario  # noqa: E402


@pytest.fixture
def inv():
    """Cenário pequeno resolvido à mão (veja test_risco.py)."""
    i = Inventario()
    i.cadastrar_equipamento("roteador", "R1", "10.0.0.1", "Ana", "TI", 8)
    i.cadastrar_equipamento("servidor", "S1", "10.0.0.2", "Ana", "TI", "Linux")
    i.cadastrar_equipamento("notebook", "N1", "10.0.0.3", "Bia", "RH", "123")
    i.cadastrar_vulnerabilidade("A", "rede", "ALTA")   # nota 7,5
    i.cadastrar_vulnerabilidade("B", "so", "MEDIA")    # nota 5
    for ativo, vuln in [(1, 1), (2, 1), (2, 2), (3, 2)]:
        i.associar_vulnerabilidade(ativo, vuln)
    i.definir_dependencia(2, 1, 0.2)  # S1 recebe 0,2 do risco de R1
    i.definir_dependencia(3, 2, 0.5)  # N1 recebe 0,5 do risco de S1
    return i
