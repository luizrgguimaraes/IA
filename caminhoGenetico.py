from random import random
from random import randrange
from random import shuffle
import random
import numpy as np
import math

#classe cidade
class Cidade:
    def __init__(self,id,nome,peso,tempo,valor):
        self.id = id
        self.nome = nome
        self.peso = peso
        self.tempo = tempo
        self.valor = valor
            
    def imprimir(self):
        return "("+str(self.id) + " - " + self.nome + " - "+str(self.peso)+"Kg - "+str(self.tempo)+"h - $"+str(self.valor)+")"

class Individuo:
    def __init__(self,caminho,qtdCidades,fit,origem,nivel):
        self.caminho = caminho
        self.qtd = qtdCidades #posicao no caminho da ultima cidade- vai de 0 a 12, abarcando as 13 cidades - +1 = qtd cidades
        self.fit = fit
        self.origem = origem
        self.nivel = nivel+1
    def imprimir(self):
        strcaminho = cidades[0].nome
        for i in range(self.qtd):
            strcaminho += " >>> "+ cidades[self.caminho[i]].nome
        strcaminho += " >>> " + cidades[0].nome
        print(strcaminho+"\n"+self.fit.imprimir()+"\n"+self.origem+str(self.nivel))
    def mutacao(self):
        for x in range(1):
            posicao1 = randrange(0,13)
            posicao2 = randrange(0,13)
            novoCaminho = list(self.caminho)
            temp = novoCaminho[posicao1]
            novoCaminho[posicao1] = novoCaminho[posicao2]
            novoCaminho[posicao2] = temp

        novaqtd = randrange(1,14)
        
        novofit = fitness(novoCaminho,novaqtd)
        if novofit:
            return Individuo(novoCaminho,novaqtd,novofit,self.origem+str(self.nivel)+"m",self.nivel)
        else:
            return None


class Fit:
    def __init__(self,qtdCidades,tempoTotal,custoTotal,valorTotal,pesoTotal):
        self.qtdCidades = qtdCidades
        self.tempoTotal = tempoTotal
        self.custoTotal = custoTotal
        self.valorTotal = valorTotal
        self.pesoTotal = pesoTotal   
        self.premio = self.valorTotal - self.custoTotal
        self.fit = self.premio + 1/self.qtdCidades
    def imprimir(self):
        return "("+str(self.qtdCidades)+" cidades por " + str(self.tempoTotal) +" horas com "+str(self.pesoTotal)+"Kg | Custo: R$ "+ str(self.custoTotal)+" | Faturamento: R$ "+ str(self.valorTotal) +" | Lucro: R$ " + str(self.premio)+")"
    
#lendo lista de cidades
cidades = []
file = open("C:\\Users\\luiz.rgguimaraes\\OneDrive\\SENAC8\\IA\\Aula 04 - Algoritmos Geneticos\\cidades.csv","r")
for line in file:
    props = line.split(",")
    cidades.append(Cidade(int(props[0]),props[1],int(props[2]),int(props[3]),int(props[4])))
file.close()

