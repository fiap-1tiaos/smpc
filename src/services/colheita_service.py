"""
Módulo de serviços para gerenciamento de colheitas
Contém funções para registro e manipulação de colheitas
"""

from src.models.colheita import Colheita
from src.utils.validation import (
    validar_data,
    validar_area_propriedade,
    validar_quantidade_colheita,
    validar_tipo_colheita,
    validar_produtividade_suspeita
)
from src.utils.menu_utils import (
    solicitar_entrada,
    exibir_mensagem_sucesso,
    exibir_mensagem_erro,
    exibir_mensagem_info,
    confirmar_acao,
    exibir_lista_numerada
)
from src.services.propriedade_service import selecionar_propriedade

def listar_propriedades(lista_propriedades):
    """
    Exibe lista de propriedades disponíveis para seleção
    
    Args:
        lista_propriedades (list): Lista de objetos Propriedade
    """
    if not lista_propriedades:
        exibir_mensagem_erro("Nenhuma propriedade cadastrada.")
        exibir_mensagem_info("Cadastre uma propriedade primeiro antes de registrar colheitas.")
        return
    
    print("\n" + "="*60)
    print("    PROPRIEDADES DISPONÍVEIS")
    print("="*60)
    
    nomes_propriedades = []
    for i, propriedade in enumerate(lista_propriedades, 1):
        nome_completo = f"{propriedade.nome} ({propriedade.area_total} ha - {propriedade.localizacao})"
        nomes_propriedades.append(nome_completo)
    
    exibir_lista_numerada(nomes_propriedades, "Escolha uma propriedade")

def registrar_colheita(lista_propriedades):
    """
    Função para registrar uma nova colheita em uma propriedade
    Solicita dados do usuário, valida e cria objeto Colheita
    
    Args:
        lista_propriedades (list): Lista de propriedades disponíveis
        
    Returns:
        bool: True se colheita foi registrada com sucesso, False caso contrário
    """
    if not lista_propriedades:
        exibir_mensagem_erro("Nenhuma propriedade cadastrada.")
        exibir_mensagem_info("Cadastre uma propriedade primeiro antes de registrar colheitas.")
        return False
    
    exibir_mensagem_info("Selecione a propriedade para registrar a colheita:")
    
    # Selecionar propriedade
    propriedade_selecionada = selecionar_propriedade(lista_propriedades)
    if propriedade_selecionada is None:
        exibir_mensagem_info("Registro de colheita cancelado.")
        return False
    
    try:
        exibir_mensagem_info("Preencha os dados da colheita:")
        
        # Solicitar data da colheita
        data = solicitar_entrada(
            "Data da colheita (DD/MM/AAAA)", 
            validar_data
        )
        if data is None:  # Usuário cancelou
            return False
        
        # Solicitar área colhida
        area_str = solicitar_entrada(
            f"Área colhida em hectares (máximo {propriedade_selecionada.area_total} ha)", 
            validar_area_propriedade
        )
        if area_str is None:  # Usuário cancelou
            return False
        
        area_colhida = float(area_str)
        
        # Verificar se área colhida não excede área total da propriedade
        if area_colhida > propriedade_selecionada.area_total:
            exibir_mensagem_erro(f"Área colhida ({area_colhida} ha) não pode ser maior que a área total da propriedade ({propriedade_selecionada.area_total} ha)")
            return False
        
        # Solicitar quantidade colhida
        quantidade_str = solicitar_entrada(
            "Quantidade colhida (toneladas)", 
            validar_quantidade_colheita
        )
        if quantidade_str is None:  # Usuário cancelou
            return False
        
        quantidade_colhida = float(quantidade_str)
        
        # Solicitar tipo de colheita
        exibir_mensagem_info("Tipos de colheita: 'manual' ou 'mecanica'")
        tipo_colheita = solicitar_entrada(
            "Tipo de colheita", 
            validar_tipo_colheita
        )
        if tipo_colheita is None:  # Usuário cancelou
            return False
        
        # Validar se a produtividade está dentro de valores razoáveis
        eh_suspeito, mensagem_alerta, produtividade_calc = validar_produtividade_suspeita(area_colhida, quantidade_colhida)
        
        if eh_suspeito:
            exibir_mensagem_erro(mensagem_alerta)
            print("\n📊 VALORES TÍPICOS PARA CANA-DE-AÇÚCAR:")
            print("• Produtividade baixa: 40-60 t/ha")
            print("• Produtividade média: 60-80 t/ha") 
            print("• Produtividade alta: 80-100 t/ha")
            print("• Produtividade excepcional: 100-120 t/ha")
            print("\n💡 DICA: Verifique se:")
            print("• A área está em HECTARES (não em metros²)")
            print("• A quantidade está em TONELADAS (não em kg)")
            print("• Os valores foram digitados corretamente")
            
            if not confirmar_acao("Deseja continuar mesmo com estes valores suspeitos?"):
                exibir_mensagem_info("Registro cancelado. Verifique os dados e tente novamente.")
                return False
        
        # Criar objeto Colheita
        colheita = Colheita(data, area_colhida, quantidade_colhida, tipo_colheita.lower())
        
        # Exibir resumo e confirmar
        print("\n" + "="*50)
        print("RESUMO DA COLHEITA:")
        print("="*50)
        print(f"Propriedade: {propriedade_selecionada.nome}")
        print(colheita)
        print(f"Produtividade Calculada: {colheita.produtividade} t/ha")
        
        # Mostrar análise básica
        if colheita.produtividade > 0:
            if colheita.eh_colheita_manual():
                exibir_mensagem_info("Colheita manual geralmente tem menor perda (até 5%)")
            else:
                exibir_mensagem_info("Colheita mecânica pode ter perdas de até 15%")
        
        if confirmar_acao("Confirma o registro desta colheita?"):
            # Adicionar colheita à propriedade
            propriedade_selecionada.adicionar_colheita(colheita)
            
            exibir_mensagem_sucesso(f"Colheita registrada com sucesso na propriedade '{propriedade_selecionada.nome}'!")
            exibir_mensagem_info(f"Produtividade calculada: {colheita.produtividade} t/ha")
            exibir_mensagem_info(f"Total de colheitas na propriedade: {propriedade_selecionada.obter_total_colheitas()}")
            
            return True
        else:
            exibir_mensagem_info("Registro de colheita cancelado pelo usuário.")
            return False
            
    except Exception as e:
        exibir_mensagem_erro(f"Erro ao registrar colheita: {e}")
        return False

