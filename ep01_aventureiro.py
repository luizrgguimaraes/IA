from random import *
import numpy as np
import math

#------------------------------------------------Entrada do Usuario
m = int(input("Digite a largura do mapa:"))
n = int(input("Digite a altura do mapa:"))
print ("\n")

#------------------------------------------------Constantes
_BARREIRA = 0
_AGUA = 3
_TERRA = 1
_MOVEDICA = 6

#------------------------------------------------Classes
class Estado:
    def __init__(self,x,y,estadoPai=None,movimento=None,nivel=0,mapa=None):
        self.x = x #posicao x
        self.y = y #posicao y
        mapa.calcDistancia(x,y)
        self.a = mapa.getCusto(x,y)+mapa.getH(x,y) #valor heuristica
        self.estadoPai = estadoPai
        self.nivel = nivel
        if estadoPai:
            self.acumulado = estadoPai.acumulado+self.a
            #self.mapa = estadoPai.mapa
        else:
            self.acumulado = self.a
        self.visitado = False
        
        

    def movimentar(self,movimento,mapa,nivel):
        x = self.x + (movimento.x)
        y = self.y + (movimento.y)
        #print("mov("+str(movimento.x)+","+str(movimento.y)+")")
        #validar fronteiras
        if x < 0 or x >=m or y < 0 or y >=n:
            #print("Invalido - Fronteiras")
            return None
        a = mapa.getCusto(x,y)+mapa.getH(x,y)
        
        #validar barreiras
        if mapa.getCusto(x,y)==_BARREIRA:
            #print("Invalido - Barreira")
            return None

        #verificar se já existe um caminho para este ponto com menor acumulo
        for ponto in fila:
            if ponto.x == x and ponto.y == y:
                if ponto.acumulado > self.acumulado+a:
                    fila[fila.index(ponto)]=self
                #print("Invalido - repetido")
                return None
        
        estado_temp = Estado(x,y,self,movimento,nivel,mapa)
        return estado_temp

    def imprimir(self,completo=False):
        saida="["+str(self.nivel)+"::("+str(self.x)+","+str(self.y)+")::"+str(self.a)+"/"+str(self.acumulado)+"::"+str(self.visitado)+"]"
        if self.estadoPai and completo:
            saida = self.estadoPai.imprimir(True)+" > "+saida
        return saida

    def igual(self,x,y):
        if self.x == x and self.y == y:
            return 1
        else:
            return 0
    
class Movimento:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def imprimir(self):
        return str(self.x)+str(self.y)

class Mapa:
    def __init__(self,m,n):
        self.m = m
        self.n = n
        #self.objetivo = None
        #self.objetivo = Estado(m-1,n-1,None,None,None,self)

        tipos = [_BARREIRA,_AGUA,_MOVEDICA,_TERRA]
        lista = []
        for i in range(m):
            for j in range(n):
                codPosicao = m*i+j
                if codPosicao==0 or codPosicao==m*n-1:
                    lista.append(_TERRA)
                else:
                    lista.append(tipos[randrange(0,4)])
                
                #distancia = math.sqrt(pow(m-1-i,2)+pow(n-1-j,2))
                #print("distancia("+str(i)+","+str(j)+")="+str(distancia))
                #lista.append(distancia)
        self.posicao = np.array(lista)
        self.posicao = self.posicao.reshape(m,n)
    
    def getCusto(self,x,y):
        return self.posicao[x,y]
        
    def calcDistancia(self,x,y):
        #print("calc("+str(x)+","+str(y)+")")
        catetox = pow(m-1-x,2)
        catetoy = pow(n-1-y,2)
        
        #print("catetos("+str(x)+","+str(y)+") = "+str(catetox)+","+str(catetoy))
        distancia = math.sqrt(catetox+catetoy)
        self.h = distancia
        #print("distancia("+str(x)+","+str(y)+")="+str(distancia))
        #return self.getCusto+distancia

    def getH(self,x,y):
        return self.h


def criterioClassificacao(e):
    return e.acumulado

def imprimirFila(nivel):
    s=""
    for a in fila:
        #if a.nivel  == nivel:
            s+=a.imprimir()
    print("Fila="+s)

def popFila(nivel):
    
    for a in fila:
        if a.nivel  == nivel and a.visitado == False:
            a.visitado = True
            return a
    return None

mapa = Mapa(m,n)



estadoInicial = Estado(0,0,None,None,0,mapa)


fila = []

#gerar movimentos possiveis
movimentosPossiveis = [
    Movimento(0,1)#norte
    ,Movimento(1,1)#nordeste
    ,Movimento(1,0)#leste
    ,Movimento(1,-1)#sudeste
    ,Movimento(0,-1)#sul
    ,Movimento(-1,-1)#sudoeste
    ,Movimento(-1,0)#oeste
    ,Movimento(-1,1)#noroeste
]

def busca(estado,mapa):
    
    print("---------------"+estado.imprimir(True))
    #print(mapa.posicao)
    for movimento in movimentosPossiveis:
        estado_temp = estado.movimentar(movimento,mapa,estado.nivel+1)
        if estado_temp == None:
            continue
        if estado_temp.igual(m-1,n-1):
            print("Resultado:"+estado_temp.imprimir(True))
            return estado_temp
        print(str(estado.x)+","+str(estado.y)+">>>"+str(movimento.x)+","+str(movimento.y)+"="+str(estado_temp.x)+","+str(estado_temp.y))
        #fila.insert(0,estado_temp)
        fila.append(estado_temp)
        fila.sort(key=criterioClassificacao)
        imprimirFila(estado.nivel+1)

    r = None    
    while r == None:
        estado=popFila(estado.nivel+1)
        if not(estado):
            return None
        r = busca(estado,mapa)    
    return r

print(mapa.posicao)
busca(estadoInicial,mapa)
print(mapa.posicao)

