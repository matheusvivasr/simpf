from source.dependencias import *

def nwt_conc(x0,ybus,eps=0.00001):
    # calcular "erros": g(x0)  = Sesp - Scalc
    g0 = gx0(x0,ybus)
    conv = abs(max(g0, key=abs))
    # testar convergencia
    if conv < eps:
        return -1
    else:
        # se nao convergir
        jacobiano = jacs(x0,ybus)
        deltaX = delx(g0,jacobiano)
        barras = ajustes_x0(x0,deltaX)
        return  barras

def  convr(barras,ybus):
    Scalc = scalc(barras,ybus)
    for barra in barras:
        p = Scalc[barra.index].real
        q = Scalc[barra.index].imag
        barra.P = p
        barra.Q = q
    return barras

def indices_bons(barras):
    out = []
    intr = []
    for barra in barras:
        if barra.tipo != 2: intr.append(barra.index)
    out.append(intr)
    intr = []
    for barra in barras:
        if barra.tipo == 0: intr.append(barra.index)
    out.append(intr)
    return out
        
def gx0(barras,ybus):
    Sesp = []
    for barra in barras: Sesp.append(barra.Sbar)
    Scalc = scalc(barras,ybus)
    indexs = indices_bons(barras)

    vetor = []
    for k in indexs[0]:
        vetor.append(Sesp[k].real - Scalc[k].real)
    for k in indexs[1]:
        vetor.append(Sesp[k].imag - Scalc[k].imag)
    return vetor

def delx(g_pt,g_der):
    # h = a*x + b
    a = g_der # jacs
    b = g_pt  # gx0
    # g_lin = gx0 + dx*(-jac) = 0
    # dx = (-jac)^(-1) * (-gx0)
    raiz = (iv(a) @ b).tolist()
    return raiz

def ajustes_x0(barras,delta_x):
    dela,delv = indices_bons(barras)
    meio = len(dela)
    delA = delta_x[:meio]
    delV = delta_x[meio:]

    for k in range(meio):
        barras[dela[k]].Ab += delA[k]

    for k in range(len(delv)):
        barras[delv[k]].Vb += delV[k]

    return barras