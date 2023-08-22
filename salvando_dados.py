def relatorio_de_equacao_idf(arquivo_salvo, resultados, parametros_da_distribuicao, dur, tre):
    
    with open(arquivo_salvo, 'w', encoding='utf-8') as arquivo:

        arquivo.write(f'-----------------------------------------------------------------------------------------\n\n')
        arquivo.write(f'       R E L A T Ó R I O   D O   C Á L C U L O   P A R A   D E T E R M I N A Ç Ã O         \n')
        arquivo.write(f'               D A   E Q U A Ç Ã O   D A S   C H U V A S   I N T E N S A S               \n\n')
        arquivo.write(f'-----------------------------------------------------------------------------------------  \n')
        arquivo.write(f'> EQUAÇÃO:                                                                               \n\n')
        arquivo.write(f'I = [a * Tr^(b)] / [(t + c)^(d)]                                                         \n\n')
        arquivo.write(f'I = [{resultados[4]} * Tr^({resultados[5]})] / [(t + {resultados[6]})^({resultados[7]})] \n\n')
        arquivo.write(f'-----------------------------------------------------------------------------------------  \n')
        arquivo.write(f'> RELATÓRIO:                                                                             \n\n')
        arquivo.write(f'Após agrupar as amostras de precipitações diárias                                          \n')
        arquivo.write(f'anuais máximas dos {resultados[3]} anos de séries históricas, foi                          \n')
        arquivo.write(f'realizado para esses dados o teste de tendência de                                         \n')
        arquivo.write(f'Mann-Kendall, constatando através dele que {resultados[0]}.                                \n')
        arquivo.write(f'Após isso iniciou-se a modelagem dos dados utilizando a                                    \n')
        arquivo.write(f'distribuição probabilísticas "{resultados[10]}", com seus parâmetros                       \n')    
        arquivo.write(f'{parametros_da_distribuicao} encontrados                                                   \n')
        arquivo.write(f'através do método da máxima verossimilhança. Com esses dados, foi                          \n')
        arquivo.write(f'feito assim o teste de aderência de "{resultados[2]}" qual constatou                       \n')
        arquivo.write(f'"{resultados[1]}". Assim sendo, houve a desagregação                                       \n')
        arquivo.write(f'das precipitações de 24 horas em chuvas de menores durações.                               \n')
        arquivo.write(f'Iniciou-se então o uso do método de otimização "{resultados[11]}",                         \n')
        arquivo.write(f'que resultou nos parâmetros da equação das chuvas intensas                                 \n')
        arquivo.write(f'que foram: "a = {resultados[4]}", "b = {resultados[5]}", "c = {resultados[6]}" e           \n')
        arquivo.write(f'"d = {resultados[7]}" . Por fim, foram feitos testes de acurácia de Nash-                  \n')
        arquivo.write(f'Sutcliff com coeficiente igual a {resultados[8]:.4f}, e RMSE (Root Mean                    \n')
        arquivo.write(f'Squared Error) com coeficiente igual a {resultados[9]:.4f}.                              \n\n')
        arquivo.write(f'-----------------------------------------------------------------------------------------  \n')
        arquivo.write(f'> INTENSIDADES:                                                                          \n\n')

        tre = [str(num) for num in tre]

        intensidades = (('|\t|' + (int(len(tre) / 2) * '\t') + 'Tr' + (round(len(tre) / 2) * '\t') + '|\n') + 
                        ('|t\t|' + "\t|".join(tre) + '\t|\n'))

        for i in range(len(dur)):
            intensidades += f'|{dur[i]}\t'

            for j in range(len(tre)):

                intensidade = ((float(resultados[4]) * float(tre[j]) ** float(resultados[5])) / 
                               ((dur[i] + float(resultados[6])) ** float(resultados[7])))

                intensidades += f'|{intensidade:.2f}\t'

            intensidades += '|\n'

        arquivo.write(intensidades)
        arquivo.write(f'\n-----------------------------------------------------------------------------------------  ')

