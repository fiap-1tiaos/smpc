"""
Módulo de integração entre banco de dados e funcionalidades do sistema
Combina operações de banco com lógica de negócio
"""
import services.database_service
from services.database_service import (
    conectar_oracle,
    testar_conexao,
    criar_tabelas,
    salvar_propriedade_oracle,
    salvar_colheita_oracle,
    buscar_propriedades_oracle,
    buscar_historico_completo,
    obter_estatisticas_banco
)
from services.propriedade_service import cadastrar_propriedade
from services.colheita_service import registrar_colheita
from services.calculation_service import gerar_relatorio_perdas, analisar_colheita
from services.file_service import salvar_backup_json, carregar_backup_json
from utils.menu_utils import (
    exibir_mensagem_sucesso,
    exibir_mensagem_erro,
    exibir_mensagem_info,
    confirmar_acao,
    exibir_cabecalho
)

# Variável para controlar se o banco está disponível
_banco_disponivel = None

def verificar_banco_disponivel():
    """
    Verifica se o banco Oracle está disponível
    
    Returns:
        bool: True se banco está disponível, False caso contrário
    """
    global _banco_disponivel
    
    if _banco_disponivel is None:
        _banco_disponivel = testar_conexao()
    
    return _banco_disponivel

def inicializar_sistema():
    """
    Inicializa o sistema verificando banco e criando tabelas se necessário
    
    Returns:
        bool: True se sistema foi inicializado, False caso contrário
    """
    exibir_cabecalho("Inicializando Sistema")
    
    # Verificar se Oracle está disponível
    if verificar_banco_disponivel():
        exibir_mensagem_sucesso("Banco Oracle conectado!")
        
        # Criar tabelas se não existirem
        if criar_tabelas():
            exibir_mensagem_info("Sistema pronto para uso com Oracle")
            return True
        else:
            exibir_mensagem_erro("Erro ao criar tabelas no Oracle")
            return False
    else:
        exibir_mensagem_info("Oracle não disponível. Sistema funcionará apenas com arquivos JSON.")
        return True

def cadastrar_propriedade_integrado():
    """
    Cadastra propriedade integrando com banco de dados
    
    Returns:
        Propriedade: Propriedade cadastrada ou None se houver erro
    """
    # Usar função existente para cadastro interativo
    propriedade = cadastrar_propriedade()
    
    if propriedade and verificar_banco_disponivel():
        # Salvar no banco Oracle
        propriedade_id = salvar_propriedade_oracle(propriedade)
        if propriedade_id:
            propriedade.id = propriedade_id
            exibir_mensagem_info("Propriedade salva no banco Oracle")
        else:
            exibir_mensagem_erro("Erro ao salvar no banco Oracle")
    
    return propriedade

def registrar_colheita_integrado(lista_propriedades):
    """
    Registra colheita integrando com banco de dados
    
    Args:
        lista_propriedades (list): Lista de propriedades disponíveis
        
    Returns:
        bool: True se colheita foi registrada, False caso contrário
    """
    # Se banco disponível, carregar propriedades do banco
    if verificar_banco_disponivel():
        propriedades_banco = buscar_propriedades_oracle()
        if propriedades_banco:
            lista_propriedades.clear()
            lista_propriedades.extend(propriedades_banco)
    
    # Usar função existente para registro interativo
    sucesso = registrar_colheita(lista_propriedades)
    
    if sucesso and verificar_banco_disponivel():
        # A última colheita adicionada
        for propriedade in lista_propriedades:
            if propriedade.colheitas:
                ultima_colheita = propriedade.colheitas[-1]
                # Salvar no banco Oracle
                colheita_id = salvar_colheita_oracle(ultima_colheita, propriedade.id)
                if colheita_id:
                    ultima_colheita.id = colheita_id
                    exibir_mensagem_info("Colheita salva no banco Oracle")
                else:
                    exibir_mensagem_erro("Erro ao salvar colheita no banco Oracle")
                break
    
    return sucesso

def gerar_relatorio_integrado(lista_propriedades):
    """
    Gera relatório integrando dados do banco
    
    Args:
        lista_propriedades (list): Lista de propriedades (será atualizada se banco disponível)
    """
    # Se banco disponível, carregar dados do banco
    if verificar_banco_disponivel():
        propriedades_banco = buscar_historico_completo()
        if propriedades_banco:
            lista_propriedades.clear()
            lista_propriedades.extend(propriedades_banco)
            exibir_mensagem_info("Dados carregados do banco Oracle")
    
    # Gerar relatório usando função existente
    gerar_relatorio_perdas(lista_propriedades)

def sincronizar_com_banco(lista_propriedades):
    """
    Sincroniza dados da memória com o banco Oracle
    
    Args:
        lista_propriedades (list): Lista de propriedades em memória
        
    Returns:
        bool: True se sincronização foi bem-sucedida
    """
    if not verificar_banco_disponivel():
        exibir_mensagem_erro("Banco Oracle não disponível para sincronização")
        return False
    
    exibir_mensagem_info("Sincronizando dados com banco Oracle...")
    
    try:
        for propriedade in lista_propriedades:
            # Verificar se propriedade já existe no banco
            if not hasattr(propriedade, 'id'):
                # Salvar nova propriedade
                propriedade_id = salvar_propriedade_oracle(propriedade)
                if propriedade_id:
                    propriedade.id = propriedade_id
                
                # Salvar colheitas da propriedade
                for colheita in propriedade.colheitas:
                    if not hasattr(colheita, 'id'):
                        colheita_id = salvar_colheita_oracle(colheita, propriedade.id)
                        if colheita_id:
                            colheita.id = colheita_id
        
        exibir_mensagem_sucesso("Sincronização com Oracle concluída!")
        return True
        
    except Exception as e:
        exibir_mensagem_erro(f"Erro durante sincronização: {e}")
        return False

