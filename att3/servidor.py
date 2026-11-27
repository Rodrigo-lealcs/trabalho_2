"""Ponto de entrada da aplicação: um servidor HTTP que permanece em execução."""

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from persistencia import carregar_equipamentos

ARQUIVO = os.environ.get("INVENTARIO_ARQUIVO", "data/inventario.json")
PORTA = int(os.environ.get("PORTA", "8000"))


class Manipulador(BaseHTTPRequestHandler):
    """Trata cada requisição que chega ao servidor."""

    def _responder(self, codigo, corpo):
        dados = json.dumps(corpo, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(dados)))
        self.end_headers()
        self.wfile.write(dados)

    def do_GET(self):
        if self.path == "/saude":
            self._responder(200, {"status": "ok"})
        elif self.path == "/equipamentos":
            equipamentos = carregar_equipamentos(ARQUIVO)
            self._responder(200, [e.para_dicionario() for e in equipamentos])
        else:
            self._responder(404, {"erro": "rota não encontrada"})

    def log_message(self, formato, *args):
        print(f"{self.address_string()} - {formato % args}", flush=True)


if __name__ == "__main__":
    os.makedirs(os.path.dirname(ARQUIVO) or ".", exist_ok=True)
    servidor = ThreadingHTTPServer(("0.0.0.0", PORTA), Manipulador)
    print(f"Servidor ativo na porta {PORTA}", flush=True)
    servidor.serve_forever()
