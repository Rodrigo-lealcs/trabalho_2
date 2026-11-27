from modelos import BancoDeDados, Equipamentos, Notebook, Outro, Roteador, Servidor, TipoAtivo


def test_codigos_do_enum():
    assert [t.value for t in TipoAtivo] == [1, 2, 3, 4, 5]


def test_filhas_herdam_da_classe_mae():
    assert issubclass(Roteador, Equipamentos)
    assert Servidor.tipo == TipoAtivo.SERVIDOR


def test_polimorfismo_fator_de_exposicao():
    ativos = [Roteador(1, "r", "10.0.0.1", "a", "ti", 8),
              Servidor(2, "s", "10.0.0.2", "a", "ti", "Linux"),
              Notebook(3, "n", "10.0.0.3", "a", "ti", "1"),
              BancoDeDados(4, "b", "10.0.0.4", "a", "ti", "pg"),
              Outro(5, "c", "10.0.0.5", "a", "ti", "Câmera")]
    assert [a.fator_exposicao() for a in ativos] == [1.2, 1.5, 1.0, 1.4, 1.1]


def test_dicionario_tem_campos_da_mae_e_da_filha():
    dados = Roteador(1, "r", "10.0.0.1", "ana", "ti", 8).para_dicionario()
    assert dados["tipo"] == "ROTEADOR"
    assert dados["quantidade_portas"] == 8
    assert dados["nome"] == "r"
