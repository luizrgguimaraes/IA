from random import randrange
import numpy as np
import math

#------------------------------------------------Constantes
_BARREIRA = 0
_AGUA = 3
_TERRA = 1
_MOVEDICA = 6
_VISITADO = 10
_ESCOLHIDO = 11
_ATUAL = 12
_ERRADO = 13
_SUCESSO = 14
#------------------------------------------------Entrada do Usuario
m = int(input("Digite a largura do mapa:"))
n = int(input("Digite a altura do mapa:"))
fixa = int(input("Mapa Fixo(1) ou Aleatorio(0):"))
# if fixa == 1:
#     listafixa = []
#     print("BARREIRA(0)   TERRA(1)    AGUA(3)     AREIA MOVEDICA(6)")
#     for i in range(m):
#         for j in range(n):
#             codPosicao = m*i+j
#             if codPosicao==0 or codPosicao==m*n-1:
#                 listafixa.append(_TERRA)
#             else:
#                 custo = int(input("Digite o elemento "+str(codPosicao+1)+"/"+str(m*n)+":"))
                # listafixa.append(custo)
intermitente = int(input("Processamento Intermitente(1) ou Continuo(0):"))

print ("\n")



#------------------------------------------------Classes
class Estado:
    def __init__(self,x,y,estadoPai=None,nivel=0,mapa=None):
        self.x = x #posicao x
        self.y = y #posicao y
        
        self.c = mapa.getCusto(x,y)
        self.d = mapa.calcDistancia(x,y)
        self.a = self.c + self.d #valor heuristica

        self.estadoPai = estadoPai
        self.nivel = nivel
        self.status = _VISITADO
        self.acumulado = self.a

        if estadoPai:
            self.acumulado += estadoPai.acumulado

    def movimentar(self,movimento,mapa,nivel):
        x = self.x + (movimento.x)
        y = self.y + (movimento.y)

        print("TENTATIVA MOVIMENTO: "+movimento.imprimir()+"=("+str(x)+","+str(y)+")")
        if x < 0 or x >=m or y < 0 or y >=n:
            print("Invalido - Fronteiras")
            return None

        if mapa.getCusto(x,y)==_BARREIRA:
            print("Invalido - Barreira")
            return None

        a = mapa.getCusto(x,y)+mapa.getH(x,y)
        #verificar se já existe um caminho para este ponto com menor acumulo
        repetido = getFila(x,y)
        if repetido:
            print("repetido")
            if repetido.acumulado >= (self.acumulado + a):
                print("substituiu")
                fila[fila.index(repetido)]=self
            else:
                print("Invalido - repetido e tem maior ou igual acumulo:")
                return None
        
        estado_temp = Estado(x,y,self,nivel+1,mapa)
        return estado_temp
    def movimentarAvancado(self,movimento,mapa,nivel):
        x = self.x + (movimento.x)
        y = self.y + (movimento.y)

        print("TENTATIVA MOVIMENTO: "+movimento.imprimir()+"=("+str(x)+","+str(y)+")")
        if x < 0 or x >=m or y < 0 or y >=n:
            print("Invalido - Fronteiras")
            return None

        if mapa.getCusto(x,y)==_BARREIRA:
            print("Invalido - Barreira")
            return None

        estado_temp = Estado(x,y,self,nivel+1,mapa)
        return estado_temp

    def imprimir(self,completo=False):
        saida="["+str(self.nivel)+"::("+str(self.x)+","+str(self.y)+")::"+str(self.c)+"::"+str(self.a)+"/"+str(self.acumulado)+"::"+simbolos[self.status]+"]"
        if self.estadoPai and completo:
            saida = self.estadoPai.imprimir(True)+" > "+saida
        return saida

    def igual(self,x,y):
        if self.x == x and self.y == y:
            return True
        else:
            return False
    
class Movimento:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def imprimir(self):
        return "+("+str(self.x)+","+str(self.y)+")"

class Posicao:
    def __init__(self,custo):
        self.custo = custo
        #self.status = status

