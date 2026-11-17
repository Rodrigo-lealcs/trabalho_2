from modelos import Roteador
roteador = Roteador(1, "roteador central", "123.245.0.1", 4)
print(roteador.quantidade_portas)
print(roteador.nome)
print(roteador.para_dicionario())