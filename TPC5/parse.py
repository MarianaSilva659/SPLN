import re
from lark import Lark, Transformer, v_args
from tabulate import tabulate

# Definição da gramática usada para analisar o texto
gramatica = r'''
start: (PAR_COM_PARENTESIS|pt_tt_line|pt_line|tt_line|FIG_LINE|UNKNOWN_LINE)*

pt_tt_line: pt_line tt_line  # Uma linha de pt e tt juntos

pt_line: PT_LINE UNKNOWN_LINE*  # Linha de texto em português (PT) com possíveis linhas desconhecidas após

tt_line: TETUN_LINE UNKNOWN_LINE*  # Linha de texto em tetum (TETUN) com possíveis linhas desconhecidas após

PAR_COM_PARENTESIS.2: /(\b\w+\b )+\(.+\)/  # Definição para uma linha com parênteses, como "palavra (definição)"

PT_LINE.3: /PORTUGUÊS: .*/  # Definição para a linha que começa com "PORTUGUÊS:"

TETUN_LINE.3: /TETUN: .*/  # Definição para a linha que começa com "TETUN:"

FIG_LINE.3: /Figura \d+\- (\b\w+\b )+\(.+\)/  # Definição para a linha que contém a palavra "Figura"

UNKNOWN_LINE.1: /.+/  # Linha desconhecida (qualquer coisa que não seja capturada pelas definições anteriores)

%import common.NEWLINE  # Importação para tratar quebras de linha
%ignore NEWLINE  # Ignorar quebras de linha para processamento

'''

# Exemplo de texto a ser processado
ex = r'''
Simplificação de Radicais (Simplifikasaun hosi Radikál sira).................................................. 118
Sinais (Sinál Sira) ...................................................................................................................... 119
Sistema (Sistema) ...................................................................................................................... 119
Subtração (Subtrasaun / Hasai / Kuran) .................................................................................... 119
Subtraendo (Subtraendu / Hamenus)......................................................................................... 119
Tangente (Tanjente) .................................................................................................................. 120
Tangram (Tangram) .................................................................................................................. 120
Teorema (Teorema) ................................................................................................................... 121
Termo (Termu) .......................................................................................................................... 121
Tetraedro (Tetraedru) ................................................................................................................ 121
Trapézio (Trapéziu) ................................................................................................................... 121
Triângulo (Triángulu)................................................................................................................ 122
Trigonometria (Trigonometria) ................................................................................................. 122
Unidade (Unidade) .................................................................................................................... 122
Valor Absoluto (Valór Absolutu) .............................................................................................. 122
Valor Médio (Valór Médiu) ...................................................................................................... 122
Variável (Variavel).................................................................................................................... 122


PORTUGUÊS: Localização de um ponto em relação ao eixo horizontal x. Pode ter
posição positiva, negativa ou nula. Exemplos: Ver em TETUN.
TETUN: Fatin ba pontu sira-ne´ebé iha relasaun ho eixu orizontál (eixu x). Bele iha
pozisaun pozitiva, negativa ka nula. Ezemplu sira:

Figura 1- Eixo X-Y com abscissas (Eixu X-Y ho absisa)
'''

processador = Lark(gramatica, parser='lalr')
tree = processador.parse(ex)

print(tree.pretty())


@v_args(inline=True)
class T(Transformer):
    def start(self, *t): return t  

    # Trata linhas que contêm parênteses
    def PAR_COM_PARENTESIS(self, t): 
        return ('pt-tt', re.split(r' *[()]', t.value)[:-1]) 

    # Trata linhas que começam com "PORTUGUÊS:"
    def PT_LINE(self, t): 
        return ('pt', t.value.split(':')[1])  

    # Junta uma linha em português (PT) com as linhas desconhecidas que seguem
    def pt_line(self, pt, *l): 
        return ('pt', pt[1] + '\n' + '\n'.join(l)) 

    # Trata linhas que começam com "TETUN:"
    def TETUN_LINE(self, t): 
        return ('tt', t.value.split(':')[1])  

    # Junta uma linha em tetum (TETUN) com as linhas desconhecidas que seguem
    def tt_line(self, tt, *l): 
        return ('tt', tt[1] + '\n' + '\n'.join(l))  

    # Trata linhas com a combinação de português e tetum (PT-TT)
    def pt_tt_line(self, pt, tt): 
        return ('pt-tt', [pt[1], tt[1]]) 

    # Trata linhas que começam com "Figura" (como para imagens ou figuras)
    def FIG_LINE(self, t): 
        return ('fig', t.value) 

    # Trata linhas desconhecidas (qualquer outra coisa que não seja capturada pelas regras anteriores)
    def UNKNOWN_LINE(self, t): 
        return t.value # Retorna a linha como está

arvore = T().transform(tree)

# Separar as linhas de dados e as linhas desconhecidas
unknown = []  
dados = []  

for item in arvore:
    if isinstance(item, str):  
        unknown.append(item)  
    else:  
        dados.append(item[1]) 


print('UNKNOWN')
print(unknown)

print('DATA')
print(tabulate(dados))
