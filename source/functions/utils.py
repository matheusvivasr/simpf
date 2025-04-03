from source import dependencias as f

def vetor_de(chave:str,lista:list):
    saida = []
    for obj in lista:
        saida.append(getattr(obj,chave))
    return saida


def atualizaE(barras:list[f.Barra], deltas):
    acc = 0
    for b in barras:
        if b.tipo != 2:
            b.Ab += deltas[acc]
            acc+=1
    for b in barras:
        if b.tipo == 0:
            b.Vb += deltas[acc]
            acc+=1

        if acc>=len(deltas):break
    return 0

def atualizaS():
    pass