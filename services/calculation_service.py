"""
Módulo de serviços para cálculos de perdas e análises
Contém funções para calcular produtividade, perdas e gerar relatórios
"""

from utils.menu_utils import (
    exibir_mensagem_info,
    exibir_mensagem_erro,
    exibir_cabecalho
)

# Dicionário com produtividades esperadas por tipo de solo (em t/ha)
# Baseado em dados científicos de instituições brasileiras de pesquisa
PRODUTIVIDADE_ESPERADA_POR_SOLO = {
    # Fonte: EMBRAPA Solos + IAC Campinas (2020-2023)
    'latossolo vermelho': 95.0,      # Solos mais férteis e bem drenados
    'latossolo vermelho-amarelo': 88.0,  # Variação do latossolo
    'nitossolo': 92.0,               # Solos estruturados, boa fertilidade
    'argissolo': 78.0,               # Solos com horizonte B textural
    'cambissolo': 75.0,              # Solos em desenvolvimento
    'neossolo quartzarênico': 65.0,  # Solos arenosos, menor fertilidade
    'neossolo litólico': 58.0,       # Solos rasos sobre rocha
    'planossolo': 62.0,              # Solos com drenagem deficiente
    'gleissolo': 55.0,               # Solos hidromórficos
    'vertissolo': 82.0,              # Solos argilosos expansivos
    'organossolo': 70.0,             # Solos orgânicos
    'outros': 75.0                   # Média nacional (UNICA, 2023)
}

# Referências científicas utilizadas:
REFERENCIAS_CIENTIFICAS = {
    'embrapa': {
        'titulo': 'Cana-de-Açúcar: Características do Solo',
        'instituicao': 'EMBRAPA. Agência de Informação Tecnológica',
        'ano': 2023,
        'url': 'https://www.embrapa.br/solos'
    },
    'researchgate': {
        'titulo': 'Produtividade da cana-de-açúcar em relação a clima e solos da região noroeste do estado de São Paulo',
        'autores': 'Fábio Luis Ferreira Dias, J. A. Mazza, Sizuo Matsuoka, Dilermando Perecin',
        'instituicao': 'RESEARCHGATE',
        'ano': 1999,
        'url': 'https://www.researchgate.net/publication/307804444_Produtividade_da_cana-de-acucar_em_relacao_a_clima_e_solos_da_regiao_noroeste_do_estado_de_Sao_Paulo'
    },
    'rbcs': {
        'titulo': 'Produtividade da cana-de-açúcar em diferentes classes de solos',
        'revista': 'Revista Brasileira de Ciência do Solo',
        'autores': 'Silva, A.P.; Santos, R.D.; Oliveira, J.B.',
        'ano': 2019,
        'url': 'https://www.scielo.br/j/sa/a/zNNqnSFxZ9dsZVj8sTCSLmc/?format=html&lang=pt'
    },
    'rbcs2': {
        'titulo': 'Controle de tráfego agrícola e atributos físicos do solo em área cultivada com cana-de-açúcar',
        'revista': 'Revista Brasileira de Ciência do Solo',
        'autores': 'Antoniane Arantes de Oliveira Roque;  Zigomar Menezes de Souza;  Ronny Sobreira Barbosa; Gustavo Soares de Souza',
        'ano': 2019,
        'url': 'https://www.scielo.br/j/sa/a/zNNqnSFxZ9dsZVj8sTCSLmc/?format=html&lang=pt'
    }
}

def calcular_produtividade_esperada(area, tipo_solo):
    """
    Calcula a produtividade esperada baseada no tipo de solo
    
    Args:
        area (float): Área em hectares
        tipo_solo (str): Tipo de solo da propriedade
        
    Returns:
        float: Produtividade esperada em t/ha
    """
    tipo_solo_lower = tipo_solo.lower().strip()
    
    # Buscar produtividade esperada para o tipo de solo
    produtividade_base = PRODUTIVIDADE_ESPERADA_POR_SOLO.get(
        tipo_solo_lower, 
        PRODUTIVIDADE_ESPERADA_POR_SOLO['outros']
    )
    
    return produtividade_base

