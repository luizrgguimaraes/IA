from random import *
import numpy as np

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
    def __init__(self,x,y,estadoPai=None,movimento=None,nivel=0):
        self.x = x #posicao x
        self.y = y #posicao y
        self.custo = 0 #valor custo
        self.a = mapa.calcular(x,y) #valor heuristica
        self.estadoPai = estadoPai
        self.nivel = nivel
        

    def movimentar(self,movimento,mapa,nivel):
        x = self.x + (movimento.x)
        y = self.y + (movimento.y)
        a = mapa.calcular(x,y)
        c = mapa.getCusto(x,y)
        print("movimento("+str(movimento.x)+","+str(movimento.y)+")>("+str(self.x)+","+str(self.y)+")="+str(c))
        #validar fronteiras
        if x < 0 or x >=m or y < 0 or y >=n:
            print("Invalido - Fronteiras")
            return None

        #validar barreiras
        if mapa.getCusto(x,y)==_BARREIRA:
            print("Invalido - Barreira")
            return None
        
        estado_temp = Estado(x,y,self,movimento,nivel)
        return estado_temp

    def imprimir(self):
        saida = "("+str(self.x)+","+str(self.y)+")="+str(self.a)
        if(self.estadoPai):
            saida = self.estadoPai.imprimir()+" > "+saida
        return saida

    def igual(self,estado):
        if self.x == estado.x and self.y == estado.y:
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
        tipos = [_BARREIRA,_AGUA,_MOVEDICA,_TERRA]
        lista = []
        for i in range(m):
            for j in range(n):
                codPosicao = m*i+j
                if codPosicao==0 or codPosicao==m*n-1:
                    lista.append(_TERRA)
                else:
                    lista.append(tipos[randrange(1,3)])
        self.posicao = np.array(lista)
        self.posicao = self.posicao.reshape(m,n)
        print(self.posicao)

    def getCusto(self,x,y):
        return self.posicao[x,y]
    
    def calcular(self,x,y):
        #print(str(x)+","+str(y))
        return self.posicao[x,y]

def criterioClassificacao(e):
    return e.a

def imprimirFila(nivel):
    s=""
    for a in fila:
        if a.nivel  == nivel:
            s+="(n"+str(a.nivel)+" - "+str(a.x)+","+str(a.y)+")"
    print("Fila="+s)

mapa = Mapa(m,n)

estadoInicial = Estado(0,0)

estadoObjetivo = Estado(m-1,n-1)


estadosGerados = [estadoInicial]

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

def busca(estado):
    for movimento in movimentosPossiveis:
        estado_temp = estado.movimentar(movimento,mapa,estado.nivel+1)
        if estado_temp == None:
            continue
        if estado_temp.igual(estadoObjetivo):
            print(estado_temp.imprimir())
            return estado_temp

        fila.append(estado_temp)
        fila.sort(reverse=True,key=criterioClassificacao)
        imprimirFila(estado.nivel+1)

    if not(fila):
        return None
    return busca(fila.pop(0))

busca(estadoInicial)
        

