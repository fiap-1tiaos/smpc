"""
Módulo de serviços para conexão e operações com banco de dados Oracle
Contém funções para CRUD e gerenciamento de dados
"""

try:
    from dotenv import load_dotenv
    import cx_Oracle
    import os

    # Carregar as variáveis de ambiente
    load_dotenv()

    instant_client_path = os.getenv('ORACLE_CLIENT_PATH')
    if os.path.exists(instant_client_path):
        os.environ["PATH"] = instant_client_path + ";" + os.environ["PATH"]
        os.add_dll_directory(instant_client_path)
    else:
        print("⚠️ Caminho do Oracle Client não encontrado. Instale o Oracle Client em https://www.oracle.com/database/technologies/instant-client/downloads.html")
    ORACLE_DISPONIVEL = True
except ImportError as e:
    print(f'ERROR {e}')
    ORACLE_DISPONIVEL = False
    cx_Oracle = None

from datetime import datetime
from config.database_config import (
    obter_string_conexao, 
    CONFIG_AVANCADA,
    SQL_CREATE_TABLES,
    SQL_INSERT,
    SQL_SELECT
)
from utils.menu_utils import (
    exibir_mensagem_sucesso,
    exibir_mensagem_erro,
    exibir_mensagem_info
)
from models.propriedade import Propriedade
from models.colheita import Colheita

# Variável global para conexão (pool de conexões)
_connection_pool = None

def conectar_oracle():
    """
    Estabelece conexão com banco Oracle
    
    Returns:
        cx_Oracle.Connection: Objeto de conexão ou None se falhar
    """
    if not ORACLE_DISPONIVEL:
        exibir_mensagem_info("Biblioteca cx_Oracle não instalada. Banco Oracle não disponível.")
        return None
    
    try:
        config_conexao = obter_string_conexao()

        # Tentar conectar
        conexao = cx_Oracle.connect(
            user=config_conexao['user'],
            password=config_conexao['password'],
            dsn=config_conexao['dsn'],
            encoding=config_conexao['encoding']
        )
        
        return conexao
        
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        exibir_mensagem_erro(f"Erro de banco de dados: {error.message}")
        return None
    except Exception as e:
        exibir_mensagem_erro(f"Erro ao conectar com Oracle: {e}")
        return None

def fechar_conexao(conexao):
    """
    Fecha conexão com o banco Oracle
    
    Args:
        conexao: Objeto de conexão Oracle
    """
    try:
        if conexao:
            conexao.close()
    except Exception as e:
        exibir_mensagem_erro(f"Erro ao fechar conexão: {e}")

def testar_conexao():
    """
    Testa a conexão com o banco Oracle
    
    Returns:
        bool: True se conexão foi bem-sucedida, False caso contrário
    """
    if not ORACLE_DISPONIVEL:
        exibir_mensagem_info("cx_Oracle não instalado. Para usar Oracle:")
        exibir_mensagem_info("1. Instale Oracle Database")
        exibir_mensagem_info("2. Execute: pip install cx_Oracle")
        return False
    
    exibir_mensagem_info("Testando conexão com Oracle...")
    
    conexao = conectar_oracle()
    if conexao:
        try:
            cursor = conexao.cursor()
            cursor.execute("SELECT 'Conexão OK' FROM DUAL")
            resultado = cursor.fetchone()
            cursor.close()
            fechar_conexao(conexao)
            
            exibir_mensagem_sucesso("Conexão com Oracle estabelecida com sucesso!")
            exibir_mensagem_info(f"Resultado do teste: {resultado[0]}")
            return True
            
        except Exception as e:
            exibir_mensagem_erro(f"Erro no teste de conexão: {e}")
            fechar_conexao(conexao)
            return False
    else:
        exibir_mensagem_erro("Não foi possível conectar ao Oracle")
        return False

