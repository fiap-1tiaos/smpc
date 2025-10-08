"""
Módulo que define a classe Propriedade para representar propriedades rurais
"""

class Propriedade:
    """
    Classe que representa uma propriedade rural produtora de cana-de-açúcar

    Attr:
        nome (str): Nome da propriedade
        area_total (float): Área total da propriedade em hectares
        localizacao (str): Localizacao da propriedade
        tipo_solo (str): Tipo de solo da propriedade
    """

    def __init__(self, nome: str, area_total: float, localizacao: str, tipo_solo: str):
        self.nome = nome
        self.area_total = area_total
        self.localizacao = localizacao
        self.tipo_solo = tipo_solo
        self.colheitas = []
        
    def __str__(self):
        return f"""
=== PROPRIEDADE RURAL ===
Nome: {self.nome}
Area Total: {self.area_total} hectares
Localizacao: {self.localizacao}
Tipo Solo: {self.tipo_solo}
==========================
        """