#lendo lista de transportes
listaModelo = [0,0,0,0,0,0,0,0,0,0,0,0,0,0
            ,0,0,0,0,0,0,0,0,0,0,0,0,0,0
            ,0,0,0,0,0,0,0,0,0,0,0,0,0,0
            ,0,0,0,0,0,0,0,0,0,0,0,0,0,0
            ,0,0,0,0,0,0,0,0,0,0,0,0,0,0
            ,0,0,0,0,0,0,0,0,0,0,0,0,0,0
            ,0,0,0,0,0,0,0,0,0,0,0,0,0,0
            ,0,0,0,0,0,0,0,0,0,0,0,0,0,0
            ,0,0,0,0,0,0,0,0,0,0,0,0,0,0
            ,0,0,0,0,0,0,0,0,0,0,0,0,0,0
            ,0,0,0,0,0,0,0,0,0,0,0,0,0,0
            ,0,0,0,0,0,0,0,0,0,0,0,0,0,0
            ,0,0,0,0,0,0,0,0,0,0,0,0,0,0
            ,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
temposTransportes = list(listaModelo)
custosTransportes = list(listaModelo)
file = open("C:\\Users\\luiz.rgguimaraes\\OneDrive\\SENAC8\\IA\\Aula 04 - Algoritmos Geneticos\\transporte.csv","r")
for line in file:
    props = line.split(",")
    #alocando custos na lista de tempos e custos de transportes
    index = int(props[0])*14+int(props[1])
    temposTransportes[index] = int(props[2])
    custosTransportes[index] = int(props[3])
    #alocando custos na inversa de tempos e custos de transportes
    index = int(props[1])*14+int(props[0])
    temposTransportes[index] = int(props[2])
    custosTransportes[index] = int(props[3])

#transformando lista de tempos e custos de transportes em arrays
temposTransportes = np.array(temposTransportes)
temposTransportes = temposTransportes.reshape(14,14)
custosTransportes = np.array(custosTransportes)
custosTransportes = custosTransportes.reshape(14,14)
file.close()

# for i in temposTransportes:
#     print(i)

# for i in custosTransportes:
#     print(i)


def printTransporte(x,y):
    origem = cidades[x].nome
    destino = cidades[y].nome
    return origem + ">>>" + destino + " = "+ str(temposTransportes[x,y])+"h" + " - $"+ str(custosTransportes[x,y])

def transporteValido(x,y):
    if temposTransportes[x,y] > 0:
        return True
    else:
        return False

# for x in range(14):
#     for y in range(14):
#         if transporteValido(x,y):
#             print(printTransporte(x,y))

#funcao para gerar um caminho aleatorio
def gerarCaminho():
    caminho = []
    for x in range(13):
        caminho.append(x+1)
    random.shuffle(caminho)
    return caminho


def fitness(caminho,qtd):
    tempoTotal = temposTransportes[0,caminho[0]]#primeira viagem
    custoTotal = custosTransportes[0,caminho[0]]#primeira viagem
    for i in range(qtd-1):
        tempoTotal += temposTransportes[caminho[i],caminho[i+1]]
        custoTotal += custosTransportes[caminho[i],caminho[i+1]]
    tempoTotal += temposTransportes[caminho[qtd-1],0]#ultima viagem
    custoTotal += custosTransportes[caminho[qtd-1],0]#ultima viagem

    valorTotal = 0
    pesoTotal = 0
    for i in range(qtd):
        valorTotal+=cidades[caminho[i]].valor
        pesoTotal+=cidades[caminho[i]].peso
        tempoTotal+=cidades[caminho[i]].tempo

    if tempoTotal > 72:
        return None
    if pesoTotal > 20:
        return None

    fit = Fit(qtd,tempoTotal,custoTotal,valorTotal,pesoTotal)
    return fit

def crossover(individuo1,individuo2):
    caminho = list(individuo1.caminho) + list(individuo2.caminho)
    # print(individuo1.caminho)
    # print(individuo2.caminho)
    # print(caminho)
    i1 = 0
    alt = 0
    while len(caminho)>13:
        if alt == 0:
            caminho.pop(i1)
            alt = 1
        else:
            i2 = caminho[(i1+1):].index(caminho[i1])
            caminho.pop(i1+1+i2)
            alt = 0
            i1 += 1

    qtd = randrange(1,14)
    
    # print(caminho)
    # print(qtd)
    # input()
    
    fit = fitness(caminho,qtd)
    if fit: 
        return Individuo(caminho,qtd,fit,"c",individuo1.nivel)
    else:
        return None
    


def criterioClassificacao(e):
    return e.fit.fit

def imprimirPopulacao(populacao,max = 10):
    i = 0
    for individuo in populacao:
        print("Indivíduo "+str(i+1)+":")
        individuo.imprimir()
        i+=1
        if i >= max:
            break
#-----------------------------SCRIPT---------------------------------------------------------        

_MAX_TENTATIVAS = 100000
_MAX_VEZES_FIT_IGUAL = 1000
    



#gerar populacao inicial com 10 individuos
def executar(melhor_Resultado_geral):
    populacao = []
    while len(populacao) < 10:
        caminho = gerarCaminho()
        qtdCidades = randrange(1,14)
        fit = fitness(caminho,qtdCidades)
        if fit:
            populacao.append(Individuo(caminho,qtdCidades,fit,"g",0))

    populacao.sort(key=criterioClassificacao,reverse=True)
    # print("---------------POPULACAO INICIAL")
    # imprimirPopulacao(populacao)


    #mutar 0s 10 primeiro individuos da populacao
    ntentativa = 0
    fit_anterior = 0
    qtdvezes_fit_igual = 0
    while ntentativa < _MAX_TENTATIVAS:
        ntentativa += 1
        # c = input("continue(c) or quit(q)")
        # if c == "q":
        #     break

        # print("---------------MUTACOES")
        mutacoes = []
        i=0
        while len(mutacoes) < 10:
            mutacao = populacao[i].mutacao()
            if mutacao:
                mutacoes.append(mutacao)
                i += 1
        # mutacoes.sort(key=criterioClassificacao,reverse=True)
        # imprimirPopulacao(mutacoes)
        populacao += mutacoes

        # print("---------------CROSSOVER")
        listacross = []
        i=0
        while i < (20-1):
            cross = crossover(populacao[i],populacao[i+1])
            if cross:
                listacross.append(cross)
                cross = crossover(populacao[i+1],populacao[i])
                if cross:
                    listacross.append(cross)
                    i += 1
                i += 1
                    
        populacao += listacross

        populacao.sort(key=criterioClassificacao,reverse=True)

        populacao = list(populacao[0:10])
        # imprimirPopulacao(populacao)

        fit_atual = populacao[0].fit.fit
        if fit_atual == fit_anterior:
            qtdvezes_fit_igual += 1
        else:
            qtdvezes_fit_igual = 0
        fit_anterior = fit_atual
        
        if qtdvezes_fit_igual >= _MAX_VEZES_FIT_IGUAL and populacao[0].fit.premio > melhor_Resultado_geral:
            break

        # print(fit_atual)
    populacao[0].imprimir()
    return [ntentativa,populacao[0].fit.premio,populacao[0].qtd,populacao[0].caminho,populacao[0].origem]
    # print("ITERACAO "+str(ntentativa))
    # imprimirPopulacao(populacao,1)

melhor_Resultado_geral = 0
while True:
    resultado = executar(melhor_Resultado_geral)
    if resultado[1] > melhor_Resultado_geral:
        melhor_Resultado_geral = resultado[1]
    print(resultado)
    user = input("Quit (q) or ENTER")
    if user == "q":
        break
    print("\n\n")

# fit = fitness([8],1)
# individuo = Individuo([8],1,fit)
# individuo.imprimir()