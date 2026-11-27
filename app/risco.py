"""Modelo de risco: (I - A) x = b.

  M: matriz equipamentos x vulnerabilidades (1 = o equipamento tem aquela vulnerabilidade)
  v: nota de cada vulnerabilidade
  b: risco próprio de cada equipamento  = fator de exposição * (M v)
  A: dependências (A[i][j] = fração do risco de j que chega em i; diagonal = 0)
  x: risco efetivo, a solução de (I - A) x = b
"""

import numpy as np

from erros import ErroRisco

LIMITE_CONDICAO = 1e12  # acima disso a matriz é considerada "quase não invertível"


def calcular_risco(inventario):
    """Devolve um dicionário com ids, b, x e as verificações."""
    ids = sorted(inventario.equipamentos)
    ids_vuln = sorted(inventario.vulnerabilidades)
    n = len(ids)
    if n == 0:
        return {"ids": [], "b": [], "x": [], "determinante": 1.0, "condicao": 1.0,
                "raio_espectral": 0.0, "diagonal_dominante": True}

    # M: linha = equipamento, coluna = vulnerabilidade
    M = np.zeros((n, len(ids_vuln)))
    for i, id_ativo in enumerate(ids):
        for id_vuln in inventario.equipamentos[id_ativo].vulnerabilidades:
            M[i, ids_vuln.index(id_vuln)] = 1

    # v: nota de cada vulnerabilidade
    v = np.array([inventario.vulnerabilidades[j].nota() for j in ids_vuln])

    # b: risco próprio. Cada equipamento responde o seu fator (polimorfismo)
    fatores = np.array([inventario.equipamentos[i].fator_exposicao() for i in ids])
    b = fatores * (M @ v)

    # A: dependências
    A = np.zeros((n, n))
    for i, id_ativo in enumerate(ids):
        for id_outro, fracao in inventario.equipamentos[id_ativo].dependencias.items():
            A[i, ids.index(id_outro)] = fracao

    I_menos_A = np.eye(n) - A

    # Verificação de invertibilidade: o número de condição decide; o determinante é só informativo
    determinante = float(np.linalg.det(I_menos_A))
    condicao = float(np.linalg.cond(I_menos_A))
    if condicao > LIMITE_CONDICAO:
        raise ErroRisco(f"(I - A) não é invertível (condição = {condicao:.3g}). Revise as dependências.")

    # Raio espectral = maior |autovalor| de A. Precisa ser < 1 para o risco não "crescer sem parar"
    raio = float(max(abs(np.linalg.eigvals(A))))
    if raio >= 1:
        raise ErroRisco(f"As dependências formam um ciclo forte demais (raio espectral = {raio:.2f}).")

    # Se a soma de cada linha de A for menor que 1, a matriz é diagonal dominante (garante invertível)
    dominante = bool(np.all(A.sum(axis=1) < 1))

    x = np.linalg.solve(I_menos_A, b)  # resolve direto, sem calcular a inversa

    return {"ids": ids, "b": b, "x": x, "determinante": determinante, "condicao": condicao,
            "raio_espectral": raio, "diagonal_dominante": dominante}