def criar_tabelas():
    """
    Cria as tabelas necessárias no banco Oracle
    
    Returns:
        bool: True se tabelas foram criadas, False caso contrário
    """
    conexao = conectar_oracle()
    if not conexao:
        return False
    
    try:
        cursor = conexao.cursor()
        
        exibir_mensagem_info("Criando tabelas no banco Oracle...")
        
        # Verificar se tabelas já existem
        cursor.execute("""
            SELECT table_name FROM user_tables 
            WHERE table_name IN ('PROPRIEDADES', 'COLHEITAS')
        """)
        tabelas_existentes = [row[0] for row in cursor.fetchall()]
        
        if 'PROPRIEDADES' in tabelas_existentes and 'COLHEITAS' in tabelas_existentes:
            exibir_mensagem_info("Tabelas já existem no banco de dados.")
            cursor.close()
            fechar_conexao(conexao)
            return True
        
        # Criar tabela propriedades
        if 'PROPRIEDADES' not in tabelas_existentes:
            cursor.execute(SQL_CREATE_TABLES['propriedades'])
            exibir_mensagem_sucesso("Tabela PROPRIEDADES criada com sucesso!")
        
        # Criar tabela colheitas
        if 'COLHEITAS' not in tabelas_existentes:
            cursor.execute(SQL_CREATE_TABLES['colheitas'])
            exibir_mensagem_sucesso("Tabela COLHEITAS criada com sucesso!")
        
        # Commit das alterações
        conexao.commit()
        cursor.close()
        fechar_conexao(conexao)
        
        exibir_mensagem_sucesso("Todas as tabelas foram criadas com sucesso!")
        return True
        
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        exibir_mensagem_erro(f"Erro ao criar tabelas: {error.message}")
        conexao.rollback()
        cursor.close()
        fechar_conexao(conexao)
        return False
    except Exception as e:
        exibir_mensagem_erro(f"Erro inesperado ao criar tabelas: {e}")
        conexao.rollback()
        cursor.close()
        fechar_conexao(conexao)
        return False

def salvar_propriedade_oracle(propriedade):
    """
    Salva uma propriedade no banco Oracle
    
    Args:
        propriedade (Propriedade): Objeto propriedade a ser salvo
        
    Returns:
        int: ID da propriedade salva ou None se houver erro
    """
    conexao = conectar_oracle()
    if not conexao:
        return None
    
    try:
        cursor = conexao.cursor()
        
        # Verificar se propriedade já existe
        cursor.execute(SQL_SELECT['propriedade_por_nome'], {'nome': propriedade.nome})
        propriedade_existente = cursor.fetchone()
        
        if propriedade_existente:
            exibir_mensagem_erro(f"Propriedade '{propriedade.nome}' já existe no banco de dados")
            cursor.close()
            fechar_conexao(conexao)
            return None
        
        # Inserir nova propriedade
        cursor.execute(SQL_INSERT['propriedade'], {
            'nome': propriedade.nome,
            'area_total': propriedade.area_total,
            'localizacao': propriedade.localizacao,
            'tipo_solo': propriedade.tipo_solo
        })
        
        # Obter ID da propriedade inserida (Oracle 12c+ com IDENTITY)
        cursor.execute("SELECT id FROM propriedades WHERE nome = :nome", {'nome': propriedade.nome})
        propriedade_id = cursor.fetchone()[0]
        
        conexao.commit()
        cursor.close()
        fechar_conexao(conexao)
        
        exibir_mensagem_sucesso(f"Propriedade '{propriedade.nome}' salva no banco Oracle!")
        exibir_mensagem_info(f"ID gerado: {propriedade_id}")
        
        return propriedade_id
        
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        exibir_mensagem_erro(f"Erro ao salvar propriedade: {error.message}")
        conexao.rollback()
        cursor.close()
        fechar_conexao(conexao)
        return None
    except Exception as e:
        exibir_mensagem_erro(f"Erro inesperado ao salvar propriedade: {e}")
        conexao.rollback()
        cursor.close()
        fechar_conexao(conexao)
        return None

