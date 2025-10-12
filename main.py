from utils.menu_utils import (
    exibir_menu_principal, 
    obter_opcao_usuario, 
    exibir_mensagem_sucesso,
    exibir_mensagem_info,
    exibir_cabecalho,
    pausar_execucao,
    confirmar_acao,
    limpar_tela
)

from services.sistema_integrado import (
    inicializar_sistema,
    cadastrar_propriedade_integrado,
    registrar_colheita_integrado,
    gerar_relatorio_integrado,
    fazer_backup_integrado,
    importar_backup_integrado,
    carregar_dados_banco,
    menu_configuracao_banco,
    exibir_status_sistema
)
from services.colheita_service import exibir_resumo_colheitas

# Lista global para armazenar propriedades (temporariamente)
propriedades_cadastradas = []

def processar_opcao_menu(opcao):
    """
    Processa a opção escolhida pelo usuário no menu
    
    Args:
        opcao (int): Opção escolhida pelo usuário
        
    Returns:
        bool: True para continuar, False para sair
    """
    if opcao == 1:
        exibir_cabecalho("Cadastrar Nova Propriedade")
        nova_propriedade = cadastrar_propriedade_integrado()
        if nova_propriedade:
            propriedades_cadastradas.append(nova_propriedade)
            exibir_mensagem_info(f"Total de propriedades: {len(propriedades_cadastradas)}")
        pausar_execucao()

    elif opcao == 2:
        exibir_cabecalho("Registrar Colheita")
        sucesso = registrar_colheita_integrado(propriedades_cadastradas)
        if sucesso:
            exibir_mensagem_info("Colheita registrada com sucesso!")
        pausar_execucao()
        
    elif opcao == 3:
        exibir_cabecalho("Consultar Relatório de Perdas")
        gerar_relatorio_integrado(propriedades_cadastradas)
        pausar_execucao()
        
    elif opcao == 4:
        exibir_cabecalho("Visualizar Histórico")
        exibir_resumo_colheitas(propriedades_cadastradas)
        pausar_execucao()
        
    elif opcao == 5:
        exibir_cabecalho("Fazer Backup dos Dados")
        fazer_backup_integrado(propriedades_cadastradas)
        pausar_execucao()
        
    elif opcao == 6:
        exibir_cabecalho("Importar Backup")
        propriedades_importadas = importar_backup_integrado()
        if propriedades_importadas:
            if confirmar_acao("Deseja substituir os dados atuais pelos dados importados?"):
                propriedades_cadastradas.clear()
                propriedades_cadastradas.extend(propriedades_importadas)
                exibir_mensagem_sucesso("Dados importados com sucesso!")
            else:
                exibir_mensagem_info("Dados não foram alterados.")
        pausar_execucao()
        
    elif opcao == 7:
        exibir_cabecalho("Configuração do Banco Oracle")
        menu_configuracao_banco()
        
    elif opcao == 8:
        exibir_status_sistema()
        pausar_execucao()
        
    elif opcao == 9:
        exibir_mensagem_sucesso("Obrigado por usar o Sistema de Monitoramento de Perdas!")
        exibir_mensagem_info("Sistema encerrado.")
        return False
    
    return True

def main():
    """
    Função principal do sistema - Loop principal do menu
    """
    exibir_cabecalho("Bem-vindo ao Sistema de Monitoramento de Perdas")
    exibir_mensagem_info("Sistema para análise de perdas na colheita de cana-de-açúcar")
    
    # Inicializar sistema (verificar banco, criar tabelas, etc.)
    inicializar_sistema()
    
    # Carregar dados existentes do banco se disponível
    propriedades_banco = carregar_dados_banco()
    if propriedades_banco:
        propriedades_cadastradas.extend(propriedades_banco)
    
    # Loop principal do sistema
    continuar = True
    while continuar:
        try:
            exibir_menu_principal()
            opcao = obter_opcao_usuario()
            continuar = processar_opcao_menu(opcao)
            
        except KeyboardInterrupt:
            print("\n\nSistema interrompido pelo usuário.")
            break
        except Exception as e:
            print(f"\nErro inesperado: {e}")
            print("Reiniciando o menu...")
            pausar_execucao()

if __name__ == "__main__":
    main()