"""
Crie uma função recursiva calcula(exp, env), que recebe uma árvore de
expressão aritmética e um dicionário com o valor das variáveis,
e retorna o resultado desta expressão.
"""
from syntax_analysis.parser import Parser
from syntax_analysis.lexer import lexer, Token


def read_file(input):
    tokens = []
    text = input.read()
    lines = text.split("\n")
    for line in lines:
        tokens.append(lexer(line))
    tokens_flat = [item for sublist in tokens for item in sublist]
    tokens_flat.append(Token('TOK_EOF', None))  # marcador de end of file
    return tokens_flat


def calcula(exp, env):
    if exp.tag == "root":          # ou isinstance(exp, RootNode)
        for e1s in exp.e1:
            calcula(e1s, env)
        for imprime in exp.arvore:
            calcula(imprime, env)
    elif exp.tag == "@":           # ou isinstance(exp, ExpPrint)
        print(calcula(exp.e1, env))
    elif exp.tag == "=":           # ou isinstance(exp, ExpIgual)
        env[exp.var] = calcula(exp.e1, env)
        return env[exp.var]
    elif exp.tag == 'number':      # ou isinstance(exp, ExpNum)
        return exp.e1
    elif exp.tag == 'var':         # ou isinstance(exp, ExpVar)
        return env[exp.e1]
    elif exp.tag == '+':           # ou isinstance(exp, ExpAdd)
        return calcula(exp.e1, env) + calcula(exp.e2, env)
    elif exp.tag == '-':           # ou isinstance(exp, ExpSub)
        return calcula(exp.e1, env) - calcula(exp.e2, env)
    elif exp.tag == '*':           # ou isinstance(exp, ExpMult)
        return calcula(exp.e1, env) * calcula(exp.e2, env)
    elif exp.tag == '/':           # ou isinstance(exp, ExpDiv)
        return calcula(exp.e1, env) / calcula(exp.e2, env)
    elif exp.tag == 'sqrt':        # ou isinstance(exp, ExpSqrt)
        return (calcula(exp.e1, env))**(1/2)
    elif exp.tag == 'neg':         # ou isinstance(exp, ExpUnop)
        return -calcula(exp.e1, env)
    else:
        raise ValueError(f"Expressão inválida: {exp}")


# teste 1
from syntax_analysis.grammar import ExpNum, ExpVar, ExpAdd
exp = ExpAdd(ExpVar("x"), ExpNum("10"))
env = {"x": 32, "y": 45}
print(calcula(exp, env))

# teste 2
tokens = lexer(input = """a = 1
b = -7
c = 10
@ sqrt(b*b - 4*a*c)""")
tokens.append(Token('TOK_EOF', None))
exp = Parser(tokens)
raiz = exp.parseS()
print(calcula(raiz, {}))

# teste 4
tokens = lexer(input = "4+5")
tokens.append(Token('TOK_EOF', None))
exp = Parser(tokens)
raiz = exp.parseS()
print(calcula(raiz, {}))

# teste 5
with open('teste.txt', 'r', encoding='utf-8') as f:
    tokens = read_file(f)
exp = Parser(tokens)
raiz = exp.parseS()
print(calcula(raiz, {}))
