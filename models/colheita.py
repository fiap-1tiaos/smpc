"""
Módulo que define a classe Colheita para representar dados de colheita de cana-de-açúcar
"""

class Colheita:
    """
    Classe que representa uma colheita de cana-de-açúcar

    
    Args:
        data (str): Data da colheita no formato DD/MM/AAAA
        area_colhida (float): Área colhida em hectares
        quantidade_colhida (float): Quantidade colhida em toneladas
        tipo_colheita (str): Tipo de colheita ('manual' ou 'mecanica')
        produtividade (float): Produtividade calculada em t/ha
    """
    
    def __init__(self, data: str, area_colhida: float, quantidade_colhida: float, tipo_colheita: str):
        self.datas = data
        self.area_colhida = area_colhida
        self.quantidade_colhida = quantidade_colhida
        self.tipo_colheita = tipo_colheita

    def __str__(self):
        return f"""
=== DADOS DE COLHEITA ===
Data: {self.data}
Area Colhida: {self.area_colhida}
Quantidade Colhida: {self.quantidade_colhida}
Tipo Colheita: {self.tipo_colheita}
        """
