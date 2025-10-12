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

    def adicionar_colheita(self, colheita):
        """
        Adiciona uma colheita à lista de colheitas da propriedade
        
        Args:
            colheita: Objeto da classe Colheita
        """
        self.colheitas.append(colheita)
    
    def obter_total_colheitas(self):
        """
        Retorna o número total de colheitas realizadas
        
        Returns:
            int: Número de colheitas
        """
        return len(self.colheitas)
    
    def obter_area_total_colhida(self):
        """
        Calcula a área total já colhida em todas as colheitas
        
        Returns:
            float: Área total colhida em hectares
        """
        return sum(colheita.area_colhida for colheita in self.colheitas)
    
    def obter_quantidade_total_colhida(self):
        """
        Calcula a quantidade total colhida em todas as colheitas
        
        Returns:
            float: Quantidade total colhida em toneladas
        """
        return sum(colheita.quantidade_colhida for colheita in self.colheitas)


class Solos:
    """
    Classe que representa uma os tipos de solo das regiões do Brasil
    """

    def obter_tipos_solo():
        """Retorna os tipos de solo de uma propriedaade"""

        return {
            1: 'Latossolo vermelho',
            2: 'Nitossolo',
            3: 'Argissolo',
            4: 'Neossolo Quartzarênico',
            5: 'Cambissolo',
            6: 'Neossolo Litólico',
            7: 'Planossolo',
            8: 'Gleissolo',
            9: 'Cambissolo',
            10: 'Vertissolo',
            11: 'Organossolo',
            12: 'Outros',
        }