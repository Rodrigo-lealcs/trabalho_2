"""Regras do inventário: cadastrar, listar, buscar, atualizar, remover.

Não usa print nem input. Se algo está errado, levanta um erro de erros.py.
Os equipamentos ficam em um dicionário {id: objeto}, então buscar pelo id é direto.
"""

import ipaddress

import persistencia
from erros import DadoInvalido, NaoEncontrado
from modelos import (BancoDeDados, Notebook, Outro, Roteador, Servidor, Severidade,
                     Status, TipoAtivo, Vulnerabilidade)


def converter_enum(enum, valor):
    """Transforma o texto digitado em um membro do Enum (aceita nome ou, nos tipos, o código)."""
    if isinstance(valor, enum):  # já veio convertido (o menu converte na hora da pergunta)
        return valor
    texto = str(valor).strip()
    try:
        if enum is TipoAtivo and texto.isdigit():
            return TipoAtivo(int(texto))
        # aceita maiúscula/minúscula e "média" com acento
        return enum[texto.upper().replace("É", "E")]
    except (KeyError, ValueError):
        opcoes = ", ".join(membro.name for membro in enum)
        raise DadoInvalido(f"Valor inválido: '{texto}'. Opções: {opcoes}.")


def texto_obrigatorio(valor, campo):
    valor = str(valor).strip()
    if valor == "":
        raise DadoInvalido(f"O campo '{campo}' não pode ficar vazio.")
    return valor


def texto_com_letras(valor, campo):
    """Texto obrigatório que precisa ter pelo menos uma letra (não aceita só números)."""
    valor = texto_obrigatorio(valor, campo)
    if not any(caractere.isalpha() for caractere in valor):
        raise DadoInvalido(f"O campo '{campo}' precisa ter letras, não só números.")
    return valor


def validar_ip(valor):
    try:
        return str(ipaddress.ip_address(str(valor).strip()))
    except ValueError:
        raise DadoInvalido(f"IP inválido: '{valor}'.")


