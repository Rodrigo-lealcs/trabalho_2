"""Menu de texto do inventário.

Aqui ficam só a conversa com o usuário (input/print) e o tratamento de erros.
As regras estão em inventario.py e risco.py.
"""

import config
from erros import ErroInventario
from inventario import Inventario, converter_enum, texto_com_letras, validar_ip
from modelos import ROTULO_EXTRA, Severidade, Status, TipoAtivo
from risco import calcular_risco


def perguntar(mensagem, validar):
    """Faz a pergunta de novo até a resposta passar na validação.

    'validar' é uma função que devolve o valor limpo ou levanta ErroInventario.
    Assim, quem erra um campo repete só aquele campo, sem voltar ao menu.
    """
    while True:
        try:
            return validar(input(mensagem))
        except ErroInventario as erro:
            print(f"  Erro: {erro}")


def ler_inteiro(mensagem):
    """Pergunta até o usuário digitar um número inteiro."""
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("  Digite um número inteiro.")


def ler_decimal(mensagem):
    while True:
        try:
            return float(input(mensagem).replace(",", "."))
        except ValueError:
            print("  Digite um número (ex.: 0,3).")


def mostrar_equipamento(e):
    print(f"[{e.id_ativo}] {e.nome} | {e.tipo.name} (código {e.tipo.value}) | {e.ip} | "
          f"responsável: {e.responsavel} | setor: {e.setor}")
    if e.vulnerabilidades:
        print(f"      vulnerabilidades: {e.vulnerabilidades}")
    for id_outro, fracao in e.dependencias.items():
        print(f"      depende do equipamento {id_outro} (fração {fracao})")


def mostrar_vulnerabilidade(v):
    print(f"[{v.id_vuln}] {v.descricao} | categoria: {v.categoria} | "
          f"{v.severidade.name} | {v.status.name}")


def cadastrar_equipamento(inv):
    print("Tipos: " + ", ".join(f"{t.value}={t.name}" for t in TipoAtivo))
    tipo = perguntar("Tipo (digite o código ou o nome, ex.: 1 ou ROTEADOR): ", lambda texto: converter_enum(TipoAtivo, texto))
    nome = perguntar("Nome do equipamento (ex.: Servidor-Web): ", lambda texto: inv.checar_nome_livre(texto_com_letras(texto, "nome")))
    ip = perguntar("IP (4 números de 0 a 255 separados por ponto, ex.: 192.168.0.1): ", validar_ip)
    responsavel = perguntar("Responsável (ex.: Ana Souza): ", lambda texto: texto_com_letras(texto, "responsável"))
    setor = perguntar("Setor (ex.: TI): ", lambda texto: texto_com_letras(texto, "setor"))
    # O campo extra depende do tipo; se estiver errado, pergunta só ele de novo
    while True:
        extra = input(f"{ROTULO_EXTRA[tipo]}: ")
        try:
            equipamento = inv.cadastrar_equipamento(tipo, nome, ip, responsavel, setor, extra)
            break
        except ErroInventario as erro:
            print(f"  Erro: {erro}")
    inv.salvar()
    print("Cadastrado:")
    mostrar_equipamento(equipamento)


def listar_equipamentos(inv):
    if not inv.equipamentos:
        print("Nenhum equipamento cadastrado.")
    for e in inv.listar_equipamentos():
        mostrar_equipamento(e)


def buscar_equipamento(inv):
    achados = inv.buscar_por_nome(input("Parte do nome para buscar (ex.: Web): "))
    if not achados:
        print("Nada encontrado.")
    for e in achados:
        mostrar_equipamento(e)


def atualizar_equipamento(inv):
    id_ativo = ler_inteiro("ID do equipamento (o número entre colchetes na lista, ex.: 1): ")
    mostrar_equipamento(inv.obter_equipamento(id_ativo))
    print("Deixe em branco (só Enter) o que não quiser mudar.")
    novos = {}
    for campo in ("nome", "ip", "responsavel", "setor"):
        valor = input(f"Novo {campo} (Enter para manter): ")
        if valor.strip() != "":
            novos[campo] = valor
    inv.atualizar_equipamento(id_ativo, **novos)
    inv.salvar()
    print("Atualizado.")


