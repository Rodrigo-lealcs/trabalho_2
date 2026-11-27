import numpy as np
import pytest

from erros import ErroRisco
from inventario import Inventario
from risco import calcular_risco


def test_cenario_resolvido_a_mao(inv):
    """b = fator * (M v):  R1 = 1,2 * 7,5 = 9 ; S1 = 1,5 * (7,5 + 5) = 18,75 ; N1 = 1 * 5 = 5
    x1 = 9 ; x2 = 18,75 + 0,2 * 9 = 20,55 ; x3 = 5 + 0,5 * 20,55 = 15,275"""
    r = calcular_risco(inv)
    assert r["b"] == pytest.approx([9, 18.75, 5])
    assert r["x"] == pytest.approx([9, 20.55, 15.275])


def test_sem_dependencias_risco_efetivo_igual_ao_proprio(inv):
    for e in inv.equipamentos.values():
        e.dependencias.clear()
    r = calcular_risco(inv)
    assert r["x"] == pytest.approx(r["b"])
    assert r["condicao"] == pytest.approx(1.0)


def test_vulnerabilidade_corrigida_nao_conta(inv):
    inv.atualizar_status(2, "CORRIGIDA")
    assert calcular_risco(inv)["b"] == pytest.approx([9, 11.25, 0])


def test_ciclo_forte_e_rejeitado():
    i = Inventario()
    for k in range(3):
        i.cadastrar_equipamento("notebook", f"n{k}", f"10.0.0.{k + 1}", "x", "y", "1")
    for a in (1, 2, 3):
        for b in (1, 2, 3):
            if a != b:
                i.definir_dependencia(a, b, 0.9)
    with pytest.raises(ErroRisco):
        calcular_risco(i)


def test_inventario_vazio():
    assert calcular_risco(Inventario())["ids"] == []
