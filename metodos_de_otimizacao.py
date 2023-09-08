import numpy

from scipy.optimize import dual_annealing
from scipy.optimize import differential_evolution
from scipy.optimize import least_squares
from scipy.optimize import minimize

from metodos_complementares import desagregacao_1
from metodos_complementares import desagregacao_2

'''
Métodos de Otimização: 

Constrained Optimization BY Linear Approximations (COBYLA), Conjugate Gradient (CG), 
Dual-Annealing (DA), Differential Evolution (DE), Broyden-Fletcher-Goldfarb-Shanno (L-BFGS-B), 
Levenberg-Marquardt (LM) / Least Squares Constrained (LSC), Método dos Mínimos Quadrados (MMQ), 
Nelder-Mead (NM), Powell, Truncated Newton (TNC).
'''

# Ajuste de parâmetros da equação IDF pelo Método dos Mínimos Quadrados

def idf_mmq(fdp_precipitacoes_iniciais,
            duracoes,
            tempos_de_retorno,
            dados_do_calculo_das_duracoes,
            metodo_de_desagregacao,
            coeficientes_de_duracoes):
        
        # Desagregação e Ajuste exponencial para diferentes tempos de retorno

        if metodo_de_desagregacao == 0:
            intensidades_para_diferentes_tempos_de_retorno = desagregacao_1(fdp_precipitacoes_iniciais,
                                                                            duracoes,
                                                                            tempos_de_retorno)
            
        elif metodo_de_desagregacao == 1:
            intensidades_para_diferentes_tempos_de_retorno = desagregacao_2(fdp_precipitacoes_iniciais, 
                                                                            duracoes, 
                                                                            tempos_de_retorno, 
                                                                            coeficientes_de_duracoes)
            
        quantidade_de_duracoes = len(duracoes)

        quantidade_de_tempos_de_retorno = len(tempos_de_retorno)

        logaritmo_natural_das_intensidades = []

        logaritmo_na_base_10_das_intensidades = []

        logaritmo_natural_das_duracoes = []

        logaritmo_na_base_10_dos_tempos_de_retorno = []
            
        for i in range(quantidade_de_tempos_de_retorno):
            
            logaritmo_natural_das_intensidades.append([])
            
            logaritmo_na_base_10_das_intensidades.append([])

            logaritmo_na_base_10_dos_tempos_de_retorno.append(numpy.log10(tempos_de_retorno[i]))

            for j in range(quantidade_de_duracoes):
                
                logaritmo_natural_das_intensidades[i].append(numpy.log(intensidades_para_diferentes_tempos_de_retorno[i][j]))
                
                logaritmo_na_base_10_das_intensidades[i].append(numpy.log10(intensidades_para_diferentes_tempos_de_retorno[i][j]))

                if i == 0:
                    logaritmo_natural_das_duracoes.append(numpy.log(duracoes[j]))

        # 1º Método dos mínimos quadrados: ajuste exponencial

        ajustes_da_funcao_a_b = [[], []]

        quantidade_de_numeros = len(logaritmo_natural_das_duracoes)

        soma_de_y = sum(logaritmo_natural_das_duracoes)
            
        for i in range(quantidade_de_tempos_de_retorno):
            soma_de_x = sum(logaritmo_natural_das_intensidades[i])
                
            yx, y_2 = [[], []]
                
            for j in range(quantidade_de_duracoes):
                yx.append(logaritmo_natural_das_duracoes[j] * logaritmo_natural_das_intensidades[i][j])
                
                y_2.append(logaritmo_natural_das_duracoes[j]**2)

            ajustes_da_funcao_a_b[0].append((quantidade_de_numeros * sum(yx) - soma_de_x * soma_de_y) / (quantidade_de_numeros * sum(y_2) - soma_de_y**2))
            
            ajustes_da_funcao_a_b[1].append(numpy.exp((soma_de_y * sum(yx) - soma_de_x * sum(y_2)) / (soma_de_y**2 - quantidade_de_numeros * sum(y_2))))

        # Parâmetro "c"

        parametro_c_para_diferentes_tempos_de_retorno = []

        for i in range(quantidade_de_tempos_de_retorno):
            intensidade_3_do_parametro_c = (intensidades_para_diferentes_tempos_de_retorno[i][0] * intensidades_para_diferentes_tempos_de_retorno[i][-1])**(1/2)

            duracao_3_do_parametro_c = (intensidade_3_do_parametro_c / ajustes_da_funcao_a_b[1][i])**(1 / ajustes_da_funcao_a_b[0][i])

            parametro_c_para_diferentes_tempos_de_retorno.append((duracao_3_do_parametro_c**2 - (duracoes[0] * duracoes[-1])) / (duracoes[0] + duracoes[-1] - duracao_3_do_parametro_c))

        parametro_c = sum(parametro_c_para_diferentes_tempos_de_retorno) / len(parametro_c_para_diferentes_tempos_de_retorno)

        # 2º Método dos mínimos quadrados: ajuste linear

        logaritmo_na_base_10_das_duracoes_mais_c = []

        for i in range(quantidade_de_duracoes):
            logaritmo_na_base_10_das_duracoes_mais_c.append((numpy.log10(duracoes[i] + parametro_c)))

        ajustes_da_funcao_a_b = [[], []]

        quantidade_de_numeros = len(logaritmo_na_base_10_das_duracoes_mais_c)

        soma_de_y = sum(logaritmo_na_base_10_das_duracoes_mais_c)
            
        for i in range(quantidade_de_tempos_de_retorno):
            soma_de_x = sum(logaritmo_na_base_10_das_intensidades[i])
                
            yx, y_2 = [[], []]
                
            for j in range(quantidade_de_duracoes):
                yx.append(logaritmo_na_base_10_das_duracoes_mais_c[j] * logaritmo_na_base_10_das_intensidades[i][j])
                
                y_2.append(logaritmo_na_base_10_das_duracoes_mais_c[j]**2)

            ajustes_da_funcao_a_b[0].append((quantidade_de_numeros * sum(yx) - soma_de_x * soma_de_y) / (quantidade_de_numeros * sum(y_2) - soma_de_y**2))
            
            ajustes_da_funcao_a_b[1].append((soma_de_y * sum(yx) - soma_de_x * sum(y_2)) / (soma_de_y**2 - quantidade_de_numeros * sum(y_2)))

        # Parâmetro "d"

        parametro_d = (sum(ajustes_da_funcao_a_b[0]) / len(ajustes_da_funcao_a_b[0])) * -1

        # 3º Método dos mínimos quadrados: ajuste linear

        constantes_k = ajustes_da_funcao_a_b[1]

        ajustes_da_funcao_a_b = [[], []]

        quantidade_de_numeros = len(logaritmo_na_base_10_dos_tempos_de_retorno)

        soma_de_y = sum(logaritmo_na_base_10_dos_tempos_de_retorno)

        soma_de_x = sum(constantes_k)

        yx, y_2 = [[], []]
            
        for i in range(quantidade_de_tempos_de_retorno):        
            yx.append(logaritmo_na_base_10_dos_tempos_de_retorno[i] * constantes_k[i])
            
            y_2.append(logaritmo_na_base_10_dos_tempos_de_retorno[i]**2)

        ajustes_da_funcao_a_b[0].append((quantidade_de_numeros * sum(yx) - soma_de_x * soma_de_y) / (quantidade_de_numeros * sum(y_2) - soma_de_y**2))

        ajustes_da_funcao_a_b[1].append((soma_de_y * sum(yx) - soma_de_x * sum(y_2)) / (soma_de_y**2 - quantidade_de_numeros * sum(y_2)))

        # Parâmetro "a"

        parametro_a = 10**ajustes_da_funcao_a_b[1][0]

        # Parâmetro "b"

        parametro_b = ajustes_da_funcao_a_b[0][0]

        # Acoplando parâmetros

        dados_do_calculo_das_duracoes.append(float(parametro_a))
        dados_do_calculo_das_duracoes.append(float(parametro_b))
        dados_do_calculo_das_duracoes.append(float(parametro_c))
        dados_do_calculo_das_duracoes.append(float(parametro_d))

        # Finalizando função

        dados_de_precipitacao = [duracoes]

        for i in range(len(intensidades_para_diferentes_tempos_de_retorno)):
            dados_de_precipitacao.append(intensidades_para_diferentes_tempos_de_retorno[i])

        dados_de_precipitacao.append(tempos_de_retorno)

        return dados_do_calculo_das_duracoes, dados_de_precipitacao

