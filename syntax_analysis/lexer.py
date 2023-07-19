"""
Análise Léxica

A análise léxica recebe o arquivo de entrada e retorna uma lista de tokens.
Cada token tem um tipo (e.x. "NUMERO", "VAR", "+", "NEWLINE")
e opcionalmente um valor (e.x. 42, "x")
"""
from syntax_analysis.regex_rules import (
    variaveis, numeros, igual, mais, menos, multiplicador, divisor, raiz, parenteses, arroba
)

class Token:
    def __init__(self, token, valor):
        self.token = token
        self.valor = valor


TOK_VARIAVEL = 'TOK_VARIAVEL'
TOK_NUMERO = 'TOK_NUMERO'
TOK_IGUAL = 'TOK_IGUAL'
TOK_PARENTESES = 'TOK_PARENTESES'
TOK_MAIS = 'TOK_MAIS'
TOK_MENOS = 'TOK_MENOS'
TOK_MULTIPLICA = 'TOK_MULTIPLICA'
TOK_DIVIDE = 'TOK_DIVIDE'
TOK_SQRT = 'TOK_SQRT'
TOK_ARROBA = 'TOK_ARROBA'
TOK_EOF = 'TOK_EOF'


def lexer(input):
    tokens = []

    for i in range(len(input)):
        m = variaveis.match(input, i)
        if m:
            tokens.append(Token(TOK_VARIAVEL, m.group(0)))
            i = m.end()
            continue
        m = numeros.match(input, i)
        if m:
            tokens.append(Token(TOK_NUMERO, float(m.group(0))))
            i = m.end()
            continue
        m = igual.match(input, i)
        if m:
            tokens.append(Token(TOK_IGUAL, m.group(0)))
            i = m.end()
            continue
        m = mais.match(input, i)
        if m:
            tokens.append(Token(TOK_MAIS, m.group(0)))
            i = m.end()
            continue
        m = menos.match(input, i)
        if m:
            tokens.append(Token(TOK_MENOS, m.group(0)))
            i = m.end()
            continue
        m = multiplicador.match(input, i)
        if m:
            tokens.append(Token(TOK_MULTIPLICA, m.group(0)))
            i = m.end()
            continue
        m = divisor.match(input, i)
        if m:
            tokens.append(Token(TOK_DIVIDE, m.group(0)))
            i = m.end()
            continue
        m = raiz.match(input, i)
        if m:
            tokens.append(Token(TOK_SQRT, m.group(0)))
            i = m.end()
            continue
        m = parenteses.match(input, i)
        if m:
            tokens.append(Token(TOK_PARENTESES, m.group(0)))
            i = m.end()
            continue
        m = arroba.match(input, i)
        if m:
            tokens.append(Token(TOK_ARROBA, m.group(0)))
            i = m.end()
            continue
    return tokens
