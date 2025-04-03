from source import dependencias as f

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
        self.updt("Vb", self.Vb/self.vbs)
        self.updt("Ab", self.Ab*f.pi/180)
        
        pots_input = ['Pg', 'Qg', 'Pl', 'Ql']
        for pot in pots_input:
            valor = getattr(self,pot,0)
            self.updt(pot, valor/self.sb)
        setattr(self, 'P', self.Pg - self.Pl)
        setattr(self, 'Q', 0 - self.Ql)

        self.updt('Qn', self.Qn if self.dados['Qn'] else -9999)
        self.updt('Qm', self.Qm if self.dados['Qm'] else  9999)

    def arrumar(self,ref):
        # "escolhendo valores" para começar o metodo de newton
        if self.tipo == 0:
            self.updt("Vb", ref[0])
            self.updt("Ab", ref[1]) 
        elif self.tipo == 1:
            self.updt("Ab", ref[1])

    def limitar_q(self, a): return max(self.Qn, min(self.Qm, a))

    @property
    def Ebar(self): return self.Vb * f.angulo(1j*self.Ab)

    @property
    def Sbar(self): return self.P + 1j*self.Q
    
    def malha(self,ybs): return ybs[self.index]