class Mapa:
    def __init__(self,m,n,fixa):
        self.m = m
        self.n = n
        #self.objetivo = None
        #self.objetivo = Estado(m-1,n-1,None,None,None,self)

        tipos = [_BARREIRA,_AGUA,_MOVEDICA,_TERRA]
        lista = []
        if fixa:
            listafixa = [1,6,0,1,6,3,1
                        ,6,0,0,1,3,1,6
                        ,3,6,1,6,0,6,1
                        ,3,1,3,3,1,0,6
                        ,6,1,3,6,6,3,0
                        ,0,1,0,3,6,6,1
                        ,0,1,0,3,0,0,1]
            for i in range(m):
                for j in range(n):
                    codPosicao = m*i+j
                    lista.append(Posicao(listafixa[codPosicao]))
        else:
            for i in range(m):
                for j in range(n):
                    codPosicao = m*i+j
                    if codPosicao==0 or codPosicao==m*n-1:
                        lista.append(Posicao(_TERRA))
                    else:
                        lista.append(Posicao(tipos[randrange(0,4)]))
        self.posicoes = np.array(lista)
        self.posicoes = self.posicoes.reshape(m,n)
        
    
    def getCusto(self,x,y):
        return self.posicoes[x,y].custo
        
    def calcDistancia(self,x,y):
        catetox = pow(m-1-x,2)
        catetoy = pow(n-1-y,2)
        
        distancia = math.sqrt(catetox+catetoy)
        self.h = distancia
        return self.h

    def getH(self,x,y):
        return self.h
    
    def imprimir(self):
        str = ""
        for x in range(self.m):
            for w in range(5):
                for y in range(self.n):
                    for z in range(10):
                        if w == 0:
                            str += "_"
                        elif z == 9:
                            str += "|"
                        elif w > 1 and w < 4 and z > 2 and z < 6 and self.posicoes[x,y].custo != _BARREIRA:
                            repetido = getFila(x,y)
                            if repetido:
                                str += simbolos[repetido.status] 
                            else:
                                str += " "
                        else:
                            str += simbolos[self.posicoes[x,y].custo]
                str += "\n"

        print(str)

def criterioClassificacao(e):
    return e.acumulado

def imprimirFila():
    s=""
    for a in fila:
        s+=a.imprimir()+"\n"
    print("Fila="+s)

def popFila(nivel,fila):

    for a in fila:
        if a.nivel  == nivel and a.status < _ESCOLHIDO:#somente os visitados
            return a
    for a in fila:
        if a.nivel  == nivel and a.status < _ERRADO:#dando mais uma chance para um escolhido
            return a
    return None

def getFila(x,y):
    for ponto in fila:
        if ponto.x == x and ponto.y == y:
            #print("encontrou")
            return ponto
    return None

def busca(estado,mapa,voltarNivel,nivel):
    estado.status = _ATUAL
    print("--BUSCA NIVEL "+str(nivel)+"-------------"+estado.imprimir(True))
    flagNenhumEstadoValido = True
    for movimento in movimentosPossiveis:
        estado_temp = estado.movimentar(movimento,mapa,estado.nivel)
        if estado_temp == None:
            continue
        flagNenhumEstadoValido = False
        if estado_temp.igual(m-1,n-1):
            fila.append(estado_temp)
            estado_temp.status = _SUCESSO
            print("Resultado:"+estado_temp.imprimir(True))
            return estado_temp
        print(estado.imprimir()+">>>"+movimento.imprimir()+"="+estado_temp.imprimir())
        #fila.insert(0,estado_temp)
        buscaAvancada(estado_temp,mapa,estado_temp.nivel)
        fila.append(estado_temp)
        
    fila.sort(key=criterioClassificacao)
    imprimirFila()

    if intermitente:
        mapa.imprimir()
        imprimirFila()
        input("continue")

    estado.status = _ESCOLHIDO

    nivel = estado.nivel
    if flagNenhumEstadoValido:
        nivel -= voltarNivel
        voltarNivel = 1
        estado.status = _ERRADO
        print("ERRADO - novonivel="+str(nivel)+"::voltarNivel="+str(voltarNivel))
    else:
        nivel += 1
        voltarNivel = 0
        print("CERTO - novonivel="+str(nivel)+"::voltarNivel="+str(voltarNivel))


    r = None    
    while r == None:
        novoestado=popFila(nivel,fila)
        if not(novoestado):
            print("novoEstado=NULL")
            return None
        print("novoEstado="+novoestado.imprimir())
        #verificar se nao há um estado melhor na fila avancada
        novoEstadoAvancado = popFila(nivel,filaAvancada)
        if novoEstadoAvancado:
            if novoestado.acumulado > novoEstadoAvancado.acumulado:
                novoestado = novoEstadoAvancado
                fila.append(novoestado)
        print(">>>>>>BUSCA")
        r = busca(novoestado,mapa,voltarNivel,nivel)    
        print("<<<<<<BUSCA")
    print("RETURN R")
    return r

def buscaAvancada(estado,mapa,nivel):
    print("--BUSCA AVANCADA NIVEL "+str(nivel)+"-------------"+estado.imprimir(True))
    for movimento in movimentosPossiveis:
        estado_temp = estado.movimentarAvancado(movimento,mapa,estado.nivel)
        if estado_temp == None:
            continue
        print(estado.imprimir()+">>>"+movimento.imprimir()+"="+estado_temp.imprimir())
        filaAvancada.append(estado_temp)

mapa = Mapa(m,n,fixa)
estadoInicial = Estado(0,0,None,0,mapa)
fila = [estadoInicial]
filaAvancada = []
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
#print(mapa.posicoes)
#
#print(mapa.custo)
simbolos = {_AGUA:"~",_BARREIRA:"#",_MOVEDICA:"+",_TERRA:" ",_VISITADO:"?",_ESCOLHIDO:"*",_ERRADO:"X",_ATUAL:"@",_SUCESSO:"$"}
mapa.imprimir()
busca(estadoInicial,mapa,0,0)
mapa.imprimir()