def remover_equipamento(inv):
    if not inv.equipamentos:
        print("Nenhum equipamento cadastrado para remover.")
        return
    print("Equipamentos cadastrados:")
    for e in inv.listar_equipamentos():
        mostrar_equipamento(e)
    e = inv.remover_equipamento(ler_inteiro("ID do equipamento (o número entre colchetes na lista, ex.: 1): "))
    inv.salvar()
    print(f"Removido: {e.nome}")


def cadastrar_vulnerabilidade(inv):
    descricao = perguntar("Descrição (ex.: Firmware desatualizado): ",
                          lambda texto: texto_com_letras(texto, "descrição"))
    categoria = perguntar("Categoria (ex.: rede, SO ou aplicação): ",
                          lambda texto: texto_com_letras(texto, "categoria"))
    print("Severidades: " + ", ".join(s.name for s in Severidade))
    severidade = perguntar("Severidade (BAIXA, MEDIA, ALTA ou CRITICA): ", lambda texto: converter_enum(Severidade, texto))
    v = inv.cadastrar_vulnerabilidade(descricao, categoria, severidade)
    inv.salvar()
    print("Cadastrada:")
    mostrar_vulnerabilidade(v)


def listar_vulnerabilidades(inv):
    if not inv.vulnerabilidades:
        print("Nenhuma vulnerabilidade cadastrada.")
    for v in inv.listar_vulnerabilidades():
        mostrar_vulnerabilidade(v)


def atualizar_status(inv):
    id_vuln = ler_inteiro("ID da vulnerabilidade (o número entre colchetes, ex.: 1): ")
    print("Status: " + ", ".join(s.name for s in Status))
    status = perguntar("Novo status (ABERTA, EM_TRATAMENTO ou CORRIGIDA): ", lambda texto: converter_enum(Status, texto))
    v = inv.atualizar_status(id_vuln, status)
    inv.salvar()
    mostrar_vulnerabilidade(v)


def remover_vulnerabilidade(inv):
    if not inv.vulnerabilidades:
        print("Nenhuma vulnerabilidade cadastrada para remover.")
        return
    print("Vulnerabilidades cadastradas:")
    for v in inv.listar_vulnerabilidades():
        mostrar_vulnerabilidade(v)
    id_vuln = ler_inteiro("ID da vulnerabilidade (o número entre colchetes, ex.: 1): ")
    v = inv.obter_vulnerabilidade(id_vuln)
    mostrar_vulnerabilidade(v)
    usada_por = [e.nome for e in inv.listar_equipamentos() if v.id_vuln in e.vulnerabilidades]
    if usada_por:
        print("Ela será tirada destes equipamentos: " + ", ".join(usada_por))
    if input("Tem certeza que quer remover? (s/n): ").strip().lower() != "s":
        print("Nada foi removido.")
        return
    inv.remover_vulnerabilidade(id_vuln)
    inv.salvar()
    print("Vulnerabilidade removida.")


def associar(inv):
    inv.associar_vulnerabilidade(ler_inteiro("ID do equipamento (o número entre colchetes na lista, ex.: 1): "),
                                 ler_inteiro("ID da vulnerabilidade (o número entre colchetes, ex.: 1): "))
    inv.salvar()
    print("Associada.")


def desassociar(inv):
    inv.desassociar_vulnerabilidade(ler_inteiro("ID do equipamento (o número entre colchetes na lista, ex.: 1): "),
                                    ler_inteiro("ID da vulnerabilidade (o número entre colchetes, ex.: 1): "))
    inv.salvar()
    print("Desassociada.")


def ver_vulnerabilidades_do_equipamento(inv):
    id_ativo = ler_inteiro("ID do equipamento (o número entre colchetes na lista, ex.: 1): ")
    mostrar_equipamento(inv.obter_equipamento(id_ativo))
    lista = inv.vulnerabilidades_do_equipamento(id_ativo)
    if not lista:
        print("  Sem vulnerabilidades associadas.")
    for v in lista:
        mostrar_vulnerabilidade(v)


