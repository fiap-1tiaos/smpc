"""
Módulo de utilitários para o menu do sistema
Contém funções para exibir menus e interagir com o usuário
"""

from colorama import init, Fore, Back, Style
from .validation import validar_opcao_menu

# Inicializar colorama para Windows
init(autoreset=True)

def exibir_menu_principal():
    """
    Exibe o menu principal do sistema com todas as opções disponíveis
    """
    largura = 70
    
    print(f"\n{Fore.CYAN}{'='*largura}")
    print(f"{Fore.YELLOW}{Style.BRIGHT}  🌾 SISTEMA DE MONITORAMENTO DE PERDAS - CANA-DE-AÇÚCAR 🌾")
    print(f"{Fore.CYAN}{'='*largura}")
    print(f"{Fore.WHITE}{Style.DIM}         Controle inteligente de produtividade agrícola")
    print(f"{Fore.CYAN}{'='*largura}")
    print()
    print(f"{Fore.WHITE}{Style.BRIGHT}📋 MENU PRINCIPAL - Escolha uma opção:")
    print()
    
    # Função auxiliar para criar linha de item do menu
    def criar_linha_menu(numero, icone, texto):
        # Conteúdo sem códigos de cor para calcular comprimento real
        conteudo_limpo = f" {numero}. {icone} {texto}"
        # Remover códigos de cor para calcular comprimento real
        import re
        conteudo_sem_cor = re.sub(r'\x1b\[[0-9;]*m', '', conteudo_limpo)
        
        espacos_necessarios = largura - len(conteudo_sem_cor) - 3
        if espacos_necessarios < 0:
            espacos_necessarios = 0
            
        return f"{Fore.CYAN}│ {numero}. {icone} {texto}{' ' * espacos_necessarios}│"
    
    # Seção 1: Gestão de Propriedades
    titulo1 = "GESTÃO DE PROPRIEDADES"
    tracejado1 = "─" * (largura - len(titulo1) - 4)
    print(f"{Fore.CYAN}┌─ {Fore.GREEN}{titulo1} {Fore.CYAN}{tracejado1}┐")
    print(criar_linha_menu(f"{Fore.GREEN}1", f"{Fore.WHITE}🏡", f"{Fore.WHITE}Cadastrar Nova Propriedade"))
    print(f"{Fore.CYAN}└{'─' * (largura - 2)}┘")
    print()
    
    # Seção 2: Colheitas e Análises
    titulo2 = "COLHEITAS E ANÁLISES"
    tracejado2 = "─" * (largura - len(titulo2) - 4)
    print(f"{Fore.CYAN}┌─ {Fore.YELLOW}{titulo2} {Fore.CYAN}{tracejado2}┐")
    print(criar_linha_menu(f"{Fore.GREEN}2", f"{Fore.WHITE}🚜", f"{Fore.WHITE}Registrar Colheita"))
    print(criar_linha_menu(f"{Fore.GREEN}3", f"{Fore.WHITE}📊", f"{Fore.WHITE}Consultar Relatório de Perdas"))
    print(criar_linha_menu(f"{Fore.GREEN}4", f"{Fore.WHITE}📋", f"{Fore.WHITE}Visualizar Histórico"))
    print(f"{Fore.CYAN}└{'─' * (largura - 2)}┘")
    print()
    
    # Seção 3: Backup e Configurações
    titulo3 = "BACKUP E CONFIGURAÇÕES"
    tracejado3 = "─" * (largura - len(titulo3) - 4)
    print(f"{Fore.CYAN}┌─ {Fore.MAGENTA}{titulo3} {Fore.CYAN}{tracejado3}┐")
    print(criar_linha_menu(f"{Fore.GREEN}5", f"{Fore.WHITE}💾", f"{Fore.WHITE}Fazer Backup dos Dados"))
    print(criar_linha_menu(f"{Fore.GREEN}6", f"{Fore.WHITE}📥", f"{Fore.WHITE}Importar Backup"))
    print(criar_linha_menu(f"{Fore.GREEN}7", f"{Fore.WHITE}🔧", f"{Fore.WHITE}Configuração do Banco Oracle"))
    print(criar_linha_menu(f"{Fore.GREEN}8", f"{Fore.WHITE}⚡", f"{Fore.WHITE}Status do Sistema"))
    print(f"{Fore.CYAN}└{'─' * (largura - 2)}┘")
    print()
    
    # Seção 4: Sistema
    titulo4 = "SISTEMA"
    tracejado4 = "─" * (largura - len(titulo4) - 4)
    print(f"{Fore.CYAN}┌─ {Fore.RED}{titulo4} {Fore.CYAN}{tracejado4}┐")
    print(criar_linha_menu(f"{Fore.RED}9", f"{Fore.WHITE}🚪", f"{Fore.WHITE}Sair do Sistema"))
    print(f"{Fore.CYAN}└{'─' * (largura - 2)}┘")
    print()

