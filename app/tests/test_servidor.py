import pytest

from erros import NaoEncontrado
from servidor import montar_resposta


def test_saude(inv):
    assert montar_resposta("/saude", inv) == (200, {"status": "ok"})


def test_lista_e_um_equipamento(inv):
    codigo, lista = montar_resposta("/equipamentos", inv)
    assert codigo == 200 and len(lista) == 3
    assert montar_resposta("/equipamentos/2", inv)[1]["tipo"] == "SERVIDOR"


def test_risco(inv):
    codigo, corpo = montar_resposta("/risco", inv)
    assert codigo == 200
    assert corpo["equipamentos"][2]["risco_efetivo"] == pytest.approx(15.275)


def test_rota_inexistente(inv):
    assert montar_resposta("/nada", inv)[0] == 404


def test_id_inexistente(inv):
    with pytest.raises(NaoEncontrado):
        montar_resposta("/equipamentos/99", inv)
