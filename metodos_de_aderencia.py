import numpy

from scipy.stats import anderson

# Teste de Aderência de Kolmogorov-Smirnov

def kolmogorov_smirnov(precipitacoes_diarias_anuais,
                       gumbel_desvio_padrao, 
                       gumbel_media, 
                       porcentagem,
                       dados_do_calculo_das_duracoes):
        
        quantidade_de_precipitacoes_diarias_anuais = len(precipitacoes_diarias_anuais)

        ordem_de_precipitacoes_diarias_anuais = []

        for i in range(quantidade_de_precipitacoes_diarias_anuais):
            ordem_de_precipitacoes_diarias_anuais.append(i)

        ks_alpha = gumbel_desvio_padrao / 1.283

        ks_beta = gumbel_media - 0.45 * gumbel_desvio_padrao

        if porcentagem == 0:
            ks_funcao_aderencia = 1.6276 / (quantidade_de_precipitacoes_diarias_anuais)**(1/2)

        elif porcentagem == 1:
            ks_funcao_aderencia = 1.3581 / (quantidade_de_precipitacoes_diarias_anuais)**(1/2)

        ks_frequencia = []

        ks_frequencia_nao_excedida = []

        ks_frequencia_excedida = []

        ks_diferenca = []

        for i in range(quantidade_de_precipitacoes_diarias_anuais):
            ks_frequencia.append(ordem_de_precipitacoes_diarias_anuais[i] / quantidade_de_precipitacoes_diarias_anuais)

            ks_frequencia_nao_excedida.append(numpy.exp(- numpy.exp(- (precipitacoes_diarias_anuais[i] - ks_beta) / ks_alpha)))

            ks_frequencia_excedida.append(1 - ks_frequencia_nao_excedida[i])

            if ks_frequencia[i] - ks_frequencia_excedida[i] < 0:
                ks_diferenca.append((ks_frequencia[i] - ks_frequencia_excedida[i]) * -1)

            else:
                ks_diferenca.append(ks_frequencia[i] - ks_frequencia_excedida[i])

        diferenca_da_aderencia = max(ks_diferenca)

        if diferenca_da_aderencia < ks_funcao_aderencia:
            dados_do_calculo_das_duracoes.append('Boa aderência')
        else:
            dados_do_calculo_das_duracoes.append('Rejeitar')

        dados_do_calculo_das_duracoes.append("KS")

        dados_do_calculo_das_duracoes.append(quantidade_de_precipitacoes_diarias_anuais)

        return dados_do_calculo_das_duracoes

# Teste de Aderência de Anderson-Darling

def anderson_darling(precipitacoes_diarias_anuais,
                     desvio_padrao, 
                     media, 
                     porcentagem,
                     distribuicao,
                     dados_do_calculo_das_duracoes):
    
    # Definindo teste

    if (distribuicao == 'EXP' or
        distribuicao == 'GUM' or
        distribuicao == 'GVE' or
        distribuicao == 'LOG' or
        distribuicao == 'NOG'):
        
        if distribuicao == 'EXP':
            distribuicao = 'expon'

        elif distribuicao == 'GUM':
            distribuicao = 'gumbel_r'

        elif distribuicao == 'GVE':
            distribuicao = 'extreme1'

        elif distribuicao == 'LOG':
            distribuicao = 'logistic'

        elif distribuicao == 'NOG':
            distribuicao = 'norm'

        # Realizando o teste

        resultados = anderson(numpy.array(precipitacoes_diarias_anuais), dist=distribuicao)

        # Verificando se a hipótese nula foi rejeitada ou não

        if porcentagem == 0:
            aderencia = resultados.statistic
            diferenca = resultados.critical_values[4]

        elif porcentagem == 1:
            aderencia = resultados.statistic
            diferenca = resultados.critical_values[2]

        if diferenca < aderencia:
            dados_do_calculo_das_duracoes.append('Boa aderência')

        else:
            dados_do_calculo_das_duracoes.append('Rejeitar')

        quantidade_de_precipitacoes_diarias_anuais = len(precipitacoes_diarias_anuais)

        dados_do_calculo_das_duracoes.append('AD')
        dados_do_calculo_das_duracoes.append(quantidade_de_precipitacoes_diarias_anuais)
    
    else:
        kolmogorov_smirnov(precipitacoes_diarias_anuais,
                           desvio_padrao, 
                           media, 
                           porcentagem,
                           dados_do_calculo_das_duracoes)
        
    return dados_do_calculo_das_duracoes
