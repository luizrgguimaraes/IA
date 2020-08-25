'''
PROBLEMA:
1. 3 raposas e 3 galinhas devem atravessar o rio, da esquerda para a direita
2. O número de raposas nunca pode ser maioria em nenhum dos lados
3. A cada viagem o barco deve conter no mínimo 1 animal
4. O barco carrega no máximo 2 animais.

Definições MODELAGEM:
a. Podemos representar o numero de raposas e galinhas por um par de numeros,
representando o numero de galinhas do lado esquerdo. Assim:
     - (raposas,galinhas) = (2,3) significa que há duas raposas e 3 galinhas do lado esquerdo, e uma raposa e
    nenhuma galinha do lado direito.

b. Precisamos também de uma variável para representar o a posição do barco: Assim:
     - barco = E = -1 significa que o barco está do lado esquerdo
     - barco = D = 1, significa que o barco está do lado direito

c. Notemos que quando o barco viaja do lado esquerdo para o lado direito, o numero de animais do lado esquerdo
diminui, e quando o barco viaja da direita para o lado esquerdo, aumenta. Assim:
     - dado o estado (3,3,E) - que significa que há 3 raposas e 3 galinhas do lado esquerdo, e o barco
     também está do lado esquerdo - ao transportar 1 raposa e uma galinha para o lado direito, temos:
        (2,2,D), ou seja....subtraiu-se (1,1)

d. Notemos também, que o movimento pode ser definido somente pelos seguintes pares (regras 3 e 4):
    movimento = {(1,0),(0,1),(1,1),(2,0)(0,2)}
    Que hora serão subtraídos do estado atual (caso barco = E), hora adicionados (barco = D)

e. Os seguintes estados são inválidos(regra 2):
    21D, 31D, 32D, e seus opostos para o lado direito, 12E, 02E, 01E
    *Se o barco está do lado em que o numero de raposas é maioria, não significa que o estado é
    inválido, porque o barco pode ter acabado de chegar...por isso, 21E, por exemplo, é um estado válido,
    enquanto 21D, significa que o barco já partiu e deixou as raposas como maioria, é inválido

f. Nosso objetivo é chegar na configuração 00D (regra 1)
'''


#------------------------------------------------Entrada do Usuario
totalraposas = int(input("Digite o numero total de raposas:"))
totalgalinhas = int(input("Digite o numero total de galinhas:"))
raposas = int(input("Digite o numero de raposas do lado esquerdo do rio:"))
galinhas = int(input("Digite o numero de galinhas do lado esquerdo do rio:"))
tripulantes = int(input("Digite o numero máximo de animais no barco a cada viagem:"))
print ("\n")

#------------------------------------------------Constantes
_E = -1
_D = 1

#------------------------------------------------Classes
class Estado:
    def __init__(self,raposas,galinhas,posicaoBarco,estadoPai=None,nivel=0):
        self.r = raposas
        self.g = galinhas
        self.b = posicaoBarco
        self.p = estadoPai
        self.dcMovimento = ""
        self.nivel = nivel

        #-----------Texto de Saida
        if self.b==_E:
            pierEsquerdo = "##"
            lado = "E"
            pierDireito = "  "
        else:
            pierDireito = "##"
            pierEsquerdo = "  "
            lado = "D"
        self.dcEstado = str(self.r) + " raposas   "+pierEsquerdo+" /~/~/~/~/~/~/ "+pierDireito+"   "+str(totalraposas-self.r) + " raposas"+"\n"
        self.dcEstado +=str(self.g) + " galinhas  "+pierEsquerdo+" ~/~/~/~/~/~/~ "+pierDireito+"   "+str(totalgalinhas-self.g) + " galinhas"+"\n" 
        self.dcEstado += "\n"+"("+str(self.r)+str(self.g)+lado+")"

    def movimentar(self,movimento):
        r = self.r + (movimento.r*self.b)
        g = self.g + (movimento.g*self.b)
        b = self.b * (-1)
        #validando movimento com base no numero total de raposas e galinhas
        if r < 0 or g < 0 or r > totalraposas or g > totalgalinhas:
            return None
        #validando o movimento com base na maioria de raposas
        if b == _D and r > g and g > 0:
                return None
        elif b == _E and r < g and g < totalgalinhas:
                return None

        if b==_E:
            lado = "esquerdo"
            operador = "+"
        else:
            lado = "direito"
            operador = "-"
        dcMovimento = operador+"("+str(movimento.r)+str(movimento.g)+")"+" = "
        dcMovimento += "transporte "+str(movimento.r)+" raposa(s) e "+str(movimento.g)+ " galinha(s) para o lado "+lado+" do rio"
        dcMovimento += " (Passo "+str(self.nivel+1)+")\n"
        estado_temp = Estado(r,g,b,self,self.nivel+1)
        estado_temp.dcMovimento = dcMovimento
        return estado_temp

    def imprimir(self):
        saida = self.dcMovimento + self.dcEstado
        if(self.p):
            saida = self.p.imprimir()+saida
        return saida

    def igual(self,estado):
        if self.r == estado.r and self.g == estado.g and self.b == estado.b:
            return 1
        else:
            return 0
    
    def repetido(self):
        for repetido in estadosGerados:
            if self.igual(repetido):
                return True
        return False


class Movimento:
    def __init__(self,raposas,galinhas):
        self.r = raposas
        self.g = galinhas


estadoInicial = Estado(int(raposas),int(galinhas),_E,None,0)

estadoObjetivo = Estado(0,0,_D)


estadosGerados = [estadoInicial]

fila = []

#gerar movimentos possiveis
movimentosPossiveis = []
for r in range(totalraposas+1):
    if r > tripulantes:
        break
    for g in range(totalgalinhas+1):
        if r + g > tripulantes or r + g == 0:
            break
        movimentosPossiveis.append(Movimento(r,g))


def busca(estado):
    for movimento in movimentosPossiveis:
        estado_temp = estado.movimentar(movimento)
        if estado_temp == None:
            continue

        if estado_temp.igual(estadoObjetivo):
            print(estado_temp.imprimir())
            return estado_temp

        if estado_temp.repetido():
            continue

        estadosGerados.append(estado_temp)
        fila.append(estado_temp)

    if not(fila):
        return None
    return busca(fila.pop(0))

busca(estadoInicial)
        

