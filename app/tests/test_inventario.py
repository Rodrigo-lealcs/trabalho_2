import pytest

from erros import DadoInvalido, NaoEncontrado
from modelos import Servidor, Severidade


def test_ids_sequenciais_e_classe_certa(inv):
    assert list(inv.equipamentos) == [1, 2, 3]
    assert isinstance(inv.obter_equipamento(2), Servidor)


def test_tipo_pode_ser_nome_ou_codigo(inv):
    novo = inv.cadastrar_equipamento("2", "S2", "10.0.0.50", "x", "y", "Linux")
    assert novo.tipo.name == "SERVIDOR"


@pytest.mark.parametrize("ip", ["999.1.1.1", "abc", ""])
def test_ip_invalido(inv, ip):
    with pytest.raises(DadoInvalido):
        inv.cadastrar_equipamento("notebook", "Novo", ip, "x", "y", "1")


def test_nome_repetido(inv):
    with pytest.raises(DadoInvalido):
        inv.cadastrar_equipamento("notebook", "r1", "10.0.0.77", "x", "y", "1")


def test_portas_invalidas(inv):
    with pytest.raises(DadoInvalido):
        inv.cadastrar_equipamento("roteador", "R9", "10.0.0.9", "x", "y", "abc")


def test_tipo_invalido(inv):
    with pytest.raises(DadoInvalido):
        inv.cadastrar_equipamento("impressora", "P", "10.0.0.9", "x", "y", "1")


def test_id_inexistente(inv):
    with pytest.raises(NaoEncontrado):
        inv.obter_equipamento(99)
    with pytest.raises(NaoEncontrado):
        inv.obter_equipamento("abc")


def test_busca_por_nome(inv):
    assert [e.nome for e in inv.buscar_por_nome("s")] == ["S1"]


def test_atualizar(inv):
    inv.atualizar_equipamento(1, nome="Borda")
    assert inv.obter_equipamento(1).nome == "Borda"


def test_remover_limpa_dependencias(inv):
    inv.remover_equipamento(1)
    assert 1 not in inv.obter_equipamento(2).dependencias


def test_associacao_repetida(inv):
    with pytest.raises(DadoInvalido):
        inv.associar_vulnerabilidade(1, 1)


@pytest.mark.parametrize("fracao", [-0.1, 1, 1.5, "x"])
def test_fracao_invalida(inv, fracao):
    with pytest.raises(DadoInvalido):
        inv.definir_dependencia(1, 2, fracao)


def test_dependencia_nele_mesmo(inv):
    with pytest.raises(DadoInvalido):
        inv.definir_dependencia(1, 1, 0.3)


@pytest.mark.parametrize("texto", ["baixa", "BAIXA", "  Baixa  ", Severidade.BAIXA])
def test_severidade_aceita_minuscula_e_enum(inv, texto):
    assert inv.cadastrar_vulnerabilidade("x", "y", texto).severidade == Severidade.BAIXA


def test_severidade_media_com_acento(inv):
    assert inv.cadastrar_vulnerabilidade("x", "y", "média").severidade == Severidade.MEDIA


@pytest.mark.parametrize("campo", ["descricao", "categoria"])
def test_vulnerabilidade_nao_aceita_so_numeros(inv, campo):
    dados = {"descricao": "Firmware velho", "categoria": "rede", "severidade": "ALTA"}
    dados[campo] = "4"
    with pytest.raises(DadoInvalido):
        inv.cadastrar_vulnerabilidade(**dados)


def test_equipamento_nao_aceita_so_numeros(inv):
    with pytest.raises(DadoInvalido):
        inv.cadastrar_equipamento("servidor", "S9", "10.0.0.9", "4", "TI", "Linux")
    with pytest.raises(DadoInvalido):
        inv.cadastrar_equipamento("servidor", "S9", "10.0.0.9", "Ana", "TI", "22")


def test_patrimonio_pode_ser_so_numero(inv):
    assert inv.cadastrar_equipamento("notebook", "N9", "10.0.0.9", "Ana", "TI", "12345").patrimonio == "12345"


def test_remover_vulnerabilidade_tira_dos_equipamentos(inv):
    inv.remover_vulnerabilidade(1)
    assert 1 not in inv.vulnerabilidades
    assert all(1 not in e.vulnerabilidades for e in inv.equipamentos.values())


def test_remover_vulnerabilidade_inexistente(inv):
    with pytest.raises(NaoEncontrado):
        inv.remover_vulnerabilidade(99)
