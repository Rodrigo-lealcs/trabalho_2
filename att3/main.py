from modelos import Roteador, Servidor
from persistencia import salvar_equipamentos

roteador = Roteador(1, "roteador central", "123.245.0.1", 4)
print(roteador.quantidade_portas)
print(roteador.nome)
print(roteador.para_dicionario())

servidor = Servidor(3, "Servidor principal", "111.123.2.1", "windows")
print(servidor.id_ativo)
print(servidor.sistema_operacional)
print(servidor.para_dicionario())

equipamentos = [roteador, servidor]
salvar_equipamentos(equipamentos, "inventario.json")