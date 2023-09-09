import numpy
import pymannkendall

# Método de Ponderação pelo Iverso da Potência das Distâncias (IDW)

def idw(dados_de_coordenadas):

    # Calculando Inverso da Potência das Distâncias (Inverse Distance Weighting (IDW))

    anos, distancias = [[], []]


    for i in range(5):
        distancias.append(1 / ((dados_de_coordenadas[i][0])**2))

        for j in range(2, len(dados_de_coordenadas[i][1])):
            anos.append(dados_de_coordenadas[i][1][j][0])

    anos = (list(set(anos)))

    anos.sort()

    # Separando Anos Iguais

    anos_iguais = []

    for i in range(len(anos)):
        con = 0

        for j in range(5):
            
            for k in range(2, len(dados_de_coordenadas[j][1])):
                if anos[i] == dados_de_coordenadas[j][1][k][0]:
                    con += 1
                    break

        if con == 5:
            anos_iguais.append(anos[i])

    # Calculando Média Ponderada

    dados_interpolados = []

    for i in range(len(anos_iguais)):
        dados_ponderados = []

        for j in range(5):
            
            for k in range(2, len(dados_de_coordenadas[j][1])):
                if anos_iguais[i] == dados_de_coordenadas[j][1][k][0]:
                    dados_ponderados.append(dados_de_coordenadas[j][1][k][1])
                    break

        media_ponderada = (dados_ponderados[0] * distancias[0] 
                            + dados_ponderados[1] * distancias[1] 
                            + dados_ponderados[2] * distancias[2] 
                            + dados_ponderados[3] * distancias[3] 
                            + dados_ponderados[4] * distancias[4]) / (distancias[0] + distancias[1] 
                                                                        + distancias[2] + distancias[3] 
                                                                        + distancias[4])

        dados_interpolados.append((anos_iguais[i], media_ponderada))

    return dados_interpolados, anos_iguais

# Método de Mann-Kendall

def mann_kendall(dados):

    '''
    # Código com menor robustez que a biblioteca "pymannkendall":

    def mann_kendall_test(dados):
        n = len(dados)
        s = 0
        for i in range(n - 1):
            for j in range(i + 1, n):
                s += numpy.sign(dados[j] - dados[i])
                
        var_s = (n * (n - 1) * (2 * n + 5)) / 18
        
        if s > 0:
            z = (s - 1) / np.sqrt(var_s)
            
        elif s < 0:
            z = (s + 1) / np.sqrt(var_s)
            
        else:
            z = 0
            
        p = 2 * (1 - norm.cdf(abs(z)))
        
        h = abs(z) > norm.ppf(1 - 0.05 / 2)
        
        trend = None
        
        if z > 0:
            trend = 'increasing'
        elif z < 0:
            trend = 'decreasing'
        else:
            trend = 'no trend'
            
        return trend, h, p, z

    dados = [1, 2, 3, 4, 5, 6, 7]

    trend, h, p, z = mann_kendall_test(dados)

    print(f"Tendência: {trend} {h} {p} {z}")
    '''

    precipitacoes = []

    for i in range(len(dados)):
        precipitacoes.append(dados[i][1])

    significancia = 0.05

    resultados = pymannkendall.original_test(precipitacoes, alpha=significancia)

    if resultados.trend == 'no trend':
        resultado = ['Não há tendência']
    
    else:
        resultado = ['Há tendência']

    return resultado

# Método de Desagregação de Dados Pluviométricos

def desagregacao_1(fdp_precipitacoes_iniciais,
                   duracoes,
                   tempos_de_retorno):
    
    # Coeficientes de Desagregação

    quantidade_de_tempos_de_retorno = len(tempos_de_retorno)
    
    quantidade_de_duracoes = len(duracoes)

    coeficientes_de_desagregacao = [1.14]

    for i in range(1,quantidade_de_duracoes):
        coeficientes_de_desagregacao.append(numpy.exp(1.5 * numpy.log(numpy.log(duracoes[i]) / 7.3)))
    
    # Desagregação

    dados_desagregados = []

    for i in range(quantidade_de_tempos_de_retorno):
        dados_desagregados.append([])
        for j in range(quantidade_de_duracoes):
            dados_desagregados[i].append(60 * fdp_precipitacoes_iniciais[i] * coeficientes_de_desagregacao[j] / duracoes[j])

    return dados_desagregados

def desagregacao_2(fdp_precipitacoes_iniciais,
                   duracoes,
                   tempos_de_retorno,
                   coeficientes):
    
    precipitacoes_desagregadas = []
    
    for i in range(len(fdp_precipitacoes_iniciais)):
        precipitacoes_desagregadas.append([])

        precipitacoes_desagregadas[i].append(fdp_precipitacoes_iniciais[i] * coeficientes[0])

        for j in range(5):
            precipitacoes_desagregadas[i].append(precipitacoes_desagregadas[i][0] * coeficientes[j + 1])
        
        precipitacoes_desagregadas[i].append(precipitacoes_desagregadas[i][5] * coeficientes[6])

        for j in range(5):
            precipitacoes_desagregadas[i].append(precipitacoes_desagregadas[i][6] * coeficientes[j + 7])

    dados_desagregados = []

    for i in range(len(tempos_de_retorno)):
        dados_desagregados.append([])

        for j in range(len(duracoes)):
            dados_desagregados[i].append(60 * precipitacoes_desagregadas[i][j] / duracoes[j])

    return dados_desagregados

