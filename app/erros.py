"""Erros do projeto.

Quando algo está errado, os módulos de regra "levantam" (raise) um destes erros.
Quem chama (o menu ou o servidor) usa try/except e mostra a mensagem.
"""


class ErroInventario(Exception):
    """Erro geral do inventário (a mensagem explica o problema)."""


class DadoInvalido(ErroInventario):
    """O usuário digitou algo que não pode ser aceito."""


class NaoEncontrado(ErroInventario):
    """O id procurado não existe."""


class ErroRisco(ErroInventario):
    """O cálculo do risco não pode ser feito."""
