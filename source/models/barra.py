from source.dependencias import *

class Barra():
    sb = 100
    vbs = 1000
    zb = 100
    def __init__(self, dados):
        self.dados = dados

        for chave, valor in self.dados.items():
            try: valor = float(valor)
            except ValueError: 
                if valor == '': valor = 0
                else: pass
            setattr(self, chave, valor)
            
        self.startpoint()

    def updt(self, chave, novo_valor):
        if hasattr(self, chave): setattr(self, chave, novo_valor)
        else: setattr(self,chave,0)

    def startpoint(self):
        # arrumando os valores do dicionario
        self.updt("index", int(self.index-1))
        self.updt("Sh",1j*self.Sh/self.zb)
        self.arrumarE()
        self.arrumarS()
        
    def arrumarE(self):
        # "escolhendo valores" para começar o metodo de newton
        if self.tipo == 2:      # slack
            self.updt("Vb", self.Vb/self.vbs)
            self.updt("Ab", angulos(self.Ab,"rad"))

        elif self.tipo == 1:    # geracao
            self.updt("Vb", self.Vb/self.vbs)
            self.updt("Ab", 0.0)

        else:                   # carga
            self.updt("Vb", 1.0)
            self.updt("Ab", 0.0)
            
    @property
    def Ebar(self): return self.Vb * angulo(1j*self.Ab)

    def arrumarS(self):
        pots_input = ['Pg', 'Qg', 'Pl', 'Ql']
        for pot in pots_input:
            valor = getattr(self,pot,0)
            self.updt(pot, valor/self.sb)
        setattr(self, 'P', self.Pg - self.Pl)
        setattr(self, 'Q', 0 - self.Ql)

        self.updt('Qn', self.Qn if self.dados['Qn'] else -9999)
        self.updt('Qm', self.Qm if self.dados['Qm'] else  9999)
    @property
    def Sbar(self): return self.P + 1j*self.Q

    def limitar_q(self, a): return max(self.Qn, min(self.Qm, a))


def angulos(numero,unidade):
    if unidade == "rad":
        return numero*Pi/180
    elif unidade == "deg":
        return numero*180/Pi