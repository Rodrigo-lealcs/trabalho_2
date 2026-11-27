"""Serviço HTTP simples que mantém o container ligado e mostra os dados em JSON.

Rotas (GET):
  /saude              -> {"status": "ok"}
  /equipamentos       -> lista de equipamentos
  /equipamentos/<id>  -> um equipamento
  /vulnerabilidades   -> lista de vulnerabilidades
  /risco              -> risco próprio e efetivo + verificações
Os dados são lidos do arquivo a cada pedido, então o que muda no menu aparece aqui.
"""

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import config
from erros import DadoInvalido, ErroInventario, NaoEncontrado
from inventario import Inventario
from risco import calcular_risco


def montar_resposta(caminho, inventario):
    """Recebe o caminho pedido e o inventário; devolve (código HTTP, dados)."""
    partes = [p for p in caminho.split("/") if p]

    if partes == ["saude"]:
        return 200, {"status": "ok"}
    if partes == ["equipamentos"]:
        return 200, [e.para_dicionario() for e in inventario.listar_equipamentos()]
    if len(partes) == 2 and partes[0] == "equipamentos":
        return 200, inventario.obter_equipamento(partes[1]).para_dicionario()
    if partes == ["vulnerabilidades"]:
        return 200, [v.para_dicionario() for v in inventario.listar_vulnerabilidades()]
    if partes == ["risco"]:
        r = calcular_risco(inventario)
        return 200, {
            "invertivel": True,
            "determinante": r["determinante"],
            "numero_de_condicao": r["condicao"],
            "raio_espectral": r["raio_espectral"],
            "equipamentos": [
                {"id_ativo": i, "risco_proprio": float(p), "risco_efetivo": float(e)}
                for i, p, e in zip(r["ids"], r["b"], r["x"])
            ],
        }
    return 404, {"erro": "Rota não encontrada."}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            inventario = Inventario(config.ARQ_EQUIPAMENTOS, config.ARQ_VULNERABILIDADES)
            inventario.carregar()
            codigo, corpo = montar_resposta(self.path.split("?")[0], inventario)
        except NaoEncontrado as erro:
            codigo, corpo = 404, {"erro": str(erro)}
        except DadoInvalido as erro:
            codigo, corpo = 400, {"erro": str(erro)}
        except ErroInventario as erro:
            codigo, corpo = 500, {"erro": str(erro)}
        dados = json.dumps(corpo, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(dados)))
        self.end_headers()
        self.wfile.write(dados)


if __name__ == "__main__":
    servidor = ThreadingHTTPServer(("0.0.0.0", config.PORTA), Handler)
    print(f"Serviço ligado na porta {config.PORTA}", flush=True)
    servidor.serve_forever()
