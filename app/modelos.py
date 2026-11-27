"""Modelos: o que são os equipamentos e as vulnerabilidades.

Aqui só ficam as classes. Não tem print, input nem arquivo.
"""

from enum import Enum, IntEnum


class TipoAtivo(IntEnum):
    """Tipos de equipamento, cada um com um código inteiro."""
    ROTEADOR = 1
    SERVIDOR = 2
    NOTEBOOK = 3
    BANCO_DE_DADOS = 4
    OUTRO = 5


class Severidade(Enum):
    """Gravidade da vulnerabilidade. O valor é a nota usada no cálculo do risco."""
    BAIXA = 2.0
    MEDIA = 5.0
    ALTA = 7.5
    CRITICA = 9.5


class Status(Enum):
    ABERTA = 1
    EM_TRATAMENTO = 2
    CORRIGIDA = 3


# Nome do campo extra de cada tipo (usado no menu)
ROTULO_EXTRA = {
    TipoAtivo.ROTEADOR: "Quantidade de portas (ex.: 24)",
    TipoAtivo.SERVIDOR: "Sistema operacional (ex.: Ubuntu 22.04 ou Windows Server 2022)",
    TipoAtivo.NOTEBOOK: "Número de patrimônio (ex.: PAT-0042)",
    TipoAtivo.BANCO_DE_DADOS: "SGBD (ex.: PostgreSQL 15 ou MySQL 8)",
    TipoAtivo.OUTRO: "O que é este equipamento (ex.: Câmera de segurança, Switch, Impressora)",
}


class Vulnerabilidade:
    def __init__(self, id_vuln, descricao, categoria, severidade, status=Status.ABERTA):
        self.id_vuln = id_vuln
        self.descricao = descricao
        self.categoria = categoria
        self.severidade = severidade
        self.status = status

    def nota(self):
        """Nota usada no risco. Se já foi corrigida, não conta mais (vale 0)."""
        if self.status == Status.CORRIGIDA:
            return 0.0
        return self.severidade.value

    def para_dicionario(self):
        return {
            "id_vuln": self.id_vuln,
            "descricao": self.descricao,
            "categoria": self.categoria,
            "severidade": self.severidade.name,
            "status": self.status.name,
        }


class Equipamentos:
    """Classe mãe: o que todo equipamento tem."""

    tipo = None  # cada classe filha define o seu

    def __init__(self, id_ativo, nome, ip, responsavel, setor):
        self.id_ativo = id_ativo
        self.nome = nome
        self.ip = ip
        self.responsavel = responsavel
        self.setor = setor
        self.vulnerabilidades = []  # ids das vulnerabilidades deste equipamento
        self.dependencias = {}      # {id do outro equipamento: fração do risco que ele passa}

    def fator_exposicao(self):
        """Peso do risco. As classes filhas sobrescrevem (polimorfismo)."""
        return 1.0

    def para_dicionario(self):
        return {
            "tipo": self.tipo.name,
            "id_ativo": self.id_ativo,
            "nome": self.nome,
            "ip": self.ip,
            "responsavel": self.responsavel,
            "setor": self.setor,
            "vulnerabilidades": self.vulnerabilidades,
            "dependencias": [
                {"depende_de": outro, "fracao": fracao}
                for outro, fracao in self.dependencias.items()
            ],
        }


class Roteador(Equipamentos):
    tipo = TipoAtivo.ROTEADOR

    def __init__(self, id_ativo, nome, ip, responsavel, setor, quantidade_portas):
        super().__init__(id_ativo, nome, ip, responsavel, setor)
        self.quantidade_portas = quantidade_portas

    def fator_exposicao(self):
        return 1.2  # fica na borda da rede

    def para_dicionario(self):
        dados = super().para_dicionario()
        dados["quantidade_portas"] = self.quantidade_portas
        return dados


class Servidor(Equipamentos):
    tipo = TipoAtivo.SERVIDOR

    def __init__(self, id_ativo, nome, ip, responsavel, setor, sistema_operacional):
        super().__init__(id_ativo, nome, ip, responsavel, setor)
        self.sistema_operacional = sistema_operacional

    def fator_exposicao(self):
        return 1.5  # concentra serviços

    def para_dicionario(self):
        dados = super().para_dicionario()
        dados["sistema_operacional"] = self.sistema_operacional
        return dados


class Notebook(Equipamentos):
    tipo = TipoAtivo.NOTEBOOK

    def __init__(self, id_ativo, nome, ip, responsavel, setor, patrimonio):
        super().__init__(id_ativo, nome, ip, responsavel, setor)
        self.patrimonio = patrimonio

    # não sobrescreve fator_exposicao: usa o 1.0 da classe mãe

    def para_dicionario(self):
        dados = super().para_dicionario()
        dados["patrimonio"] = self.patrimonio
        return dados


class BancoDeDados(Equipamentos):
    tipo = TipoAtivo.BANCO_DE_DADOS

    def __init__(self, id_ativo, nome, ip, responsavel, setor, sgbd):
        super().__init__(id_ativo, nome, ip, responsavel, setor)
        self.sgbd = sgbd

    def fator_exposicao(self):
        return 1.4  # guarda dados sensíveis

    def para_dicionario(self):
        dados = super().para_dicionario()
        dados["sgbd"] = self.sgbd
        return dados


class Outro(Equipamentos):
    """Equipamento que não se encaixa nos outros tipos (câmera, switch, impressora...)."""
    tipo = TipoAtivo.OUTRO

    def __init__(self, id_ativo, nome, ip, responsavel, setor, descricao_tipo):
        super().__init__(id_ativo, nome, ip, responsavel, setor)
        self.descricao_tipo = descricao_tipo

    def fator_exposicao(self):
        return 1.1  # valor de exemplo, um pouco acima do notebook

    def para_dicionario(self):
        dados = super().para_dicionario()
        dados["descricao_tipo"] = self.descricao_tipo
        return dados