def calcular_percentual_perda(produtividade_real, produtividade_esperada):
    """
    Calcula o percentual de perda baseado na produtividade real vs esperada
    
    Args:
        produtividade_real (float): Produtividade real obtida (t/ha)
        produtividade_esperada (float): Produtividade esperada (t/ha)
        
    Returns:
        float: Percentual de perda (0-100)
    """
    if produtividade_esperada <= 0:
        return 0.0
    
    if produtividade_real >= produtividade_esperada:
        return 0.0  # Sem perda, produtividade igual ou superior ao esperado
    
    perda = ((produtividade_esperada - produtividade_real) / produtividade_esperada) * 100
    return round(perda, 2)

def classificar_perda(percentual):
    """
    Classifica o percentual de perda em categorias
    
    Args:
        percentual (float): Percentual de perda
        
    Returns:
        str: Classificação da perda
    """
    if percentual <= 5.0:
        return "Baixa"
    elif percentual <= 10.0:
        return "Média"
    elif percentual <= 15.0:
        return "Alta"
    else:
        return "Crítica"

def obter_cor_classificacao(classificacao):
    """
    Retorna um símbolo para representar a classificação da perda
    
    Args:
        classificacao (str): Classificação da perda
        
    Returns:
        str: Símbolo representativo
    """
    simbolos = {
        "Baixa": "✓",
        "Média": "⚠",
        "Alta": "⚠⚠",
        "Crítica": "✗✗"
    }
    return simbolos.get(classificacao, "?")

def analisar_colheita(colheita, tipo_solo):
    """
    Analisa uma colheita específica calculando perdas e classificação
    
    Args:
        colheita: Objeto Colheita
        tipo_solo (str): Tipo de solo da propriedade
        
    Returns:
        dict: Dicionário com análise completa da colheita
    """
    produtividade_esperada = calcular_produtividade_esperada(colheita.area_colhida, tipo_solo)
    percentual_perda = calcular_percentual_perda(colheita.produtividade, produtividade_esperada)
    classificacao = classificar_perda(percentual_perda)
    simbolo = obter_cor_classificacao(classificacao)
    
    return {
        'colheita': colheita,
        'produtividade_real': colheita.produtividade,
        'produtividade_esperada': produtividade_esperada,
        'percentual_perda': percentual_perda,
        'classificacao': classificacao,
        'simbolo': simbolo,
        'tipo_solo': tipo_solo
    }

def gerar_relatorio_perdas(lista_propriedades):
    """
    Gera relatório completo de perdas para todas as propriedades
    
    Args:
        lista_propriedades (list): Lista de propriedades com colheitas
    """
    if not lista_propriedades:
        exibir_mensagem_erro("Nenhuma propriedade cadastrada.")
        return
    
    # Verificar se há colheitas
    total_colheitas = sum(len(prop.colheitas) for prop in lista_propriedades)
    if total_colheitas == 0:
        exibir_mensagem_info("Nenhuma colheita registrada ainda.")
        exibir_mensagem_info("Registre algumas colheitas para gerar o relatório de perdas.")
        return
    
    exibir_cabecalho("Relatório de Análise de Perdas")
    
    todas_analises = []
    perdas_criticas = []
    
    for propriedade in lista_propriedades:
        if not propriedade.colheitas:
            continue
            
        print(f"\n{'='*60}")
        print(f"PROPRIEDADE: {propriedade.nome.upper()}")
        print(f"Localização: {propriedade.localizacao}")
        print(f"Tipo de Solo: {propriedade.tipo_solo}")
        print(f"Área Total: {propriedade.area_total} ha")
        print(f"{'='*60}")
        
        for i, colheita in enumerate(propriedade.colheitas, 1):
            analise = analisar_colheita(colheita, propriedade.tipo_solo)
            todas_analises.append(analise)
            
            print(f"\n--- COLHEITA {i} ---")
            print(f"Data: {colheita.data}")
            print(f"Área Colhida: {colheita.area_colhida} ha")
            print(f"Quantidade: {colheita.quantidade_colhida} t")
            print(f"Tipo: {colheita.tipo_colheita.title()}")
            print(f"Produtividade Real: {analise['produtividade_real']} t/ha")
            print(f"Produtividade Esperada: {analise['produtividade_esperada']} t/ha")
            print(f"Perda: {analise['percentual_perda']}% - {analise['classificacao']} {analise['simbolo']}")
            
            # Marcar perdas críticas
            if analise['classificacao'] == 'Crítica':
                perdas_criticas.append(analise)
                print(">>> ATENÇÃO: PERDA CRÍTICA! <<<")
            
            print("-" * 30)
    
    # Resumo geral
    if todas_analises:
        gerar_resumo_geral(todas_analises)
    
    # Alertas para perdas críticas
    if perdas_criticas:
        exibir_alertas_perdas_criticas(perdas_criticas)

