"""
Módulo de serviços para gerenciamento de propriedades rurais
Contém funções para cadastro e manipulação de propriedades
"""

from models.propriedade import Propriedade
from utils.validation import (
    validar_nome_propriedade,
    validar_area_propriedade,
    validar_localizacao,
    validar_tipo_solo
)
from utils.menu_utils import (
    solicitar_entrada,
    exibir_mensagem_sucesso,
    exibir_mensagem_erro,
    exibir_mensagem_info,
    confirmar_acao,
    tipos_comuns_de_solos
)

def cadastrar_propriedade():
    """
    Função para cadastrar uma nova propriedade rural
    Solicita dados do usuário, valida e cria objeto Propriedade
    
    Returns:
        Propriedade: Objeto propriedade criado ou None se houver erro
    """
    exibir_mensagem_info("Preencha os dados da propriedade rural:")
    
    try:
        # Solicitar nome da propriedade
        nome = solicitar_entrada(
            "Nome da propriedade", 
            validar_nome_propriedade
        )
        if nome is None:  # Usuário cancelou
            return None
        
        # Solicitar área total
        area_str = solicitar_entrada(
            "Área total (hectares)", 
            validar_area_propriedade
        )
        if area_str is None:  # Usuário cancelou
            return None
        
        area_total = float(area_str)
        
        # Solicitar localização
        localizacao = solicitar_entrada(
            "Localização (cidade, estado)", 
            validar_localizacao
        )
        if localizacao is None:  # Usuário cancelou
            return None
        
        # Solicitar tipo de solo
        tipos_comuns_de_solos()
        
        tipo_solo = solicitar_entrada(
            "Tipo de solo", 
            validar_tipo_solo
        )
        if tipo_solo is None:  # Usuário cancelou
            return None
        solos = {
            1: 'Latossolo vermelho',
            2: 'Nitossolo',
            3: 'Argissolo',
            4: 'Neossolo Quartzarênico'
        }
        tipo_solo = solos[int(tipo_solo)]
        # Criar objeto Propriedade
        propriedade = Propriedade(nome, area_total, localizacao, tipo_solo)
        
        # Exibir resumo e confirmar
        print("\n" + "="*50)
        print("RESUMO DA PROPRIEDADE:")
        print("="*50)
        print(propriedade)
        
        if confirmar_acao("Confirma o cadastro desta propriedade?"):
            exibir_mensagem_sucesso(f"Propriedade '{nome}' cadastrada com sucesso!")
            return propriedade
        else:
            exibir_mensagem_info("Cadastro cancelado pelo usuário.")
            return None
            
    except Exception as e:
        exibir_mensagem_erro(f"Erro ao cadastrar propriedade: {e}")
        return None

def listar_propriedades_cadastradas(lista_propriedades):
    """
    Exibe lista de propriedades cadastradas de forma organizada
    
    Args:
        lista_propriedades (list): Lista de objetos Propriedade
    """
    if not lista_propriedades:
        exibir_mensagem_info("Nenhuma propriedade cadastrada ainda.")
        return
    
    print("\n" + "="*60)
    print("    PROPRIEDADES CADASTRADAS")
    print("="*60)
    
    for i, propriedade in enumerate(lista_propriedades, 1):
        print(f"\n{i}. {propriedade.nome}")
        print(f"   Área: {propriedade.area_total} ha")
        print(f"   Local: {propriedade.localizacao}")
        print(f"   Solo: {propriedade.tipo_solo}")
        print(f"   Colheitas: {propriedade.obter_total_colheitas()}")
        print("-" * 40)

def buscar_propriedade_por_nome(lista_propriedades, nome):
    """
    Busca uma propriedade pelo nome na lista
    
    Args:
        lista_propriedades (list): Lista de propriedades
        nome (str): Nome da propriedade a buscar
        
    Returns:
        Propriedade: Propriedade encontrada ou None
    """
    for propriedade in lista_propriedades:
        if propriedade.nome.lower() == nome.lower():
            return propriedade
    return None

def verificar_nome_duplicado(lista_propriedades, nome):
    """
    Verifica se já existe uma propriedade com o mesmo nome
    
    Args:
        lista_propriedades (list): Lista de propriedades
        nome (str): Nome a verificar
        
    Returns:
        bool: True se nome já existe, False caso contrário
    """
    return buscar_propriedade_por_nome(lista_propriedades, nome) is not None

def selecionar_propriedade(lista_propriedades):
    """
    Permite ao usuário selecionar uma propriedade da lista
    
    Args:
        lista_propriedades (list): Lista de propriedades disponíveis
        
    Returns:
        Propriedade: Propriedade selecionada ou None se cancelado
    """
    if not lista_propriedades:
        exibir_mensagem_erro("Nenhuma propriedade cadastrada. Cadastre uma propriedade primeiro.")
        return None
    
    listar_propriedades_cadastradas(lista_propriedades)
    
    while True:
        try:
            opcao = input(f"\nEscolha uma propriedade (1-{len(lista_propriedades)}) ou 0 para cancelar: ").strip()
            
            if opcao == '0':
                return None
            
            indice = int(opcao) - 1
            
            if 0 <= indice < len(lista_propriedades):
                propriedade_selecionada = lista_propriedades[indice]
                exibir_mensagem_sucesso(f"Propriedade '{propriedade_selecionada.nome}' selecionada.")
                return propriedade_selecionada
            else:
                exibir_mensagem_erro(f"Opção inválida. Digite um número entre 1 e {len(lista_propriedades)}")
                
        except ValueError:
            exibir_mensagem_erro("Digite um número válido.")
        except KeyboardInterrupt:
            print("\n\nOperação cancelada.")
            return None

def obter_estatisticas_propriedade(propriedade):
    """
    Calcula estatísticas básicas de uma propriedade
    
    Args:
        propriedade (Propriedade): Propriedade para calcular estatísticas
        
    Returns:
        dict: Dicionário com estatísticas da propriedade
    """
    stats = {
        'nome': propriedade.nome,
        'area_total': propriedade.area_total,
        'total_colheitas': propriedade.obter_total_colheitas(),
        'area_total_colhida': propriedade.obter_area_total_colhida(),
        'quantidade_total_colhida': propriedade.obter_quantidade_total_colhida()
    }
    
    if stats['area_total_colhida'] > 0:
        stats['produtividade_media'] = round(
            stats['quantidade_total_colhida'] / stats['area_total_colhida'], 2
        )
    else:
        stats['produtividade_media'] = 0.0
    
    return stats