def obter_opcao_usuario():
    """
    Lê e valida a opção escolhida pelo usuário no menu principal
    
    Returns:
        int: Opção válida escolhida pelo usuário (1-9)
    """
    opcoes_validas = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    largura = 70
    
    while True:
        try:
            print(f"{Fore.CYAN}┌{'─' * (largura - 2)}┐")
            
            # Criar linha de entrada com espaçamento correto
            prompt_texto = " 🎯 Digite sua escolha (1-9): "
            espacos_para_input = largura - len(prompt_texto) - 3
            
            opcao = input(f"{Fore.CYAN}│{Fore.YELLOW}{prompt_texto}{Style.RESET_ALL}").strip()
            print(f"{Fore.CYAN}└{'─' * (largura - 2)}┘")
            
            valido, mensagem = validar_opcao_menu(opcao, opcoes_validas)
            
            if valido:
                print(f"\n{Fore.GREEN}✅ Opção {opcao} selecionada!{Style.RESET_ALL}")
                return int(opcao)
            else:
                exibir_mensagem_erro(mensagem)
                
        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}👋 Saindo do sistema...")
            return 9
        except Exception as e:
            exibir_mensagem_erro("Erro inesperado. Tente novamente.")

def exibir_mensagem_sucesso(mensagem):
    """
    Exibe uma mensagem de sucesso formatada
    
    Args:
        mensagem (str): Mensagem de sucesso a ser exibida
    """
    largura = 70
    titulo = "SUCESSO"
    tracejado = "─" * (largura - len(titulo) - 4)
    
    # Calcular espaços precisos para o conteúdo (considerando emojis)
    conteudo_limpo = f" ✅ {mensagem}"
    # Emojis podem ocupar 2 espaços visuais, então ajustamos
    espacos_necessarios = largura - len(conteudo_limpo) - 2
    if espacos_necessarios < 0:
        espacos_necessarios = 0
    
    print(f"\n{Fore.GREEN}┌─ {Style.BRIGHT}{titulo} {Style.NORMAL}{tracejado}┐")
    print(f"{Fore.GREEN}│ ✅ {mensagem}{' ' * espacos_necessarios}│{Style.RESET_ALL}")
    print(f"{Fore.GREEN}└{'─' * (largura - 2)}┘{Style.RESET_ALL}")
    print()

def exibir_mensagem_erro(mensagem):
    """
    Exibe uma mensagem de erro formatada
    
    Args:
        mensagem (str): Mensagem de erro a ser exibida
    """
    largura = 70
    titulo = "ERRO"
    tracejado = "─" * (largura - len(titulo) - 4)
    
    # Calcular espaços precisos para o conteúdo (considerando emojis)
    conteudo_limpo = f" ❌ {mensagem}"
    # Emojis podem ocupar 2 espaços visuais, então ajustamos
    espacos_necessarios = largura - len(conteudo_limpo) - 2
    if espacos_necessarios < 0:
        espacos_necessarios = 0
    
    print(f"\n{Fore.RED}┌─ {Style.BRIGHT}{titulo} {Style.NORMAL}{tracejado}┐")
    print(f"{Fore.RED}│ ❌ {mensagem}{' ' * espacos_necessarios}│{Style.RESET_ALL}")
    print(f"{Fore.RED}└{'─' * (largura - 2)}┘{Style.RESET_ALL}")
    print()

def exibir_mensagem_info(mensagem):
    """
    Exibe uma mensagem informativa formatada
    
    Args:
        mensagem (str): Mensagem informativa a ser exibida
    """
    largura = 70
    titulo = "INFORMAÇÃO"
    tracejado = "─" * (largura - len(titulo) - 4)
    
    # Calcular espaços precisos para o conteúdo (considerando emojis)
    conteudo_limpo = f" ℹ️  {mensagem}"
    # Emojis podem ocupar 2 espaços visuais, então ajustamos
    espacos_necessarios = largura - len(conteudo_limpo) - 1
    if espacos_necessarios < 0:
        espacos_necessarios = 0
    
    print(f"\n{Fore.CYAN}┌─ {Style.BRIGHT}{titulo} {Style.NORMAL}{tracejado}┐")
    print(f"{Fore.CYAN}│ ℹ️  {mensagem}{' ' * espacos_necessarios}│{Style.RESET_ALL}")
    print(f"{Fore.CYAN}└{'─' * (largura - 2)}┘{Style.RESET_ALL}")
    print()

def exibir_separador():
    """
    Exibe um separador visual
    """
    print(f"{Fore.CYAN}{'-' * 70}")

def pausar_execucao():
    """
    Pausa a execução e aguarda o usuário pressionar Enter
    """
    input(f"\n{Fore.YELLOW}⏸️  Pressione Enter para continuar...{Style.RESET_ALL}")

