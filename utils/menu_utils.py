"""
Módulo de utilitários para o menu do sistema
Contém funções para exibir menus e interagir com o usuário
"""

from .validation import validar_opcao_menu

def exibir_menu_principal():
    """
    Exibe o menu principal do sistema com todas as opções disponíveis
    """
    print("\n" + "="*60)
    print("    SISTEMA DE MONITORAMENTO DE PERDAS - CANA-DE-AÇÚCAR")
    print("="*60)
    print()
    print("Escolha uma das opções abaixo:")
    print()
    print("1. Cadastrar Nova Propriedade")
    print("2. Registrar Colheita")
    print("3. Consultar Relatório de Perdas")
    print("4. Visualizar Histórico")
    print("5. Fazer Backup dos Dados")
    print("6. Importar Backup")
    print("7. Configuração do Banco Oracle")
    print("8. Status do Sistema")
    print("9. Sair")
    print()
    print("-"*60)

def obter_opcao_usuario():
    """
    Lê e valida a opção escolhida pelo usuário no menu principal
    
    Returns:
        int: Opção válida escolhida pelo usuário (1-9)
    """
    opcoes_validas = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    while True:
        try:
            opcao = input("Digite sua escolha (1-9): ").strip()
            
            valido, mensagem = validar_opcao_menu(opcao, opcoes_validas)
            
            if valido:
                return int(opcao)
            else:
                exibir_mensagem_erro(mensagem)
                
        except KeyboardInterrupt:
            print("\n\nSaindo do sistema...")
            return 9
        except Exception as e:
            exibir_mensagem_erro("Erro inesperado. Tente novamente.")

def exibir_mensagem_sucesso(mensagem):
    """
    Exibe uma mensagem de sucesso formatada
    
    Args:
        mensagem (str): Mensagem de sucesso a ser exibida
    """
    print("\n" + "✓" + " " + mensagem)
    print()

def exibir_mensagem_erro(mensagem):
    """
    Exibe uma mensagem de erro formatada
    
    Args:
        mensagem (str): Mensagem de erro a ser exibida
    """
    print("\n" + "✗ ERRO: " + mensagem)
    print()

def exibir_mensagem_info(mensagem):
    """
    Exibe uma mensagem informativa formatada
    
    Args:
        mensagem (str): Mensagem informativa a ser exibida
    """
    print("\n" + "ℹ " + mensagem)
    print()

def exibir_separador():
    """
    Exibe um separador visual
    """
    print("-" * 60)

def pausar_execucao():
    """
    Pausa a execução e aguarda o usuário pressionar Enter
    """
    input("\nPressione Enter para continuar...")

def confirmar_acao(mensagem):
    """
    Solicita confirmação do usuário para uma ação
    
    Args:
        mensagem (str): Mensagem de confirmação
        
    Returns:
        bool: True se o usuário confirmar, False caso contrário
    """
    while True:
        resposta = input(f"\n{mensagem} (s/n): ").strip().lower()
        
        if resposta in ['s', 'sim', 'y', 'yes']:
            return True
        elif resposta in ['n', 'nao', 'não', 'no']:
            return False
        else:
            exibir_mensagem_erro("Digite 's' para sim ou 'n' para não")

def limpar_tela():
    """
    Limpa a tela do terminal (funciona no Windows e Linux/Mac)
    """
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def exibir_cabecalho(titulo):
    """
    Exibe um cabeçalho formatado para seções do sistema
    
    Args:
        titulo (str): Título da seção
    """
    print("\n" + "="*60)
    print(f"    {titulo.upper()}")
    print("="*60)

def exibir_lista_numerada(itens, titulo="Lista de Itens"):
    """
    Exibe uma lista numerada de itens
    
    Args:
        itens (list): Lista de itens a serem exibidos
        titulo (str): Título da lista
    """
    print(f"\n{titulo}:")
    print("-" * len(titulo))
    
    if not itens:
        print("Nenhum item encontrado.")
        return
    
    for i, item in enumerate(itens, 1):
        print(f"{i}. {item}")

def solicitar_entrada(prompt, tipo_validacao=None):
    """
    Solicita entrada do usuário com validação opcional
    
    Args:
        prompt (str): Mensagem para solicitar a entrada
        tipo_validacao (function): Função de validação opcional
        
    Returns:
        str: Entrada válida do usuário
    """
    while True:
        try:
            entrada = input(f"{prompt}: ").strip()
            
            if tipo_validacao:
                valido, mensagem = tipo_validacao(entrada)
                if valido:
                    return entrada
                else:
                    exibir_mensagem_erro(mensagem)
            else:
                return entrada
                
        except KeyboardInterrupt:
            print("\n\nOperação cancelada pelo usuário.")
            return None
        except Exception as e:
            exibir_mensagem_erro("Erro inesperado. Tente novamente.")

def tipos_comuns_de_solos(solos):
    print(f'''
===== Tipos de Solos Comuns =====
''')
    for key, solo in solos.items():
        print(f"""
{key} - {solo}""", end="")

    print()
