from source.dependencias import *

def ybuss(bars:list[Barra],lins:list[Linha]):
    rnb = range(len(bars))
    ybus = [[0j for ç in rnb] for ç in rnb]
    for lin in lins:
            ybus[lin.k][lin.m] = -lin.phs*lin.tap*lin.y
            ybus[lin.m][lin.k] = -lin.phs*lin.tap*lin.y
            ybus[lin.k][lin.k] += (lin.tap*lin.tap)*lin.y + lin.bsh
            ybus[lin.m][lin.m] += (lin.tap*lin.tap)*lin.y + lin.bsh
    for bar in bars:
        ybus[bar.index][bar.index] += bar.Sh
    return ybus