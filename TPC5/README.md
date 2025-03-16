# TPC5

### Definição da Gramática (Usando Lark)

A variável grammar define uma gramática personalizada para a DSL, permitindo criar funções de transformação de texto.
Elementos principais da gramática:

- start → O ponto de entrada, que aceita múltiplas funções (funcao+).
- funcao → Representa uma função, sempre começando com "defr" NOMEFUNCAO : seguido por múltiplas regras (statement+).
- statement → Define o que pode estar dentro da função. Pode ser:
    - transforme_statement: Substitui palavras diretamente (palavra ==> nova_palavra).
    - lambda_statement: Aplica uma transformação usando uma função ((\w+) =e=> lambda ...).

Tokens e operadores especiais:

- NOMEFUNCAO → Representa nomes válidos de funções.
- _ARROW ("==>") → Representa uma substituição simples (palavra ==> nova_palavra).
- _ARROW_EVAL ("=e=>") → Representa uma transformação dinâmica com lambda.

### Implementação da Transformação (Classe Transformer)

A classe Transformer converte a árvore sintática gerada pelo Lark em código Python real.
Métodos principais:

start → Junta todas as funções transformadas.

funcao → Cria uma função Python para cada defr ...: na DSL.

statement → Processa cada regra dentro da função.

transforme_statement → Converte "palavra ==> nova_palavra" em código Python que usa re.sub() para substituir palavras.

lambda_statement → Converte "(\w+) =e=> lambda x: ..." em código Python que aplica uma função lambda sobre cada correspondência.



#### Input 
```
defr a:
    the ==> o
    cat ==> gato
    (\w+) =e=> lambda x: dicionario.get(x[1], x[1])
```

#### Output

```
def transform_a(t):
    t = re.sub(r'\bthe\b', 'o', t)
    t = re.sub(r'\bcat\b', 'gato', t)
    t = re.sub(r'\b(\w+)\b', lambda x: dicionario.get(x[1], x[1]), t)
    return t
```