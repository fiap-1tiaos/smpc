"""
Módulo de validação de dados de entrada do usuário
Contém funções para validar diferentes tipos de dados do sistema
"""

def validar_area_propriedade(area):
    """
    Verifica se área da propriedade é positiva e razoável (em hectares)
    
    Args:
        area (float): Área a ser validada
        
    Returns:
        tuple: (bool, str) - (é_válido, mensagem_explicativa)
    """
    try:
        area_float = float(area)

        if area_float <= 0:
            return Flase, "A área deve ser maior que zero"

        if area_float > 100000:  # Limite razoável para propriedades
            return False, "Área muito grande. Verifique se está em hectares (máximo 100.000 ha)"
        
        return True, "Área válida"
    except (ValueError, TypeError):
        return False, "Área deve ser um número válido"


def validar_quantidade_colheita(quantidade):
    """"
    Verifica se quantidade de colheita é positiva e razoável (toneladas)
    
    Args:
        quantidade (float): Quantidade a ser validada
        
    Returns:
        tuple: (bool, str) - (é_válido, mensagem_explicativa)
    """
    try:
        quantidade_float = float(quantidade)
        
        if quantidade_float <= 0:
            return False, "A quantidade colhida deve ser maior que zero"
        
        if quantidade_float > 10000000:  # Limite razoável
            return False, "Quantidade muito grande. Verifique se está em toneladas"
        
        return True, "Quantidade válida"
    
    except (ValueError, TypeError):
        return False, "Quantidade deve ser um número válido"

def validar_tipo_colheita(tipo):
    """
    Verifica o tipo de colheita: aceita apenas 'manual' ou 'mecânica'

    Args:
        tipo (str): Tipo de colheita a ser validado
        
    Returns:
        tuple: (bool, str) - (é_válido, mensagem_explicativa)
    """
    if not isinstance(tipo, str):
        return False, "Tipo de colheita deve ser um texto"
    
    tipo_lower = tipo.lower().strip()
    
    if tipo_lower not in ['manual', 'mecanica']:
        return False, "Tipo de colheita deve ser 'manual' ou 'mecanica'"
    
    return True, "Tipo de colheita válido"

def validar_nome_propriedade(nome):
    """
    Verifica se nome não está vazio e se tem um tamanho mínimo e máximo de caracteres
    Args:
        nome (str): Nome da propriedade a ser validado
        
    Returns:
        tuple: (bool, str) - (é_válido, mensagem_explicativa)
    """
    if not isinstance(nome, str):
        return False, "Nome deve ser um texto"
    
    nome_limpo = nome.strip()
    
    if len(nome_limpo) == 0:
        return False, "Nome da propriedade não pode estar vazio"
    
    if len(nome_limpo) < 3:
        return False, "Nome da propriedade deve ter pelo menos 3 caracteres"
    
    if len(nome_limpo) > 100:
        return False, "Nome da propriedade muito longo (máximo 100 caracteres)"
    
    return True, "Nome válido"

def validar_localizacao(localizacao):
    """
    Valida se a localização é válida
    
    Args:
        localizacao (str): Localização a ser validada
        
    Returns:
        tuple: (bool, str) - (é_válido, mensagem_explicativa)
    """
    if not isinstance(localizacao, str):
        return False, "Localização deve ser um texto"
    
    localizacao_limpa = localizacao.strip()
    
    if len(localizacao_limpa) == 0:
        return False, "Localização não pode estar vazia"
    
    if len(localizacao_limpa) < 5:
        return False, "Localização deve ter pelo menos 5 caracteres (ex: 'São Paulo, SP')"
    
    if len(localizacao_limpa) > 200:
        return False, "Localização muito longa (máximo 200 caracteres)"
    
    return True, "Localização válida"

def validar_tipo_solo(tipo_solo):
    """
    Valida se o tipo de solo é válido
    
    Args:
        tipo_solo (str): Tipo de solo a ser validado
        
    Returns:
        tuple: (bool, str) - (é_válido, mensagem_explicativa)
    """
    if not isinstance(tipo_solo, str):
        return False, "Tipo de solo deve ser um texto"
    
    tipo_solo_limpo = tipo_solo.strip()
    
    if len(tipo_solo_limpo) == 0:
        return False, "Tipo de solo não pode estar vazio"
    
    if len(tipo_solo_limpo) < 3:
        return False, "Tipo de solo deve ter pelo menos 3 caracteres"
    
    if len(tipo_solo_limpo) > 50:
        return False, "Tipo de solo muito longo (máximo 50 caracteres)"
    
    # Lista de tipos de solo comuns (opcional, para sugestões)
    tipos_comuns = [
        'latossolo vermelho', 'argissolo', 'neossolo', 'nitossolo',
        'cambissolo', 'planossolo', 'gleissolo', 'vertissolo'
    ]
    
    return True, "Tipo de solo válido"

def validar_data(data):
    """
    Valida se a data está em formato válido (DD/MM/AAAA)
    
    Args:
        data (str): Data a ser validada
        
    Returns:
        tuple: (bool, str) - (é_válido, mensagem_explicativa)
    """
    if not isinstance(data, str):
        return False, "Data deve ser um texto no formato DD/MM/AAAA"
    
    data_limpa = data.strip()
    
    if len(data_limpa) == 0:
        return False, "Data não pode estar vazia"
    
    # Verifica formato básico DD/MM/AAAA
    partes = data_limpa.split('/')
    
    if len(partes) != 3:
        return False, "Data deve estar no formato DD/MM/AAAA (ex: 15/01/2024)"
    
    try:
        dia = int(partes[0])
        mes = int(partes[1])
        ano = int(partes[2])

        # Validações básicas
        if dia < 1 or dia > 31:
            return False, "Dia deve estar entre 1 e 31"
        
        if mes < 1 or mes > 12:
            return False, "Mês deve estar entre 1 e 12"
        
        if ano < 1900 or ano > 2030:
            return False, "Ano deve estar entre 1900 e 2030"
        
        return True, "Data válida"
    
    except ValueError:
        return False, "Data deve conter apenas números no formato DD/MM/AAAA"

def validar_opcao_menu(opcao, opcoes_validas):
    """
    Valida se a opção escolhida no menu é válida
    
    Args:
        opcao (str): Opção escolhida pelo usuário
        opcoes_validas (list): Lista de opções válidas
        
    Returns:
        tuple: (bool, str) - (é_válido, mensagem_explicativa)
    """
    try:
        opcao_int = int(opcao)
        
        if opcao_int in opcoes_validas:
            return True, "Opção válida"
        else:
            opcoes_str = ", ".join(map(str, opcoes_validas))
            return False, f"Opção inválida. Escolha entre: {opcoes_str}"
    
    except (ValueError, TypeError):
        opcoes_str = ", ".join(map(str, opcoes_validas))
        return False, f"Digite um número válido. Opções disponíveis: {opcoes_str}"