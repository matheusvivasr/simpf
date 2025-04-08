from source.dependencias import *

cam = "IEEE_14B.txt"
dbar,dlin = leitura(cam)
barras = []
for i in dbar:  
    barras.append(Barra(i))
    
linhas = []
for i in dlin:
    linhas.append(Linha(i))

print()
for i in barras:
    print([i.index+1, round(i.Vb,3),  round(i.Ab,2), round(i.P,3), round(i.Q,3)])

ybus = ybuss(barras,linhas)
for i in range(19):
    nilton  = nwt_conc(barras,ybus)
    if nilton == -1: 
        barras = convr(barras,ybus)
        break
    else: barras = nilton

print()
for i in barras:
    print([i.index+1, round(i.Vb,3),  round(i.Ab,2), round(i.P,3), round(i.Q,3)])