# Ajuste de parâmetros da equação IDF por Otimização

def idf_otimizar(fdp_precipitacoes_iniciais,
                 duracoes,
                 tempos_de_retorno,
                 dados_do_calculo_das_duracoes,
                 metodo,
                 metodo_de_desagregacao,
                 iteracoes,
                 varredura,
                 partida,
                 intervalo_inicial,
                 intervalo_final,
                 coeficientes_de_duracoes):
    
    if metodo == 'NM':
        metodo = 'Nelder-Mead'

    if metodo_de_desagregacao == 0:    
        dados_desagregados = desagregacao_1(fdp_precipitacoes_iniciais,
                                            duracoes,
                                            tempos_de_retorno)
    elif metodo_de_desagregacao == 1:    
        dados_desagregados = desagregacao_2(fdp_precipitacoes_iniciais,
                                            duracoes,
                                            tempos_de_retorno,
                                            coeficientes_de_duracoes)

    def funcao(par, res):
        matriz = []    

        for i in range(len(res) - 1):
            matriz.append((par[0] * tempos_de_retorno[i] ** par[1]) / ((res[0,:] + par[2]) ** par[3]))
        
        erroTotQ = 0

        for i in range(1, len(tempos_de_retorno) + 1):

            erroTotQ += numpy.sum((matriz[i - 1] - res[i,:]) ** 2) # RMSE

            #erroTotQ += numpy.sum(numpy.abs(matriz[i - 1] - res[i,:])) # MAE

            #erroTotQ += numpy.sqrt(numpy.mean((matriz[i - 1] - res[i,:]) ** 2)) / (numpy.max(res[i,:]) - numpy.min(res[i,:])) # NRMSE

            #erroTotQ += 100 * numpy.mean(numpy.abs((matriz[i - 1] - res[i,:]) / res[i,:])) # MAPE
            
        return erroTotQ
    
    dados_para_iteracao = [duracoes]

    for i in range(len(dados_desagregados)):
        dados_para_iteracao.append(dados_desagregados[i])

    matriz_de_dados = numpy.vstack(tuple(dados_para_iteracao))

    armazenamento = []

    parametros, dados_de_precipitacao = idf_mmq(fdp_precipitacoes_iniciais,
                                                duracoes,
                                                tempos_de_retorno,
                                                armazenamento,
                                                metodo_de_desagregacao,
                                                coeficientes_de_duracoes)
    
    iteracoes = (iteracoes + 1) * 1000

    if varredura == 0:
        parametros_iniciais = parametros
        intervalos = [(0, 1000), (0, 1), (0, 100), (0, 1)]

    elif varredura == 1:
        parametros_iniciais = partida
        intervalos = [(float(intervalo_inicial[0]), float(intervalo_final[0])), (float(intervalo_inicial[1]), float(intervalo_final[1])), 
                      (float(intervalo_inicial[2]), float(intervalo_final[2])), (float(intervalo_inicial[3]), float(intervalo_final[3]))]
  
    if metodo == "DA":
        resultados = dual_annealing(funcao, bounds=intervalos, args=(matriz_de_dados,), maxiter=iteracoes)

    elif metodo == "DE":
        resultados = differential_evolution(funcao, bounds=intervalos, args=(matriz_de_dados,), strategy='best1bin', popsize=15, tol=0.01, maxiter=iteracoes)

    elif metodo == "LM":
        resultados = least_squares(funcao, parametros_iniciais, args=(matriz_de_dados,), max_nfev=iteracoes)
    
    else:
        resultados = minimize(funcao, parametros_iniciais, args=(matriz_de_dados,), method=metodo, options={'maxiter': iteracoes})

    numpy.set_printoptions(formatter={'float': '{: 0.3f}'.format})

    for i in range(4):
        dados_do_calculo_das_duracoes.append(resultados.x[i])

    return dados_do_calculo_das_duracoes, dados_de_precipitacao