def salvar_colheita_oracle(colheita, propriedade_id):
    """
    Salva uma colheita no banco Oracle
    
    Args:
        colheita (Colheita): Objeto colheita a ser salvo
        propriedade_id (int): ID da propriedade associada
        
    Returns:
        int: ID da colheita salva ou None se houver erro
    """
    conexao = conectar_oracle()
    if not conexao:
        return None
    
    try:
        cursor = conexao.cursor()
        
        # Calcular percentual de perda (será implementado depois)
        percentual_perda = 0.0  # Por enquanto, será calculado posteriormente
        
        # Inserir nova colheita usando RETURNING clause
        colheita_id_var = cursor.var(cx_Oracle.NUMBER)
        cursor.execute("""
            INSERT INTO colheitas (propriedade_id, data_colheita, area_colhida, 
                                  quantidade_colhida, tipo_colheita, produtividade, percentual_perda)
            VALUES (:propriedade_id, TO_DATE(:data_colheita, 'DD/MM/YYYY'), :area_colhida,
                    :quantidade_colhida, :tipo_colheita, :produtividade, :percentual_perda)
            RETURNING id INTO :colheita_id
        """, {
            'propriedade_id': propriedade_id,
            'data_colheita': colheita.data,
            'area_colhida': colheita.area_colhida,
            'quantidade_colhida': colheita.quantidade_colhida,
            'tipo_colheita': colheita.tipo_colheita,
            'produtividade': colheita.produtividade,
            'percentual_perda': percentual_perda,
            'colheita_id': colheita_id_var
        })
        
        colheita_id = colheita_id_var.getvalue()[0]
        
        conexao.commit()
        cursor.close()
        fechar_conexao(conexao)
        
        exibir_mensagem_sucesso(f"Colheita salva no banco Oracle!")
        exibir_mensagem_info(f"ID gerado: {colheita_id}")
        
        return colheita_id
        
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        exibir_mensagem_erro(f"Erro ao salvar colheita: {error.message}")
        conexao.rollback()
        cursor.close()
        fechar_conexao(conexao)
        return None
    except Exception as e:
        exibir_mensagem_erro(f"Erro inesperado ao salvar colheita: {e}")
        conexao.rollback()
        cursor.close()
        fechar_conexao(conexao)
        return None

def buscar_propriedades_oracle():
    """
    Busca todas as propriedades do banco Oracle
    
    Returns:
        list: Lista de objetos Propriedade ou None se houver erro
    """
    conexao = conectar_oracle()
    if not conexao:
        return None
    
    try:
        cursor = conexao.cursor()
        cursor.execute(SQL_SELECT['todas_propriedades'])
        
        propriedades = []
        for row in cursor.fetchall():
            propriedade = Propriedade(
                nome=row[1],
                area_total=float(row[2]),
                localizacao=row[3],
                tipo_solo=row[4]
            )
            # Adicionar ID para referência
            propriedade.id = row[0]
            propriedades.append(propriedade)
        
        cursor.close()
        fechar_conexao(conexao)
        
        return propriedades
        
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        exibir_mensagem_erro(f"Erro ao buscar propriedades: {error.message}")
        cursor.close()
        fechar_conexao(conexao)
        return None
    except Exception as e:
        exibir_mensagem_erro(f"Erro inesperado ao buscar propriedades: {e}")
        cursor.close()
        fechar_conexao(conexao)
        return None

def buscar_colheitas_por_propriedade(propriedade_id):
    """
    Busca colheitas de uma propriedade específica
    
    Args:
        propriedade_id (int): ID da propriedade
        
    Returns:
        list: Lista de objetos Colheita ou None se houver erro
    """
    conexao = conectar_oracle()
    if not conexao:
        return None
    
    try:
        cursor = conexao.cursor()
        cursor.execute(SQL_SELECT['colheitas_por_propriedade'], {'propriedade_id': propriedade_id})
        
        colheitas = []
        for row in cursor.fetchall():
            # Converter data Oracle para string
            data_colheita = row[2].strftime('%d/%m/%Y') if row[2] else ''
            
            colheita = Colheita(
                data=data_colheita,
                area_colhida=float(row[3]),
                quantidade_colhida=float(row[4]),
                tipo_colheita=row[5]
            )
            # Adicionar ID para referência
            colheita.id = row[0]
            colheitas.append(colheita)
        
        cursor.close()
        fechar_conexao(conexao)
        
        return colheitas
        
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        exibir_mensagem_erro(f"Erro ao buscar colheitas: {error.message}")
        cursor.close()
        fechar_conexao(conexao)
        return None
    except Exception as e:
        exibir_mensagem_erro(f"Erro inesperado ao buscar colheitas: {e}")
        cursor.close()
        fechar_conexao(conexao)
        return None