def confirmar_acao(mensagem):
    """
    Solicita confirmação do usuário para uma ação
    
    Args:
        mensagem (str): Mensagem de confirmação
        
    Returns:
        bool: True se o usuário confirmar, False caso contrário
    """
    while True:
        resposta = input(f"\n{Fore.YELLOW}❓ {mensagem} {Fore.GREEN}(s/n){Style.RESET_ALL}: ").strip().lower()
        
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
    print(f"\n{Fore.MAGENTA}{'='*70}")
    print(f"{Fore.YELLOW}{Style.BRIGHT}    📋 {titulo.upper()}")
    print(f"{Fore.MAGENTA}{'='*70}")

def exibir_lista_numerada(itens, titulo="Lista de Itens"):
    """
    Exibe uma lista numerada de itens
    
    Args:
        itens (list): Lista de itens a serem exibidos
        titulo (str): Título da lista
    """
    print(f"\n{Fore.CYAN}{Style.BRIGHT}📝 {titulo}:")
    print(f"{Fore.CYAN}{'-' * (len(titulo) + 4)}")
    
    if not itens:
        print(f"{Fore.YELLOW}⚠️  Nenhum item encontrado.")
        return
    
    for i, item in enumerate(itens, 1):
        print(f"{Fore.GREEN}{i}. {Fore.WHITE}{item}")

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
            entrada = input(f"{Fore.CYAN}📝 {prompt}: {Style.RESET_ALL}").strip()
            
            if tipo_validacao:
                valido, mensagem = tipo_validacao(entrada)
                if valido:
                    return entrada
                else:
                    exibir_mensagem_erro(mensagem)
            else:
                return entrada
                
        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}⚠️  Operação cancelada pelo usuário.")
            return None
        except Exception as e:
            exibir_mensagem_erro("Erro inesperado. Tente novamente.")

def tipos_comuns_de_solos(solos):
    """
    Exibe tipos de solos comuns com formatação colorida
    
    Args:
        solos (dict): Dicionário com tipos de solos
    """
    print(f"\n{Fore.MAGENTA}{'='*50}")
    print(f"{Fore.YELLOW}{Style.BRIGHT}    🌱 TIPOS DE SOLOS COMUNS 🌱")
    print(f"{Fore.MAGENTA}{'='*50}")
    
    for key, solo in solos.items():
        print(f"{Fore.GREEN}{key}. {Fore.WHITE}{solo}")
    
    print(f"{Fore.MAGENTA}{'='*50}")

def exibir_mensagem_alerta(mensagem):
    """
    Exibe uma mensagem de alerta formatada
    
    Args:
        mensagem (str): Mensagem de alerta a ser exibida
    """
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}⚠️  ATENÇÃO: {mensagem}{Style.RESET_ALL}")
    print()

def exibir_titulo_secao(titulo, icone="📋"):
    """
    Exibe um título de seção com formatação especial
    
    Args:
        titulo (str): Título da seção
        icone (str): Ícone para o título
    """
    print(f"\n{Fore.BLUE}{Style.BRIGHT}{icone} {titulo.upper()}")
    print(f"{Fore.BLUE}{'-' * (len(titulo) + 4)}")

def exibir_banner_boas_vindas():
    """
    Exibe um banner de boas-vindas elaborado
    """
    largura = 70
    
    print(f"\n{Fore.GREEN}{'█' * largura}")
    print(f"{Fore.GREEN}█{' ' * (largura - 2)}█")
    print(f"{Fore.GREEN}█{Fore.YELLOW}{Style.BRIGHT}  🌾 BEM-VINDO AO SISTEMA DE MONITORAMENTO AGRÍCOLA 🌾  {Fore.GREEN}█")
    print(f"{Fore.GREEN}█{' ' * (largura - 2)}█")
    print(f"{Fore.GREEN}█{Fore.WHITE}  📊 Controle inteligente de produtividade na cana-de-açúcar{' ' * (largura - 62)}█")
    print(f"{Fore.GREEN}█{Fore.WHITE}  🎯 Análise de perdas e otimização de colheitas{' ' * (largura - 49)}█")
    print(f"{Fore.GREEN}█{Fore.WHITE}  💾 Integração com banco de dados Oracle{' ' * (largura - 42)}█")
    print(f"{Fore.GREEN}█{' ' * (largura - 2)}█")
    print(f"{Fore.GREEN}{'█' * largura}{Style.RESET_ALL}")

def exibir_rodape():
    """
    Exibe um rodapé formatado para o sistema
    """
    largura = 70
    
    print(f"\n{Fore.CYAN}{'='*largura}")
    print(f"{Fore.WHITE}{Style.DIM}  Sistema desenvolvido para monitoramento de perdas na colheita")
    print(f"{Fore.WHITE}{Style.DIM}         🌾 Tecnologia a serviço da agricultura 🌾")
    print(f"{Fore.CYAN}{'='*largura}{Style.RESET_ALL}")

def exibir_separador_secao():
    """
    Exibe um separador visual entre seções
    """
    largura = 70
    
    print(f"\n{Fore.MAGENTA}{'▓' * largura}")
    print(f"{Fore.MAGENTA}{'▓' * largura}{Style.RESET_ALL}\n")
