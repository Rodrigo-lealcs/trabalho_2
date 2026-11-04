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