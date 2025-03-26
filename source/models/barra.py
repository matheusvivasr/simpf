from cmath import exp as fasor
from cmath import phase as fase
from math import pi
class Barra():
    sb = 100
    vbs = 1000
    zb = 100
    def __init__(self, dados, ref = [1.0 ,0.0]):
        for chave, valor in dados.items():
            setattr(self, chave, valor)
        self.startpoint(ref)

    def updt(self, chave, novo_valor):
        if hasattr(self, chave): setattr(self, chave, novo_valor)
        else: setattr(self,chave,0)

    def startpoint(self,ref):
        if self.index == 0:
            self.updt("Vb", ref[0])
            self.updt("Ab",ref[1]) 
        elif self.index == 1:
            self.updt("Vb", float(self.Vb)/self.vbs)
            self.updt("Ab",ref[1])
        elif self.index == 2:
            self.updt("Vb", float(self.Vb)/self.vbs)
            self.updt("Ab", float(self.Ab)*pi/180)
        
        pots_input = ['Pg', 'Qg', 'Pl', 'Ql']
        for pot in pots_input:
            valor = getattr(self,pot,0)
            val = float(valor.strip()) if valor.strip().isdigit() else 0
            self.updt(pot, val/self.sb)
        setattr(self, 'P', self.Pg - self.Pl)
        setattr(self, 'Q', self.Qg - self.Ql)

        qmin = float(self.Qn) if self.Qn.isdigit() else -9999
        qmax = float(self.Qm) if self.Qm.isdigit() else  9999
        self.updt('Qn',qmin)
        self.updt('Qm',qmax)

    def limitar_q(self, a): return max(self.Qn, min(self.Qm, a))

    @property
    def Ebar(self): return self.Vb * fasor(1j*self.Ab)
    @Ebar.setter
    def Ebar(self,dV,dA):
        self.updt('Vb', getattr(self,'Vb',1) - dV)
        self.updt('Ab', getattr(self,'Ab',0) - dA)
        self.Ebar = self.Vb * fasor(1j*self.Ab)

    @property
    def Sbar(self): return self.P + 1j*self.Q
    @Sbar.setter
    def Sbar(self,dP,dQ):
        self.updt('P', getattr(self,'P',0) - dP)
        self.updt('Q', getattr(self,'Q',0) - dQ)
        self.Sbar = self.P + 1j*self.Q

    @property
    def bsh(self): 
        valor = getattr(self,'Sh')
        shunt = 1j*float(self.Sh)/self.zb if self.Sh.isdigit() else 0
        return shunt
    