
from copy import deepcopy

#****************************************************************************************ANIMAIS
_LEAO = 0
_ANTILOPE = 1
_HIENA = 2
_TIGRE = 3
_PAVAO = 4
_SURICATE = 5
_JAVALI = 6

class Animal:
    def __init__(self,nome,id):
        self.id = id
        self.nome = nome
        self.jaulas = [1,2,3,4]
        self.numRestricoes = 0


animais = [Animal("Leão",0),Animal("Antílope",1),Animal("Hiena",2),Animal("Tigre",3),Animal("Pavão",4),Animal("Suricate",5),Animal("Javali",6)]

#*******************************************************************************FUNCOES AUXILIARES
def imprimirJaulas(animais):
    for j in range(1,5):
        jaulastr = "Jaula" + str(j) + ":" 
        for animal in animais:
            if j in animal.jaulas:
                jaulastr += " - " + animal.nome
        print(jaulastr)

def criterioPossibilidades(a):
    return len(a.jaulas)

def criterioRestricoes(a):
    return a.numRestricoes

def criterioId(a):
    return a.id

def analisarNumRestricoes(animais,restricoes):
    for a in animais:
        a.numRestricoes = 0
        for r in restricoes:
            if r[1] == a.id or r[2] == a.id:
                a.numRestricoes += 1
        # print("Restricoes " + a.nome + " = " + str(a.numRestricoes))


#********************************************************************************DEFINICAO DAS RESTRICOES
_IMPOSSIVEL = 0
_POSSIVEL = 1
_SATISFEITA = 2
status = ["IMPOSSIVEL","POSSIVEL","SATISFEITA"]

qtdpassos = 0

_REGRA_ATRIBUICAO = 0
def regraAtribuicao(animais,animal_id,njaula):
    global qtdpassos
    qtdpassos += 1        
    animais[animal_id].jaulas = [njaula]
    return _SATISFEITA

_REGRA_DIFERENTE = 1
def regraDiferente(animais,a,b):
    global qtdpassos
    qtdpassos += 1        
    len1 = len(animais[a].jaulas)
    len2 = len(animais[b].jaulas)
    if len1 == 1 and len2 == 1:
        if animais[a].jaulas[0] == animais[b].jaulas[0]:
            return _IMPOSSIVEL
        else:
            return _SATISFEITA
    if len1 == 1:
        if animais[a].jaulas[0] in animais[b].jaulas:
            animais[b].jaulas.remove(animais[a].jaulas[0])
        return _SATISFEITA
    elif len2 == 1:
        if animais[b].jaulas[0] in animais[a].jaulas:
            animais[a].jaulas.remove(animais[b].jaulas[0])
        return _SATISFEITA
    return _POSSIVEL
    
_REGRA_IGUAL = 2
def regraIgual(animais,a,b):
    global qtdpassos
    qtdpassos += 1        
    
    if len(animais[a].jaulas) < len(animais[b].jaulas):
        animais[b].jaulas = list(animais[a].jaulas)
    elif len(animais[a].jaulas) > len(animais[b].jaulas):
        animais[a].jaulas = list(animais[b].jaulas)
        
    if len(animais[a].jaulas) == 1 and len(animais[b].jaulas) == 1:
        if animais[a].jaulas[0] == animais[b].jaulas[0]:
            return _SATISFEITA
        else:
            return _IMPOSSIVEL
    return _POSSIVEL    

_REGRA_LONGE = 3
def regraLonge(animais,a,b):
    global qtdpassos
    qtdpassos += 1        
    
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
    return _POSSIVEL

_REGRA_TODOS_ALOCADOS = 4
def regraTodosAlocados(animais):
    global qtdpassos
    qtdpassos += 1        
    
    for animal in animais:
        if len(animal.jaulas) == 0:
            return _IMPOSSIVEL
        if len(animal.jaulas) > 1:
            return _POSSIVEL
    return _SATISFEITA

