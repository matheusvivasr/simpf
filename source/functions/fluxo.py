from source.dependencias import *
# =
# ()

def icalc(barras:list[Barra],ybus):
    Is = [0j for ç in range(len(barras))]
    for bark in barras:
        for barm in barras:
            Is[bark.index] += ybus[bark.index][barm.index] * barm.Ebar
    return Is

def scalc(barras:list[Barra],ybus):
    Ic = icalc(barras,ybus)
    Sc = [0j for ç in range(len(barras))]
    for bark in barras:
        Sc[bark.index] = bark.Ebar * Ic[bark.index].conjugate()
    return Sc

def deltaS(barras:list[Barra],ybus):
    pvect = []
    qvect = []
    Scal = scalc(barras,ybus)

    for b in barras:
        delS = b.Sbar - Scal[b.index]
        if b.tipo == 0:
            pvect.append(delS.real)
            qvect.append(delS.imag)
        if b.tipo == 1:
            pvect.append(delS.real)
    out = []
    for s in pvect: out.append(s)
    for s in qvect: out.append(s) 
    return out

def jacs(barras:list[Barra],ybus):
    rnb = range(len(barras))
    Ic = icalc(barras,ybus)
    sda = [[0j for ç in rnb] for ç in rnb]
    sdv = [[0j for ç in rnb] for ç in rnb]
    james = []

    # derivadas parciais 
    for bk in barras:
        sda[bk.index][bk.index] = 0j # angulo
        sdv[bk.index][bk.index] = 0j # tensao
        for bm in barras:
            # del bk / del bm
            if bk.index == bm.index:
                sda[bk.index][bk.index] = (1j*bk.Ebar) * (Ic[bk.index] - ybus[bk.index][bk.index]*bk.Ebar).conjugate()
                sdv[bk.index][bk.index] = angulo(1j*fase(bk.Ebar)) * (Ic[bk.index] + ybus[bk.index][bk.index]*bk.Ebar).conjugate()
            else:
                sda[bk.index][bm.index] = (-1j)*(bk.Ebar*(ybus[bk.index][bm.index]*bm.Ebar).conjugate())
                sdv[bk.index][bm.index] =  bk.Ebar*(ybus[bk.index][bm.index]*angulo(1j*fase(bm.Ebar))).conjugate()
    
    # del Pk / 
    for bk in barras:
        jam = []
        if bk.tipo != 2:
            # /del Am 
            for bm in barras:
                if bm.tipo != 2:
                    jam.append(sda[bk.index][bm.index].real)

            # /del Vm 
            for bm in barras:
                if bm.tipo == 0:
                    jam.append(sdv[bk.index][bm.index].real)
        # linha delP
        if jam != []:james.append(jam)

    # del Qk / 
    for bk in barras:
        jam = []
        if bk.tipo == 0:
            # /del Am 
            for bm in barras:
                if bm.tipo != 2:
                    jam.append(sda[bk.index][bm.index].imag)

            # /del Vm 
            for bm in barras:
                if bm.tipo == 0:
                    jam.append(sdv[bk.index][bm.index].imag)

        # linha delQ
        if jam != []:james.append(jam)

    return james
