##########################################################################################################################
# Olá meninas.

# Este é o código que falei, das bombinhas. Resolvi colocá-lo aqui porque ele possui uma funcionalidade que será muito útil no seu projeto: como fazer gráficos que se atualizam automaticamente, utilizam o tempo atual em um dos eixos e os ajusta automaticamente para mantê-lo legível e organizado.

# Novamente, todos os comentários possuem um "comentário" no início, então vocês podem dar um CTRL+F para navegar entre eles facilmente. 

# Abraços.
# Augusto.
##########################################################################################################################

import serial #Comentário Biblioteca de comunicação serial entre o arduino e o RPi
import re #Comentário para a separção das strings
from datetime import datetime
from time import sleep
import matplotlib
from matplotlib.dates import date2num, DateFormatter
from PIL import ImageTk
import numpy as np
matplotlib.use('TkAgg') #Comentário Backend utilizado. importante caso formos utilizar a RPi no modo headless (sem monitor) ou não.
import matplotlib.pyplot as plt
import pandas as pd

esv=[] #comentário listas para segurar os valores da variável tempo de enchimento
enc=[]
esv_t=[] #comentário listas para segurar o horário de cada medida;
enc_t=[]
plt.ion() #comentário coloca o plot do matplotlib como interativo. importante caso queiram qua o gráfico atualize automaticamente, mas não é o nosso caso (na interface, o gráfico do parâmetro fica na tela até o usuário apertar o "x" e sair)
plt.show()# comentário exibe o gráfico
def sort(): #define uma função customizada "sort"
    if line[0]=='C': #comentário se o primeiro termo for um "C", de 'enChimento':
        dt = datetime.now()#.strftime("%d-%m-%Y, %H:%M:%S") #comentário define dt como a tomada do tempo atual
        #ts = datetime.timestamp(dt)
        #date_time = datetime.fromtimestamp(ts)
        #str_date_time = date_time.strftime("%d-%m-%Y, %H:%M:%S")
        #str_date_time = pd.to_datetime(str_date_time)
        num = pd.to_numeric(line[1]) #comentário converte o valor para numérico. O código dá erro caso não faça isso.
        enc.append(num) #Comentário insere o tempo de enchimento na lista enc
        enc_t.append(dt) #comentário insere o horário em que a medida foi tomada na lista enc_t
        dt = dt.strftime("%d/%m/%Y %H:%M:%S") #Comentário Converte a data para uma string no formato dia/mes/ano hora/minuto/segundo. SÓ FAÇA ISSO DEPOIS QUE A DATA ESTEJA NA LISTA ENC_T, PORQUE VOCÊ ESTARÁ INSERINDO UMA STRING E O SISTEMA NÃO SABE QUAL É MAIOR QUE QUAL.
        file_object = open("Tempos_de_Enchimento.txt", 'a') #Comentário: cria um arquivo para salvar os dados ou abre um arquivo existente no modo "append";
        file_object.write(dt)#comentário escreve a data no formato string
        file_object.write(", ") #comentário separa por vírgula
        file_object.write(line[1])#comentário escreve o tempo de enchimento
        file_object.write("\n")#comentário começa uma nova linha
        file_object.close() #comentário fecha o arquivo
        print(enc) #comentário escrewve os resultados. Esta linha só está aqui para verificar qual o formato das saídas. Podem tirar se quiserem (comentem com #)
        print(enc_t)#comentário idem à de cima
    elif line[0]=='V': #comentário Mesma coisa do que a de enchimento, mas esta é para esVaziamento. A estutura é a mesma.
        dt = datetime.now()#.strftime("%d-%m-%Y, %H:%M:%S")
        #ts = datetime.timestamp(dt)
        #date_time = datetime.fromtimestamp(ts)
        #str_date_time = date_time.strftime("%d-%m-%Y, %H:%M:%S")
        #str_date_time = pd.to_datetime(str_date_time)
        num = pd.to_numeric(line[1])
        esv.append(num)
        esv_t.append(dt)
        dt = dt.strftime("%d/%m/%Y %H:%M:%S")
        file_object1 = open("Tempos_de_Esvaziamento.txt", 'a')
        file_object1.write(dt)
        file_object1.write(", ")
        file_object1.write(line[1])
        file_object1.write("\n")
        file_object1.close()
        print(esv)
        print(esv_t)


if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1) #comentário Define os parâmetros de comunicação serial. ttyACM0 é a porta USB. 
    ser.reset_input_buffer() #comentário limpa dados que possam estar "entupindo" a entrada
    while True:  #comentário cria um loop infinito.
        if ser.in_waiting > 0:#comentário caso haja entrada de dados pelo port serial
            line = ser.readline().decode('utf-8').rstrip() #comentário cria uma variável "line" e salva nela o que está escrito na entrada de dados.
            line = re.split('(\d+)', line) #Comentário "Quebra" a string, serparando os números das letras (útil para extrair o valor enviado) 
            #print(line)
            sort() #Comentário  Chama a função sort(), definida anteriormente
            ax= plt.subplot()
            plt.plot(esv_t, esv, color='red', label="Tempo de Esvaziamento") #Comentário Plot da curva de esvaziamento
            plt.plot(enc_t, enc, color='blue',label="Tempo de Enchimento") #Comentário  Plot da curva de enchimento
            plt.xlabel("Data e Hora") #Comentário Título do eixo x: data e Hora 
            plt.ylabel("Tempo(ms)") #Comentário Título do eixo y: Tempo(ms)
            handles, labels = plt.gca().get_legend_handles_labels() #Comentário  Configuração para que a legenda não se repita a cada iteração
            by_label = dict(zip(labels, handles)) #Comentário  Configuração para que a legenda não se repita a cada iteração
            plt.legend(by_label.values(), by_label.keys())  #Comentário Exibe a legenda
            ax.xaxis.set_major_formatter(DateFormatter('%d/%m/%Y %H:%M')) #Comentário Define o formato da data e hora no eixo
            plt.setp(ax.get_xticklabels(), rotation=30, ha='right') #Comentário Organiza os elementos do eixo x para que eles não se sobreponham
            # plt.legend()
            plt.pause(5)

