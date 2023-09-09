import numpy

from scipy.stats import expon
from scipy.stats import gamma
from scipy.stats import genpareto
from scipy.stats import genextreme
from scipy.stats import kappa4
from scipy.stats import genlogistic
from scipy.stats import lognorm
from scipy.stats import gennorm
from scipy.stats import pearson3
from scipy.stats import weibull_min

'''
EXP - Exponencial
GAM - Gama
GUM - Gumbel
GPA - Generalizada de Pareto
GVE - Generalizada de Valores Extremos
KP4 - Kappa 4 parâmetros
LOG - Logística Generalizada
LN2 - Log-Normal 2 parâmetros
NOG - Normal Generalizada
PT3 - Pearson tipo 3
WEI - Weibull
'''

# Ajuste de Dados

def precipitacoes(precipitacoes_diarias_anuais_e_anos):

    # Precipitações máximas diárias anuais e Anos

    quantidade_de_precipitacoes_diarias_anuais = len(precipitacoes_diarias_anuais_e_anos)

    precipitacoes_diarias_anuais = []

    for i in range(quantidade_de_precipitacoes_diarias_anuais):
                precipitacoes_diarias_anuais.append(precipitacoes_diarias_anuais_e_anos[i][1])

    precipitacoes_diarias_anuais.sort(key=float)

    precipitacoes_diarias_anuais.reverse()

    return (precipitacoes_diarias_anuais, 
            quantidade_de_precipitacoes_diarias_anuais)  

# Chow-Gumbel

def chow_gumbel(precipitacoes_diarias_anuais_e_anos, tempos_de_retorno):

    # Constantes

    constante_pi = 3.1415926535897932

    constante_euler_mascheroni = 0.5772156649015329

    (precipitacoes_diarias_anuais, 
     quantidade_de_precipitacoes_diarias_anuais) = precipitacoes(precipitacoes_diarias_anuais_e_anos)

    # Tempo de retorno

    tempos_de_retorno.reverse()

    quantidade_de_tempos_de_retorno = len(tempos_de_retorno)

    # Método de Chow-Gumbel

    gumbel_media = sum(precipitacoes_diarias_anuais) / len(precipitacoes_diarias_anuais)

    desvio_padrao = 0

    for i in range(quantidade_de_precipitacoes_diarias_anuais):
        desvio_padrao += (gumbel_media - precipitacoes_diarias_anuais[i])**2

    gumbel_desvio_padrao = (desvio_padrao / (quantidade_de_precipitacoes_diarias_anuais - 1))**(1/2)

    gumbel_beta = (6**(1 / 2) / constante_pi) * gumbel_desvio_padrao

    gumbel_mi = gumbel_media - constante_euler_mascheroni * gumbel_beta

    gumbel_precipitacoes_iniciais = []

    for i in range(quantidade_de_tempos_de_retorno):
        gumbel_precipitacoes_iniciais.append(gumbel_mi - numpy.log(numpy.log(tempos_de_retorno[i] / (tempos_de_retorno[i] - 1))) * gumbel_beta)

    return (precipitacoes_diarias_anuais,
            gumbel_desvio_padrao, 
            gumbel_media,
            gumbel_precipitacoes_iniciais,
            (gumbel_mi, gumbel_beta))

def modelagem(precipitacoes_diarias_anuais_e_anos, tempos_de_retorno, probabilidade):

    # Ajustando dados

    precipitacoes_diarias_anuais = precipitacoes(precipitacoes_diarias_anuais_e_anos)[0]
    
    # Definido função
   
    if probabilidade == "EXP":
         modelo_probabilistico = expon
    
    elif probabilidade == "GAM":
         modelo_probabilistico = gamma
    
    elif probabilidade == "GPA":
         modelo_probabilistico = genpareto
         
    elif probabilidade == "GVE":
         modelo_probabilistico = genextreme
    
    elif probabilidade == "KP4":
         modelo_probabilistico = kappa4

    elif probabilidade == "LOG":
         modelo_probabilistico = genlogistic
    
    elif probabilidade == "LN2":
         modelo_probabilistico = lognorm
    
    elif probabilidade == "NOG":
         modelo_probabilistico = gennorm
    
    elif probabilidade == "PT3":
         modelo_probabilistico = pearson3
    
    elif probabilidade == "WEI":
         modelo_probabilistico = weibull_min

    # Descobrindo parâmetros da função

    if probabilidade == "LN2":
         parametros = modelo_probabilistico.fit(precipitacoes_diarias_anuais, floc=0)
    else:
         parametros = modelo_probabilistico.fit(precipitacoes_diarias_anuais)

    media, variancia = modelo_probabilistico.stats(*parametros, moments='mv')

    desvio_padrao = variancia**(1/2)

    # Cálculando precipitações para diferentes tempos de retorno

    precipitacoes_iniciais = []

    for i in range(len(tempos_de_retorno)):
        precipitacoes_iniciais.append(modelo_probabilistico.ppf((1 - 1/tempos_de_retorno[i]), *parametros))

    return (precipitacoes_diarias_anuais,
            desvio_padrao, 
            media,
            precipitacoes_iniciais,
            parametros)
