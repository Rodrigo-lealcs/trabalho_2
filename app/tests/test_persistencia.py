import json

import pytest

import persistencia
from erros import ErroInventario
from inventario import Inventario


def test_salvar_e_carregar(inv, tmp_path):
    inv.arq_equipamentos = str(tmp_path / "inventario.json")
    inv.arq_vulnerabilidades = str(tmp_path / "vulnerabilidades.json")
    inv.salvar()

    outro = Inventario(inv.arq_equipamentos, inv.arq_vulnerabilidades)
    outro.carregar()
    antes = [e.para_dicionario() for e in inv.listar_equipamentos()]
    depois = [e.para_dicionario() for e in outro.listar_equipamentos()]
    assert antes == depois


def test_json_e_lista_de_objetos_com_dependencias(inv, tmp_path):
    caminho = str(tmp_path / "inventario.json")
    persistencia.salvar_equipamentos(inv.equipamentos.values(), caminho)
    with open(caminho, encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
    assert isinstance(dados, list)
    assert dados[1]["dependencias"] == [{"depende_de": 1, "fracao": 0.2}]


def test_arquivo_que_nao_existe_vale_lista_vazia(tmp_path):
    assert persistencia.carregar_equipamentos(str(tmp_path / "nao_existe.json")) == []


@pytest.mark.parametrize("conteudo", ["{ quebrado", '{"a": 1}', '[{"tipo": "ROTEADOR"}]'])
def test_arquivo_ruim_gera_erro(tmp_path, conteudo):
    arquivo = tmp_path / "ruim.json"
    arquivo.write_text(conteudo)
    with pytest.raises(ErroInventario):
        persistencia.carregar_equipamentos(str(arquivo))


def test_tipo_outro_salva_e_carrega(tmp_path):
    i = Inventario(str(tmp_path / "inv.json"), str(tmp_path / "vuln.json"))
    i.cadastrar_equipamento("outro", "Camera-Hall", "10.0.2.1", "Ana", "Seguranca", "Câmera de segurança")
    i.salvar()
    outro = Inventario(i.arq_equipamentos, i.arq_vulnerabilidades)
    outro.carregar()
    assert outro.obter_equipamento(1).descricao_tipo == "Câmera de segurança"
