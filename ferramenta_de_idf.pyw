print("\nPorque para mim o viver é Cristo, e o morrer é ganho. Filipenses 1:21\n")

import tkinter as tk
import pandas as pd
import numpy as np
import base64
import sys
import os

from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename

from dados_da_paraiba import banco_de_dados_total
from dados_da_paraiba import banco_de_dados_maximos
from img_da_ferramenta import imagens_de_ferramenta

from metodos_de_frequencia import chow_gumbel
from metodos_de_frequencia import modelagem

from metodos_de_aderencia import kolmogorov_smirnov
from metodos_de_aderencia import anderson_darling

from metodos_de_otimizacao import idf_mmq
from metodos_de_otimizacao import idf_otimizar

from metodos_complementares import mann_kendall
from metodos_complementares import nash_stucliff
from metodos_complementares import rmse
from metodos_complementares import idw
from metodos_complementares import limiar_de_falhas
from metodos_complementares import precipitacoes_maximas

from salvando_dados import relatorio_de_equacao_idf
from salvando_dados import relatorio_de_precipitacoes_maximas
from salvando_dados import compilacao_do_banco_de_dados

root = Tk()

class funcoes():

    # Conversão de ícone
    def conversao_de_icone(self, janela):
        
        icone = base64.b64decode(imagens_de_ferramenta('guarda-chuva'))

        with open("icone_temporario.ico", "wb") as ico:
            ico.write(icone)

        janela.iconbitmap('icone_temporario.ico')

        os.remove("icone_temporario.ico")

    # Resultados
    def idf_por_interpolacao_da_paraiba(self):

        # Equações de Chuvas Intensas das Cidades que NÃO Possuem Dados

        if self.coordenada_apurada_x != '':

            self.interpolar_valores = True

            # Extraindo Dados

            dados_de_coordenadas = banco_de_dados_maximos((self.coordenada_apurada_x, self.coordenada_apurada_y), self.interpolar_valores)

            # Calculando Inverso da Potência das Distâncias (Inverse Distance Weighting (IDW))

            dados_interpolados, anos_iguais = idw(dados_de_coordenadas)

            # Calculando Dados Interpolados

            if len(anos_iguais) != 0:
                self.ano_inicial_da_cidade = anos_iguais[0]
                self.ano_final_da_cidade = anos_iguais[len(anos_iguais)-1]

                self.dados_da_aba_1 = self.calculando_3(dados_interpolados)

                for i in range(4):
                    self.dados_da_aba_1[i + 4] = '%.4f' % self.dados_da_aba_1[i + 4]

        # Nulo

        else:
            self.ano_inicial_da_cidade               = ''
            self.ano_final_da_cidade                 = ''
            self.coordenada_apurada_x                = ''
            self.coordenada_apurada_y                = ''

            self.dados_da_aba_1 = ['','','','','','','','','','','','']

        self.funcao_destruicao_1() 

    def idf_das_cidades_paraibanas(self):
        self.interpolar_valores = False

        # Equações de Chuvas Intensas das Cidades que Possuem Dados

        if self.lista_de_cidades.get() != ' ':

            dados_da_cidade = banco_de_dados_maximos(self.lista_de_cidades.get(), 
                                                     self.interpolar_valores)

            self.ano_inicial_da_cidade = dados_da_cidade[2][0]
            self.ano_final_da_cidade = dados_da_cidade[len(dados_da_cidade)-1][0]

            self.coordenada_apurada_x = dados_da_cidade[1][1]
            self.coordenada_apurada_y = dados_da_cidade[1][0]

            self.precipitacoes_e_anos_paraibanas = []

            for i in range(2,len(dados_da_cidade)):
                self.precipitacoes_e_anos_paraibanas.append(dados_da_cidade[i])

            self.dados_da_aba_1 = self.calculando_3(self.precipitacoes_e_anos_paraibanas)

            for i in range(4):
                self.dados_da_aba_1[i + 4] = '%.4f' % self.dados_da_aba_1[i + 4]

        # Nulo

        else:

            self.ano_inicial_da_cidade               = ''
            self.ano_final_da_cidade                 = ''
            self.coordenada_apurada_x                = ''
            self.coordenada_apurada_y                = ''

            self.dados_da_aba_1 = ['','','','','','','','','','','','']

        self.funcao_destruicao_1()                  
            
    def idf_do_usuario(self):     
        self.dados_da_aba_2 = self.calculando_3(self.quadro_1_itens)

        for i in range(4):
            self.dados_da_aba_2[i + 4] = '%.4f' % self.dados_da_aba_2[i + 4]
            
        self.funcao_destruicao_2()

    # Botões de Apagar
    def apagando_1(self):
        selecionador = self.quadro_1.selection()[0]

        self.quadro_1.delete(selecionador)

        del (self.quadro_1_itens[int(selecionador)])

        self.funcao_destruicao_2()

    def apagando_2(self):
        selecionador = self.quadro_2.selection()[0]

        self.quadro_2.delete(selecionador)

        del (self.quadro_2_itens[int(selecionador)])

        self.funcao_destruicao_2()

    def apagando_3(self):
        selecionador = self.quadro_3.selection()[0]

        self.quadro_3.delete(selecionador)

        del (self.quadro_3_itens[int(selecionador)])

        self.funcao_destruicao_2()

    def apagando_4(self):
        selecionador = self.quadro_5.selection()[0]

        self.quadro_5.delete(selecionador)

        del (self.quadro_5_itens[int(selecionador)])

        self.funcao_destruicao_3()

    # Botões de Calcular
    def calculando_1(self, 
                     anos_e_precipitacoes, 
                     modelagem_variavel, 
                     aderencia_variavel, 
                     otimizacao_variavel):

        dados_finais = mann_kendall(anos_e_precipitacoes)

        if modelagem_variavel == 'GUM':

            dados_calculados = chow_gumbel(anos_e_precipitacoes, 
                                           self.quadro_3_itens)
            
        elif (modelagem_variavel == 'EXP' or
              modelagem_variavel == 'GAM' or
              modelagem_variavel == 'GPA' or
              modelagem_variavel == 'GVE' or
              modelagem_variavel == 'KP4' or
              modelagem_variavel == 'LOG' or
              modelagem_variavel == 'LN2' or
              modelagem_variavel == 'NOG' or
              modelagem_variavel == 'PT3' or
              modelagem_variavel == 'WEI'):

            dados_calculados = modelagem(anos_e_precipitacoes, 
                                         self.quadro_3_itens,
                                         modelagem_variavel)

        precipitacoes_iniciais = dados_calculados[3]

        if aderencia_variavel == 'KS':

            dados_finais = kolmogorov_smirnov(dados_calculados[0],
                                              dados_calculados[1],
                                              dados_calculados[2],
                                              self.n_porcentagem_de_aderencia,
                                              dados_finais)
            
        elif aderencia_variavel == 'AD':
            
            dados_finais = anderson_darling(dados_calculados[0],
                                            dados_calculados[1],
                                            dados_calculados[2],
                                            self.n_porcentagem_de_aderencia,
                                            modelagem_variavel,
                                            dados_finais)
            
        if otimizacao_variavel == "MMQ":

            dados_finais, dados_de_precipitacao = idf_mmq(precipitacoes_iniciais,
                                                          self.quadro_2_itens,
                                                          self.quadro_3_itens,
                                                          dados_finais,
                                                          self.n_coeficientes_de_desagregacao,
                                                          self.coeficientes_de_duracoes)

        elif (otimizacao_variavel == "COBYLA" or
              otimizacao_variavel == "CG" or
              otimizacao_variavel == "DA" or
              otimizacao_variavel == "DE" or
              otimizacao_variavel == "L-BFGS-B" or
              otimizacao_variavel == "LM" or
              otimizacao_variavel == "MMQ" or
              otimizacao_variavel == "NM" or
              otimizacao_variavel == "POWELL" or
              otimizacao_variavel == "TNC"):

            dados_finais, dados_de_precipitacao = idf_otimizar(precipitacoes_iniciais,
                                                               self.quadro_2_itens,
                                                               self.quadro_3_itens,
                                                               dados_finais,
                                                               otimizacao_variavel,
                                                               self.n_coeficientes_de_desagregacao,
                                                               self.n_quantidade_de_iteracoes,
                                                               self.n_varredura,
                                                               self.v_partida,
                                                               self.v_intervalo_inicial,
                                                               self.v_intervalo_final,
                                                               self.coeficientes_de_duracoes)
            
        dados_finais = nash_stucliff(dados_finais, 
                                     dados_de_precipitacao)

        dados_finais = rmse(dados_finais, 
                            dados_de_precipitacao)

        dados_finais.append(modelagem_variavel)
        dados_finais.append(otimizacao_variavel)
        dados_finais.append(dados_calculados[4])
                        
        return dados_finais

    def calculando_2(self):

        self.quadro_4_itens, self.quadro_5_itens = precipitacoes_maximas(self.quadro_4_itens, 
                                                                         self.quadro_5_itens)
        (anos_falhos, 
        self.relatorio_2_variaveis[0], 
        self.relatorio_2_variaveis[1]) = limiar_de_falhas(self.quadro_5_itens, self.limiar_de_erro)

        for i in range(len(anos_falhos)):
            for j in range(len(self.quadro_4_itens)):
                if anos_falhos[i] == self.quadro_4_itens[j][0]:
                    self.quadro_4_itens[j][1] = np.nan

        self.relatorio_2_variaveis[2] = '%.4f' % (int(self.limiar_de_erro) / self.relatorio_2_variaveis[0])

        self.relatorio_2_variaveis[3] = '%.4f' % (self.relatorio_2_variaveis[1] / self.relatorio_2_variaveis[0])

        self.funcao_destruicao_3()

    def calculando_3(self, anos_e_precipitacoes):

        modelagem_variavel = self.funcao_densidade_probabilidade.get()
        aderencia_variavel = self.aderencia.get()
        otimizacao_variavel = self.otimizacao.get()

        testes = []

        # Melhores Modelagem, Aderência e Otimização

        if self.n_melhor_modelagem == 0 and self.n_melhor_aderencia == 0 and self.n_melhor_otimizacao == 0:
            for i in range(len(self.lista_de_funcoes_cumulativas_de_probabilidade)):
                for j in range(len(self.lista_de_aderencias)):
                    for k in range(len(self.lista_de_otimizacoes)):
                        testes.append(self.calculando_1(anos_e_precipitacoes, 
                                                        self.lista_de_funcoes_cumulativas_de_probabilidade[i], 
                                                        self.lista_de_aderencias[j], 
                                                        self.lista_de_otimizacoes[k]))

            testes_ordenados = sorted(testes, reverse=True, key=lambda x: x[8])

            dados_calculados = testes_ordenados[0]

        # Melhores Modelagem e Aderência

        elif self.n_melhor_modelagem == 0 and self.n_melhor_aderencia == 0:
            for i in range(len(self.lista_de_funcoes_cumulativas_de_probabilidade)):
                for j in range(len(self.lista_de_aderencias)):
                    testes.append(self.calculando_1(anos_e_precipitacoes, 
                                                    self.lista_de_funcoes_cumulativas_de_probabilidade[i], 
                                                    self.lista_de_aderencias[j], 
                                                    otimizacao_variavel))

            testes_ordenados = sorted(testes, reverse=True, key=lambda x: x[8])

            dados_calculados = testes_ordenados[0]

        # Melhores Modelagem e Otimização

        elif self.n_melhor_modelagem == 0 and self.n_melhor_otimizacao == 0:
            for i in range(len(self.lista_de_funcoes_cumulativas_de_probabilidade)):
                for j in range(len(self.lista_de_otimizacoes)):
                    testes.append(self.calculando_1(anos_e_precipitacoes, 
                                                    self.lista_de_funcoes_cumulativas_de_probabilidade[i], 
                                                    aderencia_variavel, 
                                                    self.lista_de_otimizacoes[j]))

            testes_ordenados = sorted(testes, reverse=True, key=lambda x: x[8])

            dados_calculados = testes_ordenados[0]

        # Melhores Aderência e Otimização

        elif self.n_melhor_aderencia == 0 and self.n_melhor_otimizacao == 0:
            for i in range(len(self.lista_de_aderencias)):
                for j in range(len(self.lista_de_otimizacoes)):
                    testes.append(self.calculando_1(anos_e_precipitacoes, 
                                                    modelagem_variavel, 
                                                    self.lista_de_aderencias[i], 
                                                    self.lista_de_otimizacoes[j]))

            testes_ordenados = sorted(testes, reverse=True, key=lambda x: x[8])

            dados_calculados = testes_ordenados[0]

        # Melhor Modelagem

        elif self.n_melhor_modelagem == 0:
            for i in range(len(self.lista_de_funcoes_cumulativas_de_probabilidade)):
                testes.append(self.calculando_1(anos_e_precipitacoes, 
                                                self.lista_de_funcoes_cumulativas_de_probabilidade[i], 
                                                aderencia_variavel, 
                                                otimizacao_variavel))

            testes_ordenados = sorted(testes, reverse=True, key=lambda x: x[8])

            dados_calculados = testes_ordenados[0]

        # Melhor Aderência

        elif self.n_melhor_aderencia == 0:
            for i in range(len(self.lista_de_aderencias)):
                testes.append(self.calculando_1(anos_e_precipitacoes, 
                                                modelagem_variavel, 
                                                self.lista_de_aderencias[i], 
                                                otimizacao_variavel))

            testes_ordenados = sorted(testes, reverse=True, key=lambda x: x[8])

            dados_calculados = testes_ordenados[0]

        # Melhor Otimização

        elif self.n_melhor_otimizacao == 0:
            for i in range(len(self.lista_de_otimizacoes)):
                testes.append(self.calculando_1(anos_e_precipitacoes, 
                                                modelagem_variavel, 
                                                aderencia_variavel, 
                                                self.lista_de_otimizacoes[i]))

            testes_ordenados = sorted(testes, reverse=True, key=lambda x: x[8])

            dados_calculados = testes_ordenados[0]

        # Escolha do Usuário

        else:
            dados_calculados = self.calculando_1(anos_e_precipitacoes, 
                                                 modelagem_variavel, 
                                                 aderencia_variavel, 
                                                 otimizacao_variavel)

        return dados_calculados

    # Direcionador de Coordenadas
    def direcionador(self):
        self.coordenada_apurada_x = longitude_x
        self.coordenada_apurada_y = latitude_y

        self.ano_inicial_da_cidade = ""
        self.ano_final_da_cidade   = ""

        self.dados_da_aba_1 = ['','','','','','','','','','','','']

        self.funcao_destruicao_1()

    # Botão de Exportar
    def exportando(self):
        self.quadro_1_itens = []

        for i in range(len(self.quadro_4_itens)):
            if not np.isnan(self.quadro_4_itens[i][1]):
                self.quadro_1_itens.append(self.quadro_4_itens[i])

        self.funcao_destruicao_2()

    # Funções de Destruição
    def funcao_destruicao_1(self):
        self.parametro_a.destroy()
        self.parametro_b.destroy()
        self.parametro_c.destroy()
        self.parametro_d.destroy()
        self.latitude_1.destroy()
        self.longitude_1.destroy()
        self.ano_inicial.destroy()
        self.ano_final.destroy()
        self.tipo_de_frequencia_resposta.destroy()
        self.qualidade_1.destroy()
        self.amostra_1.destroy()
        self.metodo_1.destroy()
        self.latitude_2.destroy()
        self.longitude_2.destroy()

        self.aba_1_funcoes_destrutivas()

    def funcao_destruicao_2(self):
        self.quadro_1.destroy()
        self.y_scroll_1.destroy()
        self.lista_de_insercao_1.destroy()
        self.funcao_densidade_probabilidade_otimizada.destroy()
        self.aderencia_otimizada.destroy()
        self.otimizacao_otimizada.destroy()

        if self.n_coeficientes_de_desagregacao == 0:
            self.funcao_destruicao_2_1()

        elif self.n_coeficientes_de_desagregacao == 1:
            self.funcao_destruicao_2_2()

        self.quadro_3.destroy()
        self.y_scroll_3.destroy()
        self.parametro_a_1.destroy()
        self.parametro_b_1.destroy()
        self.parametro_c_1.destroy()
        self.parametro_d_1.destroy()

        self.aba_2_funcoes_destrutivas()
    
    def funcao_destruicao_2_1(self):
        self.quadro_2.destroy()
        self.y_scroll_2.destroy()
        self.titulo_duracao.destroy()
        self.digitar_duracao.destroy()
        self.botao_inserir_2.destroy()
        self.botao_apagar_2.destroy()
    
    def funcao_destruicao_2_2(self):
        self.h24d01_texto.destroy()
        self.h24d01.destroy()
        self.h12h24_texto.destroy()
        self.h12h24.destroy()
        self.h10d24_texto.destroy()
        self.h10h24.destroy()
        self.h08h24_texto.destroy()
        self.h08h24.destroy()
        self.h06h24_texto.destroy()
        self.h06h24.destroy()
        self.h01h24_texto.destroy()
        self.h01h24.destroy()
        self.m30h01_texto.destroy()
        self.m30h01.destroy()
        self.m25m30_texto.destroy()
        self.m25m30.destroy()
        self.m20m30_texto.destroy()
        self.m20m30.destroy()
        self.m15m30_texto.destroy()
        self.m15m30.destroy()
        self.m10m30_texto.destroy()
        self.m10m30.destroy()
        self.m05m30_texto.destroy()
        self.m05m30.destroy()
        self.titulo_coeficientes.destroy()
        self.digitar_duracao.destroy()
        self.duracao_de_coeficientes.destroy()
        self.botao_inserir_2.destroy()

    def funcao_destruicao_2_3(self):
        self.quadro_1.destroy()
        self.y_scroll_1.destroy()
        self.lista_de_insercao_1.destroy()
        self.quadro_3.destroy()
        self.y_scroll_3.destroy()
        self.parametro_a_1.destroy()
        self.parametro_b_1.destroy()
        self.parametro_c_1.destroy()
        self.parametro_d_1.destroy()
        self.funcao_densidade_probabilidade_otimizada.destroy()
        self.aderencia_otimizada.destroy()
        self.otimizacao_otimizada.destroy()

        self.aba_2_funcoes_destrutivas()

    def funcao_destruicao_3(self):
        self.quadro_4.destroy()
        self.y_scroll_4.destroy()
        self.quadro_5.destroy()
        self.y_scroll_5.destroy()
        self.x_scroll_5.destroy()
        self.lista_de_insercao_2.destroy()

        self.aba_3_funcoes_destrutivas()

    def funcao_destruicao_4(self):
        dados = self.lista_de_cidades_bdd.get()

        self.janelas_extras.destroy()

        self.quadro_bdd_itens = banco_de_dados_total(dados)

        self.bdd()

    # Botões de Salvar
    def salvando_1(self):
        arquivo_salvo = asksaveasfilename(defaultextension=".txt", filetypes=[('Arquivo de texto UTF-8', '*.txt')])
        
        relatorio_de_equacao_idf(arquivo_salvo, self.relatorio_1_variaveis, self.variaveis_da_distribuicao, self.quadro_2_itens, self.quadro_3_itens)

    def salvando_2(self):
        arquivo_salvo = asksaveasfilename(defaultextension=".txt", filetypes=[('Arquivo de texto UTF-8', '*.txt')])

        relatorio_de_precipitacoes_maximas(arquivo_salvo, self.relatorio_2_variaveis, self.quadro_4_itens)

    def salvando_3(self):
        arquivo_salvo = asksaveasfilename(defaultextension=".csv", filetypes=[('CSV', '*.csv'), ('Arquivo de texto UTF-8', '*.txt')])

        compilacao_do_banco_de_dados(arquivo_salvo, self.quadro_bdd_itens)

    # Botões de Inserir
    def inserindo_1(self):
        if str(self.digitar_numero.get()) != "":
            self.quadro_1_itens.append([float(self.digitar_numero.get()),
                                        float(self.digitar_precipitacao.get())])

        if str(self.lista_de_insercao_1.get()) != "":
            lista_excel = np.asarray(pd.read_excel(str(self.lista_de_insercao_1.get()), index_col=None, header=None))

            for i in range(len(lista_excel)):
                self.quadro_1_itens.append(lista_excel[i])

        self.funcao_destruicao_2()

    def inserindo_2(self):
        if self.n_coeficientes_de_desagregacao == 0:
            if str(self.digitar_duracao.get()) != "":
                self.quadro_2_itens.append((int(self.digitar_duracao.get())))

        elif self.n_coeficientes_de_desagregacao == 1:
            self.n_duracao_de_coeficientes = self.duracao_de_coeficientes.current()

            self.coeficientes_de_duracoes[self.n_duracao_de_coeficientes] = self.digitar_duracao.get()

        self.funcao_destruicao_2()

    def inserindo_3(self):
        if str(self.digitar_anos.get()) != "":
            self.quadro_3_itens.append((int(self.digitar_anos.get())))

        self.funcao_destruicao_2()

    def inserindo_4(self):
        if str(self.anos_1.get()) != "":

            lista = [self.anos_1.get(), self.meses_1.get(), self.dia_1.get(), 
                     self.dia_2.get(),   self.dia_3.get(),  self.dia_4.get(), 
                     self.dia_5.get(),   self.dia_6.get(),  self.dia_7.get(), 
                     self.dia_8.get(),  self.dia_19.get(), self.dia_10.get(), 
                     self.dia_11.get(), self.dia_12.get(), self.dia_13.get(), 
                     self.dia_14.get(), self.dia_15.get(), self.dia_16.get(), 
                     self.dia_17.get(), self.dia_18.get(), self.dia_19.get(),
                     self.dia_20.get(), self.dia_21.get(), self.dia_22.get(), 
                     self.dia_23.get(), self.dia_24.get(), self.dia_25.get(), 
                     self.dia_26.get(), self.dia_27.get(), self.dia_28.get(), 
                     self.dia_29.get(), self.dia_30.get(), self.dia_31.get()]
            
            flutuante = []
            
            for i in range(len(lista)):
                if lista[i] == '':
                    flutuante.append(np.nan)

                else:
                    flutuante.append(float(lista[i]))

            self.quadro_5_itens.append(flutuante)

        if str(self.lista_de_insercao_2.get()) != "":

            lista_excel = np.asarray(pd.read_excel(str(self.lista_de_insercao_2.get()), index_col=None, header=None))

            for i in range(len(lista_excel)):
                self.quadro_5_itens.append(lista_excel[i])

        self.funcao_destruicao_3()

    # Botões de Limpar
    def limpando_1(self):
        self.quadro_1_itens = []

        self.funcao_destruicao_2()

    def limpando_2(self):
        self.quadro_5_itens = []

        self.funcao_destruicao_3()

    # Botões de Procurar
    def procurar_arquivos_1(self):
        self.arquivo_1 = askopenfilename(filetypes=[('Arquivos do Excel', ['*.xlsx', '*.csv'])])

        self.lista_procurar_1.append(self.arquivo_1)

        self.funcao_destruicao_2()

    def procurar_arquivos_2(self):
        self.arquivo_2 = askopenfilename(filetypes=[('Arquivos do Excel', ['*.xlsx', '*.csv'])])

        self.lista_procurar_2.append(self.arquivo_2)

        self.funcao_destruicao_3()

    # Botões de Relatório
    def relatorio_1(self):

        # 1.0 Configurações da Página

        self.janelas_extras = tk.Toplevel(self.root)

        self.janelas_extras.geometry("200x500")

        self.janelas_extras.resizable(False, False)

        self.janelas_extras.grab_set()

        self.fundo_de_configuracoes = Label(self.janelas_extras, text='', relief="raised", bg='#F0F0F0', fg='#800000')
        self.fundo_de_configuracoes.place(relx=0.02, rely=0.01, relwidth=0.960, relheight=0.980)

        self.conversao_de_icone(self.janelas_extras)

        # 1.1 Fundo de Configurações:

        self.fundo_de_configuracoes_2 = Label(self.janelas_extras, text='', relief="groove", bg='#F0F0F0', fg='#800000')
        self.fundo_de_configuracoes_2.place(relx=0.05, rely=0.045, relwidth=0.90, relheight=0.93)

        self.relatorio_texto = Label(self.janelas_extras, text='Relatório :', bg='#F0F0F0', fg='#000000')
        self.relatorio_texto.place(relx=0.08, rely=0.031, relwidth=0.285, relheight=0.03)

            # 1.2 Parâmetros da Equação

        self.parametros_texto = Label(self.janelas_extras, text='Parâmetros da IDF:', bg='#F0F0F0', fg='#000000')
        self.parametros_texto.place(relx=0.07, rely=0.0725, relwidth=0.5, relheight=0.03)

        self.parametro_a_texto = Label(self.janelas_extras, text='a :', bg='#F0F0F0', fg='#000000')
        self.parametro_a_texto.place(relx=0.08, rely=0.1025, relwidth=0.05, relheight=0.05)

        self.parametro_a = Label(self.janelas_extras, text=self.relatorio_1_variaveis[4], relief="sunken", bg='#FFFFFF', fg='#000000')
        self.parametro_a.place(relx=0.15, rely=0.1055, relwidth=0.325, relheight=0.05)

        self.parametro_b_texto = Label(self.janelas_extras, text='b :', bg='#F0F0F0', fg='#000000')
        self.parametro_b_texto.place(relx=0.52, rely=0.1025, relwidth=0.055, relheight=0.05)

        self.parametro_b = Label(self.janelas_extras, text=self.relatorio_1_variaveis[5], relief="sunken", bg='#FFFFFF', fg='#000000')
        self.parametro_b.place(relx=0.595, rely=0.1055, relwidth=0.325, relheight=0.05)

        self.partida_em_c_texto = Label(self.janelas_extras, text='c :', bg='#F0F0F0', fg='#000000')
        self.partida_em_c_texto.place(relx=0.08, rely=0.1595, relwidth=0.05, relheight=0.05)

        self.parametro_c = Label(self.janelas_extras, text=self.relatorio_1_variaveis[6], relief="sunken", bg='#FFFFFF', fg='#000000')
        self.parametro_c.place(relx=0.15, rely=0.1625, relwidth=0.325, relheight=0.05)

        self.parametro_d_texto = Label(self.janelas_extras, text='d :', bg='#F0F0F0', fg='#000000')
        self.parametro_d_texto.place(relx=0.52, rely=0.1595, relwidth=0.055, relheight=0.05)

        self.parametro_d = Label(self.janelas_extras, text=self.relatorio_1_variaveis[7], relief="sunken", bg='#FFFFFF', fg='#000000')
        self.parametro_d.place(relx=0.595, rely=0.1625, relwidth=0.325, relheight=0.05)

            # 1.3 Modelagem Probabilística

        self.relatorio_modelagem_texto = Label(self.janelas_extras, text='Modelagem :', bg='#F0F0F0', fg='#000000')
        self.relatorio_modelagem_texto.place(relx=0.07, rely=0.2365, relwidth=0.35, relheight=0.03)

        self.relatorio_modelagem = Label(self.janelas_extras, text=self.relatorio_1_variaveis[10], relief="sunken", bg='#FFFFFF', fg='#000000')
        self.relatorio_modelagem.place(relx=0.07, rely=0.2695, relwidth=0.41, relheight=0.05)

            # 1.4 Método de Otimização

        self.relatorio_otimizacao_texto = Label(self.janelas_extras, text='Otimização :', bg='#F0F0F0', fg='#000000')
        self.relatorio_otimizacao_texto.place(relx=0.52, rely=0.2365, relwidth=0.32, relheight=0.03)

        self.relatorio_otimizacao = Label(self.janelas_extras, text=self.relatorio_1_variaveis[11], relief="sunken", bg='#FFFFFF', fg='#000000')
        self.relatorio_otimizacao.place(relx=0.52, rely=0.2695, relwidth=0.41, relheight=0.05)

            # 1.5 Aderência Probabilística

        self.relatorio_aderencia_texto = Label(self.janelas_extras, text='Aderência :', bg='#F0F0F0', fg='#000000')
        self.relatorio_aderencia_texto.place(relx=0.07, rely=0.3435, relwidth=0.32, relheight=0.03)

        self.relatorio_aderencia = Label(self.janelas_extras, text=self.relatorio_1_variaveis[2], relief="sunken", bg='#FFFFFF', fg='#000000')
        self.relatorio_aderencia.place(relx=0.07, rely=0.3765, relwidth=0.41, relheight=0.05)

           # 1.7 Número da Amostra de Anos

        self.relatorio_amostra_texto = Label(self.janelas_extras, text='Amostra :', bg='#F0F0F0', fg='#000000')
        self.relatorio_amostra_texto.place(relx=0.52, rely=0.3435, relwidth=0.28, relheight=0.03)

        self.relatorio_amostra = Label(self.janelas_extras, text=self.relatorio_1_variaveis[3], relief="sunken", bg='#FFFFFF', fg='#000000')
        self.relatorio_amostra.place(relx=0.52, rely=0.3765, relwidth=0.41, relheight=0.05)

            # 1.8 Qualidade da Aderência

        self.qualidade_de_aderencia_texto = Label(self.janelas_extras, text='Qualidade da Aderência :', bg='#F0F0F0', fg='#000000')
        self.qualidade_de_aderencia_texto.place(relx=0.07, rely=0.4505, relwidth=0.67, relheight=0.03)

        self.qualidade_de_aderencia = Label(self.janelas_extras, text=self.relatorio_1_variaveis[1], relief="sunken", bg='#FFFFFF', fg='#000000')
        self.qualidade_de_aderencia.place(relx=0.07, rely=0.4835, relwidth=0.855, relheight=0.05)

            # 1.9 Mann-Kendall

        self.relatorio_mk_texto = Label(self.janelas_extras, text='MK :', bg='#F0F0F0', fg='#000000')
        self.relatorio_mk_texto.place(relx=0.07, rely=0.5575, relwidth=0.13, relheight=0.03)

        self.relatorio_mk = Label(self.janelas_extras, text=self.relatorio_1_variaveis[0], relief="sunken", bg='#FFFFFF', fg='#000000')
        self.relatorio_mk.place(relx=0.07, rely=0.5905, relwidth=0.855, relheight=0.05)

            # 1.10 Nash-Stucliffe

        self.relatorio_ns_texto = Label(self.janelas_extras, text='NS :', bg='#F0F0F0', fg='#000000')
        self.relatorio_ns_texto.place(relx=0.07, rely=0.6645, relwidth=0.12, relheight=0.03)

        self.relatorio_ns = Label(self.janelas_extras, text='%.4f' % self.relatorio_1_variaveis[8], relief="sunken", bg='#FFFFFF', fg='#000000')
        self.relatorio_ns.place(relx=0.07, rely=0.6975, relwidth=0.41, relheight=0.05)

            # 1.11 RMSE

        self.relatorio_rmse_texto = Label(self.janelas_extras, text='RMSE :', bg='#F0F0F0', fg='#000000')
        self.relatorio_rmse_texto.place(relx=0.52, rely=0.6645, relwidth=0.20, relheight=0.03)

        self.relatorio_rmse = Label(self.janelas_extras, text='%.4f' % self.relatorio_1_variaveis[9], relief="sunken", bg='#FFFFFF', fg='#000000')
        self.relatorio_rmse.place(relx=0.52, rely=0.6975, relwidth=0.41, relheight=0.05)

            # 1.12 Parâmetros de Frequência
            
        if (self.relatorio_1_variaveis[10] == 'EXP' or 
            self.relatorio_1_variaveis[10] == 'GUM'):
            location, location_number = 'μ', self.relatorio_1_variaveis[-1][-2]
            scale, scale_number = 'β', self.relatorio_1_variaveis[-1][-1]
        
        elif (self.relatorio_1_variaveis[10] == 'GAM'):
            shape, shape_number = 'α', self.relatorio_1_variaveis[-1][-3]
            location, location_number = 'λ', self.relatorio_1_variaveis[-1][-2]
            scale, scale_number = 'β', self.relatorio_1_variaveis[-1][-1]

        elif (self.relatorio_1_variaveis[10] == 'GPA' or
              self.relatorio_1_variaveis[10] == 'GVE' or
              self.relatorio_1_variaveis[10] == 'LOG'):
            shape, shape_number = 'ξ', self.relatorio_1_variaveis[-1][-3]
            location, location_number = 'μ', self.relatorio_1_variaveis[-1][-2]
            scale, scale_number = 'σ', self.relatorio_1_variaveis[-1][-1]

        elif self.relatorio_1_variaveis[10] == 'KP4':
            asymmetry, asymmetry_number = 'h', self.relatorio_1_variaveis[-1][-4]
            kurtosis, kurtosis_number = 'k', self.relatorio_1_variaveis[-1][-3]
            location, location_number = 'μ', self.relatorio_1_variaveis[-1][-2]
            scale, scale_number = 'σ', self.relatorio_1_variaveis[-1][-1]

        elif self.relatorio_1_variaveis[10] == 'LN2':
            shape, shape_number = 'σ', self.relatorio_1_variaveis[-1][-3]
            location, location_number = 'μ', self.relatorio_1_variaveis[-1][-2]
            scale, scale_number = 'β', self.relatorio_1_variaveis[-1][-1]

        elif self.relatorio_1_variaveis[10] == 'NOG':
            shape, shape_number = 'β', self.relatorio_1_variaveis[-1][-3]
            location, location_number = 'μ', self.relatorio_1_variaveis[-1][-2]
            scale, scale_number = 'σ', self.relatorio_1_variaveis[-1][-1]

        elif self.relatorio_1_variaveis[10] == 'PT3':
            shape, shape_number = 'β', self.relatorio_1_variaveis[-1][-3]
            location, location_number = 'ξ', self.relatorio_1_variaveis[-1][-2]
            scale, scale_number = 'ω', self.relatorio_1_variaveis[-1][-1]

        elif self.relatorio_1_variaveis[10] == 'WEI':
            shape, shape_number = 'k', self.relatorio_1_variaveis[-1][-3]
            location, location_number = 'θ', self.relatorio_1_variaveis[-1][-2]
            scale, scale_number = 'λ', self.relatorio_1_variaveis[-1][-1]

        self.parametros_texto = Label(self.janelas_extras, text='Parâmetros de Modelagem:', bg='#F0F0F0', fg='#000000')
        self.parametros_texto.place(relx=0.07, rely=0.7715, relwidth=0.75, relheight=0.03)

        self.parametro_location_texto = Label(self.janelas_extras, text=location, bg='#F0F0F0', fg='#000000')
        self.parametro_location_texto.place(relx=0.07, rely=0.8015, relwidth=0.065, relheight=0.05)

        self.parametro_location = Label(self.janelas_extras, text= '%.4f' % location_number, relief="sunken", bg='#FFFFFF', fg='#000000')
        self.parametro_location.place(relx=0.15, rely=0.8045, relwidth=0.325, relheight=0.05)

        self.parametro_scale_texto = Label(self.janelas_extras, text=scale, bg='#F0F0F0', fg='#000000')
        self.parametro_scale_texto.place(relx=0.51, rely=0.8015, relwidth=0.065, relheight=0.05)

        self.parametro_scale = Label(self.janelas_extras, text= '%.4f' % scale_number, relief="sunken", bg='#FFFFFF', fg='#000000')
        self.parametro_scale.place(relx=0.595, rely=0.8045, relwidth=0.325, relheight=0.05)

        self.variaveis_da_distribuicao = f'"{location} = {location_number:.4f}", "{scale} = {scale_number:.4f}"'

        if len(self.relatorio_1_variaveis[-1]) == 3:

            self.partida_variacao_1_texto = Label(self.janelas_extras, text=shape, bg='#F0F0F0', fg='#000000')
            self.partida_variacao_1_texto.place(relx=0.08, rely=0.8555, relwidth=0.065, relheight=0.05)

            self.parametro_variacao_1 = Label(self.janelas_extras, text= '%.4f' % shape_number, relief="sunken", bg='#FFFFFF', fg='#000000')
            self.parametro_variacao_1.place(relx=0.15, rely=0.8585, relwidth=0.325, relheight=0.05)

            self.variaveis_da_distribuicao += f', "{shape} = {shape_number:.4f}"'

        elif len(self.relatorio_1_variaveis[-1]) == 4:

            self.partida_variacao_1_texto = Label(self.janelas_extras, text=kurtosis, bg='#F0F0F0', fg='#000000')
            self.partida_variacao_1_texto.place(relx=0.08, rely=0.8555, relwidth=0.065, relheight=0.05)

            self.parametro_variacao_1 = Label(self.janelas_extras, text= '%.4f' % kurtosis_number, relief="sunken", bg='#FFFFFF', fg='#000000')
            self.parametro_variacao_1.place(relx=0.15, rely=0.8585, relwidth=0.325, relheight=0.05)

            self.parametro_variacao_2_texto = Label(self.janelas_extras, text=asymmetry, bg='#F0F0F0', fg='#000000')
            self.parametro_variacao_2_texto.place(relx=0.52, rely=0.8555, relwidth=0.065, relheight=0.05)

            self.parametro_variacao_2 = Label(self.janelas_extras, text= '%.4f' % asymmetry_number, relief="sunken", bg='#FFFFFF', fg='#000000')
            self.parametro_variacao_2.place(relx=0.595, rely=0.8585, relwidth=0.325, relheight=0.05)

            self.variaveis_da_distribuicao += f', "{kurtosis} = {kurtosis_number:.4f}", "{asymmetry} = {asymmetry_number:.4f}"'

        self.botao_de_salvar_1 = Button(self.janelas_extras, text='Salvar', bg='#F0F0F0', fg='#000000',
                                          command=self.salvando_1)
        self.botao_de_salvar_1.place(relx=0.08, rely=0.92, relwidth=0.3, relheight=0.04)

    def relatorio_1_1(self):

        if self.dados_da_aba_1[0] != '':
            self.relatorio_1_variaveis = self.dados_da_aba_1

            self.relatorio_1()

        else:
            pass

    def relatorio_1_2(self):

        if self.dados_da_aba_2[0] != '':
            self.relatorio_1_variaveis = self.dados_da_aba_2

            self.relatorio_1()

        else:
            pass

    def relatorio_2(self):

        # 1.0 Configurações da Página

        if self.relatorio_2_variaveis[3] != '':

            self.janelas_extras = tk.Toplevel(self.root)

            self.janelas_extras.geometry("200x200")

            self.janelas_extras.resizable(False, False)

            self.janelas_extras.grab_set()

            self.fundo_de_configuracoes = Label(self.janelas_extras, text='', relief="raised", bg='#F0F0F0', fg='#800000')
            self.fundo_de_configuracoes.place(relx=0.03, rely=0.03, relwidth=0.940, relheight=0.940)

            self.conversao_de_icone(self.janelas_extras)

            # 1.1 Fundo de Configurações:

            self.fundo_de_configuracoes_2 = Label(self.janelas_extras, text='', relief="groove", bg='#F0F0F0', fg='#800000')
            self.fundo_de_configuracoes_2.place(relx=0.06, rely=0.11, relwidth=0.88, relheight=0.83)

            self.relatorio_texto = Label(self.janelas_extras, text='Relatório :', bg='#F0F0F0', fg='#000000')
            self.relatorio_texto.place(relx=0.08, rely=0.08, relwidth=0.285, relheight=0.05)

            # 1.2 Dias Totais

            self.relatorio_dias_texto = Label(self.janelas_extras, text='Dias :', bg='#F0F0F0', fg='#000000')
            self.relatorio_dias_texto.place(relx=0.08, rely=0.2, relwidth=0.15, relheight=0.1)

            self.relatorio_dias = Label(self.janelas_extras, text=self.relatorio_2_variaveis[0], relief="sunken", bg='#FFFFFF', fg='#000000')
            self.relatorio_dias.place(relx=0.08, rely=0.29, relwidth=0.41, relheight=0.12)

            # 1.3 Dias Falhos

            self.relatorio_dias_falhos_texto = Label(self.janelas_extras, text='Dias Falhos :', bg='#F0F0F0', fg='#000000')
            self.relatorio_dias_falhos_texto.place(relx=0.51, rely=0.2, relwidth=0.35, relheight=0.1)

            self.relatorio_dias_falhos = Label(self.janelas_extras, text=self.relatorio_2_variaveis[1], relief="sunken", bg='#FFFFFF', fg='#000000')
            self.relatorio_dias_falhos.place(relx=0.51, rely=0.29, relwidth=0.41, relheight=0.12)

            # 1.4 Limiar de Falhas

            self.relatorio_limiar_texto = Label(self.janelas_extras, text='Limiar :', bg='#F0F0F0', fg='#000000')
            self.relatorio_limiar_texto.place(relx=0.08, rely=0.45, relwidth=0.2, relheight=0.1)

            self.relatorio_limiar = Label(self.janelas_extras, text=str(self.relatorio_2_variaveis[2])+'%', relief="sunken", bg='#FFFFFF', fg='#000000')
            self.relatorio_limiar.place(relx=0.08, rely=0.54, relwidth=0.41, relheight=0.12)

            # 1.5 Porcentagem de Falhas

            self.relatorio_falhas_texto = Label(self.janelas_extras, text='Falhas :', bg='#F0F0F0', fg='#000000')
            self.relatorio_falhas_texto.place(relx=0.51, rely=0.45, relwidth=0.2, relheight=0.1)

            self.relatorio_falhas = Label(self.janelas_extras, text=str(self.relatorio_2_variaveis[3])+'%', relief="sunken", bg='#FFFFFF', fg='#000000')
            self.relatorio_falhas.place(relx=0.51, rely=0.54, relwidth=0.41, relheight=0.12)

            self.botao_de_salvar_2 = Button(self.janelas_extras, text='Salvar', bg='#F0F0F0', fg='#000000',
                                            command=self.salvando_2)
            self.botao_de_salvar_2.place(relx=0.1, rely=0.77, relwidth=0.33, relheight=0.125)

    # Menu de Opções
    def menus(self):
        barra_de_menu = Menu(self.root)
        root.config(menu=barra_de_menu)

        menu_de_arquivos = Menu(barra_de_menu)
        barra_de_menu.add_cascade(label='Arquivos', menu = menu_de_arquivos)
        menu_de_arquivos.add_command(label='Reiniciar', command=self.reiniciar)
        menu_de_arquivos.add_command(label='Sair', command=self.sair)

        menu_de_opcoes = Menu(barra_de_menu)
        barra_de_menu.add_cascade(label='Opções', menu = menu_de_opcoes)
        menu_de_opcoes.add_command(label='Banco de Dados', command=self.bdd)
        menu_de_opcoes.add_command(label='Configurações', command=self.configuracoes)
        menu_de_opcoes.add_command(label='Varreduras', command=self.varreduras)

        menu_de_ajuda = Menu(barra_de_menu)
        barra_de_menu.add_cascade(label='Ajuda', menu = menu_de_ajuda)
        menu_de_ajuda.add_command(label='Estudo', command=self.estudo)
        menu_de_ajuda.add_command(label='Ferramenta', command=self.ferramenta)
        menu_de_ajuda.add_command(label='Siglas', command=self.siglas)

    # Opções de Ajuda
    def ajuda(self, img):

        # Configurações da Página

        self.janela_de_ajuda = tk.Toplevel()

        self.janela_de_ajuda.geometry("750x500")

        self.janela_de_ajuda.resizable(False, False)

        self.janela_de_ajuda.grab_set()
        
        self.main_frame = Frame(self.janela_de_ajuda)
        self.main_frame.pack(fill=BOTH, expand=1)

        self.conversao_de_icone(self.janela_de_ajuda)

        # Criando um Canvas

        self.my_canvas = Canvas(self.main_frame)

        self.my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        # Adicionando ScrollBar ao Canvas

        self.my_scrollbar = ttk.Scrollbar(self.main_frame, orient=VERTICAL, command=self.my_canvas.yview)
        self.my_scrollbar.pack(side=RIGHT, fill=Y)

        # Configurando o Canvas

        self.my_canvas.configure(yscrollcommand=self.my_scrollbar.set)
        self.my_canvas.bind('<Configure>', lambda e: self.my_canvas.configure(scrollregion = self.my_canvas.bbox("all")))

        # Adicionando Imagem à Janela na Tela

        self.informacoes = tk.PhotoImage(data=imagens_de_ferramenta(img))

        self.my_canvas.create_image(1, 1, image=self.informacoes, anchor=tk.NW)

    def estudo(self):
        self.ajuda('estudo')

    def ferramenta(self):
        self.ajuda('ferramenta')

    def siglas(self):
        self.ajuda('siglas')

    # Opção Banco de Dados
    def bdd(self):

        # Configurações da Página

        self.janelas_extras = tk.Toplevel(self.root)

        self.janelas_extras.geometry("750x500")

        self.janelas_extras.resizable(False, False)

        self.janelas_extras.grab_set()

        self.conversao_de_icone(self.janelas_extras)

        # Fundo da Tabela de Precipitações:

        self.fundo_bdd = Label(self.janelas_extras, text='', relief="raised", bg='#F0F0F0', fg='#800000')
        self.fundo_bdd.place(relx=0.005, rely=0.01, relwidth=0.985, relheight=0.98)

        self.fundo_de_precipitacoes_bdd = Label(self.janelas_extras, text='', relief="groove", bg='#F0F0F0', fg='#800000')
        self.fundo_de_precipitacoes_bdd.place(relx=0.015, rely=0.04, relwidth=0.965, relheight=0.935)

        self.precipitacoes_bdd = Label(self.janelas_extras, text='Precipitações :', bg='#F0F0F0', fg='#000000')
        self.precipitacoes_bdd.place(relx=0.025, rely=0.02, relwidth=0.11, relheight=0.035)

        # Tabela de Precipitações:

        self.quadro_bdd = ttk.Treeview(self.janelas_extras,
                                     columns=('Cidade', 'Latitude', 'Longitude', 'Ano', 'Mês', 
                                              'Dia 01', 'Dia 02', 'Dia 03', 'Dia 04', 
                                              'Dia 05', 'Dia 06', 'Dia 07', 'Dia 08', 
                                              'Dia 09', 'Dia 10', 'Dia 11', 'Dia 12', 
                                              'Dia 13', 'Dia 14', 'Dia 15', 'Dia 16', 
                                              'Dia 17', 'Dia 18', 'Dia 19', 'Dia 20', 
                                              'Dia 21', 'Dia 22', 'Dia 23', 'Dia 24', 
                                              'Dia 25', 'Dia 26', 'Dia 27', 'Dia 28', 
                                              'Dia 29', 'Dia 30', 'Dia 31'))

        self.quadro_bdd.column('#0', width=0, stretch=NO)
        self.quadro_bdd.column('Cidade', anchor=CENTER, width=100)
        self.quadro_bdd.column('Latitude' , anchor=CENTER, width=75)
        self.quadro_bdd.column('Longitude', anchor=CENTER, width=75)
        self.quadro_bdd.column('Ano', anchor=CENTER, width=50)
        self.quadro_bdd.column('Mês', anchor=CENTER, width=50)
        self.quadro_bdd.column('Dia 01', anchor=CENTER, width=50)
        self.quadro_bdd.column('Dia 02', anchor=CENTER, width=50)
        self.quadro_bdd.column('Dia 03', anchor=CENTER, width=50)
        self.quadro_bdd.column('Dia 04', anchor=CENTER, width=50)
        self.quadro_bdd.column('Dia 05', anchor=CENTER, width=50)
        self.quadro_bdd.column('Dia 06', anchor=CENTER, width=50)
        self.quadro_bdd.column('Dia 07', anchor=CENTER, width=50)
        self.quadro_bdd.column('Dia 08', anchor=CENTER, width=50)
        self.quadro_bdd.column('Dia 09', anchor=CENTER, width=50)
        self.quadro_bdd.column('Dia 10', anchor=CENTER, width=50)
        self.quadro_bdd.column('Dia 11', anchor=CENTER, width=50)
        self.quadro_bdd.column('Dia 12', anchor=CENTER, width=50)
        self.quadro_bdd.column('Dia 13', anchor=CENTER, width=50)
        self.quadro_bdd.column('Dia 14', anchor=CENTER, width=50)
        self.quadro_bdd.column('Dia 15', anchor=CENTER, width=50)
        self.quadro_bdd.column('Dia 16', anchor=CENTER, width=50)
        self.quadro_bdd.column('Dia 17', anchor=CENTER, width=50)
        self.quadro_bdd.column('Dia 18', anchor=CENTER, width=50)
        self.quadro_bdd.column('Dia 19', anchor=CENTER, width=50)
        self.quadro_bdd.column('Dia 20', anchor=CENTER, width=50)
        self.quadro_bdd.column('Dia 21', anchor=CENTER, width=50)
        self.quadro_bdd.column('Dia 22', anchor=CENTER, width=50)
        self.quadro_bdd.column('Dia 23', anchor=CENTER, width=50)
        self.quadro_bdd.column('Dia 24', anchor=CENTER, width=50)
        self.quadro_bdd.column('Dia 25', anchor=CENTER, width=50)
        self.quadro_bdd.column('Dia 26', anchor=CENTER, width=50)
        self.quadro_bdd.column('Dia 27', anchor=CENTER, width=50)
        self.quadro_bdd.column('Dia 28', anchor=CENTER, width=50)
        self.quadro_bdd.column('Dia 29', anchor=CENTER, width=50)
        self.quadro_bdd.column('Dia 30', anchor=CENTER, width=50)
        self.quadro_bdd.column('Dia 31', anchor=CENTER, width=50)

        self.quadro_bdd.heading('Cidade', text='Cidade', anchor=CENTER)
        self.quadro_bdd.heading('Latitude' , text='Latitude' , anchor=CENTER)
        self.quadro_bdd.heading('Longitude', text='Longitude', anchor=CENTER)
        self.quadro_bdd.heading('Ano', text='Ano', anchor=CENTER)
        self.quadro_bdd.heading('Mês', text='Mês', anchor=CENTER)
        self.quadro_bdd.heading('Dia 01', text='Dia 01', anchor=CENTER)
        self.quadro_bdd.heading('Dia 02', text='Dia 02', anchor=CENTER)
        self.quadro_bdd.heading('Dia 03', text='Dia 03', anchor=CENTER)
        self.quadro_bdd.heading('Dia 04', text='Dia 04', anchor=CENTER)
        self.quadro_bdd.heading('Dia 05', text='Dia 05', anchor=CENTER)
        self.quadro_bdd.heading('Dia 06', text='Dia 06', anchor=CENTER)
        self.quadro_bdd.heading('Dia 07', text='Dia 07', anchor=CENTER)
        self.quadro_bdd.heading('Dia 08', text='Dia 08', anchor=CENTER)
        self.quadro_bdd.heading('Dia 09', text='Dia 09', anchor=CENTER)
        self.quadro_bdd.heading('Dia 10', text='Dia 10', anchor=CENTER)
        self.quadro_bdd.heading('Dia 11', text='Dia 11', anchor=CENTER)
        self.quadro_bdd.heading('Dia 12', text='Dia 12', anchor=CENTER)
        self.quadro_bdd.heading('Dia 13', text='Dia 13', anchor=CENTER)
        self.quadro_bdd.heading('Dia 14', text='Dia 14', anchor=CENTER)
        self.quadro_bdd.heading('Dia 15', text='Dia 15', anchor=CENTER)
        self.quadro_bdd.heading('Dia 16', text='Dia 16', anchor=CENTER)
        self.quadro_bdd.heading('Dia 17', text='Dia 17', anchor=CENTER)
        self.quadro_bdd.heading('Dia 18', text='Dia 18', anchor=CENTER)
        self.quadro_bdd.heading('Dia 19', text='Dia 19', anchor=CENTER)
        self.quadro_bdd.heading('Dia 20', text='Dia 20', anchor=CENTER)
        self.quadro_bdd.heading('Dia 21', text='Dia 21', anchor=CENTER)
        self.quadro_bdd.heading('Dia 22', text='Dia 22', anchor=CENTER)
        self.quadro_bdd.heading('Dia 23', text='Dia 23', anchor=CENTER)
        self.quadro_bdd.heading('Dia 24', text='Dia 24', anchor=CENTER)
        self.quadro_bdd.heading('Dia 25', text='Dia 25', anchor=CENTER)
        self.quadro_bdd.heading('Dia 26', text='Dia 26', anchor=CENTER)
        self.quadro_bdd.heading('Dia 27', text='Dia 27', anchor=CENTER)
        self.quadro_bdd.heading('Dia 28', text='Dia 28', anchor=CENTER)
        self.quadro_bdd.heading('Dia 29', text='Dia 29', anchor=CENTER)
        self.quadro_bdd.heading('Dia 30', text='Dia 30', anchor=CENTER)
        self.quadro_bdd.heading('Dia 31', text='Dia 31', anchor=CENTER)

        self.quadro_bdd.place(relx=0.025, rely=0.065, relwidth=0.925, relheight=0.8)

        self.y_scroll_bdd = ttk.Scrollbar(self.janelas_extras, orient=tk.VERTICAL, command=self.quadro_bdd.yview)

        self.quadro_bdd['yscroll'] = self.y_scroll_bdd.set

        self.y_scroll_bdd.place(relx=0.95, rely=0.065, relwidth=0.025, relheight=0.8)

        self.x_scroll_bdd = ttk.Scrollbar(self.janelas_extras, orient=tk.HORIZONTAL, command=self.quadro_bdd.xview)

        self.quadro_bdd['xscroll'] = self.x_scroll_bdd.set

        self.x_scroll_bdd.place(relx=0.025, rely=0.865, relwidth=0.925, relheight=0.04)

        for i in range(len(self.quadro_bdd_itens)):
                    self.quadro_bdd.insert(parent='', index=i, iid=i, text='', values=(
                    self.quadro_bdd_itens[i][0],  self.quadro_bdd_itens[i][1],  self.quadro_bdd_itens[i][2],
                    self.quadro_bdd_itens[i][3],  self.quadro_bdd_itens[i][4],  self.quadro_bdd_itens[i][5],
                    self.quadro_bdd_itens[i][6],  self.quadro_bdd_itens[i][7],  self.quadro_bdd_itens[i][8],
                    self.quadro_bdd_itens[i][9],  self.quadro_bdd_itens[i][10], self.quadro_bdd_itens[i][11],
                    self.quadro_bdd_itens[i][12], self.quadro_bdd_itens[i][13], self.quadro_bdd_itens[i][14],
                    self.quadro_bdd_itens[i][15], self.quadro_bdd_itens[i][16], self.quadro_bdd_itens[i][17],
                    self.quadro_bdd_itens[i][18], self.quadro_bdd_itens[i][19], self.quadro_bdd_itens[i][20],
                    self.quadro_bdd_itens[i][21], self.quadro_bdd_itens[i][22], self.quadro_bdd_itens[i][23],
                    self.quadro_bdd_itens[i][24], self.quadro_bdd_itens[i][25], self.quadro_bdd_itens[i][26],
                    self.quadro_bdd_itens[i][27], self.quadro_bdd_itens[i][28], self.quadro_bdd_itens[i][29],
                    self.quadro_bdd_itens[i][30], self.quadro_bdd_itens[i][31], self.quadro_bdd_itens[i][32],
                    self.quadro_bdd_itens[i][33], self.quadro_bdd_itens[i][34], self.quadro_bdd_itens[i][35]))
        
        # Seleção da Cidade

        self.cidade_bdd = Label(self.janelas_extras, text='Cidades :', bg='#F0F0F0', fg='#000000')
        self.cidade_bdd.place(relx=0.025, rely=0.91, relwidth=0.0725, relheight=0.05)

        valores_da_lista = self.cidades_registradas

        self.lista_de_cidades_bdd = ttk.Combobox(self.janelas_extras, values=(valores_da_lista))
        self.lista_de_cidades_bdd.place(relx=0.1025, rely=0.91, relwidth=0.242, relheight=0.05)
        self.lista_de_cidades_bdd.current(0)

        self.botao_de_buscar_bdd = Button(self.janelas_extras, text='Buscar', bg='#F0F0F0', fg='#000000',
                                          command=self.funcao_destruicao_4)
        self.botao_de_buscar_bdd.place(relx=0.35, rely=0.91, relwidth=0.1, relheight=0.05)

        self.botao_de_exportar_bdd = Button(self.janelas_extras, text='Exportar', bg='#F0F0F0', fg='#000000',
                                          command=self.bdd_funcoes)
        self.botao_de_exportar_bdd.place(relx=0.458, rely=0.91, relwidth=0.1, relheight=0.05)

        self.botao_de_salvar_3 = Button(self.janelas_extras, text='Salvar', bg='#F0F0F0', fg='#000000',
                                          command=self.salvando_3)
        self.botao_de_salvar_3.place(relx=0.566, rely=0.91, relwidth=0.1, relheight=0.05)

    def bdd_funcoes(self):

        if self.quadro_bdd_itens != []:
            self.quadro_5_itens = []
            
            for i in range(len(self.quadro_bdd_itens)):
                lista, flutuante = self.quadro_bdd_itens[i][3:], []

                for j in range(len(lista)):
                    if lista[j] == '':
                        flutuante.append(np.nan)

                    else:
                        flutuante.append(float(lista[j]))

                self.quadro_5_itens.append(flutuante)

        self.funcao_destruicao_3()

    # Opção Reiniciar
    def reiniciar(self):
        self.__init__()

    # Opção Sair
    def sair(self):
        print("\nEm verdade que não convém gloriar-me; mas passarei às visões e revelações do Senhor. 2 Coríntios 12:1\n")

        self.root.destroy()
        sys.exit()

    # Opção de Configurações
    def configuracoes(self):
       
        # 1.0 Configurações da Página

        self.janelas_extras = tk.Toplevel(self.root)

        self.janelas_extras.geometry("200x500")

        self.janelas_extras.resizable(False, False)

        self.janelas_extras.grab_set()

        self.fundo_de_configuracoes = Label(self.janelas_extras, text='', relief="raised", bg='#F0F0F0', fg='#800000')
        self.fundo_de_configuracoes.place(relx=0.02, rely=0.01, relwidth=0.960, relheight=0.980)

        self.conversao_de_icone(self.janelas_extras)

        # 1.1 Fundo de Configurações:

        self.fundo_de_configuracoes_2 = Label(self.janelas_extras, text='', relief="groove", bg='#F0F0F0', fg='#800000')
        self.fundo_de_configuracoes_2.place(relx=0.05, rely=0.045, relwidth=0.90, relheight=0.93)

        self.configuracoes_texto = Label(self.janelas_extras, text='Configurações :', bg='#F0F0F0', fg='#000000')
        self.configuracoes_texto.place(relx=0.08, rely=0.031, relwidth=0.45, relheight=0.03)

        # 1.2 Coeficientes de Desagregação

        self.coeficientes_de_desagregacao_texto = Label(self.janelas_extras, text='Coeficientes de Desagregação :', bg='#F0F0F0', fg='#000000')
        self.coeficientes_de_desagregacao_texto.place(relx=0.07, rely=0.085, relwidth=0.82, relheight=0.03)

        self.coeficientes_de_desagregacao = ttk.Combobox(self.janelas_extras, values=["Coeficientes DAEE/CETESB", "Coeficientes Próprios"])
        self.coeficientes_de_desagregacao.place(relx=0.07, rely=0.118, relwidth=0.855, relheight=0.05)
        self.coeficientes_de_desagregacao.current(self.n_coeficientes_de_desagregacao)

        # 1.3 Porcentagem de Aderência

        self.porcentagem_de_aderencia_texto = Label(self.janelas_extras, text='Porcentagem de Aderência :', bg='#F0F0F0', fg='#000000')
        self.porcentagem_de_aderencia_texto.place(relx=0.07, rely=0.195, relwidth=0.75, relheight=0.03)

        self.porcentagem_de_aderencia = ttk.Combobox(self.janelas_extras, values=["1%", "5%"])
        self.porcentagem_de_aderencia.place(relx=0.07, rely=0.228, relwidth=0.855, relheight=0.05)
        self.porcentagem_de_aderencia.current(self.n_porcentagem_de_aderencia)

        # 1.4 Dias Limite de Falha

        self.dias_limite_de_falha_texto = Label(self.janelas_extras, text='Dias Limite de Falha :', bg='#F0F0F0', fg='#000000')
        self.dias_limite_de_falha_texto.place(relx=0.07, rely=0.305, relwidth=0.56, relheight=0.03)

        self.dias_limite_de_falha_entrada = Entry(self.janelas_extras)
        self.dias_limite_de_falha_entrada.place(relx=0.07, rely=0.338, relwidth=0.425, relheight=0.05)

        if self.limiar_de_erro == '':
            self.limiar_de_erro = 0

        self.dias_limite_de_falha_registro = Label(self.janelas_extras, text=int(self.limiar_de_erro), relief="sunken", bg='#FFFFFF', fg='#000000')
        self.dias_limite_de_falha_registro.place(relx=0.505, rely=0.338, relwidth=0.425, relheight=0.05)

        # 1.5 Melhor de Modelagem

        self.melhor_modelagem_texto = Label(self.janelas_extras, text='Melhor Modelagem :', bg='#F0F0F0', fg='#000000')
        self.melhor_modelagem_texto.place(relx=0.07, rely=0.415, relwidth=0.55, relheight=0.03)

        self.melhor_modelagem = ttk.Combobox(self.janelas_extras, values=["Ativado", "Desativado"])
        self.melhor_modelagem.place(relx=0.07, rely=0.448, relwidth=0.855, relheight=0.05)
        self.melhor_modelagem.current(self.n_melhor_modelagem)
        
        # 1.6 Melhor de Aderência

        self.melhor_aderencia_texto = Label(self.janelas_extras, text='Melhor Aderência :', bg='#F0F0F0', fg='#000000')
        self.melhor_aderencia_texto.place(relx=0.07, rely=0.525, relwidth=0.5, relheight=0.03)

        self.melhor_aderencia = ttk.Combobox(self.janelas_extras, values=["Ativado", "Desativado"])
        self.melhor_aderencia.place(relx=0.07, rely=0.558, relwidth=0.855, relheight=0.05)
        self.melhor_aderencia.current(self.n_melhor_aderencia)

        # 1.7 Melhor de Otimização

        self.melhor_otimizacao_texto = Label(self.janelas_extras, text='Melhor Otimização :', bg='#F0F0F0', fg='#000000')
        self.melhor_otimizacao_texto.place(relx=0.07, rely=0.635, relwidth=0.53, relheight=0.03)

        self.melhor_otimizacao = ttk.Combobox(self.janelas_extras, values=["Ativado", "Desativado"])
        self.melhor_otimizacao.place(relx=0.07, rely=0.668, relwidth=0.855, relheight=0.05)
        self.melhor_otimizacao.current(self.n_melhor_otimizacao)

        # 1.8 Quantidade de Iterações

        self.quantidade_de_iteracoes_texto = Label(self.janelas_extras, text='Iterações :', bg='#F0F0F0', fg='#000000')
        self.quantidade_de_iteracoes_texto.place(relx=0.07, rely=0.745, relwidth=0.28, relheight=0.03)

        self.quantidade_de_iteracoes = ttk.Combobox(self.janelas_extras, values=[1000, 2000, 3000,
                                                                                 4000, 5000, 6000,
                                                                                 7000, 8000, 9000,
                                                                                 10000])
        self.quantidade_de_iteracoes.place(relx=0.07, rely=0.778, relwidth=0.855, relheight=0.05)
        self.quantidade_de_iteracoes.current(self.n_quantidade_de_iteracoes)

        # 2.0 Botão de Salvar

        self.botao_salvar_0 = tk.Button(self.janelas_extras, text='Salvar', bg='#F0F0F0', fg='#000000', command=self.configuracoes_funcoes)
        self.botao_salvar_0.place(relx=0.14, rely=0.9, relwidth=0.34, relheight=0.045)

    def configuracoes_funcoes(self):

        # Reconfigurando...

        if self.n_coeficientes_de_desagregacao == 0:
            self.funcao_destruicao_2_1()

        elif self.n_coeficientes_de_desagregacao == 1:
            self.quadro_2_itens = [1440, 720, 600, 480, 360, 60, 30, 25, 20, 15, 10, 5]
            self.funcao_destruicao_2_2()

        self.n_coeficientes_de_desagregacao = self.coeficientes_de_desagregacao.current()
        self.n_porcentagem_de_aderencia = self.porcentagem_de_aderencia.current()
        self.limiar_de_erro = self.dias_limite_de_falha_entrada.get()
        self.n_melhor_modelagem = self.melhor_modelagem.current()
        self.n_melhor_aderencia = self.melhor_aderencia.current()
        self.n_melhor_otimizacao = self.melhor_otimizacao.current()
        self.n_quantidade_de_iteracoes = self.quantidade_de_iteracoes.current()

        self.funcao_destruicao_2_3()

        self.janelas_extras.destroy()
        self.configuracoes()       

    # Opção de Varreduras
    def varreduras(self):
        
        # 1.0 Configurações da Página

        self.janelas_extras = tk.Toplevel(self.root)

        self.janelas_extras.geometry("200x500")

        self.janelas_extras.resizable(False, False)

        self.janelas_extras.grab_set()

        self.fundo_de_configuracoes = Label(self.janelas_extras, text='', relief="raised", bg='#F0F0F0', fg='#800000')
        self.fundo_de_configuracoes.place(relx=0.02, rely=0.01, relwidth=0.960, relheight=0.980)

        self.conversao_de_icone(self.janelas_extras)

        # 1.1 Fundo de Configurações:

        self.fundo_de_configuracoes_2 = Label(self.janelas_extras, text='', relief="groove", bg='#F0F0F0', fg='#800000')
        self.fundo_de_configuracoes_2.place(relx=0.05, rely=0.045, relwidth=0.90, relheight=0.93)

        self.configuracoes_texto = Label(self.janelas_extras, text='Varreduras :', bg='#F0F0F0', fg='#000000')
        self.configuracoes_texto.place(relx=0.08, rely=0.031, relwidth=0.35, relheight=0.03)

            # 1.2 Numeros de Partida

        self.numeros_de_partida = Label(self.janelas_extras, text='Numeros de Partida :', bg='#F0F0F0', fg='#000000')
        self.numeros_de_partida.place(relx=0.07, rely=0.085, relwidth=0.56, relheight=0.03)

        self.partida_em_a_texto = Label(self.janelas_extras, text='a :', bg='#F0F0F0', fg='#000000')
        self.partida_em_a_texto.place(relx=0.08, rely=0.115, relwidth=0.05, relheight=0.05)

        self.partida_em_a = Label(self.janelas_extras, text=self.v_partida[0], relief="sunken", bg='#FFFFFF', fg='#000000')
        self.partida_em_a.place(relx=0.15, rely=0.118, relwidth=0.325, relheight=0.05)

        self.partida_em_b_texto = Label(self.janelas_extras, text='b :', bg='#F0F0F0', fg='#000000')
        self.partida_em_b_texto.place(relx=0.52, rely=0.115, relwidth=0.055, relheight=0.05)

        self.partida_em_b = Label(self.janelas_extras, text=self.v_partida[1], relief="sunken", bg='#FFFFFF', fg='#000000')
        self.partida_em_b.place(relx=0.595, rely=0.118, relwidth=0.325, relheight=0.05)

        self.partida_em_c_texto = Label(self.janelas_extras, text='c :', bg='#F0F0F0', fg='#000000')
        self.partida_em_c_texto.place(relx=0.08, rely=0.172, relwidth=0.05, relheight=0.05)

        self.partida_em_c = Label(self.janelas_extras, text=self.v_partida[2], relief="sunken", bg='#FFFFFF', fg='#000000')
        self.partida_em_c.place(relx=0.15, rely=0.175, relwidth=0.325, relheight=0.05)

        self.partida_em_d_texto = Label(self.janelas_extras, text='d :', bg='#F0F0F0', fg='#000000')
        self.partida_em_d_texto.place(relx=0.52, rely=0.172, relwidth=0.055, relheight=0.05)

        self.partida_em_d = Label(self.janelas_extras, text=self.v_partida[3], relief="sunken", bg='#FFFFFF', fg='#000000')
        self.partida_em_d.place(relx=0.595, rely=0.175, relwidth=0.325, relheight=0.05)

        self.inserir_partida = Entry(self.janelas_extras)
        self.inserir_partida.place(relx=0.15, rely=0.232, relwidth=0.325, relheight=0.05)

        self.parametro_partida = ttk.Combobox(self.janelas_extras, values=['', "a", "b", "c", "d"])
        self.parametro_partida.place(relx=0.595, rely=0.232, relwidth=0.325, relheight=0.05)
        self.parametro_partida.current(0)

            # 1.3 Intervalo Inicial

        self.numeros_de_intervalo_inicial = Label(self.janelas_extras, text='Intervalo Inicial :', bg='#F0F0F0', fg='#000000')
        self.numeros_de_intervalo_inicial.place(relx=0.07, rely=0.3, relwidth=0.45, relheight=0.03)

        self.intervalo_inicial_em_a_texto = Label(self.janelas_extras, text='a :', bg='#F0F0F0', fg='#000000')
        self.intervalo_inicial_em_a_texto.place(relx=0.08, rely=0.327, relwidth=0.05, relheight=0.05)

        self.intervalo_inicial_em_a = Label(self.janelas_extras, text=self.v_intervalo_inicial[0], relief="sunken", bg='#FFFFFF', fg='#000000')
        self.intervalo_inicial_em_a.place(relx=0.15, rely=0.33, relwidth=0.325, relheight=0.05)

        self.intervalo_inicial_em_b_texto = Label(self.janelas_extras, text='b :', bg='#F0F0F0', fg='#000000')
        self.intervalo_inicial_em_b_texto.place(relx=0.52, rely=0.327, relwidth=0.055, relheight=0.05)

        self.intervalo_inicial_em_b = Label(self.janelas_extras, text=self.v_intervalo_inicial[1], relief="sunken", bg='#FFFFFF', fg='#000000')
        self.intervalo_inicial_em_b.place(relx=0.595, rely=0.33, relwidth=0.325, relheight=0.05)

        self.intervalo_inicial_em_c_texto = Label(self.janelas_extras, text='c :', bg='#F0F0F0', fg='#000000')
        self.intervalo_inicial_em_c_texto.place(relx=0.08, rely=0.381, relwidth=0.05, relheight=0.05)

        self.intervalo_inicial_em_c = Label(self.janelas_extras, text=self.v_intervalo_inicial[2], relief="sunken", bg='#FFFFFF', fg='#000000')
        self.intervalo_inicial_em_c.place(relx=0.15, rely=0.384, relwidth=0.325, relheight=0.05)

        self.intervalo_inicial_em_d_texto = Label(self.janelas_extras, text='d :', bg='#F0F0F0', fg='#000000')
        self.intervalo_inicial_em_d_texto.place(relx=0.52, rely=0.381, relwidth=0.055, relheight=0.05)

        self.intervalo_inicial_em_d = Label(self.janelas_extras, text=self.v_intervalo_inicial[3], relief="sunken", bg='#FFFFFF', fg='#000000')
        self.intervalo_inicial_em_d.place(relx=0.595, rely=0.384, relwidth=0.325, relheight=0.05)

        self.inserir_intervalo_inicial = Entry(self.janelas_extras)
        self.inserir_intervalo_inicial.place(relx=0.15, rely=0.441, relwidth=0.325, relheight=0.05)

        self.parametro_intervalo_inicial = ttk.Combobox(self.janelas_extras, values=['', "a", "b", "c", "d"])
        self.parametro_intervalo_inicial.place(relx=0.595, rely=0.441, relwidth=0.325, relheight=0.05)
        self.parametro_intervalo_inicial.current(0)

            # 1.3 Intervalo Final
            
        self.numeros_de_intervalo_final = Label(self.janelas_extras, text='Intervalo Final :', bg='#F0F0F0', fg='#000000')
        self.numeros_de_intervalo_final.place(relx=0.07, rely=0.515, relwidth=0.42, relheight=0.03)

        self.intervalo_final_em_a_texto = Label(self.janelas_extras, text='a :', bg='#F0F0F0', fg='#000000')
        self.intervalo_final_em_a_texto.place(relx=0.08, rely=0.545, relwidth=0.05, relheight=0.05)

        self.intervalo_final_em_a = Label(self.janelas_extras, text=self.v_intervalo_final[0], relief="sunken", bg='#FFFFFF', fg='#000000')
        self.intervalo_final_em_a.place(relx=0.15, rely=0.548, relwidth=0.325, relheight=0.05)

        self.intervalo_final_em_b_texto = Label(self.janelas_extras, text='b :', bg='#F0F0F0', fg='#000000')
        self.intervalo_final_em_b_texto.place(relx=0.52, rely=0.545, relwidth=0.055, relheight=0.05)

        self.intervalo_final_em_b = Label(self.janelas_extras, text=self.v_intervalo_final[1], relief="sunken", bg='#FFFFFF', fg='#000000')
        self.intervalo_final_em_b.place(relx=0.595, rely=0.548, relwidth=0.325, relheight=0.05)

        self.intervalo_final_em_c_texto = Label(self.janelas_extras, text='c :', bg='#F0F0F0', fg='#000000')
        self.intervalo_final_em_c_texto.place(relx=0.08, rely=0.602, relwidth=0.05, relheight=0.05)

        self.intervalo_final_em_c = Label(self.janelas_extras, text=self.v_intervalo_final[2], relief="sunken", bg='#FFFFFF', fg='#000000')
        self.intervalo_final_em_c.place(relx=0.15, rely=0.605, relwidth=0.325, relheight=0.05)

        self.intervalo_final_em_d_texto = Label(self.janelas_extras, text='d :', bg='#F0F0F0', fg='#000000')
        self.intervalo_final_em_d_texto.place(relx=0.52, rely=0.602, relwidth=0.055, relheight=0.05)

        self.intervalo_final_em_d = Label(self.janelas_extras, text=self.v_intervalo_final[3], relief="sunken", bg='#FFFFFF', fg='#000000')
        self.intervalo_final_em_d.place(relx=0.595, rely=0.605, relwidth=0.325, relheight=0.05)

        self.inserir_intervalo_final = Entry(self.janelas_extras)
        self.inserir_intervalo_final.place(relx=0.15, rely=0.662, relwidth=0.325, relheight=0.05)

        self.parametro_intervalo_final = ttk.Combobox(self.janelas_extras, values=['', "a", "b", "c", "d"])
        self.parametro_intervalo_final.place(relx=0.595, rely=0.662, relwidth=0.325, relheight=0.05)
        self.parametro_intervalo_final.current(0)

            # 1.4 Varredura

        self.varredura_texto = Label(self.janelas_extras, text='Varredura :', bg='#F0F0F0', fg='#000000')
        self.varredura_texto.place(relx=0.07, rely=0.730, relwidth=0.32, relheight=0.03)

        self.varredura = ttk.Combobox(self.janelas_extras, values=["Automática", "Manual"])
        self.varredura.place(relx=0.07, rely=0.766, relwidth=0.855, relheight=0.05)
        self.varredura.current(self.n_varredura)

        # 2.0 Botão de Salvar

        self.botao_salvar_1 = tk.Button(self.janelas_extras, text='Salvar', bg='#F0F0F0', fg='#000000', command=self.varreduras_funcoes)
        self.botao_salvar_1.place(relx=0.14, rely=0.9, relwidth=0.34, relheight=0.045)

    def varreduras_funcoes(self):

        self.n_parametro_partida = self.parametro_partida.current()

        if self.n_parametro_partida == 1:
            self.v_partida[0] = self.inserir_partida.get()

        elif self.n_parametro_partida == 2:
            self.v_partida[1] = self.inserir_partida.get()

        elif self.n_parametro_partida == 3:
            self.v_partida[2] = self.inserir_partida.get()

        elif self.n_parametro_partida == 4:
            self.v_partida[3] = self.inserir_partida.get()

        self.n_parametro_intervalo_inicial = self.parametro_intervalo_inicial.current()

        if self.n_parametro_intervalo_inicial == 1:
            self.v_intervalo_inicial[0] = self.inserir_intervalo_inicial.get()

        elif self.n_parametro_intervalo_inicial == 2:
            self.v_intervalo_inicial[1] = self.inserir_intervalo_inicial.get()

        elif self.n_parametro_intervalo_inicial == 3:
            self.v_intervalo_inicial[2] = self.inserir_intervalo_inicial.get()

        elif self.n_parametro_intervalo_inicial == 4:
            self.v_intervalo_inicial[3] = self.inserir_intervalo_inicial.get()

        self.n_parametro_intervalo_final = self.parametro_intervalo_final.current()

        if self.n_parametro_intervalo_final == 1:
            self.v_intervalo_final[0] = self.inserir_intervalo_final.get()

        elif self.n_parametro_intervalo_final == 2:
            self.v_intervalo_final[1] = self.inserir_intervalo_final.get()

        elif self.n_parametro_intervalo_final == 3:
            self.v_intervalo_final[2] = self.inserir_intervalo_final.get()

        elif self.n_parametro_intervalo_final == 4:
            self.v_intervalo_final[3] = self.inserir_intervalo_final.get()

        self.n_varredura = self.varredura.current()

        self.janelas_extras.destroy()
        self.varreduras()

