import re

def leitura(path:str):
    with open(path,'r') as arq:
        doc = arq.read()
    dbar = getbarras(doc)
    dlin = getlinhas(doc)
    return dbar,dlin

def getbarras(doc):
    rgx = r"DBAR(.*?)99999\n"
    cols = [5,1,1,1,2,12,2,4,4,5,5,5,5,6,5,5,5,3,4]
    heads = ['index','op','est','tipo','Gb', 'nome','Gl', 'Vb', 'Ab','Pg', 'Qg', 'Qn', 'Qm','Bc', 'Pl', 'Ql', 'Sh', 'Are', 'Vf']
    return getfromdoc(doc, rgx, cols, heads)

def getlinhas(doc):
    rgx = r"DLIN(.*?)99999\n"
    cols = [5,5,5,5,6,6,6,5,5,5,5,6,4,4,2,4]
    heads = ['k','dOd','m','ncep','r','x','bsh','tap','tm','tx','phs','Bc','Cn','Ce','Ns','Cq']
    return getfromdoc(doc, rgx, cols, heads)

def getfromdoc(doc, rgx, cols, heads):
    tabela = re.search(rgx, doc, re.DOTALL).group(1).split('\n')
    tabela = tabela[2:-1]
    out = []
    for lin in tabela:
        ini = 0
        item = {}
        for i, head in enumerate(heads):
            fim = ini+cols[i]
            item[head] = lin[ini:fim].strip()
            ini = fim
        out.append(item)
    return out