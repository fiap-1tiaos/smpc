"""
Módulo de serviços para manipulação de arquivos JSON
Contém funções para backup e restauração de dados
"""

import json
import os
from datetime import datetime
from src.models.propriedade import Propriedade
from src.models.colheita import Colheita
from src.utils.menu_utils import (
    exibir_mensagem_sucesso,
    exibir_mensagem_erro,
    exibir_mensagem_info,
    confirmar_acao
)

def converter_propriedade_para_dict(propriedade):
    """
    Converte um objeto Propriedade para dicionário
    
    Args:
        propriedade (Propriedade): Objeto propriedade a ser convertido
        
    Returns:
        dict: Dicionário com dados da propriedade
    """
    colheitas_dict = []
    for colheita in propriedade.colheitas:
        colheita_dict = {
            'data': colheita.data,
            'area_colhida': colheita.area_colhida,
            'quantidade_colhida': colheita.quantidade_colhida,
            'tipo_colheita': colheita.tipo_colheita,
            'produtividade': colheita.produtividade
        }
        colheitas_dict.append(colheita_dict)
    
    propriedade_dict = {
        'nome': propriedade.nome,
        'area_total': propriedade.area_total,
        'localizacao': propriedade.localizacao,
        'tipo_solo': propriedade.tipo_solo,
        'colheitas': colheitas_dict
    }
    
    return propriedade_dict

def converter_dict_para_propriedade(dict_propriedade):
    """
    Converte um dicionário para objeto Propriedade
    
    Args:
        dict_propriedade (dict): Dicionário com dados da propriedade
        
    Returns:
        Propriedade: Objeto propriedade criado
    """
    # Criar propriedade
    propriedade = Propriedade(
        dict_propriedade['nome'],
        dict_propriedade['area_total'],
        dict_propriedade['localizacao'],
        dict_propriedade['tipo_solo']
    )
    
    # Adicionar colheitas se existirem
    if 'colheitas' in dict_propriedade:
        for colheita_dict in dict_propriedade['colheitas']:
            colheita = Colheita(
                colheita_dict['data'],
                colheita_dict['area_colhida'],
                colheita_dict['quantidade_colhida'],
                colheita_dict['tipo_colheita']
            )
            propriedade.adicionar_colheita(colheita)
    
    return propriedade

def salvar_backup_json(lista_propriedades, nome_arquivo=None):
    """
    Salva backup das propriedades em arquivo JSON
    
    Args:
        lista_propriedades (list): Lista de propriedades a serem salvas
        nome_arquivo (str): Nome do arquivo (opcional)
        
    Returns:
        bool: True se salvou com sucesso, False caso contrário
    """
    try:
        # Definir nome do arquivo se não fornecido
        if nome_arquivo is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"backup_colheitas_{timestamp}.json"
        
        # Garantir que o arquivo tenha extensão .json
        if not nome_arquivo.endswith('.json'):
            nome_arquivo += '.json'
        
        # Caminho completo do arquivo
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        caminho_arquivo = os.path.join(base_dir, "scripts", "data", nome_arquivo)
        
        # Criar pasta data se não existir
        os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)
        
        # Converter propriedades para dicionários
        propriedades_dict = []
        for propriedade in lista_propriedades:
            propriedades_dict.append(converter_propriedade_para_dict(propriedade))
        
        # Estrutura do backup
        backup_data = {
            'versao': '1.0',
            'data_backup': datetime.now().isoformat(),
            'total_propriedades': len(lista_propriedades),
            'total_colheitas': sum(len(prop.colheitas) for prop in lista_propriedades),
            'propriedades': propriedades_dict
        }
        
        # Salvar arquivo JSON
        with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
            json.dump(backup_data, arquivo, indent=2, ensure_ascii=False)
        
        exibir_mensagem_sucesso(f"Backup salvo com sucesso!")
        exibir_mensagem_info(f"Arquivo: {caminho_arquivo}")
        exibir_mensagem_info(f"Propriedades: {backup_data['total_propriedades']}")
        exibir_mensagem_info(f"Colheitas: {backup_data['total_colheitas']}")
        
        return True
        
    except Exception as e:
        exibir_mensagem_erro(f"Erro ao salvar backup: {e}")
        return False

def carregar_backup_json(nome_arquivo):
    """
    Carrega backup de arquivo JSON
    
    Args:
        nome_arquivo (str): Nome do arquivo a ser carregado
        
    Returns:
        list: Lista de propriedades carregadas ou None se houver erro
    """
    try:
        # Caminho completo do arquivo
        caminho_arquivo = os.path.join("scripts", "data", nome_arquivo)
        
        # Verificar se arquivo existe
        if not os.path.exists(caminho_arquivo):
            exibir_mensagem_erro(f"Arquivo não encontrado: {caminho_arquivo}")
            return None
        
        # Carregar arquivo JSON
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            backup_data = json.load(arquivo)
        
        # Validar estrutura do backup
        if not validar_estrutura_json(backup_data):
            exibir_mensagem_erro("Estrutura do arquivo de backup inválida")
            return None
        
        # Converter dicionários para objetos
        propriedades_carregadas = []
        for prop_dict in backup_data['propriedades']:
            propriedade = converter_dict_para_propriedade(prop_dict)
            propriedades_carregadas.append(propriedade)
        
        exibir_mensagem_sucesso(f"Backup carregado com sucesso!")
        exibir_mensagem_info(f"Arquivo: {nome_arquivo}")
        exibir_mensagem_info(f"Versão: {backup_data.get('versao', 'N/A')}")
        exibir_mensagem_info(f"Data do backup: {backup_data.get('data_backup', 'N/A')}")
        exibir_mensagem_info(f"Propriedades carregadas: {len(propriedades_carregadas)}")
        
        return propriedades_carregadas
        
    except json.JSONDecodeError as e:
        exibir_mensagem_erro(f"Erro ao ler arquivo JSON: {e}")
        return None
    except Exception as e:
        exibir_mensagem_erro(f"Erro ao carregar backup: {e}")
        return None