class programa(funcoes):

    # Inicialização e Variáveis
    def __init__(self):

        # 1.0 Variáveis

            # 1.1 Interface Principal

        self.coordenada_apurada_x = ''
        self.coordenada_apurada_y = ''

        self.ano_inicial_da_cidade = ''
        self.ano_final_da_cidade   = ''

        self.lista_procurar_1 = ['']
        self.lista_procurar_2 = ['']

        self.quadro_1_itens = []
        self.quadro_2_itens = [1440, 720, 600, 480, 360, 60, 30, 25, 20, 15, 10, 5]
        self.quadro_3_itens = [2, 5, 10, 25, 50, 75, 100]
        self.quadro_4_itens = []
        self.quadro_5_itens = []

        self.quadro_bdd_itens = []

        self.cidades_registradas = [
                                    ' ','Agua Branca', 'Aguiar', 'Alagoa Grande', 'Alagoa Nova', 'Alagoinha', 'Alcantil',               'Algodão de Jandaíra', 
                                    'Alhandra', 'Amparo', 'Aparecida', 'Arara', 'Araruna', 'Araçagi', 'Areia', 'Areia de Baraúnas',                  'Areial', 
                                    'Aroeiras', 'Assunção', 'Bananeiras', 'Baraúna', 'Barra de Santa Rosa', 'Barra de Santana',         'Barra de São Miguel', 
                                    'Bayeux', 'Baía da Traição', 'Belém', 'Belém do Brejo do Cruz', 'Bernardino Batista', 'Boa Ventura',          'Boa Vista', 
                                    'Bom Jesus', 'Bom Sucesso', 'Bonito de Santa Fé', 'Boqueirão/Açude Boqueirão', 'Borborema',               'Brejo do Cruz', 
                                    'Brejo dos Santos', 'Caaporã', 'Cabaceiras', 'Cabedelo', 'Cachoeira dos Índios',                       'Cacimba de Areia', 
                                    'Cacimba de Dentro', 'Cacimbas', 'Caiçara', 'Cajazeiras',                            'Cajazeiras/Açude Engenheiro Avidos', 
                                    'Cajazeiras/Açude Lagoa do Arroz', 'Cajazeirinhas', 'Caldas Brandão', 'Camalaú',                 'Campina Grande/EMBRAPA', 
                                    'Campina Grande/INSA', 'Campina Grande/São José da Mata',                          'Campina Grande/Sítio Açude de Dentro', 
                                    'Campo de Santana/Tacima', 'Capim', 'Caraúbas', 'Carrapateira', 'Casserengue/Sítio Salgado',                'Catingueira', 
                                    'Catolé do Rocha', 'Catolé do Rocha/Escola Técnica ', 'Caturité', 'Caturité/Fazenda Campo de Emas',           'Conceição', 
                                    'Condado', 'Conde', 'Conde/Açude Gramame Mamuaba', 'Congo', 'Coremas/Açude Coremas',                           'Coxixola', 
                                    'Cruz do Espírito Santo', 'Cubati', 'Cuitegi', 'Cuité', 'Cuité de Mamanguape', 'Curral Velho',           'Curral de Cima', 
                                    'Damião', 'Desterro', 'Diamante', 'Dona Inês', 'Duas Estradas', 'Emas', 'Esperança',               'Esperança/São Miguel', 
                                    'Fagundes', 'Frei Martinho', 'Gado Bravo', 'Guarabira', 'Gurinhém', 'Gurjão', 'Ibiara', 'Igaracy',            'Imaculada', 
                                    'Ingá', 'Itabaiana', 'Itaporanga', 'Itaporanga/Fazenda Veludo', 'Itapororoca', 'Itatuba', 'Jacaraú',             'Jericó', 
                                    'Joca Claudino/Santarém', 'João Pessoa/CEDRES', 'João Pessoa/DFAARA', 'João Pessoa/Mangabeira',       'João Pessoa/Mares', 
                                    'Juarez Távora', 'Juazeirinho', 'Junco do Seridó', 'Juripiranga', 'Juru', 'Lagoa', 'Lagoa Seca',        'Lagoa de Dentro', 
                                    'Lastro', 'Livramento', 'Logradouro', 'Lucena', 'Malta', 'Mamanguape', 'Mamanguape/ASPLAN', 'Manaíra',         'Marcação', 
                                    'Mari', 'Marizópolis', 'Massaranduba', 'Mataraca', 'Matinhas', 'Mato Grosso', 'Maturéia', 'Mogeiro',           'Montadas', 
                                    'Monte Horebe', 'Monteiro/EMBRAPA', 'Mulungu', 'Mãe D`Água', 'Natuba', 'Nazarezinho', 'Nova Floresta',      'Nova Olinda', 
                                    'Nova Palmeira', 'Olho D`Água', 'Olivedos', 'Ouro Velho', 'Parari', 'Passagem', 'Patos/EMBRAPA',               'Paulista', 
                                    'Pedra Branca', 'Pedra Lavrada', 'Pedras de Fogo', 'Pedro Régis', 'Piancó', 'Picuí', 'Pilar', 'Pilões',     'Pilõezinhos', 
                                    'Pirpirituba', 'Pitimbu', 'Pocinhos', 'Pombal', 'Poço Dantas', 'Poço de José de Moura', 'Prata',        'Princesa Isabel', 
                                    'Puxinanã', 'Queimadas', 'Quixaba', 'Remígio', 'Riacho de Santo Antônio',  'Riacho dos Cavalos/Jenipapeiro dos Carreiros', 
                                    'Riachão', 'Riachão do Bacamarte', 'Riachão do Poço', 'Rio Tinto', 'Salgadinho', 'Salgado de São Félix',  'Santa Cecília', 
                                    'Santa Cruz', 'Santa Helena', 'Santa Inês', 'Santa Luzia', 'Santa Luzia/Riacho do Saco', 'Santa Rita',  'Santa Teresinha', 
                                    'Santana de Mangueira', 'Santana dos Garrotes', 'Santo André', 'Sapé', 'Serra Branca', 'Serra Grande',    'Serra Redonda', 
                                    'Serra da Raiz', 'Serraria', 'Sertãozinho', 'Sobrado', 'Soledade', 'Soledade/Fazenda Pendência', 'Solânea',     'Sossêgo', 
                                    'Sousa', 'Sousa/São Gonçalo', 'Sumé', 'Sumé/UFCG', 'São Bentinho', 'São Bento', 'São Domingos',  'São Domingos do Cariri', 
                                    'São Francisco', 'São José da Lagoa Tapada', 'São José de Caiana', 'São José de Espinharas',       'São José de Piranhas', 
                                    'São José de Princesa', 'São José do Bonfim', 'São José do Brejo do Cruz', 'São José do Sabugi', 'São José dos Cordeiros', 
                                    'São José dos Ramos', 'São João do Cariri', 'São João do Rio do Peixe/Antenor Navarro', 'São João do Tigre', 'São Mamede', 
                                    'São Miguel de Taipu', 'São Sebastião de Lagoa de Roça', 'São Sebastião do Umbuzeiro',            'São Vicente do Seridó', 
                                    'São Vicente do Seridó/Seridó', 'Taperoá', 'Tavares', 'Teixeira', 'Tenório', 'Triunfo', 'Uiraúna',            'Umbuzeiro', 
                                    'Vieirópolis', 'Vista Serrana/Desterro de Malta', 'Várzea',                                                      'Zabelê'
                                   ]
        
        self.poscicao_da_lista = 0

        self.coeficientes_de_duracoes = [1.14, 0.85, 0.82, 0.78, 
                                         0.72, 0.42, 0.74, 0.91, 
                                         0.81, 0.70, 0.54, 0.34]
        
        self.n_duracao_de_coeficientes = 0

            # 1.2 Configurações

        self.n_coeficientes_de_desagregacao = 0
        self.n_porcentagem_de_aderencia = 1
        self.limiar_de_erro = 365
        self.n_melhor_modelagem = 1
        self.n_melhor_aderencia = 1
        self.n_melhor_otimizacao = 1
        self.n_quantidade_de_iteracoes = 0

            # 1.3 Varreduras

        self.v_partida = ['','','','']
        self.v_intervalo_inicial = ['','','','']
        self.v_intervalo_final = ['','','','']
        self.n_varredura = 0

            # 1.4 Relatórios

        self.dados_da_aba_1 = ['','','','', 
                               '','','','', 
                               '','','','']

        self.dados_da_aba_2 = ['','','','', 
                               '','','','', 
                               '','','','']

        self.relatorio_1_variaveis = ['','','','',
                                      '','','','',
                                      '','','','']

        self.relatorio_2_variaveis = ['','','','']

            # 1.5 Salvar

        self.tipo_dados_salvos = ''
        
        # 2.0 Funções

        self.root = root
        self.tela()
        self.frame_tela()
        self.menus()
        self.apps_da_pagina_1()
        root.mainloop()

    # Configurações da Tela
    def tela(self):
        self.root.title("D'Água")
        self.root.configure(background='#F0F0F0')
        self.root.geometry('750x500')
        self.root.resizable(False, False)
        self.root.maxsize(width=1920, height=1080)
        self.root.minsize(width=750, height=500)

        self.root.protocol("WM_DELETE_WINDOW", self.sair)

        self.conversao_de_icone(self.root)

    # Configurações do Frame da Tela
    def frame_tela(self):
        self.frame = Frame(self.root, bd=0.1, bg='#FFFFFF',
                           highlightbackground='#F0F0F0', highlightthickness=2)
        self.frame.place(relx=0.005, rely=0.01, relwidth=0.99, relheight=0.98)

    # Aplicativos da Página 1
    def apps_da_pagina_1(self):

        # Configurações de Abas

        self.abas = ttk.Notebook(self.frame)

        self.aba_1 = Frame(self.abas)
        self.aba_1.configure(background='#F0F0F0')
        self.abas.add(self.aba_1, text=" Equações do Mapa ")

        self.aba_2 = Frame(self.abas)
        self.aba_2.configure(background='#F0F0F0')
        self.abas.add(self.aba_2, text=" Equação das Chuvas ")

        self.aba_3 = Frame(self.abas)
        self.aba_3.configure(background='#F0F0F0')
        self.abas.add(self.aba_3, text=" Tratamento de Dados ")

        self.abas.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.aba_1_funcoes()
        self.aba_1_funcoes_destrutivas()
        self.aba_2_funcoes()
        self.aba_2_funcoes_destrutivas()
        self.aba_3_funcoes()
        self.aba_3_funcoes_destrutivas()

    # Widgets Estáticos da Aba 1 da Página 1
    def aba_1_funcoes(self):

        # 1.0 Fundo do Mapa da Paraíba

        self.fundo_da_paraiba = Label(self.aba_1, text='', relief="ridge", bg='#FFFFFF', fg='#800000')
        self.fundo_da_paraiba.place(relx=0.005, rely=0.01, relwidth=0.6435, relheight=0.795)

        # 1.1 Mapa da Paraíba

        self.paraiba_png = tk.PhotoImage(data=imagens_de_ferramenta('paraiba'))

        self.paraiba_tela = Button(self.aba_1, image=self.paraiba_png, bg='#FFFFFF', cursor="plus", fg='#F0F0F0', bd=0,
                                   command=self.direcionador)
        self.paraiba_tela.place(relx=0.008, rely=0.016, relwidth=0.638, relheight=0.785)

        # 1.2 Posição do Mouse

        self.latitude = Label(self.aba_1, text="", relief="sunken", bg='#FFFFFF', fg='#000000')
        self.latitude.place(relx=0.1, rely=0.885, relwidth=0.125, relheight=0.05)

        self.longitude = Label(self.aba_1, text="", relief="sunken", bg='#FFFFFF', fg='#000000')
        self.longitude.place(relx=0.34, rely=0.885, relwidth=0.125, relheight=0.05)

        def motion(event):
            global latitude_y, longitude_x

            self.latitude.destroy()
            self.longitude.destroy()

            latitude_y  = "%.3f" % float((+ 5 * 10**(-6) * event.y**2) - (0.0102 * event.y) - 5.5143)
            longitude_x = "%.3f" % float((- 4 * 10**(-7) * event.x**2) + (0.0088 * event.x) - 38.792)

            if float(longitude_x) > -34.795 or float(longitude_x) < -38.750 or float(latitude_y) > -5.990 or float(latitude_y) < -8.210:
                latitude_y  = ""
                longitude_x = ""

            self.latitude = Label(self.aba_1, text=str(latitude_y), relief="sunken", bg='#FFFFFF', fg='#000000')
            self.latitude.place(relx=0.1, rely=0.885, relwidth=0.125, relheight=0.05)

            self.longitude = Label(self.aba_1, text=str(longitude_x), relief="sunken", bg='#FFFFFF', fg='#000000')
            self.longitude.place(relx=0.34, rely=0.885, relwidth=0.125, relheight=0.05)

        self.paraiba_tela.bind('<Motion>', motion)

        # 2.0 Fundo das Informações do Estado

        self.fundo_da_paraiba = Label(self.aba_1, text='', relief="raised", bg='#F0F0F0', fg='#800000')
        self.fundo_da_paraiba.place(relx=0.655, rely=0.01, relwidth=0.3385, relheight=0.98)

        # 2.1 Seleção da Cidade

        self.cidade = Label(self.aba_1, text='Cidades :', bg='#F0F0F0', fg='#000000')
        self.cidade.place(relx=0.6625, rely=0.025, relwidth=0.0725, relheight=0.05)

        self.lista_de_cidades = ttk.Combobox(self.aba_1, values=self.cidades_registradas)
        self.lista_de_cidades.place(relx=0.74, rely=0.025, relwidth=0.242, relheight=0.05)
        self.lista_de_cidades.current(0)

        # 2.2 Parâmetros da Equação

        self.fundo_dos_parametros = Label(self.aba_1, text='', relief="groove", bg='#F0F0F0', fg='#800000')
        self.fundo_dos_parametros.place(relx=0.665, rely=0.105, relwidth=0.3185, relheight=0.245)

        self.parametros_da_equação_idf = Label(self.aba_1, text='Parâmetros da Equação I.D.F. :', bg='#F0F0F0',
                                               fg='#000000')
        self.parametros_da_equação_idf.place(relx=0.675, rely=0.08, relwidth=0.225, relheight=0.05)

        self.parametro_a_letra = Label(self.aba_1, text='a :', bg='#F0F0F0', fg='#000000')
        self.parametro_a_letra.place(relx=0.675, rely=0.165, relwidth=0.02, relheight=0.025)

        self.parametro_b_letra = Label(self.aba_1, text='b :', bg='#F0F0F0', fg='#000000')
        self.parametro_b_letra.place(relx=0.840, rely=0.165, relwidth=0.0225, relheight=0.025)

        self.parametro_c_letra = Label(self.aba_1, text='c :', bg='#F0F0F0', fg='#000000')
        self.parametro_c_letra.place(relx=0.675, rely=0.265, relwidth=0.02, relheight=0.025)

        self.parametro_d_letra = Label(self.aba_1, text='d :', bg='#F0F0F0', fg='#000000')
        self.parametro_d_letra.place(relx=0.840, rely=0.265, relwidth=0.0225, relheight=0.025)

        # 2.3 Coordenadas Selecionadas

        self.fundo_das_coordenadas_1 = Label(self.aba_1, text='', relief="groove", bg='#F0F0F0', fg='#800000')
        self.fundo_das_coordenadas_1.place(relx=0.665, rely=0.3790, relwidth=0.3185, relheight=0.165)

        self.coordenadas_selecionadas = Label(self.aba_1, text='Coordenadas Selecionadas :', bg='#F0F0F0',
                                              fg='#000000')
        self.coordenadas_selecionadas.place(relx=0.675, rely=0.3550, relwidth=0.21, relheight=0.05)

        self.latitude_numero_1 = Label(self.aba_1, text='Latitude :', bg='#F0F0F0', fg='#000000')
        self.latitude_numero_1.place(relx=0.675, rely=0.415, relwidth=0.065, relheight=0.035)

        self.longitude_numero_1 = Label(self.aba_1, text='Longitude :', bg='#F0F0F0', fg='#000000')
        self.longitude_numero_1.place(relx=0.845, rely=0.415, relwidth=0.0815, relheight=0.035)

        # 2.4 Anos do Cálculo

        self.fundo_dos_anos = Label(self.aba_1, text='', relief="groove", bg='#F0F0F0', fg='#800000')
        self.fundo_dos_anos.place(relx=0.665, rely=0.57, relwidth=0.3185, relheight=0.405)

        self.informacoes_adicionais = Label(self.aba_1, text='Informações Adicionais :', bg='#F0F0F0',
                                            fg='#000000')
        self.informacoes_adicionais.place(relx=0.675, rely=0.545, relwidth=0.19, relheight=0.05)

        self.ano_inicial_numero = Label(self.aba_1, text='Ano Inicial :', bg='#F0F0F0', fg='#000000')
        self.ano_inicial_numero.place(relx=0.675, rely=0.605, relwidth=0.086, relheight=0.035)

        self.ano_final_numero = Label(self.aba_1, text='Ano Final :', bg='#F0F0F0', fg='#000000')
        self.ano_final_numero.place(relx=0.845, rely=0.605, relwidth=0.0815, relheight=0.035)

        self.tipo_de_frequencia = Label(self.aba_1, text='Modelagem :', bg='#F0F0F0',
                                                          fg='#000000')
        self.tipo_de_frequencia.place(relx=0.675, rely=0.725, relwidth=0.095, relheight=0.035)

        self.qualidade_numero = Label(self.aba_1, text='Otimização :', bg='#F0F0F0', fg='#000000')
        self.qualidade_numero.place(relx=0.845, rely=0.725, relwidth=0.09, relheight=0.035)

        self.amostra_numero = Label(self.aba_1, text='Aderência :', bg='#F0F0F0', fg='#000000')
        self.amostra_numero.place(relx=0.675, rely=0.845, relwidth=0.08, relheight=0.035)

        self.metodo_numero = Label(self.aba_1, text='Amostra :', bg='#F0F0F0', fg='#000000')
        self.metodo_numero.place(relx=0.845, rely=0.845, relwidth=0.07, relheight=0.035)

        # 3.0 Fundo das Coordenadas do Mapa e Botões

        self.fundo_calculo_de_latlon = Label(self.aba_1, text='', relief="raised", bg='#F0F0F0', fg='#800000')
        self.fundo_calculo_de_latlon.place(relx=0.005, rely=0.815, relwidth=0.644, relheight=0.175)

        # 3.1 Coordenadas do Mapa

        self.fundo_das_coordenadas_2 = Label(self.aba_1, text='', relief="groove", bg='#F0F0F0', fg='#800000')
        self.fundo_das_coordenadas_2.place(relx=0.014, rely=0.84, relwidth=0.46, relheight=0.135)

        self.coordenadas_do_mapa = Label(self.aba_1, text='Coordenadas do Mapa :', bg='#F0F0F0',
                                         fg='#000000')
        self.coordenadas_do_mapa.place(relx=0.024, rely=0.82, relwidth=0.18, relheight=0.05)

        self.latitude_numero_2 = Label(self.aba_1, text='Latitude :', bg='#F0F0F0', fg='#000000')
        self.latitude_numero_2.place(relx=0.024, rely=0.89, relwidth=0.065, relheight=0.035)

        self.longitude_numero_2 = Label(self.aba_1, text='Longitude :', bg='#F0F0F0', fg='#000000')
        self.longitude_numero_2.place(relx=0.25, rely=0.89, relwidth=0.0815, relheight=0.035)

        # 3.2 Botões de Calcular e Interpolar

        self.botao_calcular_0 = tk.Button(self.aba_1, text='Calcular', bg='#F0F0F0', fg='#000000', command=self.idf_das_cidades_paraibanas)
        self.botao_calcular_0.place(relx=0.481, rely=0.840, relwidth=0.158, relheight=0.04)

        self.botao_interpolar = tk.Button(self.aba_1, text='Interpolar', bg='#F0F0F0', fg='#000000', command=self.idf_por_interpolacao_da_paraiba)
        self.botao_interpolar.place(relx=0.481, rely=0.88625, relwidth=0.158, relheight=0.04)

        self.botao_relatorio_1 = tk.Button(self.aba_1, text='Relatório', bg='#F0F0F0', fg='#000000', command=self.relatorio_1_1)
        self.botao_relatorio_1.place(relx=0.481, rely=0.9325, relwidth=0.158, relheight=0.04)

    # Widgets Dinâmicos da Aba 1 da Página 1
    def aba_1_funcoes_destrutivas(self):

            # 2.2 Parâmetros da Equação

        self.parametro_a = Label(self.aba_1, text=self.dados_da_aba_1[4], relief="sunken", bg='#FFFFFF', fg='#000000')
        self.parametro_a.place(relx=0.7, rely=0.155, relwidth=0.1, relheight=0.05)

        self.parametro_b = Label(self.aba_1, text=self.dados_da_aba_1[5], relief="sunken", bg='#FFFFFF', fg='#000000')
        self.parametro_b.place(relx=0.870, rely=0.155, relwidth=0.1, relheight=0.05)

        self.parametro_c = Label(self.aba_1, text=self.dados_da_aba_1[6], relief="sunken", bg='#FFFFFF', fg='#000000')
        self.parametro_c.place(relx=0.7, rely=0.255, relwidth=0.1, relheight=0.05)

        self.parametro_d = Label(self.aba_1, text=self.dados_da_aba_1[7], relief="sunken", bg='#FFFFFF', fg='#000000')
        self.parametro_d.place(relx=0.870, rely=0.255, relwidth=0.1, relheight=0.05)

            # 2.3 Coordenadas Selecionadas

        self.latitude_1 = Label(self.aba_1, text=self.coordenada_apurada_y, relief="sunken", bg='#FFFFFF', fg='#000000')
        self.latitude_1.place(relx=0.675, rely=0.455, relwidth=0.125, relheight=0.05)

        self.longitude_1 = Label(self.aba_1, text=self.coordenada_apurada_x, relief="sunken", bg='#FFFFFF',
                                 fg='#000000')
        self.longitude_1.place(relx=0.845, rely=0.455, relwidth=0.125, relheight=0.05)

            # 2.4 Anos do Cálculo

        self.ano_inicial = Label(self.aba_1, text=self.ano_inicial_da_cidade, relief="sunken", bg='#FFFFFF', fg='#000000')
        self.ano_inicial.place(relx=0.675, rely=0.645, relwidth=0.125, relheight=0.05)

        self.ano_final = Label(self.aba_1, text=self.ano_final_da_cidade, relief="sunken", bg='#FFFFFF', fg='#000000')
        self.ano_final.place(relx=0.845, rely=0.645, relwidth=0.125, relheight=0.05)

        self.tipo_de_frequencia_resposta = Label(self.aba_1, text=self.dados_da_aba_1[10], relief="sunken", bg='#FFFFFF', fg='#000000')
        self.tipo_de_frequencia_resposta.place(relx=0.675, rely=0.765, relwidth=0.125, relheight=0.05)

        self.qualidade_1 = Label(self.aba_1, text=self.dados_da_aba_1[11], relief="sunken", bg='#FFFFFF', fg='#000000')
        self.qualidade_1.place(relx=0.845, rely=0.765, relwidth=0.125, relheight=0.05)

        self.amostra_1 = Label(self.aba_1, text=self.dados_da_aba_1[2], relief="sunken", bg='#FFFFFF', fg='#000000')
        self.amostra_1.place(relx=0.675, rely=0.885, relwidth=0.125, relheight=0.05)

        self.metodo_1 = Label(self.aba_1, text=self.dados_da_aba_1[3], relief="sunken", bg='#FFFFFF', fg='#000000')
        self.metodo_1.place(relx=0.845, rely=0.885, relwidth=0.125, relheight=0.05)

            # 3.1 Coordenadas do Mapa

        self.latitude_2 = Label(self.aba_1, text=self.coordenada_apurada_y, relief="sunken", bg='#FFFFFF', fg='#000000')
        self.latitude_2.place(relx=0.1, rely=0.885, relwidth=0.125, relheight=0.05)

        self.longitude_2 = Label(self.aba_1, text=self.coordenada_apurada_x, relief="sunken", bg='#FFFFFF',
                                 fg='#000000')
        self.longitude_2.place(relx=0.34, rely=0.885, relwidth=0.125, relheight=0.05)

    # Widgets Estáticos da Aba 2 da Página 1
    def aba_2_funcoes(self):

        # 1.0 Fundo de Precipitações Máximas:

        self.fundo_do_quadro_1 = Label(self.aba_2, text='', relief="raised", bg='#F0F0F0', fg='#800000')
        self.fundo_do_quadro_1.place(relx=0.005, rely=0.01, relwidth=0.3645, relheight=0.98)

            # 1.1 Fundo de Precipitações Máximas

        self.fundo_de_precipitacoes_maximas = Label(self.aba_2, text='', relief="groove", bg='#F0F0F0', fg='#800000')
        self.fundo_de_precipitacoes_maximas.place(relx=0.015, rely=0.04, relwidth=0.3435, relheight=0.58)

        self.precipitacoes_maximas = Label(self.aba_2, text='Precipitações Máximas :', bg='#F0F0F0', fg='#000000')
        self.precipitacoes_maximas.place(relx=0.025, rely=0.02, relwidth=0.18, relheight=0.035)

            # 1.2 Tabela de Precipitações Máximas:

            # 1.3 Barras de Rolagem da Tabela de Precipitações Máximas

            # 1.4 Entrada de Nº's e Precipitações

        self.fundo_de_digitar_numero = Label(self.aba_2, text='', relief="groove", bg='#F0F0F0', fg='#800000')
        self.fundo_de_digitar_numero.place(relx=0.015, rely=0.645, relwidth=0.3435, relheight=0.325)

        self.insercao_de_informacoes = Label(self.aba_2, text='Inserção em Tabela :', bg='#F0F0F0',
                                             fg='#000000')
        self.insercao_de_informacoes.place(relx=0.025, rely=0.63, relwidth=0.165, relheight=0.0335)

        self.titulo_numero = Label(self.aba_2, text='Nº :', bg='#F0F0F0', fg='#000000')
        self.titulo_numero.place(relx=0.035, rely=0.675, relwidth=0.03, relheight=0.0335)

        self.digitar_numero = Entry(self.aba_2, text="")
        self.digitar_numero.place(relx=0.035, rely=0.72, relwidth=0.135, relheight=0.04)

        self.titulo_precipitacao = Label(self.aba_2, text='Precipitação :', bg='#F0F0F0', fg='#000000')
        self.titulo_precipitacao.place(relx=0.2, rely=0.675, relwidth=0.1, relheight=0.0335)

        self.digitar_precipitacao = Entry(self.aba_2, text="")
        self.digitar_precipitacao.place(relx=0.2, rely=0.72, relwidth=0.135, relheight=0.04)

        self.botao_procurar = tk.Button(self.aba_2, text='Procurar', bg='#F0F0F0', fg='#000000',
                                        command=self.procurar_arquivos_1)
        self.botao_procurar.place(relx=0.245, rely=0.8, relwidth=0.09, relheight=0.05)

        self.botao_inserir_1 = tk.Button(self.aba_2, text='Inserir', bg='#F0F0F0', fg='#000000',
                                         command=self.inserindo_1)
        self.botao_inserir_1.place(relx=0.035, rely=0.89, relwidth=0.09, relheight=0.05)

        self.botao_apagar_1 = tk.Button(self.aba_2, text='Apagar', bg='#F0F0F0', fg='#000000', command=self.apagando_1)
        self.botao_apagar_1.place(relx=0.14, rely=0.89, relwidth=0.09, relheight=0.05)

        self.botao_limpar = tk.Button(self.aba_2, text='Limpar', bg='#F0F0F0', fg='#000000', command=self.limpando_1)
        self.botao_limpar.place(relx=0.245, rely=0.89, relwidth=0.09, relheight=0.05)

        # 2.0 Fundo de Durações:

        self.fundo_do_quadro_2 = Label(self.aba_2, text='', relief="raised", bg='#F0F0F0', fg='#800000')
        self.fundo_do_quadro_2.place(relx=0.38, rely=0.01, relwidth=0.2135, relheight=0.98)

            # 2.1 Fundo de Durações:

        self.fundo_de_duracoes = Label(self.aba_2, text='', relief="groove", bg='#F0F0F0', fg='#800000')
        self.fundo_de_duracoes.place(relx=0.39, rely=0.04, relwidth=0.1925, relheight=0.58)

        self.duracoes = Label(self.aba_2, text='Durações :', bg='#F0F0F0', fg='#000000')
        self.duracoes.place(relx=0.4, rely=0.02, relwidth=0.0825, relheight=0.035)

            # 2.2 Fundo de Entrada de Durações

        self.fundo_de_digitar_numero_2 = Label(self.aba_2, text='', relief="groove", bg='#F0F0F0', fg='#800000')
        self.fundo_de_digitar_numero_2.place(relx=0.39, rely=0.645, relwidth=0.1925, relheight=0.325)

        self.insercao_de_duracoes = Label(self.aba_2, text='Inserção em Tabela :', bg='#F0F0F0', fg='#000000')
        self.insercao_de_duracoes.place(relx=0.4025, rely=0.63, relwidth=0.165, relheight=0.0335)

            # 2.3 Tipo de Cálculo de Durações

        # 3.0 Fundo de Tempos de Retorno:

        self.fundo_do_quadro_3 = Label(self.aba_2, text='', relief="raised", bg='#F0F0F0', fg='#800000')
        self.fundo_do_quadro_3.place(relx=0.605, rely=0.01, relwidth=0.2135, relheight=0.98)

            # 3.1 Fundo de Tempos de Retorno:

        self.fundo_de_tempo_de_retorno = Label(self.aba_2, text='', relief="groove", bg='#F0F0F0', fg='#800000')
        self.fundo_de_tempo_de_retorno.place(relx=0.615, rely=0.04, relwidth=0.1925, relheight=0.58)

        self.duracoes = Label(self.aba_2, text='Tempos de Retorno :', bg='#F0F0F0', fg='#000000')
        self.duracoes.place(relx=0.625, rely=0.02, relwidth=0.155, relheight=0.035)

            # 3.2 Quadro de Tempos de Retorno:

            # 3.3 Barra de Rolagem da Tabela de Tempo de Retorno

            # 3.4 Entrada de Anos

        self.fundo_de_digitar_numero_3 = Label(self.aba_2, text='', relief="groove", bg='#F0F0F0', fg='#800000')
        self.fundo_de_digitar_numero_3.place(relx=0.615, rely=0.645, relwidth=0.1925, relheight=0.325)

        self.insercao_de_anos = Label(self.aba_2, text='Incerção em Tabela :', bg='#F0F0F0', fg='#000000')
        self.insercao_de_anos.place(relx=0.6275, rely=0.63, relwidth=0.165, relheight=0.0335)

        self.titulo_anos = Label(self.aba_2, text='Ano :', bg='#F0F0F0', fg='#000000')
        self.titulo_anos.place(relx=0.675, rely=0.675, relwidth=0.07, relheight=0.0335)

        self.digitar_anos = Entry(self.aba_2, text="")
        self.digitar_anos.place(relx=0.643, rely=0.72, relwidth=0.135, relheight=0.04)

        self.botao_inserir_3 = tk.Button(self.aba_2, text='Inserir', bg='#F0F0F0', fg='#000000',
                                         command=self.inserindo_3)
        self.botao_inserir_3.place(relx=0.665, rely=0.8, relwidth=0.09, relheight=0.05)

        self.botao_apagar_3 = tk.Button(self.aba_2, text='Apagar', bg='#F0F0F0', fg='#000000', command=self.apagando_3)
        self.botao_apagar_3.place(relx=0.665, rely=0.89, relwidth=0.09, relheight=0.05)

        # 4.0 Fundo dos Resultados

        self.fundo_do_quadro_4 = Label(self.aba_2, text='', relief="raised", bg='#F0F0F0', fg='#800000')
        self.fundo_do_quadro_4.place(relx=0.83, rely=0.01, relwidth=0.1625, relheight=0.98)

            # 4.1 Parâmetros

        self.fundo_de_resultados = Label(self.aba_2, text='', relief="groove", bg='#F0F0F0', fg='#800000')
        self.fundo_de_resultados.place(relx=0.84, rely=0.04, relwidth=0.14, relheight=0.3)

        self.resultados = Label(self.aba_2, text='Parâmetros :', bg='#F0F0F0', fg='#000000')
        self.resultados.place(relx=0.85, rely=0.02, relwidth=0.1, relheight=0.035)

        self.parametro_a_letra_1 = Label(self.aba_2, text='a :', bg='#F0F0F0', fg='#000000')
        self.parametro_a_letra_1.place(relx=0.848, rely=0.0765, relwidth=0.02, relheight=0.025)

        self.parametro_b_letra_1 = Label(self.aba_2, text='b :', bg='#F0F0F0', fg='#000000')
        self.parametro_b_letra_1.place(relx=0.848, rely=0.1415, relwidth=0.02, relheight=0.025)

        self.parametro_c_letra_1 = Label(self.aba_2, text='c :', bg='#F0F0F0', fg='#000000')
        self.parametro_c_letra_1.place(relx=0.848, rely=0.2065, relwidth=0.02, relheight=0.025)

        self.parametro_d_letra_1 = Label(self.aba_2, text='d :', bg='#F0F0F0', fg='#000000')
        self.parametro_d_letra_1.place(relx=0.848, rely=0.2715, relwidth=0.02, relheight=0.025)

            # 4.2 Cálculo

        self.fundo_de_determinacao = Label(self.aba_2, text='', relief="groove", bg='#F0F0F0', fg='#800000')
        self.fundo_de_determinacao.place(relx=0.84, rely=0.36, relwidth=0.14, relheight=0.365)

        self.metodos_texto = Label(self.aba_2, text='Métodos :', bg='#F0F0F0', fg='#000000')
        self.metodos_texto.place(relx=0.85, rely=0.34, relwidth=0.08, relheight=0.035)

        self.funcao_densidade_probabilidade_titulo = Label(self.aba_2, text='Modelagem :', bg='#F0F0F0', fg='#000000')
        self.funcao_densidade_probabilidade_titulo.place(relx=0.84925, rely=0.38, relwidth=0.125, relheight=0.04)

        self.lista_de_funcoes_cumulativas_de_probabilidade = ["EXP", "GAM", "GUM", 
                                                              "GPA", "GVE", "KP4", 
                                                              "LN2", "LOG", "NOG", 
                                                              "PT3", "WEI"]
        self.funcao_densidade_probabilidade = ttk.Combobox(self.aba_2, values=self.lista_de_funcoes_cumulativas_de_probabilidade)
        self.funcao_densidade_probabilidade.place(relx=0.8495, rely=0.4250, relwidth=0.12, relheight=0.05)
        self.funcao_densidade_probabilidade.current(2)

        self.aderencia_titulo = Label(self.aba_2, text='Aderência :', bg='#F0F0F0', fg='#000000')
        self.aderencia_titulo.place(relx=0.84925, rely=0.49, relwidth=0.12, relheight=0.04)

        self.lista_de_aderencias = ["AD", "KS"]
        self.aderencia = ttk.Combobox(self.aba_2, values=self.lista_de_aderencias)
        self.aderencia.place(relx=0.8495, rely=0.535, relwidth=0.12, relheight=0.05)
        self.aderencia.current(1)

        self.otimizacao_titulo = Label(self.aba_2, text='Otimização :', bg='#F0F0F0', fg='#000000')
        self.otimizacao_titulo.place(relx=0.84925, rely=0.6, relwidth=0.12, relheight=0.04)

        self.lista_de_otimizacoes = ["DA", "DE", "COBYLA", "CG", "L-BFGS-B", "LM", "MMQ", "NM", "POWELL", "TNC"]
        self.otimizacao = ttk.Combobox(self.aba_2, values=self.lista_de_otimizacoes)
        self.otimizacao.place(relx=0.8495, rely=0.645, relwidth=0.12, relheight=0.05)
        self.otimizacao.current(6)

            # 4.3 Relatório e Cálculo

        self.fundo_de_relatorio_e_calculo = Label(self.aba_2, text='', relief="groove", bg='#F0F0F0', fg='#800000')
        self.fundo_de_relatorio_e_calculo.place(relx=0.84, rely=0.75, relwidth=0.14, relheight=0.22)

        self.botao_calcular_1 = tk.Button(self.aba_2, text='Calcular', bg='#F0F0F0', fg='#000000', command=self.idf_do_usuario)
        self.botao_calcular_1.place(relx=0.865, rely=0.8, relwidth=0.09, relheight=0.05)

        self.botao_relatorio_2 = tk.Button(self.aba_2, text='Relatório', bg='#F0F0F0', fg='#000000', command=self.relatorio_1_2)
        self.botao_relatorio_2.place(relx=0.865, rely=0.89, relwidth=0.09, relheight=0.05)

    # Widgets Dinâmicos da Aba 2 da Página 1
    def aba_2_funcoes_destrutivas(self):

        # 1.2 Tabela de Precipitações Máximas:

        self.quadro_1 = ttk.Treeview(self.aba_2, columns=('Nº', 'Precipitação'))

        self.quadro_1.column('#0', width=0, stretch=NO)
        self.quadro_1.column('Nº', anchor=CENTER, width=20)
        self.quadro_1.column('Precipitação', anchor=CENTER, width=80)

        self.quadro_1.heading('Nº', text='Nº', anchor=CENTER)
        self.quadro_1.heading('Precipitação', text='Precipitação', anchor=CENTER)

        self.quadro_1.place(relx=0.025, rely=0.0665, relwidth=0.3, relheight=0.535)

        # 1.3 Barras de Rolagem da Tabela de Precipitações Máximas

        self.y_scroll_1 = ttk.Scrollbar(self.aba_2, orient=tk.VERTICAL, command=self.quadro_1.yview)

        self.quadro_1['yscroll'] = self.y_scroll_1.set

        self.y_scroll_1.place(relx=0.325, rely=0.0665, relwidth=0.025, relheight=0.535)

        for i in range(len(self.quadro_1_itens)):
            self.quadro_1.insert(parent='', index=i, iid=i, text='',
                                 values=(self.quadro_1_itens[i][0], self.quadro_1_itens[i][1]))

        # 1.4 Entrada de Nº's e Precipitações

        self.lista_de_insercao_1 = ttk.Combobox(self.aba_2, values=self.lista_procurar_1)
        self.lista_de_insercao_1.place(relx=0.035, rely=0.8, relwidth=0.195, relheight=0.05)
        self.lista_de_insercao_1.current(len(self.lista_procurar_1) - 1)

        # 2.3 Tipo de Cálculo de Durações

        if self.n_coeficientes_de_desagregacao == 0:

                # 2.3.1 Tabela:

            self.quadro_2 = ttk.Treeview(self.aba_2, columns=('Durações'))

            self.quadro_2.column('#0', width=0, stretch=NO)
            self.quadro_2.column('Durações', anchor=CENTER, width=80)

            self.quadro_2.heading('Durações', text='Durações', anchor=CENTER)

            self.quadro_2.place(relx=0.4, rely=0.0665, relwidth=0.15, relheight=0.535)

                # 2.3.2 Barras de Rolagem da Tabela das Durações

            self.y_scroll_2 = ttk.Scrollbar(self.aba_2, orient=tk.VERTICAL, command=self.quadro_2.yview)

            self.quadro_2['yscroll'] = self.y_scroll_2.set

            self.y_scroll_2.place(relx=0.55, rely=0.0665, relwidth=0.025, relheight=0.535)

            self.quadro_2_itens.sort(reverse=True)

            for i in range(len(self.quadro_2_itens)):
                self.quadro_2.insert(parent='', index=i, iid=i, text='', values=(str(self.quadro_2_itens[i])))

                # 2.3.3 Entrada de Durações

            self.titulo_duracao = Label(self.aba_2, text='Duração :', bg='#F0F0F0', fg='#000000')
            self.titulo_duracao.place(relx=0.45, rely=0.675, relwidth=0.07, relheight=0.0335)

            self.digitar_duracao = Entry(self.aba_2, text="")
            self.digitar_duracao.place(relx=0.418, rely=0.72, relwidth=0.135, relheight=0.04)

            self.botao_inserir_2 = tk.Button(self.aba_2, text='Inserir', bg='#F0F0F0', fg='#000000',
                                            command=self.inserindo_2)
            self.botao_inserir_2.place(relx=0.44, rely=0.8, relwidth=0.09, relheight=0.05)

            self.botao_apagar_2 = tk.Button(self.aba_2, text='Apagar', bg='#F0F0F0', fg='#000000', command=self.apagando_2)
            self.botao_apagar_2.place(relx=0.44, rely=0.89, relwidth=0.09, relheight=0.05)

        elif self.n_coeficientes_de_desagregacao == 1:

            # 2.3.1 Diferentes Coeficientes de Duração:

            self.h24d01_texto = Label(self.aba_2, text='24h/01d', bg='#F0F0F0', fg='#000000')
            self.h24d01_texto.place(relx=0.3955, rely=0.0710, relwidth=0.07, relheight=0.025)
            self.h24d01 = Label(self.aba_2, text=self.coeficientes_de_duracoes[0], relief="sunken", bg='#FFFFFF', fg='#000000')
            self.h24d01.place(relx=0.4735, rely=0.0675, relwidth=0.1, relheight=0.04)

            self.h12h24_texto = Label(self.aba_2, text='12h/24h', bg='#F0F0F0', fg='#000000')
            self.h12h24_texto.place(relx=0.3955, rely=0.1162, relwidth=0.07, relheight=0.025)
            self.h12h24 = Label(self.aba_2, text=self.coeficientes_de_duracoes[1], relief="sunken", bg='#FFFFFF', fg='#000000')
            self.h12h24.place(relx=0.4735, rely=0.1127, relwidth=0.1, relheight=0.04)

            self.h10d24_texto = Label(self.aba_2, text='10h/24h', bg='#F0F0F0', fg='#000000')
            self.h10d24_texto.place(relx=0.3955, rely=0.1614, relwidth=0.07, relheight=0.025)
            self.h10h24 = Label(self.aba_2, text=self.coeficientes_de_duracoes[2], relief="sunken", bg='#FFFFFF', fg='#000000')
            self.h10h24.place(relx=0.4735, rely=0.1579, relwidth=0.1, relheight=0.04)

            self.h08h24_texto = Label(self.aba_2, text='08h/24h', bg='#F0F0F0', fg='#000000')
            self.h08h24_texto.place(relx=0.3955, rely=0.2066, relwidth=0.07, relheight=0.025)
            self.h08h24 = Label(self.aba_2, text=self.coeficientes_de_duracoes[3], relief="sunken", bg='#FFFFFF', fg='#000000')
            self.h08h24.place(relx=0.4735, rely=0.2031, relwidth=0.1, relheight=0.04)

            self.h06h24_texto = Label(self.aba_2, text='06h/24h', bg='#F0F0F0', fg='#000000')
            self.h06h24_texto.place(relx=0.3955, rely=0.2518, relwidth=0.07, relheight=0.025)
            self.h06h24 = Label(self.aba_2, text=self.coeficientes_de_duracoes[4], relief="sunken", bg='#FFFFFF', fg='#000000')
            self.h06h24.place(relx=0.4735, rely=0.2483, relwidth=0.1, relheight=0.04)

            self.h01h24_texto = Label(self.aba_2, text='01h/24h', bg='#F0F0F0', fg='#000000')
            self.h01h24_texto.place(relx=0.3955, rely=0.2970, relwidth=0.07, relheight=0.025)
            self.h01h24 = Label(self.aba_2, text=self.coeficientes_de_duracoes[5], relief="sunken", bg='#FFFFFF', fg='#000000')
            self.h01h24.place(relx=0.4735, rely=0.2935, relwidth=0.1, relheight=0.04)

            self.m30h01_texto = Label(self.aba_2, text='30m/01h', bg='#F0F0F0', fg='#000000')
            self.m30h01_texto.place(relx=0.3955, rely=0.3422, relwidth=0.07, relheight=0.025)
            self.m30h01 = Label(self.aba_2, text=self.coeficientes_de_duracoes[6], relief="sunken", bg='#FFFFFF', fg='#000000')
            self.m30h01.place(relx=0.4735, rely=0.3387, relwidth=0.1, relheight=0.04)

            self.m25m30_texto = Label(self.aba_2, text='25m/30m', bg='#F0F0F0', fg='#000000')
            self.m25m30_texto.place(relx=0.3955, rely=0.3874, relwidth=0.07, relheight=0.025)
            self.m25m30 = Label(self.aba_2, text=self.coeficientes_de_duracoes[7], relief="sunken", bg='#FFFFFF', fg='#000000')
            self.m25m30.place(relx=0.4735, rely=0.3839, relwidth=0.1, relheight=0.04)

            self.m20m30_texto = Label(self.aba_2, text='20m/30m', bg='#F0F0F0', fg='#000000')
            self.m20m30_texto.place(relx=0.3955, rely=0.4326, relwidth=0.07, relheight=0.025)
            self.m20m30 = Label(self.aba_2, text=self.coeficientes_de_duracoes[8], relief="sunken", bg='#FFFFFF', fg='#000000')
            self.m20m30.place(relx=0.4735, rely=0.4291, relwidth=0.1, relheight=0.04)

            self.m15m30_texto = Label(self.aba_2, text='15m/30m', bg='#F0F0F0', fg='#000000')
            self.m15m30_texto.place(relx=0.3955, rely=0.4778, relwidth=0.07, relheight=0.025)
            self.m15m30 = Label(self.aba_2, text=self.coeficientes_de_duracoes[9], relief="sunken", bg='#FFFFFF', fg='#000000')
            self.m15m30.place(relx=0.4735, rely=0.4743, relwidth=0.1, relheight=0.04)

            self.m10m30_texto = Label(self.aba_2, text='10m/30m', bg='#F0F0F0', fg='#000000')
            self.m10m30_texto.place(relx=0.3955, rely=0.5230, relwidth=0.07, relheight=0.025)
            self.m10m30 = Label(self.aba_2, text=self.coeficientes_de_duracoes[10], relief="sunken", bg='#FFFFFF', fg='#000000')
            self.m10m30.place(relx=0.4735, rely=0.5195, relwidth=0.1, relheight=0.04)

            self.m05m30_texto = Label(self.aba_2, text='05m/30m', bg='#F0F0F0', fg='#000000')
            self.m05m30_texto.place(relx=0.3955, rely=0.5682, relwidth=0.07, relheight=0.025)
            self.m05m30 = Label(self.aba_2, text=self.coeficientes_de_duracoes[11], relief="sunken", bg='#FFFFFF', fg='#000000')
            self.m05m30.place(relx=0.4735, rely=0.5647, relwidth=0.1, relheight=0.04)

            # 2.3.2 Entrada de Coeficientes

            self.titulo_coeficientes = Label(self.aba_2, text='Coeficientes :', bg='#F0F0F0', fg='#000000')
            self.titulo_coeficientes.place(relx=0.4325, rely=0.675, relwidth=0.1, relheight=0.0335)

            self.digitar_duracao = Entry(self.aba_2, text="")
            self.digitar_duracao.place(relx=0.418, rely=0.72, relwidth=0.135, relheight=0.04)

            self.duracao_de_coeficientes = ttk.Combobox(self.aba_2, values=["24h/01d", "12h/24h", "10h/24h", "08h/24h",
                                                                            "06h/24h", "01h/24h", "30m/01h", "25m/30m",
                                                                            "20m/30m", "15m/30m", "10m/30m", "05m/30m"])
            self.duracao_de_coeficientes.place(relx=0.418, rely=0.8, relwidth=0.135, relheight=0.05)
            self.duracao_de_coeficientes.current(self.n_duracao_de_coeficientes)

            self.botao_inserir_2 = tk.Button(self.aba_2, text='Inserir', bg='#F0F0F0', fg='#000000',
                                            command=self.inserindo_2)
            self.botao_inserir_2.place(relx=0.44, rely=0.89, relwidth=0.09, relheight=0.05)

        # 3.2 Quadro de Tempos de Retorno:

        self.quadro_3 = ttk.Treeview(self.aba_2, columns=('Anos'))

        self.quadro_3.column('#0', width=0, stretch=NO)
        self.quadro_3.column('Anos', anchor=CENTER, width=80)

        self.quadro_3.heading('Anos', text='Anos', anchor=CENTER)

        self.quadro_3.place(relx=0.625, rely=0.0665, relwidth=0.15, relheight=0.535)

        # 3.3 Barra de Rolagem da Tabela de Tempo de Retorno

        self.y_scroll_3 = ttk.Scrollbar(self.aba_2, orient=tk.VERTICAL, command=self.quadro_3.yview)

        self.quadro_3['yscroll'] = self.y_scroll_3.set

        self.y_scroll_3.place(relx=0.775, rely=0.0665, relwidth=0.025, relheight=0.535)

        self.quadro_3_itens.sort(reverse=True)

        for i in range(len(self.quadro_3_itens)):
            self.quadro_3.insert(parent='', index=i, iid=i, text='', values=(str(self.quadro_3_itens[i])))

        # 4.1 Parâmetros

        self.parametro_a_1 = Label(self.aba_2, text=self.dados_da_aba_2[4], relief="sunken", bg='#FFFFFF', fg='#000000')
        self.parametro_a_1.place(relx=0.87, rely=0.0665, relwidth=0.1, relheight=0.05)

        self.parametro_b_1 = Label(self.aba_2, text=self.dados_da_aba_2[5], relief="sunken", bg='#FFFFFF', fg='#000000')
        self.parametro_b_1.place(relx=0.87, rely=0.1315, relwidth=0.1, relheight=0.05)

        self.parametro_c_1 = Label(self.aba_2, text=self.dados_da_aba_2[6], relief="sunken", bg='#FFFFFF', fg='#000000')
        self.parametro_c_1.place(relx=0.87, rely=0.1965, relwidth=0.1, relheight=0.05)

        self.parametro_d_1 = Label(self.aba_2, text=self.dados_da_aba_2[7], relief="sunken", bg='#FFFFFF', fg='#000000')
        self.parametro_d_1.place(relx=0.87, rely=0.2615, relwidth=0.1, relheight=0.05)

        # 4.2 Cálculo

        self.funcao_densidade_probabilidade_otimizada = Label(self.aba_2, text='Otimizado', relief="sunken", bg='#FFFFFF', fg='#000000')

        if self.n_melhor_modelagem == 0:
            self.funcao_densidade_probabilidade_otimizada.place(relx=0.8495, rely=0.4250, relwidth=0.12, relheight=0.05)

        self.aderencia_otimizada = Label(self.aba_2, text='Otimizado', relief="sunken", bg='#FFFFFF', fg='#000000')

        if self.n_melhor_aderencia == 0:
            self.aderencia_otimizada.place(relx=0.8495, rely=0.535, relwidth=0.12, relheight=0.05)
        
        self.otimizacao_otimizada = Label(self.aba_2, text='Otimizado', relief="sunken", bg='#FFFFFF', fg='#000000')

        if self.n_melhor_otimizacao == 0:
            self.otimizacao_otimizada.place(relx=0.8495, rely=0.645, relwidth=0.12, relheight=0.05)

    # Widgets Estáticos da Aba 3 da Página 1
    def aba_3_funcoes(self):

        # 1.0 Fundo de Precipitações Máximas:

        self.fundo_do_quadro_4 = Label(self.aba_3, text='', relief="raised", bg='#F0F0F0', fg='#800000')
        self.fundo_do_quadro_4.place(relx=0.005, rely=0.01, relwidth=0.3645, relheight=0.63)

            # 1.1 Fundo de Precipitações Máximas:

        self.fundo_de_precipitacoes_maximas_1 = Label(self.aba_3, text='', relief="groove", bg='#F0F0F0', fg='#800000')
        self.fundo_de_precipitacoes_maximas_1.place(relx=0.015, rely=0.04, relwidth=0.3435, relheight=0.58)

        self.precipitacoes_maximas_1 = Label(self.aba_3, text='Precipitações Máximas :', bg='#F0F0F0', fg='#000000')
        self.precipitacoes_maximas_1.place(relx=0.025, rely=0.02, relwidth=0.18, relheight=0.035)

            # 1.2 Tabela de Precipitações Máximas:

            # 1.3 Barras de Rolagem da Tabela de Precipitações Máximas

        # 2.0 Fundo de Precipitações

        self.fundo_do_quadro_5 = Label(self.aba_3, text='', relief="raised", bg='#F0F0F0', fg='#800000')
        self.fundo_do_quadro_5.place(relx=0.38, rely=0.01, relwidth=0.6125, relheight=0.98)

            # 2.1 Fundo de Precipitações:

        self.fundo_de_precipitacoes = Label(self.aba_3, text='', relief="groove", bg='#F0F0F0', fg='#800000')
        self.fundo_de_precipitacoes.place(relx=0.39, rely=0.04, relwidth=0.59, relheight=0.455)

        self.precipitacoes = Label(self.aba_3, text='Precipitações :', bg='#F0F0F0', fg='#000000')
        self.precipitacoes.place(relx=0.40, rely=0.02, relwidth=0.11, relheight=0.035)

            # 2.2 Tabela de Precipitações:

            # 2.3 Fundo de dias de Precipitações:

        self.fundo_de_dias = Label(self.aba_3, text='', relief="groove", bg='#F0F0F0', fg='#800000')
        self.fundo_de_dias.place(relx=0.39, rely=0.52, relwidth=0.590, relheight=0.45)

        self.dias_preciptados = Label(self.aba_3, text='Dias Preciptados :', bg='#F0F0F0', fg='#000000')
        self.dias_preciptados.place(relx=0.40, rely=0.5, relwidth=0.1325, relheight=0.035)

            # 2.4 Dias de Precipitações:

        self.dia_1_letra = Label(self.aba_3, text='01 :', bg='#F0F0F0', fg='#000000')
        self.dia_1_letra.place(relx=0.4040, rely=0.545, relwidth=0.05, relheight=0.025)

        self.dia_1 = Entry(self.aba_3, text='')
        self.dia_1.place(relx=0.4040, rely=0.580, relwidth=0.04725, relheight=0.05)

        self.dia_2_letra = Label(self.aba_3, text='02 :', bg='#F0F0F0', fg='#000000')
        self.dia_2_letra.place(relx=0.4610, rely=0.545, relwidth=0.05, relheight=0.025)

        self.dia_2 = Entry(self.aba_3, text='')
        self.dia_2.place(relx=0.4610, rely=0.580, relwidth=0.04725, relheight=0.05)

        self.dia_3_letra = Label(self.aba_3, text='03 :', bg='#F0F0F0', fg='#000000')
        self.dia_3_letra.place(relx=0.5180, rely=0.545, relwidth=0.05, relheight=0.025)

        self.dia_3 = Entry(self.aba_3, text='')
        self.dia_3.place(relx=0.5180, rely=0.580, relwidth=0.04725, relheight=0.05)

        self.dia_4_letra = Label(self.aba_3, text='04 :', bg='#F0F0F0', fg='#000000')
        self.dia_4_letra.place(relx=0.5750, rely=0.545, relwidth=0.05, relheight=0.025)

        self.dia_4 = Entry(self.aba_3, text='')
        self.dia_4.place(relx=0.5750, rely=0.580, relwidth=0.04725, relheight=0.05)

        self.dia_5_letra = Label(self.aba_3, text='05 :', bg='#F0F0F0', fg='#000000')
        self.dia_5_letra.place(relx=0.6320, rely=0.545, relwidth=0.05, relheight=0.025)

        self.dia_5 = Entry(self.aba_3, text='')
        self.dia_5.place(relx=0.6320, rely=0.580, relwidth=0.04725, relheight=0.05)

        self.dia_6_letra = Label(self.aba_3, text='06 :', bg='#F0F0F0', fg='#000000')
        self.dia_6_letra.place(relx=0.6890, rely=0.545, relwidth=0.05, relheight=0.025)

        self.dia_6 = Entry(self.aba_3, text='')
        self.dia_6.place(relx=0.6890, rely=0.580, relwidth=0.04725, relheight=0.05)

        self.dia_7_letra = Label(self.aba_3, text='07 :', bg='#F0F0F0', fg='#000000')
        self.dia_7_letra.place(relx=0.7460, rely=0.545, relwidth=0.05, relheight=0.025)

        self.dia_7 = Entry(self.aba_3, text='')
        self.dia_7.place(relx=0.7460, rely=0.580, relwidth=0.04725, relheight=0.05)

        self.dia_8_letra = Label(self.aba_3, text='08 :', bg='#F0F0F0', fg='#000000')
        self.dia_8_letra.place(relx=0.8030, rely=0.545, relwidth=0.05, relheight=0.025)

        self.dia_8 = Entry(self.aba_3, text='')
        self.dia_8.place(relx=0.8030, rely=0.580, relwidth=0.04725, relheight=0.05)

        self.dia_9_letra = Label(self.aba_3, text='09 :', bg='#F0F0F0', fg='#000000')
        self.dia_9_letra.place(relx=0.8600, rely=0.545, relwidth=0.05, relheight=0.025)

        self.dia_9 = Entry(self.aba_3, text='')
        self.dia_9.place(relx=0.8600, rely=0.580, relwidth=0.04725, relheight=0.05)

        self.dia_10_letra = Label(self.aba_3, text='10 :', bg='#F0F0F0', fg='#000000')
        self.dia_10_letra.place(relx=0.9170, rely=0.545, relwidth=0.05, relheight=0.025)

        self.dia_10 = Entry(self.aba_3, text='')
        self.dia_10.place(relx=0.9170, rely=0.580, relwidth=0.04725, relheight=0.05)

        self.dia_11_letra = Label(self.aba_3, text='11 :', bg='#F0F0F0', fg='#000000')
        self.dia_11_letra.place(relx=0.4040, rely=0.645, relwidth=0.05, relheight=0.025)

        self.dia_11 = Entry(self.aba_3, text='')
        self.dia_11.place(relx=0.4040, rely=0.680, relwidth=0.04725, relheight=0.05)

        self.dia_12_letra = Label(self.aba_3, text='12 :', bg='#F0F0F0', fg='#000000')
        self.dia_12_letra.place(relx=0.4610, rely=0.645, relwidth=0.05, relheight=0.025)

        self.dia_12 = Entry(self.aba_3, text='')
        self.dia_12.place(relx=0.4610, rely=0.680, relwidth=0.04725, relheight=0.05)

        self.dia_13_letra = Label(self.aba_3, text='13 :', bg='#F0F0F0', fg='#000000')
        self.dia_13_letra.place(relx=0.5180, rely=0.645, relwidth=0.05, relheight=0.025)

        self.dia_13 = Entry(self.aba_3, text='')
        self.dia_13.place(relx=0.5180, rely=0.680, relwidth=0.04725, relheight=0.05)

        self.dia_14_letra = Label(self.aba_3, text='14 :', bg='#F0F0F0', fg='#000000')
        self.dia_14_letra.place(relx=0.5750, rely=0.645, relwidth=0.05, relheight=0.025)

        self.dia_14 = Entry(self.aba_3, text='')
        self.dia_14.place(relx=0.5750, rely=0.680, relwidth=0.04725, relheight=0.05)

        self.dia_15_letra = Label(self.aba_3, text='15 :', bg='#F0F0F0', fg='#000000')
        self.dia_15_letra.place(relx=0.6320, rely=0.645, relwidth=0.05, relheight=0.025)

        self.dia_15 = Entry(self.aba_3, text='')
        self.dia_15.place(relx=0.6320, rely=0.680, relwidth=0.04725, relheight=0.05)

        self.dia_16_letra = Label(self.aba_3, text='16 :', bg='#F0F0F0', fg='#000000')
        self.dia_16_letra.place(relx=0.6890, rely=0.645, relwidth=0.05, relheight=0.025)

        self.dia_16 = Entry(self.aba_3, text='')
        self.dia_16.place(relx=0.6890, rely=0.680, relwidth=0.04725, relheight=0.05)

        self.dia_17_letra = Label(self.aba_3, text='17 :', bg='#F0F0F0', fg='#000000')
        self.dia_17_letra.place(relx=0.7460, rely=0.645, relwidth=0.05, relheight=0.025)

        self.dia_17 = Entry(self.aba_3, text='')
        self.dia_17.place(relx=0.7460, rely=0.680, relwidth=0.04725, relheight=0.05)

        self.dia_18_letra = Label(self.aba_3, text='18 :', bg='#F0F0F0', fg='#000000')
        self.dia_18_letra.place(relx=0.8030, rely=0.645, relwidth=0.05, relheight=0.025)

        self.dia_18 = Entry(self.aba_3, text='')
        self.dia_18.place(relx=0.8030, rely=0.680, relwidth=0.04725, relheight=0.05)

        self.dia_19_letra = Label(self.aba_3, text='19 :', bg='#F0F0F0', fg='#000000')
        self.dia_19_letra.place(relx=0.8600, rely=0.645, relwidth=0.05, relheight=0.025)

        self.dia_19 = Entry(self.aba_3, text='')
        self.dia_19.place(relx=0.8600, rely=0.680, relwidth=0.04725, relheight=0.05)

        self.dia_20_letra = Label(self.aba_3, text='20 :', bg='#F0F0F0', fg='#000000')
        self.dia_20_letra.place(relx=0.9170, rely=0.645, relwidth=0.05, relheight=0.025)

        self.dia_20 = Entry(self.aba_3, text='')
        self.dia_20.place(relx=0.9170, rely=0.680, relwidth=0.04725, relheight=0.05)

        self.dia_21_letra = Label(self.aba_3, text='21 :', bg='#F0F0F0', fg='#000000')
        self.dia_21_letra.place(relx=0.4040, rely=0.745, relwidth=0.05, relheight=0.025)

        self.dia_21 = Entry(self.aba_3, text='')
        self.dia_21.place(relx=0.4040, rely=0.780, relwidth=0.04725, relheight=0.05)

        self.dia_22_letra = Label(self.aba_3, text='22 :', bg='#F0F0F0', fg='#000000')
        self.dia_22_letra.place(relx=0.4610, rely=0.745, relwidth=0.05, relheight=0.025)

        self.dia_22 = Entry(self.aba_3, text='')
        self.dia_22.place(relx=0.4610, rely=0.780, relwidth=0.04725, relheight=0.05)

        self.dia_23_letra = Label(self.aba_3, text='23 :', bg='#F0F0F0', fg='#000000')
        self.dia_23_letra.place(relx=0.5180, rely=0.745, relwidth=0.05, relheight=0.025)

        self.dia_23 = Entry(self.aba_3, text='')
        self.dia_23.place(relx=0.5180, rely=0.780, relwidth=0.04725, relheight=0.05)

        self.dia_24_letra = Label(self.aba_3, text='24 :', bg='#F0F0F0', fg='#000000')
        self.dia_24_letra.place(relx=0.5750, rely=0.745, relwidth=0.05, relheight=0.025)

        self.dia_24 = Entry(self.aba_3, text='')
        self.dia_24.place(relx=0.5750, rely=0.780, relwidth=0.04725, relheight=0.05)

        self.dia_25_letra = Label(self.aba_3, text='25 :', bg='#F0F0F0', fg='#000000')
        self.dia_25_letra.place(relx=0.6320, rely=0.745, relwidth=0.05, relheight=0.025)

        self.dia_25 = Entry(self.aba_3, text='')
        self.dia_25.place(relx=0.6320, rely=0.780, relwidth=0.04725, relheight=0.05)

        self.dia_26_letra = Label(self.aba_3, text='26 :', bg='#F0F0F0', fg='#000000')
        self.dia_26_letra.place(relx=0.6890, rely=0.745, relwidth=0.05, relheight=0.025)

        self.dia_26 = Entry(self.aba_3, text='')
        self.dia_26.place(relx=0.6890, rely=0.780, relwidth=0.04725, relheight=0.05)

        self.dia_27_letra = Label(self.aba_3, text='27 :', bg='#F0F0F0', fg='#000000')
        self.dia_27_letra.place(relx=0.7460, rely=0.745, relwidth=0.05, relheight=0.025)

        self.dia_27 = Entry(self.aba_3, text='')
        self.dia_27.place(relx=0.7460, rely=0.780, relwidth=0.04725, relheight=0.05)

        self.dia_28_letra = Label(self.aba_3, text='28 :', bg='#F0F0F0', fg='#000000')
        self.dia_28_letra.place(relx=0.8030, rely=0.745, relwidth=0.05, relheight=0.025)

        self.dia_28 = Entry(self.aba_3, text='')
        self.dia_28.place(relx=0.8030, rely=0.780, relwidth=0.04725, relheight=0.05)

        self.dia_29_letra = Label(self.aba_3, text='29 :', bg='#F0F0F0', fg='#000000')
        self.dia_29_letra.place(relx=0.8600, rely=0.745, relwidth=0.05, relheight=0.025)

        self.dia_29 = Entry(self.aba_3, text='')
        self.dia_29.place(relx=0.8600, rely=0.780, relwidth=0.04725, relheight=0.05)

        self.dia_30_letra = Label(self.aba_3, text='30 :', bg='#F0F0F0', fg='#000000')
        self.dia_30_letra.place(relx=0.9170, rely=0.745, relwidth=0.05, relheight=0.025)

        self.dia_30 = Entry(self.aba_3, text='')
        self.dia_30.place(relx=0.9170, rely=0.780, relwidth=0.04725, relheight=0.05)

        self.dia_31_letra = Label(self.aba_3, text='31 :', bg='#F0F0F0', fg='#000000')
        self.dia_31_letra.place(relx=0.4040, rely=0.845, relwidth=0.05, relheight=0.025)

        self.dia_31 = Entry(self.aba_3, text='')
        self.dia_31.place(relx=0.4040, rely=0.880, relwidth=0.04725, relheight=0.05)

            # 2.5 Anos e Meses Preciptados

        self.meses_1_letra = Label(self.aba_3, text='Mês :', bg='#F0F0F0', fg='#000000')
        self.meses_1_letra.place(relx=0.4925, rely=0.845, relwidth=0.05, relheight=0.025)

        self.meses_1 = Entry(self.aba_3, text='')
        self.meses_1.place(relx=0.4610, rely=0.880, relwidth=0.105, relheight=0.05)

        self.anos_1_letra = Label(self.aba_3, text='Ano :', bg='#F0F0F0', fg='#000000')
        self.anos_1_letra.place(relx=0.585, rely=0.845, relwidth=0.05, relheight=0.025)

        self.anos_1 = Entry(self.aba_3, text='')
        self.anos_1.place(relx=0.575, rely=0.880, relwidth=0.065, relheight=0.05)

            # 2.6 Botões de Dias de Precipitação

        self.botao_procurar_2 = tk.Button(self.aba_3, text='Procurar', bg='#F0F0F0', fg='#000000',
                                          command=self.procurar_arquivos_2)
        self.botao_procurar_2.place(relx=0.875, rely=0.880, relwidth=0.09, relheight=0.05)

        # 3.0 Fundo dos Botões de Operação

        self.fundo_do_quadro_6 = Label(self.aba_3, text='', relief="raised", bg='#F0F0F0', fg='#800000')
        self.fundo_do_quadro_6.place(relx=0.005, rely=0.655, relwidth=0.364, relheight=0.335)

            # 3.1 Fundo dos Botões de Operação

        self.fundo_de_operacao = Label(self.aba_3, text='', relief="groove", bg='#F0F0F0', fg='#800000')
        self.fundo_de_operacao.place(relx=0.015, rely=0.68, relwidth=0.343, relheight=0.29)

        self.operacao = Label(self.aba_3, text='Botões de Operação :', bg='#F0F0F0', fg='#000000')
        self.operacao.place(relx=0.025, rely=0.66, relwidth=0.16, relheight=0.035)

            # 3.2 Botões de Operação

        self.botao_exportar_1 = tk.Button(self.aba_3, text='Exportar', bg='#F0F0F0', fg='#000000',
                                          command=self.exportando)
        self.botao_exportar_1.place(relx=0.075, rely=0.72, relwidth=0.09, relheight=0.05)

        self.botao_inserir_4 = tk.Button(self.aba_3, text='Inserir', bg='#F0F0F0', fg='#000000',
                                         command=self.inserindo_4)
        self.botao_inserir_4.place(relx=0.21, rely=0.72, relwidth=0.09, relheight=0.05)

        self.botao_limpar_2 = tk.Button(self.aba_3, text='Limpar', bg='#F0F0F0', fg='#000000', command=self.limpando_2)
        self.botao_limpar_2.place(relx=0.21, rely=0.8, relwidth=0.09, relheight=0.05)

        self.botao_apagar_4 = tk.Button(self.aba_3, text='Apagar', bg='#F0F0F0', fg='#000000', command=self.apagando_4)
        self.botao_apagar_4.place(relx=0.075, rely=0.8, relwidth=0.09, relheight=0.05)

        self.botao_calcular_2 = tk.Button(self.aba_3, text='Calcular', bg='#F0F0F0', fg='#000000',
                                          command=self.calculando_2)
        self.botao_calcular_2.place(relx=0.075, rely=0.88, relwidth=0.09, relheight=0.05)

        self.botao_relatorio_3 = tk.Button(self.aba_3, text='Relatório', bg='#F0F0F0', fg='#000000', command=self.relatorio_2)
        self.botao_relatorio_3.place(relx=0.21, rely=0.88, relwidth=0.09, relheight=0.05)
        
    # Widgets Dinâmicos da Aba 3 da Página 1
    def aba_3_funcoes_destrutivas(self):

            # 1.2 Tabela de Precipitações Máximas:

        self.quadro_4 = ttk.Treeview(self.aba_3, columns=('Nº', 'Precipitação'))

        self.quadro_4.column('#0', width=0, stretch=NO)
        self.quadro_4.column('Nº', anchor=CENTER, width=20)
        self.quadro_4.column('Precipitação', anchor=CENTER, width=80)

        self.quadro_4.heading('Nº', text='Nº', anchor=CENTER)
        self.quadro_4.heading('Precipitação', text='Precipitação', anchor=CENTER)

        self.quadro_4.place(relx=0.025, rely=0.0665, relwidth=0.3, relheight=0.535)

            # 1.3 Barras de Rolagem da Tabela de Precipitações Máximas

        self.y_scroll_4 = ttk.Scrollbar(self.aba_3, orient=tk.VERTICAL, command=self.quadro_4.yview)

        self.quadro_4['yscroll'] = self.y_scroll_4.set

        self.y_scroll_4.place(relx=0.325, rely=0.0665, relwidth=0.025, relheight=0.535)

        self.quadro_4_itens.sort()

        for i in range(len(self.quadro_4_itens)):
            self.quadro_4.insert(parent='', index=i, iid=i, text='', values=(self.quadro_4_itens[i][0],
                                                                             self.quadro_4_itens[i][1]))

            # 2.2 Tabela de Precipitações:

        self.quadro_5 = ttk.Treeview(self.aba_3,
                                     columns=('Ano', 'Mês', 'Dia 01', 'Dia 02', 'Dia 03', 'Dia 04', 'Dia 05',
                                              'Dia 06', 'Dia 07', 'Dia 08', 'Dia 09', 'Dia 10', 'Dia 11',
                                              'Dia 12', 'Dia 13', 'Dia 14', 'Dia 15', 'Dia 16', 'Dia 17',
                                              'Dia 18', 'Dia 19', 'Dia 20', 'Dia 21', 'Dia 22', 'Dia 23',
                                              'Dia 24', 'Dia 25', 'Dia 26', 'Dia 27', 'Dia 28', 'Dia 29',
                                              'Dia 30', 'Dia 31'))

        self.quadro_5.column('#0', width=0, stretch=NO)
        self.quadro_5.column('Ano', anchor=CENTER, width=50)
        self.quadro_5.column('Mês', anchor=CENTER, width=100)
        self.quadro_5.column('Dia 01', anchor=CENTER, width=50)
        self.quadro_5.column('Dia 02', anchor=CENTER, width=50)
        self.quadro_5.column('Dia 03', anchor=CENTER, width=50)
        self.quadro_5.column('Dia 04', anchor=CENTER, width=50)
        self.quadro_5.column('Dia 05', anchor=CENTER, width=50)
        self.quadro_5.column('Dia 06', anchor=CENTER, width=50)
        self.quadro_5.column('Dia 07', anchor=CENTER, width=50)
        self.quadro_5.column('Dia 08', anchor=CENTER, width=50)
        self.quadro_5.column('Dia 09', anchor=CENTER, width=50)
        self.quadro_5.column('Dia 10', anchor=CENTER, width=50)
        self.quadro_5.column('Dia 11', anchor=CENTER, width=50)
        self.quadro_5.column('Dia 12', anchor=CENTER, width=50)
        self.quadro_5.column('Dia 13', anchor=CENTER, width=50)
        self.quadro_5.column('Dia 14', anchor=CENTER, width=50)
        self.quadro_5.column('Dia 15', anchor=CENTER, width=50)
        self.quadro_5.column('Dia 16', anchor=CENTER, width=50)
        self.quadro_5.column('Dia 17', anchor=CENTER, width=50)
        self.quadro_5.column('Dia 18', anchor=CENTER, width=50)
        self.quadro_5.column('Dia 19', anchor=CENTER, width=50)
        self.quadro_5.column('Dia 20', anchor=CENTER, width=50)
        self.quadro_5.column('Dia 21', anchor=CENTER, width=50)
        self.quadro_5.column('Dia 22', anchor=CENTER, width=50)
        self.quadro_5.column('Dia 23', anchor=CENTER, width=50)
        self.quadro_5.column('Dia 24', anchor=CENTER, width=50)
        self.quadro_5.column('Dia 25', anchor=CENTER, width=50)
        self.quadro_5.column('Dia 26', anchor=CENTER, width=50)
        self.quadro_5.column('Dia 27', anchor=CENTER, width=50)
        self.quadro_5.column('Dia 28', anchor=CENTER, width=50)
        self.quadro_5.column('Dia 29', anchor=CENTER, width=50)
        self.quadro_5.column('Dia 30', anchor=CENTER, width=50)
        self.quadro_5.column('Dia 31', anchor=CENTER, width=50)

        self.quadro_5.heading('Ano', text='Ano', anchor=CENTER)
        self.quadro_5.heading('Mês', text='Mês', anchor=CENTER)
        self.quadro_5.heading('Dia 01', text='Dia 01', anchor=CENTER)
        self.quadro_5.heading('Dia 02', text='Dia 02', anchor=CENTER)
        self.quadro_5.heading('Dia 03', text='Dia 03', anchor=CENTER)
        self.quadro_5.heading('Dia 04', text='Dia 04', anchor=CENTER)
        self.quadro_5.heading('Dia 05', text='Dia 05', anchor=CENTER)
        self.quadro_5.heading('Dia 06', text='Dia 06', anchor=CENTER)
        self.quadro_5.heading('Dia 07', text='Dia 07', anchor=CENTER)
        self.quadro_5.heading('Dia 08', text='Dia 08', anchor=CENTER)
        self.quadro_5.heading('Dia 09', text='Dia 09', anchor=CENTER)
        self.quadro_5.heading('Dia 10', text='Dia 10', anchor=CENTER)
        self.quadro_5.heading('Dia 11', text='Dia 11', anchor=CENTER)
        self.quadro_5.heading('Dia 12', text='Dia 12', anchor=CENTER)
        self.quadro_5.heading('Dia 13', text='Dia 13', anchor=CENTER)
        self.quadro_5.heading('Dia 14', text='Dia 14', anchor=CENTER)
        self.quadro_5.heading('Dia 15', text='Dia 15', anchor=CENTER)
        self.quadro_5.heading('Dia 16', text='Dia 16', anchor=CENTER)
        self.quadro_5.heading('Dia 17', text='Dia 17', anchor=CENTER)
        self.quadro_5.heading('Dia 18', text='Dia 18', anchor=CENTER)
        self.quadro_5.heading('Dia 19', text='Dia 19', anchor=CENTER)
        self.quadro_5.heading('Dia 20', text='Dia 20', anchor=CENTER)
        self.quadro_5.heading('Dia 21', text='Dia 21', anchor=CENTER)
        self.quadro_5.heading('Dia 22', text='Dia 22', anchor=CENTER)
        self.quadro_5.heading('Dia 23', text='Dia 23', anchor=CENTER)
        self.quadro_5.heading('Dia 24', text='Dia 24', anchor=CENTER)
        self.quadro_5.heading('Dia 25', text='Dia 25', anchor=CENTER)
        self.quadro_5.heading('Dia 26', text='Dia 26', anchor=CENTER)
        self.quadro_5.heading('Dia 27', text='Dia 27', anchor=CENTER)
        self.quadro_5.heading('Dia 28', text='Dia 28', anchor=CENTER)
        self.quadro_5.heading('Dia 29', text='Dia 29', anchor=CENTER)
        self.quadro_5.heading('Dia 30', text='Dia 30', anchor=CENTER)
        self.quadro_5.heading('Dia 31', text='Dia 31', anchor=CENTER)

        self.quadro_5.place(relx=0.4, rely=0.0665, relwidth=0.5461, relheight=0.38)

        self.y_scroll_5 = ttk.Scrollbar(self.aba_3, orient=tk.VERTICAL, command=self.quadro_5.yview)

        self.quadro_5['yscroll'] = self.y_scroll_5.set

        self.y_scroll_5.place(relx=0.946, rely=0.0665, relwidth=0.025, relheight=0.38)

        self.x_scroll_5 = ttk.Scrollbar(self.aba_3, orient=tk.HORIZONTAL, command=self.quadro_5.xview)

        self.quadro_5['xscroll'] = self.x_scroll_5.set

        self.x_scroll_5.place(relx=0.402, rely=0.445, relwidth=0.545, relheight=0.04)

        for i in range(len(self.quadro_5_itens)):
            self.quadro_5.insert(parent='', index=i, iid=i, text='', values=(
            self.quadro_5_itens[i][0],  self.quadro_5_itens[i][1],  self.quadro_5_itens[i][2],
            self.quadro_5_itens[i][3],  self.quadro_5_itens[i][4],  self.quadro_5_itens[i][5],
            self.quadro_5_itens[i][6],  self.quadro_5_itens[i][7],  self.quadro_5_itens[i][8],
            self.quadro_5_itens[i][9],  self.quadro_5_itens[i][10], self.quadro_5_itens[i][11],
            self.quadro_5_itens[i][12], self.quadro_5_itens[i][13], self.quadro_5_itens[i][14],
            self.quadro_5_itens[i][15], self.quadro_5_itens[i][16], self.quadro_5_itens[i][17],
            self.quadro_5_itens[i][18], self.quadro_5_itens[i][19], self.quadro_5_itens[i][20],
            self.quadro_5_itens[i][21], self.quadro_5_itens[i][22], self.quadro_5_itens[i][23],
            self.quadro_5_itens[i][24], self.quadro_5_itens[i][25], self.quadro_5_itens[i][26],
            self.quadro_5_itens[i][27], self.quadro_5_itens[i][28], self.quadro_5_itens[i][29],
            self.quadro_5_itens[i][30], self.quadro_5_itens[i][31], self.quadro_5_itens[i][32]))

            # 2.6 Botões de Dias de Precipitação

        self.lista_de_insercao_2 = ttk.Combobox(self.aba_3, values=self.lista_procurar_2)
        self.lista_de_insercao_2.place(relx=0.658, rely=0.880, relwidth=0.2, relheight=0.05)
        self.lista_de_insercao_2.current(len(self.lista_procurar_2) - 1)

programa()
