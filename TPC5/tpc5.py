from lark import Lark, Transformer

grammar = r"""
start: funcao+

funcao: "defr" NOMEFUNCAO ":" NEWLINE statement+

statement: ( lambda_statement | transforme_statement) NEWLINE

lambda_statement: BASE _ARROW_EVAL /[^\n]+/

transforme_statement: BASE _ARROW NOMEFUNCAO

BASE: NOMEFUNCAO | /[^ ]+/

NOMEFUNCAO.1: /[a-zA-Z_][a-zA-Z_0-9]*/
_ARROW.2: "==>"
_ARROW_EVAL.2: "=e=>"

%import common.NEWLINE
%import common.WS
%ignore WS
"""

class Transformer(Transformer):
    def start(self, items):
        funçao_tranformada = ""
        for funçao in items:
            funçao_tranformada += funçao
        return funçao_tranformada

    def funcao(self, items):
        nome_funçao, _, *statements = items
        code = f"def transform_{nome_funçao}(t):\n"
        for statement in statements:
            code += f"    {statement}\n"
        code += "    return t\n"
        return code

    def statement(self, items):
        statement, _ = items
        return items[0]

    def transforme_statement(self, items):
        old_word, new_word = items
        transformaçao =  f"t = re.sub(r'\\b{old_word}\\b', '{new_word}', t)"
        return transformaçao
        
    def lambda_statement(self, items):
        regex, transformer = items
        lambda_return =  f"t = re.sub(r'\\b{regex}\\b', {transformer}, t)"
        return lambda_return

parse = Lark(grammar, parser='lalr', transformer=None)

text = """
defr a:
    the ==> o
    cat ==> gato
    (\\w+) =e=> lambda x: dicionario.get(x[1], x[1])
"""

tree = parse.parse(text)
print(tree)

transformer = Transformer()
result = transformer.transform(tree)
print(result)