def definir_dependencia(inv):
    print("O equipamento 'origem' recebe uma fração do risco do 'destino'.")
    inv.definir_dependencia(ler_inteiro("ID da origem, quem depende (ex.: 2): "),
                            ler_inteiro("ID do destino, de quem depende (ex.: 1): "),
                            ler_decimal("Fração de 0 até menos que 1 (ex.: 0,3 significa 30% do risco): "))
    inv.salvar()
    print("Dependência registrada.")


def remover_dependencia(inv):
    inv.remover_dependencia(ler_inteiro("ID da origem (ex.: 2): "), ler_inteiro("ID do destino (ex.: 1): "))
    inv.salvar()
    print("Dependência removida.")


def mostrar_risco(inv):
    r = calcular_risco(inv)
    if not r["ids"]:
        print("Cadastre equipamentos antes de calcular o risco.")
        return
    print("\nVerificação de (I - A):")
    print(f"  determinante        = {r['determinante']:.6g}")
    print(f"  número de condição  = {r['condicao']:.6g}  (aceito até 1e12)")
    print(f"  raio espectral de A = {r['raio_espectral']:.6g}  (precisa ser menor que 1)")
    print(f"  diagonal dominante  = {'sim' if r['diagonal_dominante'] else 'não'}")
    print("\n  ID  Nome                 Risco próprio   Risco efetivo")
    for id_ativo, proprio, efetivo in zip(r["ids"], r["b"], r["x"]):
        print(f"  {id_ativo:<3} {inv.equipamentos[id_ativo].nome:<20} {proprio:>13.2f} {efetivo:>15.2f}")


OPCOES = {
    "1": ("Cadastrar equipamento", cadastrar_equipamento),
    "2": ("Listar equipamentos", listar_equipamentos),
    "3": ("Buscar equipamento por nome", buscar_equipamento),
    "4": ("Atualizar equipamento", atualizar_equipamento),
    "5": ("Remover equipamento", remover_equipamento),
    "6": ("Cadastrar vulnerabilidade", cadastrar_vulnerabilidade),
    "7": ("Listar vulnerabilidades", listar_vulnerabilidades),
    "8": ("Atualizar status de vulnerabilidade", atualizar_status),
    "9": ("Associar vulnerabilidade a equipamento", associar),
    "10": ("Desassociar vulnerabilidade", desassociar),
    "11": ("Ver vulnerabilidades de um equipamento", ver_vulnerabilidades_do_equipamento),
    "12": ("Definir dependência entre equipamentos", definir_dependencia),
    "13": ("Remover dependência", remover_dependencia),
    "14": ("Calcular risco (I - A) x = b", mostrar_risco),
    "15": ("Remover vulnerabilidade", remover_vulnerabilidade),
}


def menu():
    inv = Inventario(config.ARQ_EQUIPAMENTOS, config.ARQ_VULNERABILIDADES)
    try:
        inv.carregar()
    except ErroInventario as erro:
        print(f"Erro ao carregar os dados: {erro}")
        return

    while True:
        print("\n=== Inventário de equipamentos e vulnerabilidades ===")
        for numero, (texto, _) in OPCOES.items():
            print(f"{numero:>2} - {texto}")
        print(" 0 - Sair")
        try:
            escolha = input("Opção: ").strip()
        except EOFError:
            return
        if escolha == "0":
            print("Até logo.")
            return
        if escolha not in OPCOES:
            print("Opção inválida.")
            continue
        try:
            OPCOES[escolha][1](inv)
        except ErroInventario as erro:
            print(f"Erro: {erro}")
        # Pausa para o usuário ler o resultado antes de o menu aparecer de novo
        try:
            input("\nPressione Enter para voltar ao menu...")
        except EOFError:
            return


if __name__ == "__main__":
    menu()