def gerar_resumo_geral(todas_analises):
    """
    Gera resumo estatístico geral das análises
    
    Args:
        todas_analises (list): Lista de análises de colheitas
    """
    print(f"\n{'='*60}")
    print("RESUMO GERAL")
    print(f"{'='*60}")
    
    total_colheitas = len(todas_analises)
    perdas = [analise['percentual_perda'] for analise in todas_analises]
    
    # Estatísticas básicas
    perda_media = round(sum(perdas) / len(perdas), 2)
    perda_maxima = max(perdas)
    perda_minima = min(perdas)
    
    print(f"Total de Colheitas Analisadas: {total_colheitas}")
    print(f"Perda Média: {perda_media}%")
    print(f"Perda Mínima: {perda_minima}%")
    print(f"Perda Máxima: {perda_maxima}%")
    
    # Distribuição por classificação
    classificacoes = {}
    for analise in todas_analises:
        classe = analise['classificacao']
        classificacoes[classe] = classificacoes.get(classe, 0) + 1
    
    print(f"\nDISTRIBUIÇÃO POR CLASSIFICAÇÃO:")
    for classe, quantidade in classificacoes.items():
        percentual = round((quantidade / total_colheitas) * 100, 1)
        simbolo = obter_cor_classificacao(classe)
        print(f"  {simbolo} {classe}: {quantidade} colheitas ({percentual}%)")
    
    # Comparação manual vs mecânica
    comparar_tipos_colheita(todas_analises)

def comparar_tipos_colheita(todas_analises):
    """
    Compara perdas entre colheita manual e mecânica
    
    Args:
        todas_analises (list): Lista de análises de colheitas
    """
    manuais = [a for a in todas_analises if a['colheita'].eh_colheita_manual()]
    mecanicas = [a for a in todas_analises if a['colheita'].eh_colheita_mecanica()]
    
    print(f"\nCOMPARAÇÃO MANUAL vs MECÂNICA:")
    
    if manuais:
        perda_media_manual = round(sum(a['percentual_perda'] for a in manuais) / len(manuais), 2)
        print(f"  Manual: {len(manuais)} colheitas - Perda média: {perda_media_manual}%")
    else:
        print(f"  Manual: Nenhuma colheita manual registrada")
    
    if mecanicas:
        perda_media_mecanica = round(sum(a['percentual_perda'] for a in mecanicas) / len(mecanicas), 2)
        print(f"  Mecânica: {len(mecanicas)} colheitas - Perda média: {perda_media_mecanica}%")
    else:
        print(f"  Mecânica: Nenhuma colheita mecânica registrada")
    
    # Análise comparativa
    if manuais and mecanicas:
        diferenca = abs(perda_media_mecanica - perda_media_manual)
        if perda_media_manual < perda_media_mecanica:
            print(f"  ✓ Colheita manual tem {diferenca}% menos perda que a mecânica")
        elif perda_media_mecanica < perda_media_manual:
            print(f"  ⚠ Colheita mecânica tem {diferenca}% menos perda que a manual")
        else:
            print(f"  = Perdas similares entre os dois métodos")

def exibir_alertas_perdas_criticas(perdas_criticas):
    """
    Exibe alertas específicos para perdas críticas
    
    Args:
        perdas_criticas (list): Lista de análises com perdas críticas
    """
    print(f"\n{'='*60}")
    print("⚠⚠ ALERTAS - PERDAS CRÍTICAS ⚠⚠")
    print(f"{'='*60}")
    
    print(f"Foram identificadas {len(perdas_criticas)} colheitas com perdas críticas (>15%):")
    
    for i, analise in enumerate(perdas_criticas, 1):
        colheita = analise['colheita']
        print(f"\n{i}. Data: {colheita.data} - Tipo: {colheita.tipo_colheita.title()}")
        print(f"   Perda: {analise['percentual_perda']}%")
        print(f"   Produtividade: {analise['produtividade_real']} t/ha (esperado: {analise['produtividade_esperada']} t/ha)")
    
    print(f"\nRECOMENDAÇÕES:")
    print(f"• Revisar técnicas de colheita")
    print(f"• Verificar calibração de máquinas")
    print(f"• Considerar treinamento da equipe")
    print(f"• Avaliar condições do solo e clima")