def validar_estrutura_json(backup_data):
    """
    Valida se a estrutura do JSON está correta
    
    Args:
        backup_data (dict): Dados do backup carregado
        
    Returns:
        bool: True se estrutura é válida, False caso contrário
    """
    try:
        # Verificar campos obrigatórios
        campos_obrigatorios = ['versao', 'propriedades']
        for campo in campos_obrigatorios:
            if campo not in backup_data:
                return False
        
        # Verificar se propriedades é uma lista
        if not isinstance(backup_data['propriedades'], list):
            return False
        
        # Verificar estrutura de cada propriedade
        for propriedade in backup_data['propriedades']:
            campos_propriedade = ['nome', 'area_total', 'localizacao', 'tipo_solo']
            for campo in campos_propriedade:
                if campo not in propriedade:
                    return False
            
            # Verificar colheitas se existirem
            if 'colheitas' in propriedade:
                if not isinstance(propriedade['colheitas'], list):
                    return False
                
                for colheita in propriedade['colheitas']:
                    campos_colheita = ['data', 'area_colhida', 'quantidade_colhida', 'tipo_colheita']
                    for campo in campos_colheita:
                        if campo not in colheita:
                            return False
        
        return True
        
    except Exception:
        return False

def listar_arquivos_backup():
    """
    Lista todos os arquivos de backup disponíveis na pasta scripts/data
    
    Returns:
        list: Lista de dicionários contendo informações dos arquivos de backup
    """
    try:
        # Caminho absoluto até a pasta smcp/
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        pasta_data = os.path.join(base_dir, "scripts", "data")
        
        # Se a pasta não existir, retorna lista vazia
        if not os.path.exists(pasta_data):
            return []
        
        arquivos = []
        for arquivo in os.listdir(pasta_data):
            if arquivo.endswith('.json'):
                caminho_completo = os.path.join(pasta_data, arquivo)
                tamanho = os.path.getsize(caminho_completo)
                modificacao = os.path.getmtime(caminho_completo)
                data_modificacao = datetime.fromtimestamp(modificacao).strftime("%d/%m/%Y %H:%M")
                
                arquivos.append({
                    'nome': arquivo,
                    'tamanho': tamanho,
                    'data_modificacao': data_modificacao
                })
        
        # Ordena por data de modificação (opcional: mais recentes primeiro)
        arquivos.sort(key=lambda x: x['data_modificacao'], reverse=True)
        
        return arquivos
        
    except Exception as e:
        exibir_mensagem_erro(f"Erro ao listar arquivos: {e}")
        return []

def fazer_backup_interativo(lista_propriedades):
    """
    Função interativa para fazer backup
    
    Args:
        lista_propriedades (list): Lista de propriedades
        
    Returns:
        bool: True se backup foi realizado, False caso contrário
    """
    if not lista_propriedades:
        exibir_mensagem_erro("Nenhuma propriedade cadastrada para fazer backup.")
        return False
    
    total_colheitas = sum(len(prop.colheitas) for prop in lista_propriedades)
    
    print(f"\nDADOS PARA BACKUP:")
    print(f"• Propriedades: {len(lista_propriedades)}")
    print(f"• Colheitas: {total_colheitas}")
    
    if confirmar_acao("Deseja fazer o backup destes dados?"):
        return salvar_backup_json(lista_propriedades)
    else:
        exibir_mensagem_info("Backup cancelado pelo usuário.")
        return False

def importar_backup_interativo():
    """
    Função interativa para importar backup
    
    Returns:
        list: Lista de propriedades importadas ou None se cancelado
    """
    arquivos = listar_arquivos_backup()
    
    if not arquivos:
        exibir_mensagem_erro("Nenhum arquivo de backup encontrado na pasta 'scripts/data'.")
        exibir_mensagem_info("Coloque arquivos .json na pasta 'scripts/data' para importar.")
        return None
    
    print(f"\nARQUIVOS DE BACKUP DISPONÍVEIS:")
    print("-" * 60)
    
    for i, arquivo in enumerate(arquivos, 1):
        print(f"{i}. {arquivo['nome']}")
        print(f"   Tamanho: {arquivo['tamanho']} bytes")
        print(f"   Modificado: {arquivo['data_modificacao']}")
        print()
    
    try:
        opcao = input(f"Escolha um arquivo (1-{len(arquivos)}) ou 0 para cancelar: ").strip()
        
        if opcao == '0':
            return None
        
        indice = int(opcao) - 1
        
        if 0 <= indice < len(arquivos):
            arquivo_selecionado = arquivos[indice]['nome']
            
            if confirmar_acao(f"Importar backup do arquivo '{arquivo_selecionado}'?"):
                return carregar_backup_json(arquivo_selecionado)
            else:
                exibir_mensagem_info("Importação cancelada.")
                return None
        else:
            exibir_mensagem_erro(f"Opção inválida. Digite um número entre 1 e {len(arquivos)}")
            return None
            
    except ValueError:
        exibir_mensagem_erro("Digite um número válido.")
        return None
    except Exception as e:
        exibir_mensagem_erro(f"Erro durante importação: {e}")
        return None