restricoes = [
    # (TIPO DE REGRA,   PARAMETRO1, PARAMETRO2)
    (_REGRA_ATRIBUICAO, _LEAO,      1           )
    ,(_REGRA_LONGE,     _LEAO,      _ANTILOPE   )
    ,(_REGRA_LONGE,     _TIGRE,     _ANTILOPE   )
    ,(_REGRA_DIFERENTE, _LEAO,      _TIGRE      )
    ,(_REGRA_DIFERENTE, _TIGRE,     _SURICATE   )
    ,(_REGRA_DIFERENTE, _TIGRE,     _JAVALI     )
    ,(_REGRA_DIFERENTE, _TIGRE,     _PAVAO      )
    ,(_REGRA_DIFERENTE, _PAVAO,     _LEAO       )
    ,(_REGRA_IGUAL,     _SURICATE,  _JAVALI     )
    ,(_REGRA_IGUAL,     _HIENA,     _TIGRE      )
    ,(_REGRA_TODOS_ALOCADOS, None, None)
    ]


#****************************************************************************************APLICACAO DAS REGRAS        
def aplicar(animais,regra):
    if regra[0] == _REGRA_ATRIBUICAO:
        return regraAtribuicao(animais,regra[1],regra[2])
    elif regra[0] == _REGRA_DIFERENTE:
        return regraDiferente(animais,regra[1],regra[2])
    elif regra[0] == _REGRA_IGUAL:
        return regraIgual(animais,regra[1],regra[2])
    elif regra[0] == _REGRA_LONGE:
        a = regraLonge(animais,regra[1],regra[2])
        b = regraLonge(animais,regra[2],regra[1])
        if a == _IMPOSSIVEL or b == _IMPOSSIVEL:
            return _IMPOSSIVEL
        if a == _SATISFEITA or b == _SATISFEITA:
            return _SATISFEITA
        return _POSSIVEL
    elif regra[0] == _REGRA_TODOS_ALOCADOS:
        return regraTodosAlocados(animais)

def aplicarRegras(animais,restricoes):
    nrestricao = 0
    while len(restricoes)>0 and nrestricao < len(restricoes):
        restricao = restricoes[nrestricao]
        resultadoRegra = aplicar(animais,restricao)
        
        if resultadoRegra == _IMPOSSIVEL:
            return _IMPOSSIVEL
        if resultadoRegra == _SATISFEITA:
            restricoes.pop(nrestricao)
        else:
            nrestricao += 1    
    
    if len(restricoes) == 0:
        return _SATISFEITA
    return _POSSIVEL


#*********************************************************************************************BACKTRACKING

def backTracking(animais,restricoes,nivel):
    global qtdpassos
    validacaoRegras = aplicarRegras(animais,restricoes)
    if validacaoRegras == _SATISFEITA:
        imprimirJaulas(animais)
        return True
    if validacaoRegras == _IMPOSSIVEL:
        return False
    
    # MCV
    analisarNumRestricoes(animais,restricoes)
    animais.sort(key=criterioRestricoes,reverse=True)
    # MRV
    # animais.sort(key=criterioPossibilidades,reverse=True)
    
    # puro = 43 passos
    # MRV = 30 passos 
    # MCV = 27 passos

    for a in range(len(animais)):
        if len(animais[a].jaulas) == 1:
            continue
        for j in animais[a].jaulas:
            cloneanimais = deepcopy(animais)
            clonerestricoes = deepcopy(restricoes)
            regraAtribuicao(cloneanimais,a,j)
            # input()
            cloneanimais.sort(key=criterioId,reverse=False)
            if backTracking(cloneanimais,clonerestricoes,nivel+1) == True:
                return True

    return False



# print("\n"+"**************************************************************** INICIO ********************")
#imprimirJaulas(animais)
backTracking(animais,restricoes,0)
print(qtdpassos)




    