def buscar_historico_completo():
    """
    Busca histórico completo de propriedades e colheitas
    
    Returns:
        list: Lista de propriedades com colheitas carregadas ou None se houver erro
    """
    # Buscar todas as propriedades
    propriedades = buscar_propriedades_oracle()
    if propriedades is None:
        return None
    
    # Para cada propriedade, buscar suas colheitas
    for propriedade in propriedades:
        colheitas = buscar_colheitas_por_propriedade(propriedade.id)
        if colheitas:
            propriedade.colheitas = colheitas
    
    return propriedades

def obter_estatisticas_banco():
    """
    Obtém estatísticas gerais do banco de dados
    
    Returns:
        dict: Dicionário com estatísticas ou None se houver erro
    """
    conexao = conectar_oracle()
    if not conexao:
        return None
    
    try:
        cursor = conexao.cursor()
        cursor.execute(SQL_SELECT['estatisticas_gerais'])
        
        row = cursor.fetchone()
        if row:
            stats = {
                'total_propriedades': int(row[0]) if row[0] else 0,
                'total_colheitas': int(row[1]) if row[1] else 0,
                'area_total_colhida': float(row[2]) if row[2] else 0.0,
                'quantidade_total_colhida': float(row[3]) if row[3] else 0.0,
                'produtividade_media': float(row[4]) if row[4] else 0.0,
                'perda_media': float(row[5]) if row[5] else 0.0
            }
        else:
            stats = {
                'total_propriedades': 0,
                'total_colheitas': 0,
                'area_total_colhida': 0.0,
                'quantidade_total_colhida': 0.0,
                'produtividade_media': 0.0,
                'perda_media': 0.0
            }
        
        cursor.close()
        fechar_conexao(conexao)
        
        return stats
        
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        exibir_mensagem_erro(f"Erro ao obter estatísticas: {error.message}")
        cursor.close()
        fechar_conexao(conexao)
        return None
    except Exception as e:
        exibir_mensagem_erro(f"Erro inesperado ao obter estatísticas: {e}")
        cursor.close()
        fechar_conexao(conexao)
        return None

def limpar_dados_banco():
    """
    Remove todos os dados das tabelas (apenas para desenvolvimento/teste)
    
    Returns:
        bool: True se dados foram removidos, False caso contrário
    """
    conexao = conectar_oracle()
    if not conexao:
        return False
    
    try:
        cursor = conexao.cursor()
        
        # Remover colheitas primeiro (devido à foreign key)
        cursor.execute("DELETE FROM colheitas")
        colheitas_removidas = cursor.rowcount
        
        # Remover propriedades
        cursor.execute("DELETE FROM propriedades")
        propriedades_removidas = cursor.rowcount
        
        conexao.commit()
        cursor.close()
        fechar_conexao(conexao)
        
        exibir_mensagem_sucesso("Dados removidos do banco Oracle!")
        exibir_mensagem_info(f"Colheitas removidas: {colheitas_removidas}")
        exibir_mensagem_info(f"Propriedades removidas: {propriedades_removidas}")
        
        return True
        
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        exibir_mensagem_erro(f"Erro ao limpar dados: {error.message}")
        conexao.rollback()
        cursor.close()
        fechar_conexao(conexao)
        return False
    except Exception as e:
        exibir_mensagem_erro(f"Erro inesperado ao limpar dados: {e}")
        conexao.rollback()
        cursor.close()
        fechar_conexao(conexao)
        return False