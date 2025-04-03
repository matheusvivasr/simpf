from source import dependencias as f


def iteran(barras:list[f.Barra], linhas:list[f.Linha], epslon=0.00001): 
    ybus = f.ybuss(barras,linhas)
    erros = f.deltaS(barras,ybus) 
    jac = f.jacs(barras,ybus)
    iojac = -f.inv(jac)

    sol = []
    if max(abs(var) for var in erros) < epslon: 
        print(max(abs(var) for var in erros))
        print("a mimir")
    else:
        for lin in iojac.tolist():
            ss = 0
            for k in range(len(lin)):
                ss+= lin[k]*erros[k]
                
            sol.append(-ss)
    
    return sol