def listar_colheitas_propriedade(propriedade):
    """
    Lista todas as colheitas de uma propriedade específica
    
    Args:
        propriedade (Propriedade): Propriedade para listar colheitas
    """
    if not propriedade.colheitas:
        exibir_mensagem_info(f"Nenhuma colheita registrada na propriedade '{propriedade.nome}'")
        return
    
    print(f"\n" + "="*60)
    print(f"    COLHEITAS DA PROPRIEDADE: {propriedade.nome.upper()}")
    print("="*60)
    
    for i, colheita in enumerate(propriedade.colheitas, 1):
        print(f"\n--- COLHEITA {i} ---")
        print(f"Data: {colheita.data}")
        print(f"Área: {colheita.area_colhida} ha")
        print(f"Quantidade: {colheita.quantidade_colhida} t")
        print(f"Tipo: {colheita.tipo_colheita.title()}")
        print(f"Produtividade: {colheita.produtividade} t/ha")
        print("-" * 30)

def obter_estatisticas_colheitas(lista_propriedades):
    """
    Calcula estatísticas gerais das colheitas
    
    Args:
        lista_propriedades (list): Lista de propriedades
        
    Returns:
        dict: Dicionário com estatísticas das colheitas
    """
    stats = {
        'total_colheitas': 0,
        'total_area_colhida': 0.0,
        'total_quantidade_colhida': 0.0,
        'colheitas_manuais': 0,
        'colheitas_mecanicas': 0,
        'produtividade_media': 0.0
    }
    
    todas_colheitas = []
    
    for propriedade in lista_propriedades:
        for colheita in propriedade.colheitas:
            todas_colheitas.append(colheita)
            stats['total_colheitas'] += 1
            stats['total_area_colhida'] += colheita.area_colhida
            stats['total_quantidade_colhida'] += colheita.quantidade_colhida
            
            if colheita.eh_colheita_manual():
                stats['colheitas_manuais'] += 1
            else:
                stats['colheitas_mecanicas'] += 1
    
    # Calcular produtividade média
    if stats['total_area_colhida'] > 0:
        stats['produtividade_media'] = round(
            stats['total_quantidade_colhida'] / stats['total_area_colhida'], 2
        )
    
    return stats

def exibir_resumo_colheitas(lista_propriedades):
    """
    Exibe um resumo geral de todas as colheitas
    
    Args:
        lista_propriedades (list): Lista de propriedades
    """
    stats = obter_estatisticas_colheitas(lista_propriedades)
    
    if stats['total_colheitas'] == 0:
        exibir_mensagem_info("Nenhuma colheita registrada ainda.")
        return
    
    print("\n" + "="*60)
    print("    RESUMO GERAL DAS COLHEITAS")
    print("="*60)
    print(f"Total de Colheitas: {stats['total_colheitas']}")
    print(f"Área Total Colhida: {stats['total_area_colhida']} hectares")
    print(f"Quantidade Total Colhida: {stats['total_quantidade_colhida']} toneladas")
    print(f"Produtividade Média: {stats['produtividade_media']} t/ha")
    print()
    print("DISTRIBUIÇÃO POR TIPO:")
    print(f"  • Colheitas Manuais: {stats['colheitas_manuais']}")
    print(f"  • Colheitas Mecânicas: {stats['colheitas_mecanicas']}")
    
    if stats['colheitas_manuais'] > 0 and stats['colheitas_mecanicas'] > 0:
        percentual_manual = round((stats['colheitas_manuais'] / stats['total_colheitas']) * 100, 1)
        percentual_mecanica = round((stats['colheitas_mecanicas'] / stats['total_colheitas']) * 100, 1)
        print(f"  • Percentual Manual: {percentual_manual}%")
        print(f"  • Percentual Mecânica: {percentual_mecanica}%")
    
    print("="*60)