from source.dependencias import *

class Linha():
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
        self.updt('k',int(self.k-1))
        self.updt('m',int(self.m-1))
        
        setattr(self,'y', self.zb/(self.r+1j*self.x))
        self.updt('bsh', 1j*self.bsh/(2*self.zb) ) 

        self.updt('tap', 1/self.tap if self.dados['tap'] else  1)
        self.updt('phs',angulo(1j*angulos(self.phs,"rad")))
        
def angulos(numero,unidade):
    if unidade == "rad":
        return numero*Pi/180
    elif unidade == "deg":
        return numero*180/Pi