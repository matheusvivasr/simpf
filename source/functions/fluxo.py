from source.dependencias import *

def icalc(barras:list[Barra],ybus):
    '''
        calcula a corrente total que sai de uma barra a partir da tensao, angulo e matriz admitancia

        retorna
            vetor contendo as respectivas correntes calculadas
    '''

    Is = [0j for ç in range(len(barras))]
    for bark in barras:
        for barm in barras:
            Is[bark.index] += ybus[bark.index][barm.index] * barm.Ebar
    return Is

def scalc(barras:list[Barra],ybus):
    '''
        calcula a potencia total que sai da barra, pela formula S = E.I*
        
        retorna
            vetor contendo as respectivas potencias calculadas
    '''

    Ic = icalc(barras,ybus)
    Sc = [0j for ç in range(len(barras))]
    for bark in barras:
        Sc[bark.index] = bark.Ebar * Ic[bark.index].conjugate()
    return Sc