def relatorio_de_precipitacoes_maximas(arquivo_salvo, resultados, precipitacoes):

    with open(arquivo_salvo, 'w', encoding='utf-8') as arquivo:
        
        arquivo.write(f'-----------------------------------------------------------------------------------------\n\n')
        arquivo.write(f'            R E L A T Ó R I O   D E   T R A T A M E N T O   D E   D A D O S              \n\n')
        arquivo.write(f'-----------------------------------------------------------------------------------------  \n')
        arquivo.write(f'> RELATÓRIO:                                                                             \n\n')
        arquivo.write(f'Foram analisados pelo menos {resultados[0]}                                                \n')
        arquivo.write(f'dias. Foi observado que destes,                                                            \n') 
        arquivo.write(f'{resultados[1]} não possuiam dados, que                                                    \n')
        arquivo.write(f'representa {resultados[3]}% da quantidade                                                  \n')
        arquivo.write(f'total de dias. O limiar de falhas                                                          \n')
        arquivo.write(f'definido foi de {resultados[2]}%, podendo                                                  \n')
        arquivo.write(f'haver pelo menos {int(float(resultados[2]) * float(resultados[0]))} dias falhos            \n')
        arquivo.write(f'sem que haja o comprometimento da                                                          \n')        
        arquivo.write(f'informação que se busca, que é o                                                           \n')
        arquivo.write(f'da maior precipitação pluviométrica                                                        \n')
        arquivo.write(f'do ano em um dia.                                                                        \n\n')
        arquivo.write(f'-----------------------------------------------------------------------------------------\n\n')
        arquivo.write(f'> PRECIPITAÇÕES MÁXIMAS:                                                                 \n\n')
        arquivo.write('|Nº\t|Prec.\t|                                                                              \n')

        for i in range(len(precipitacoes)):
            arquivo.write(f'|{precipitacoes[i][0]}\t|{precipitacoes[i][1]}\t|                                      \n')

        arquivo.write(f'\n-----------------------------------------------------------------------------------------  ')

def compilacao_do_banco_de_dados(arquivo_salvo, dados):

    with open(arquivo_salvo, 'w', encoding='utf-8') as arquivo:
        
        arquivo.write('Cidade;Latitude;Longitude;Ano;Mes;Dia 01;Dia 02;Dia 03;Dia 04;Dia 05;Dia 06;Dia 07;Dia 08;')
        arquivo.write('Dia 09;Dia 10;Dia 11;Dia 12;Dia 13;Dia 14;Dia 15;Dia 16;Dia 17;Dia 18;Dia 19;Dia 20;Dia 21;')
        arquivo.write('Dia 22;Dia 23;Dia 24;Dia 25;Dia 26;Dia 27;Dia 28;Dia 29;Dia 30;Dia 31\n')

        for i in range(len(dados)):

            arquivo.write(f'{dados[i][0]};{float(dados[i][1]):.2f};{float(dados[i][2]):.2f};{dados[i][3]};{dados[i][4]};')
            arquivo.write(f'{dados[i][5]};{dados[i][6]};{dados[i][7]};{dados[i][8]};{dados[i][9]};')
            arquivo.write(f'{dados[i][10]};{dados[i][11]};{dados[i][12]};{dados[i][13]};{dados[i][14]};')
            arquivo.write(f'{dados[i][15]};{dados[i][16]};{dados[i][17]};{dados[i][18]};{dados[i][19]};')
            arquivo.write(f'{dados[i][20]};{dados[i][21]};{dados[i][22]};{dados[i][23]};{dados[i][24]};')
            arquivo.write(f'{dados[i][25]};{dados[i][26]};{dados[i][27]};{dados[i][28]};{dados[i][29]};')
            arquivo.write(f'{dados[i][30]};{dados[i][31]};{dados[i][32]};{dados[i][33]};{dados[i][34]};')
            arquivo.write(f'{dados[i][35]}\n')