# Método de Nash-Stucliff

def nash_stucliff(dados_finais, dados_de_precipitacao):

    # Compilando dados previstos

    tempos_de_retorno = dados_de_precipitacao[-1]

    duracoes = dados_de_precipitacao[0]

    gerando_dados = []

    parametros = dados_finais[4:]

    for i in range(len(tempos_de_retorno)):
        gerando_dados.append([])

        for j in range(len(duracoes)):
            gerando_dados[i].append((parametros[0] * tempos_de_retorno[i] ** parametros[1]) / 
                                    (parametros[2]+ duracoes[j]) ** parametros[3])
            
    # Definindo os dados observados e previstos

    dados_observados = numpy.array(dados_de_precipitacao[1:-1])

    dados_gerados = numpy.array(gerando_dados)

    # Calculando a média dos valores observados

    media_dados_observados = numpy.mean(dados_observados)

    # Calculando as somas dos quadrados das diferenças

    numerador = numpy.sum((dados_observados - dados_gerados)**2)
    
    denominador = numpy.sum((dados_observados - media_dados_observados)**2)

    # Calculando o coeficiente de eficiência de Nash-Sutcliffe

    nash_sutcliffe = 1 - numerador/denominador

    dados_finais.append(nash_sutcliffe)

    return dados_finais

# Método do Erro Quadrático Médio (Mean Squared Error)

def rmse(dados_finais, dados_de_precipitacao):

    # Compilando dados previstos

    tempos_de_retorno = dados_de_precipitacao[-1]

    duracoes = dados_de_precipitacao[0]

    gerando_dados = []

    parametros = dados_finais[4:]

    for i in range(len(tempos_de_retorno)):
        gerando_dados.append([])

        for j in range(len(duracoes)):
            gerando_dados[i].append((parametros[0] * tempos_de_retorno[i] ** parametros[1]) / 
                                    (parametros[2]+ duracoes[j]) ** parametros[3])
            
    dados_observados = dados_de_precipitacao[1:-1]

    # Calculando RMSE

    diferencas = numpy.array(dados_observados) - numpy.array(gerando_dados)

    soma_diferencas_quadradas = numpy.sum(diferencas ** 2)

    rmse = numpy.sqrt(soma_diferencas_quadradas / len(dados_observados))

    dados_finais.append(rmse)

    return dados_finais

# Cálculo do Limiar de Falhas

def limiar_de_falhas(lista_1, limiar):

    # Configurações iniciais

    anos = []

    anos_falhos = []

    dias_falhos = []

    for i in range(len(lista_1)):
        anos.append(lista_1[i][0])

    anos = list(set(anos))

    # Varrendo erros diários

    for i in range(len(anos)):
        erros = 0
        meses = []
        ano = anos[i]

        for j in range(len(lista_1)):
            if float(lista_1[j][1]) == 2:
                dias = 28
            elif (float(lista_1[j][1]) == 4 or
                  float(lista_1[j][1]) == 6 or
                  float(lista_1[j][1]) == 9 or
                  float(lista_1[j][1]) == 11 ):
                dias = 30
            else:
                dias = 31

            if anos[i] == float(lista_1[j][0]):
                meses.append(float(lista_1[j][1]))

                for k in range(dias):
                    if lista_1[j][k + 2] == '':
                        erros += 1
                    elif numpy.isnan(float(lista_1[j][k + 2])) == True:
                        erros += 1

        # Varrendo erros mensais

        if len(meses) < 12:
            for i in range(12):
                verificador = 0

                for j in range(len(meses)):
                    if (i + 1) != meses[j]:
                        verificador += 1                 

                if len(meses) == verificador:
                    if (i + 1) == 2:
                        erros += 28
                    elif ((i + 1) == 4 or
                          (i + 1) == 6 or
                          (i + 1) == 9 or
                          (i + 1) == 11):
                        erros += 30
                    else:
                        erros += 31

        # Verificando limiar de falhas

        if erros > int(limiar):
            anos_falhos.append(ano)

        dias_totais = len(anos) * 365

        dias_falhos.append(erros)
        
    return anos_falhos, dias_totais, dias_falhos

# Cálculo das Precipitações Máximas

def precipitacoes_maximas(lista_1, lista_2):
    
    for i in range(len(lista_2)):
        con = 0
        for j in range(len(lista_1)):
            if lista_2[i][0] == lista_1[j][0]:
                con = 1
                break

        if con == 0:
            lista_1.append([int(lista_2[i][0]), numpy.nan])

    for i in range(len(lista_2)):
        for j in range(len(lista_1)):
            if lista_2[i][0] == lista_1[j][0]:
                if (max(lista_2[i][2:len(lista_2[i])]) != 0):
                    lista_1[j][1] = max(lista_2[i][2:len(lista_2[i])])

    return lista_1, lista_2
