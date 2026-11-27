from modelos import Roteador, Servidor
from persistencia import salvar_equipamentos, carregar_equipamentos

roteador = Roteador(1, "roteador central", "123.245.0.1", 4)
servidor = Servidor(3, "Servidor principal", "111.123.2.1", "windows")

salvar_equipamentos([roteador, servidor], "inventario.json")

lidos = carregar_equipamentos("inventario.json")
for equipamento in lidos:
    print(equipamento.para_dicionario())