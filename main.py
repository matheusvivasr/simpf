from source import dependencias as f

cam = "IEEE_14B.txt"
dbar,dlin = f.leitura(cam)
barras = []
for i in dbar:  
    barras.append(f.Barra(i))
    
linhas = []
for i in dlin:
    linhas.append(f.Linha(i))

ybus = f.ybuss(barras,linhas)
acc=0
sover = f.iteran(barras,linhas)
while sover!=[]:
    print(f"it: {acc}")
    f.atualizaE(barras,sover)
    sover = f.iteran(barras,linhas)
    if acc>1000:break
    acc+=1

for i in barras:
    print([i.index+1, round(i.Vb,3),  round(i.Ab*180/f.pi,2), round(i.P,3), round(i.Q,3)])