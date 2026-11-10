class Equipamentos:
    """classe Base para representar um ativo de rede no inventário."""

    def __init__(self, id_ativo, nome, ip):
        self.id_ativo = id_ativo
        self.nome = nome
        self.ip = ip
        self.vulnerabilidades = []

    def adicionar_vulnerabilidades(self, severidade):
        """Guarda a nota de severidade da vulnerabilidade no equipamento.""" 
        self.vulnerabilidades.append(severidade)

    def para_dicionario(self):
        """Converte o objeto em um dicionário para persistência em JSON"""
        return{
            "id_ativo": self.id_ativo,
            "nome": self.nome,
            "ip": self.ip,
            "vulnerabilidades": self.vulnerabilidades
        }
    
class Roteador(Equipamentos):
    """Classe derivada representando um roteador de rede"""
    def __init__(self, id_ativo, nome, ip, quantidade_portas):
        super().__init__(id_ativo, nome, ip)
        self.quantidade_portas = quantidade_portas

class Servidor(Equipamentos):
    """Classe derivada representando um roteador de rede"""
    def __init__(self, id_ativo, nome, ip, sistema_operacional):
        super().__init__(id_ativo, nome, ip)
        self.sistema_operacional = sistema_operacional

        