def carregar_dados_banco():
    """
    Carrega todos os dados do banco Oracle
    
    Returns:
        list: Lista de propriedades carregadas ou lista vazia se erro
    """
    if not verificar_banco_disponivel():
        exibir_mensagem_info("Banco Oracle não disponível. Usando dados em memória.")
        return []
    
    propriedades = buscar_historico_completo()
    if propriedades:
        exibir_mensagem_sucesso(f"Carregadas {len(propriedades)} propriedades do banco Oracle")
        return propriedades
    else:
        exibir_mensagem_info("Nenhum dado encontrado no banco Oracle")
        return []

def fazer_backup_integrado(lista_propriedades):
    """
    Faz backup integrando dados do banco e memória
    
    Args:
        lista_propriedades (list): Lista de propriedades
        
    Returns:
        bool: True se backup foi realizado
    """
    # Se banco disponível, carregar dados mais recentes
    if verificar_banco_disponivel():
        propriedades_banco = buscar_historico_completo()
        if propriedades_banco:
            lista_propriedades.clear()
            lista_propriedades.extend(propriedades_banco)
            exibir_mensagem_info("Dados atualizados do banco Oracle para backup")
    
    # Fazer backup usando função existente
    from services.file_service import fazer_backup_interativo
    return fazer_backup_interativo(lista_propriedades)

def importar_backup_integrado():
    """
    Importa backup e sincroniza com banco se disponível
    
    Returns:
        list: Lista de propriedades importadas ou None se cancelado
    """
    from services.file_service import importar_backup_interativo
    
    propriedades_importadas = importar_backup_interativo()
    
    if propriedades_importadas and verificar_banco_disponivel():
        if confirmar_acao("Deseja sincronizar os dados importados com o banco Oracle?"):
            sucesso = sincronizar_com_banco(propriedades_importadas)
            if sucesso:
                exibir_mensagem_sucesso("Dados importados e sincronizados com Oracle!")
            else:
                exibir_mensagem_erro("Dados importados, mas erro na sincronização com Oracle")
    
    return propriedades_importadas

def exibir_status_sistema():
    """
    Exibe status atual do sistema (banco, dados, etc.)
    """
    exibir_cabecalho("Status do Sistema")
    
    # Status do banco
    if verificar_banco_disponivel():
        print("✓ Banco Oracle: CONECTADO")
        
        # Estatísticas do banco
        stats = obter_estatisticas_banco()
        if stats:
            print(f"  • Propriedades: {stats['total_propriedades']}")
            print(f"  • Colheitas: {stats['total_colheitas']}")
            print(f"  • Área total colhida: {stats['area_total_colhida']:.2f} ha")
            print(f"  • Produtividade média: {stats['produtividade_media']:.2f} t/ha")
    else:
        print("✗ Banco Oracle: NÃO DISPONÍVEL")
        print("  • Sistema funcionando apenas com arquivos JSON")
    
    print("\nFuncionalidades disponíveis:")
    print("✓ Cadastro de propriedades")
    print("✓ Registro de colheitas")
    print("✓ Relatórios de perdas")
    print("✓ Backup/restore JSON")
    
    if verificar_banco_disponivel():
        print("✓ Persistência em Oracle")
        print("✓ Sincronização automática")
    else:
        print("⚠ Dados apenas em memória (não persistentes)")

def menu_configuracao_banco():
    """
    Menu para configuração e teste do banco Oracle
    """
    while True:
        exibir_cabecalho("Configuração do Banco Oracle")
        
        print("1. Testar Conexão")
        print("2. Criar/Verificar Tabelas")
        print("3. Exibir Status do Sistema")
        print("4. Ver Referências Científicas")
        print("5. Limpar Dados do Banco (CUIDADO!)")
        print("6. Voltar ao Menu Principal")
        
        try:
            opcao = input("\nEscolha uma opção (1-6): ").strip()
            
            if opcao == '1':
                testar_conexao()
            elif opcao == '2':
                criar_tabelas()
            elif opcao == '3':
                exibir_status_sistema()
            elif opcao == '4':
                from services.calculation_service import exibir_referencias_cientificas
                exibir_referencias_cientificas()
            elif opcao == '5':
                if confirmar_acao("ATENÇÃO: Isso removerá TODOS os dados do banco Oracle. Confirma?"):
                    from services.database_service import limpar_dados_banco
                    limpar_dados_banco()
            elif opcao == '6':
                break
            else:
                exibir_mensagem_erro("Opção inválida. Digite um número entre 1 e 6.")
            
            input("\nPressione Enter para continuar...")
            
        except KeyboardInterrupt:
            print("\n\nVoltando ao menu principal...")
            break
        except Exception as e:
            exibir_mensagem_erro(f"Erro inesperado: {e}")
            input("\nPressione Enter para continuar...")