class Inventario:
    def __init__(self, arq_equipamentos=None, arq_vulnerabilidades=None):
        self.arq_equipamentos = arq_equipamentos
        self.arq_vulnerabilidades = arq_vulnerabilidades
        self.equipamentos = {}      # {id: Equipamentos}
        self.vulnerabilidades = {}  # {id: Vulnerabilidade}

    # ---------- arquivos ----------
    def carregar(self):
        if self.arq_equipamentos:
            lista = persistencia.carregar_equipamentos(self.arq_equipamentos)
            self.equipamentos = {e.id_ativo: e for e in lista}
        if self.arq_vulnerabilidades:
            lista = persistencia.carregar_vulnerabilidades(self.arq_vulnerabilidades)
            self.vulnerabilidades = {v.id_vuln: v for v in lista}

    def salvar(self):
        if self.arq_equipamentos:
            persistencia.salvar_equipamentos(self.equipamentos.values(), self.arq_equipamentos)
        if self.arq_vulnerabilidades:
            persistencia.salvar_vulnerabilidades(self.vulnerabilidades.values(),
                                                 self.arq_vulnerabilidades)

    # ---------- equipamentos ----------
    def checar_nome_livre(self, nome):
        """Levanta erro se já existe um equipamento com esse nome."""
        for e in self.equipamentos.values():
            if e.nome.lower() == nome.lower():
                raise DadoInvalido(f"Já existe um equipamento chamado '{nome}'.")
        return nome

    def cadastrar_equipamento(self, tipo, nome, ip, responsavel, setor, extra):
        """'extra' é o campo próprio do tipo: portas, sistema operacional, patrimônio ou SGBD."""
        tipo = converter_enum(TipoAtivo, tipo)
        nome = texto_com_letras(nome, "nome")
        ip = validar_ip(ip)
        responsavel = texto_com_letras(responsavel, "responsável")
        setor = texto_com_letras(setor, "setor")
        self.checar_nome_livre(nome)

        novo_id = max(self.equipamentos, default=0) + 1
        base = (novo_id, nome, ip, responsavel, setor)
        if tipo == TipoAtivo.ROTEADOR:
            if not str(extra).strip().isdigit() or int(extra) <= 0:
                raise DadoInvalido("A quantidade de portas deve ser um número inteiro maior que zero.")
            equipamento = Roteador(*base, int(extra))
        elif tipo == TipoAtivo.SERVIDOR:
            equipamento = Servidor(*base, texto_com_letras(extra, "sistema operacional"))
        elif tipo == TipoAtivo.NOTEBOOK:
            equipamento = Notebook(*base, texto_obrigatorio(extra, "patrimônio"))
        elif tipo == TipoAtivo.BANCO_DE_DADOS:
            equipamento = BancoDeDados(*base, texto_com_letras(extra, "SGBD"))
        else:
            equipamento = Outro(*base, texto_com_letras(extra, "descrição do tipo"))
        self.equipamentos[novo_id] = equipamento
        return equipamento

    def obter_equipamento(self, id_ativo):
        try:
            return self.equipamentos[int(id_ativo)]
        except (KeyError, ValueError):
            raise NaoEncontrado(f"Equipamento '{id_ativo}' não encontrado.")

    def listar_equipamentos(self):
        return [self.equipamentos[i] for i in sorted(self.equipamentos)]

    def buscar_por_nome(self, trecho):
        trecho = str(trecho).strip().lower()
        return [e for e in self.listar_equipamentos() if trecho in e.nome.lower()]

    def atualizar_equipamento(self, id_ativo, nome=None, ip=None, responsavel=None, setor=None):
        """Só altera o que foi informado (os outros ficam None)."""
        equipamento = self.obter_equipamento(id_ativo)
        if nome is not None:
            equipamento.nome = texto_com_letras(nome, "nome")
        if ip is not None:
            equipamento.ip = validar_ip(ip)
        if responsavel is not None:
            equipamento.responsavel = texto_com_letras(responsavel, "responsável")
        if setor is not None:
            equipamento.setor = texto_com_letras(setor, "setor")
        return equipamento

    def remover_equipamento(self, id_ativo):
        equipamento = self.obter_equipamento(id_ativo)
        del self.equipamentos[equipamento.id_ativo]
        # ninguém mais pode depender de um equipamento que não existe
        for outro in self.equipamentos.values():
            outro.dependencias.pop(equipamento.id_ativo, None)
        return equipamento

    # ---------- vulnerabilidades ----------
    def cadastrar_vulnerabilidade(self, descricao, categoria, severidade):
        descricao = texto_com_letras(descricao, "descrição")
        categoria = texto_com_letras(categoria, "categoria")
        severidade = converter_enum(Severidade, severidade)
        novo_id = max(self.vulnerabilidades, default=0) + 1
        vuln = Vulnerabilidade(novo_id, descricao, categoria, severidade)
        self.vulnerabilidades[novo_id] = vuln
        return vuln

    def obter_vulnerabilidade(self, id_vuln):
        try:
            return self.vulnerabilidades[int(id_vuln)]
        except (KeyError, ValueError):
            raise NaoEncontrado(f"Vulnerabilidade '{id_vuln}' não encontrada.")

    def listar_vulnerabilidades(self):
        return [self.vulnerabilidades[i] for i in sorted(self.vulnerabilidades)]

    def atualizar_status(self, id_vuln, status):
        vuln = self.obter_vulnerabilidade(id_vuln)
        vuln.status = converter_enum(Status, status)
        return vuln

    def remover_vulnerabilidade(self, id_vuln):
        """Apaga a vulnerabilidade do catálogo e a tira de todos os equipamentos que a tinham."""
        vuln = self.obter_vulnerabilidade(id_vuln)
        del self.vulnerabilidades[vuln.id_vuln]
        for equipamento in self.equipamentos.values():
            if vuln.id_vuln in equipamento.vulnerabilidades:
                equipamento.vulnerabilidades.remove(vuln.id_vuln)
        return vuln

    def associar_vulnerabilidade(self, id_ativo, id_vuln):
        equipamento = self.obter_equipamento(id_ativo)
        vuln = self.obter_vulnerabilidade(id_vuln)
        if vuln.id_vuln in equipamento.vulnerabilidades:
            raise DadoInvalido("Essa vulnerabilidade já está associada a este equipamento.")
        equipamento.vulnerabilidades.append(vuln.id_vuln)

    def desassociar_vulnerabilidade(self, id_ativo, id_vuln):
        equipamento = self.obter_equipamento(id_ativo)
        vuln = self.obter_vulnerabilidade(id_vuln)
        if vuln.id_vuln not in equipamento.vulnerabilidades:
            raise NaoEncontrado("Essa vulnerabilidade não está associada a este equipamento.")
        equipamento.vulnerabilidades.remove(vuln.id_vuln)

    def vulnerabilidades_do_equipamento(self, id_ativo):
        equipamento = self.obter_equipamento(id_ativo)
        return [self.vulnerabilidades[i] for i in equipamento.vulnerabilidades]

    # ---------- dependências entre equipamentos ----------
    def definir_dependencia(self, id_origem, id_destino, fracao):
        """O equipamento 'origem' recebe 'fracao' do risco do 'destino'."""
        origem = self.obter_equipamento(id_origem)
        destino = self.obter_equipamento(id_destino)
        if origem.id_ativo == destino.id_ativo:
            raise DadoInvalido("Um equipamento não pode depender dele mesmo.")
        try:
            fracao = float(fracao)
        except ValueError:
            raise DadoInvalido("A fração deve ser um número.")
        if fracao < 0 or fracao >= 1:
            raise DadoInvalido("A fração deve ser maior ou igual a 0 e menor que 1.")
        origem.dependencias[destino.id_ativo] = fracao

    def remover_dependencia(self, id_origem, id_destino):
        origem = self.obter_equipamento(id_origem)
        if int(id_destino) not in origem.dependencias:
            raise NaoEncontrado("Essa dependência não existe.")
        del origem.dependencias[int(id_destino)]
