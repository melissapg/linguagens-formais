import re


variaveis = re.compile(r"([a-zA-Z_][a-zA-Z0-9_]*)+\b(?<!sqrt)")
numeros  = re.compile(r"[0-9]+")
igual = re.compile(r"=")
mais = re.compile(r"\+")
menos = re.compile(r"\-")
multiplicador = re.compile(r"\*")
divisor = re.compile(r"\/")
raiz = re.compile(r"sqrt")
parenteses = re.compile(r"\(|\)")
arroba = re.compile(r"@")

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

class RootNode:
    # S -> VS PS
    def __init__(self, e1, arvore) -> None:
        self.tag = 'root'
        self.e1 = e1
        self.arvore = arvore

class ExpPrint:
    def __init__(self, e1) -> None:
        self.tag = '@' 
        self.e1 = e1

class ExpIgual:
    def __init__(self, var, e1) -> None:
        self.tag = '='
        self.var = var
        self.e1 = e1

class ExpNum:
    # f -> <[0-9]+>
    def __init__(self, e1)  -> None:
        self.tag = 'number'
        self.e1 = float(e1)

class ExpVar:
    # f -> <var>
    def __init__(self, e1)  -> None:
        self.tag = 'var'
        self.e1 = e1

class ExpUnop:
    # f -> '-' f
    def __init__(self, e1) -> None:
        self.tag = 'neg'
        self.e1 = e1

class ExpAdd:
    # e -> e '+' t
    def __init__(self, e1, e2) -> None:
        self.tag = '+'
        self.e1 = e1
        self.e2 = e2

class ExpSub:
    # e -> e '-' t
    def __init__(self, e1, e2) -> None:
        self.tag = '-'
        self.e1 = e1
        self.e2 = e2

class ExpMult:
    # t -> t '*' f
    def __init__(self, e1, e2) -> None:
        self.tag = '*'
        self.e1 = e1
        self.e2 = e2

class ExpDiv:
    # t -> t '/' f
    def __init__(self, e1, e2) -> None:
        self.tag = '/'
        self.e1 = e1
        self.e2 = e2

class ExpSqrt:
    # f -> <sqrt> f
    def __init__(self, e1) -> None:
        self.tag = 'sqrt'
        self.e1 = e1


class Parser:
    def __init__(self, tokens_list):
        self.tokens = tokens_list
        self.token = tokens_list[0]
        self.next_token_idx = 1

    def peek(self, tipo) -> bool:
        """
        Retorna True se proximo token tem esse tipo.
        """
        if(self.token.token == tipo):
            return True
        else:
            return False

    def consome(self, tipo) -> str or bool:
        """
        Se o token for do tipo esperado, o consome e retorna o valor opcional.
        Senão, imprime um erro de sintaxe e interrompe o parser.
        """
        if self.token.token == tipo:
            valor = self.token.valor
            self.avanca()
            return valor
        else:
            SyntaxError

    def avanca(self) -> None:
        """
        Anda 1 token para frente sem olhar o tipo.
        """
        if self.next_token_idx < len(self.tokens):
            self.token = self.tokens[self.next_token_idx]
            self.next_token_idx += 1
    
    def parseS(self):
        """
        Parsea a variável S.

        S -> VS PS
        """
        vs = self.parseVS()
        ps = self.parsePS()
        s = RootNode(vs, ps)
        return s

    def parseVS(self):
        """
        Parsea a variável VS.

        VS ->
        VS -> VS <var> '=' E <newline>
        """
        vars = []
        while self.peek(TOK_VARIAVEL):
            variavel = self.consome(TOK_VARIAVEL)
            self.consome(TOK_IGUAL)
            e = self.parseE()
            vars.append(ExpIgual(variavel, e))
        return vars

    def parsePS(self):
        """
        Parsea a variável PS.

        PS ->
        PS -> PS '@' E <newline>
        """
        arv = []
        while not self.peek(TOK_EOF):
            self.consome(TOK_ARROBA)
            e = self.parseE()
            arv.append(ExpPrint(e))
        return arv

    def parseE(self):
        """
        Parsea a variável E.

        E -> E '+' T
        E -> E '-' T
        E -> T
        """
        e = self.parseT()
        while self.peek(TOK_MAIS) or self.peek(TOK_MENOS):
            if self.peek(TOK_MAIS):
                self.consome(TOK_MAIS)
                t = self.parseT()
                e = ExpAdd(e, t)
            elif self.peek(TOK_MENOS):
                self.consome(TOK_MENOS)
                t = self.parseT()
                e = ExpSub(e, t)
            else:
                break
        return e

    def parseT(self):
        """
        Parsea a variável T.

        T -> T '*' F
        T -> T '/' F
        T -> F
        """
        t = self.parseF()
        while self.peek(TOK_MULTIPLICA) or self.peek(TOK_DIVIDE):
            if self.peek(TOK_MULTIPLICA):
                self.consome(TOK_MULTIPLICA)
                f = self.parseF()
                t = ExpMult(t, f)
            elif self.peek(TOK_DIVIDE):
                self.consome(TOK_DIVIDE)
                f = self.parseF()
                t = ExpDiv(t, f)
            else:
                break
        return t

    def parseF(self):
        """
        Parsea a variável F.

        F -> '-' F
        F -> <num>
        F -> <var>
        F -> <sqrt> '(' E ')'
        F -> '(' E ')'
        """
        if self.peek(TOK_MENOS):
            print("parseF - TOK_MENOS")
            self.consome(TOK_MENOS)
            f = self.parseF()
            return ExpUnop(f)

        elif self.peek(TOK_NUMERO):
            print("parseF - TOK_NUMERO")
            n = self.consome(TOK_NUMERO)
            return ExpNum(n)

        elif self.peek(TOK_VARIAVEL):
            print("parseF - TOK_VARIAVEL")
            n = self.consome(TOK_VARIAVEL)
            return ExpVar(n)

        elif self.peek(TOK_SQRT):
            print("parseF - TOK_SQRT")
            self.consome(TOK_SQRT)
            self.consome(TOK_PARENTESES)
            e = self.parseE()
            self.consome(TOK_PARENTESES)
            return ExpSqrt(e)

        elif self.peek(TOK_PARENTESES):
            print("parseF - TOK_PARENTESES")
            self.consome(TOK_PARENTESES)
            e = self.parseE()
            self.consome(TOK_PARENTESES)
            return e
        else:
            SyntaxError

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

# teste 5
import sys
tokens = read_file(sys.stdin)
exp = Parser(tokens)
raiz = exp.parseS()
calcula(raiz, {})