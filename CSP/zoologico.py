
from copy import deepcopy

#STATUS RESTRICAO
_IMPOSSIVEL = 0
_NAO_SATISFEITA = 1
_SATISFEITA = 2

status = ["IMPOSSIVEL","NAO_SATISFEITA","SATISFEITA"]

_LEAO = 0
_ANTILOPE = 1
_HIENA = 2
_TIGRE = 3
_PAVAO = 4
_SURICATE = 5
_JAVALI = 6

class Animal:
    def __init__(self,nome):
        self.nome = nome
        self.jaulas = [1,2,3,4]

animaisInicial = [Animal("Leão")
            ,Animal("Antílope")
            ,Animal("Hiena")
            ,Animal("Tigre")
            ,Animal("Pavão")
            ,Animal("Suricate")
            ,Animal("Javali")
            ]



def get(animais,id):
    for animal in animais:
        if animal.id == id:
            return animal

def mostrarJaulas(animais):
    fit = 0
    for jaula_id in range(1,5):
        jaula = "Jaula" + str(jaula_id) + ":" 
        for animal in animais:
            if jaula_id in animal.jaulas:
                jaula += " - " + animal.nome
                fit += 1
        print(jaula)
    print("FIT = "+str(fit))



#TIPO DE RESTRICAO 0
_REGRA_ATRIBUICAO = 0
def atribuicao(animais,animal_id,njaula):
    print(">>> ATRIBUINDO "+ animais[animal_id].nome + " = " + str(njaula))
    animais[animal_id].jaulas = [njaula]
    return _SATISFEITA

#TIPO DE RESTRICAO 1
_REGRA_DIFERENTE = 1
def jaulaDiferente(animais,a,b):
    print(">>> JAULA "+ animais[a].nome + " DIFERENTE DE " + animais[b].nome)
    len1 = len(animais[a].jaulas)
    len2 = len(animais[b].jaulas)
    if len1 == 1 and len2 == 1:
        if animais[a].jaulas[0] == animais[b].jaulas[0]:
            return _IMPOSSIVEL
        else:
            return _SATISFEITA
    if len1 == 1:
        animais[b].jaulas.remove(animais[a].jaulas[0])
        return _SATISFEITA
    elif len2 == 1:
        animais[a].jaulas.remove(animais[b].jaulas[0])
        return _SATISFEITA
    return _NAO_SATISFEITA
    
#TIPO DE RESTRICAO 2
_REGRA_IGUAL = 2
def jaulaIgual(animais,a,b):
    print(">>> JAULA "+ animais[a].nome + " MESMA DE " + animais[b].nome)
    
    if len(animais[a].jaulas) < len(animais[b].jaulas):
        animais[b].jaulas = list(animais[a].jaulas)
    elif len(animais[a].jaulas) > len(animais[b].jaulas):
        animais[a].jaulas = list(animais[b].jaulas)
        
    if len(animais[a].jaulas) == 1 and len(animais[b].jaulas) == 1:
        if animais[a].jaulas[0] == animais[b].jaulas[0]:
            return _SATISFEITA
        else:
            return _IMPOSSIVEL
    return _NAO_SATISFEITA    

#TIPO DE RESTRICAO 3        
_REGRA_VIZINHOS = 3
def jaulaDiferenteVizinha(animais,a,b):
    print(">>> JAULA "+ animais[a].nome + " LONGE DE " + animais[b].nome)
    
    if len(animais[a].jaulas) == 1:
        if animais[a].jaulas[0] in animais[b].jaulas:
            animais[b].jaulas.remove(animais[a].jaulas[0])
        if (animais[a].jaulas[0]-1) in animais[b].jaulas:
            animais[b].jaulas.remove(animais[a].jaulas[0]-1)
        if (animais[a].jaulas[0]+1) in animais[b].jaulas:
            animais[b].jaulas.remove(animais[a].jaulas[0]+1)
        if len(animais[b].jaulas) == 0:
            return _IMPOSSIVEL
        return _SATISFEITA
    return _NAO_SATISFEITA

_REGRA_TODOS_ALOCADOS = 4
def animaisAlocados(animais):
    print(">>> TODOS ALOCADOS")
    for animal in animais:
        if len(animal.jaulas) == 0:
            return _IMPOSSIVEL
        if len(animal.jaulas) > 1:
            return _NAO_SATISFEITA
    return _SATISFEITA
        
    