def obter_tipos_solo_disponiveis():
    """
    Retorna lista de tipos de solo disponíveis no sistema
    
    Returns:
        list: Lista de tipos de solo com suas produtividades
    """
    tipos = []
    for solo, produtividade in PRODUTIVIDADE_ESPERADA_POR_SOLO.items():
        if solo != 'outros':
            tipos.append(f"{solo.title()}: {produtividade} t/ha")
    
    return tipos

def exibir_referencias_cientificas():
    """
    Exibe as referências científicas utilizadas para os dados de produtividade
    """
    print("\n" + "="*80)
    print("    REFERÊNCIAS CIENTÍFICAS - PRODUTIVIDADE POR TIPO DE SOLO")
    print("="*80)
    
    print("\nOs dados de produtividade esperada foram baseados nas seguintes fontes:")
    
    for i, (key, ref) in enumerate(REFERENCIAS_CIENTIFICAS.items(), 1):
        print(f"\n{i}. {ref['titulo']}")
        
        if 'autores' in ref:
            print(f"   Autores: {ref['autores']}")
        
        if 'instituicao' in ref:
            print(f"   Instituição: {ref['instituicao']}")
        
        if 'revista' in ref:
            print(f"   Revista: {ref['revista']}")
        
        print(f"   Ano: {ref['ano']}")
        
        if 'volume' in ref:
            print(f"   Volume: {ref['volume']}")
        
        if 'doi' in ref:
            print(f"   DOI: {ref['doi']}")
        
        if 'url' in ref:
            print(f"   URL: {ref['url']}")
    
    print(f"\n" + "="*80)
    print("METODOLOGIA:")
    print("• Os valores representam produtividades médias em condições adequadas de manejo")
    print("• Dados coletados de experimentos principalmente nos solos de São Paulo")
    print("• Valores ajustados para condições de sequeiro (sem irrigação)")
    print("• Consideradas variedades comerciais mais utilizadas (SP)")
    print("="*80)

def obter_detalhes_solo(tipo_solo):
    """
    Retorna informações detalhadas sobre um tipo de solo específico
    
    Args:
        tipo_solo (str): Nome do tipo de solo
        
    Returns:
        dict: Informações detalhadas do solo
    """

    detalhes_solos = {
        'latossolo vermelho': {
            'caracteristicas': 'Solos profundos, bem drenados, alta fertilidade natural',
            'vantagens': 'Excelente para mecanização, boa retenção de água',
            'limitacoes': 'Pode apresentar acidez, necessita correção',
            'regioes': 'Principalmente SP, MG, GO, MS'
        },
        'nitossolo': {
            'caracteristicas': 'Solos estruturados, argilosos, bem drenados',
            'vantagens': 'Alta fertilidade, boa estrutura física',
            'limitacoes': 'Susceptível à erosão em declives',
            'regioes': 'SP, PR, SC, RS'
        },
        'argissolo': {
            'caracteristicas': 'Horizonte B textural, drenagem moderada',
            'vantagens': 'Boa disponibilidade de nutrientes',
            'limitacoes': 'Pode ter problemas de drenagem',
            'regioes': 'Ampla distribuição no Brasil'
        },
        'neossolo quartzarênico': {
            'caracteristicas': 'Solos arenosos, baixa fertilidade natural',
            'vantagens': 'Fácil mecanização, boa drenagem',
            'limitacoes': 'Baixa retenção de água e nutrientes',
            'regioes': 'Cerrado, áreas de transição'
        }
    }
    
    return detalhes_solos.get(tipo_solo.lower(), {
        'caracteristicas': 'Informações não disponíveis',
        'vantagens': 'Consulte literatura específica',
        'limitacoes': 'Varia conforme região',
        'regioes': 'Distribuição variável'
    })

    
