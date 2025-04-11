from source.dependencias import *

def nwt_conc(x0,ybus,eps=0.00001):
    '''
        segue o metodo de newton adaptado para sistema de 2 varaiaveis e valores complexos.

        retorna
            se o sistema convergir, -1;
            se não, atualiza os valores de [V, A] para o proximo teste.

    '''

    g0 = gx0(x0,ybus)
    conv = abs(max(g0, key=abs))

    if conv < eps:
        return -1
    
    else:
        jacobiano = jacs(x0,ybus)
        deltaX = delx(g0,jacobiano)
        barras = ajustes_x0(x0,deltaX)
        return  barras

def indices_bons(barras):
    '''
        cria uma lista com os indices  das barras para o fluxo de potencia
        retorna
            out = [ [PQ+PV], [PQ] ]
    '''

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
    '''
        calcula g(x0)  = Sesp - Scalc
        
        retorna
            lista com o residuo de potencia ativa e reativa na ordem que newton usa.
            formato [ dP(PQ+PV), dQ(PQ) ]
    '''

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
    '''
        encontra o ajuste para o vetor de deltax.

        retorna
            lista resultante da operacao matricial: J(x0)^-1 * g(x0).
            formato [ dA(PQ+PV), dV(PQ) ]
    '''

    b = g_pt  # gx0
    a = g_der # jacs
    raiz = (matriz_inversa(a) @ b).tolist()
    return raiz

def ajustes_x0(barras,delta_x):
    '''
        soma os valores obtidos em "delx" com os valores atuais nas barras.

        retorna
            lista de barras com tensao e angulo atualizados.
    '''

    indA,indV = indices_bons(barras)
    meio = len(indA)
    delA = delta_x[:meio]
    delV = delta_x[meio:]

    for k in range(meio):
        barras[indA[k]].Ab += delA[k]

    for k in range(len(indV)):
        barras[indV[k]].Vb += delV[k]

    return barras

def jacs(barras:list[Barra],ybus):

    '''
        calcula a matriz jacobiana do sistema.
        simultaneamente calcula todas as derivadas em relacao ao angulo (sda) e a tensao (sdv)
        e depois monta a matriz jacobiana com os indices interessantes de cada vetor de derivadas
        retorna
            vetor no formato: [ [ sda.real (PV+PQ) ; sdv.real (PQ) ] (PV+PQ) ; 
                                [ sda.imag (PV+PQ) ; sdv.imag (PQ) ] (PQ)     ]

    '''

    rnb = range(len(barras))
    Ic = icalc(barras,ybus)
    sda = [[0j for ç in rnb] for ç in rnb]
    sdv = [[0j for ç in rnb] for ç in rnb]

    for bk in barras:
        sda[bk.index][bk.index] = 0j # angulo
        sdv[bk.index][bk.index] = 0j # tensao
        for bm in barras:
            if bk.index == bm.index:
                sda[bk.index][bk.index] = (1j*bk.Ebar) * (Ic[bk.index] - ybus[bk.index][bk.index]*bk.Ebar).conjugate()
                sdv[bk.index][bk.index] = angulo(1j*fase(bk.Ebar)) * (Ic[bk.index] + ybus[bk.index][bk.index]*bk.Ebar).conjugate()
            else:
                sda[bk.index][bm.index] = (-1j)*(bk.Ebar*(ybus[bk.index][bm.index]*bm.Ebar).conjugate())
                sdv[bk.index][bm.index] =  bk.Ebar*(ybus[bk.index][bm.index]*angulo(1j*fase(bm.Ebar))).conjugate()

    jacobiano = []
    indP,indQ = indices_bons(barras)
    for k in indP:
        jac_linha = []
        for m in indP: jac_linha.append(sda[k][m].real)
        for m in indQ: jac_linha.append(sdv[k][m].real)
        jacobiano.append(jac_linha)
    for k in indQ:
        jac_linha = []
        for m in indP: jac_linha.append(sda[k][m].imag)
        for m in indQ: jac_linha.append(sdv[k][m].imag)
        jacobiano.append(jac_linha)

    return jacobiano

def  convr(barras,ybus):
    '''
        Planejada para ser usada apos o sistema convergir.
        calcula as potencias ativa e reativa em todas as barras e as substitui.
        assume que Scalc = Sesp e portanto nao ha necessidade de escolher quais barras sofrem atualizacao.
        
        retorna 
            vetor de barras com potencias atualizadas.
    '''
    Scalc = scalc(barras,ybus)
    for barra in barras:
        p = Scalc[barra.index].real
        q = Scalc[barra.index].imag
        barra.P = p
        barra.Q = q
    return barras