def aplicar(animais,regra):
    if regra[0] == _REGRA_ATRIBUICAO:
        return atribuicao(animais,regra[1],regra[2])
    elif regra[0] == _REGRA_DIFERENTE:
        return jaulaDiferente(animais,regra[1],regra[2])
    elif regra[0] == _REGRA_IGUAL:
        return jaulaIgual(animais,regra[1],regra[2])
    elif regra[0] == _REGRA_VIZINHOS:
        a = jaulaDiferenteVizinha(animais,regra[1],regra[2])
        b = jaulaDiferenteVizinha(animais,regra[2],regra[1])
        if a == _IMPOSSIVEL or b == _IMPOSSIVEL:
            return _IMPOSSIVEL
        if a == _SATISFEITA or b == _SATISFEITA:
            return _SATISFEITA
        return _NAO_SATISFEITA
    elif regra[0] == _REGRA_TODOS_ALOCADOS:
        return animaisAlocados(animais)


restricoesInicial = [
    # (TIPO DE REGRA,   PARAMETRO1, PARAMETRO2)
    (_REGRA_ATRIBUICAO, _LEAO,     1           )
    ,(_REGRA_DIFERENTE, _LEAO,     _TIGRE      )
    ,(_REGRA_IGUAL,     _SURICATE, _JAVALI     )
    ,(_REGRA_IGUAL,     _HIENA,    _TIGRE      )
    ,(_REGRA_DIFERENTE, _TIGRE,    _SURICATE   )
    ,(_REGRA_DIFERENTE, _TIGRE,    _JAVALI     )
    ,(_REGRA_DIFERENTE, _TIGRE,    _PAVAO      )
    ,(_REGRA_VIZINHOS,  _LEAO,     _ANTILOPE   )
    ,(_REGRA_VIZINHOS,  _TIGRE,    _ANTILOPE   )
    ,(_REGRA_DIFERENTE, _PAVAO,    _LEAO       )
    ,(_REGRA_TODOS_ALOCADOS, None, None)
    ]



def aplicarRegras(animais,restricoes):
    nrestricao = 0
    
    while len(restricoes)>0 and nrestricao < len(restricoes):
        restricao = restricoes[nrestricao]
        print("**** APLICAR RESTRICAO "+str(nrestricao+1)+"/"+str(len(restricoes)))
        resultadoRegra = aplicar(animais,restricao)
        
        print(status[resultadoRegra])
        mostrarJaulas(animais)
        print(restricoes)

        if resultadoRegra == _IMPOSSIVEL:
            return _IMPOSSIVEL
        if resultadoRegra == _SATISFEITA:
            print("remover regra "+str(nrestricao))
            restricoes.pop(nrestricao)
        else:
            nrestricao += 1    
        input()
    if len(restricoes) == 0:#todas as restrições estão satisfeitas
        return _SATISFEITA
    return _NAO_SATISFEITA

def backTracking(animais,restricoes,nivel):
    print("\n"+"*************** BACKTRACKING nivel " + str(nivel))
    validacaoRegras = aplicarRegras(animais,restricoes)
    if validacaoRegras == _SATISFEITA:
        print("FINALIZADO COM SUCESSO")
        return True
    if validacaoRegras == _IMPOSSIVEL:
        return False
    
    for a in range(len(animais)):
        if len(animais[a].jaulas) == 1:
            continue
        for j in animais[a].jaulas:
            cloneanimais = deepcopy(animais)
            clonerestricoes = deepcopy(restricoes)
            print("\n"+"******* ATRIBUICAO nivel " + str(nivel))
            atribuicao(cloneanimais,a,j)
            mostrarJaulas(cloneanimais)
            # cloneanimais[a].jaulas = [j]
            r = backTracking(cloneanimais,clonerestricoes,nivel+1)
            if r == True:
                return True
    return False

print("\n"+"******************* INICIO ********************")
mostrarJaulas(animaisInicial)
backTracking(animaisInicial,restricoesInicial,0)

# print(animaisInicial)
# animais = deepcopy(animaisInicial)
# print(animais)
