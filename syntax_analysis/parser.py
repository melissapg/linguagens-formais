"""
Análise Sintática

A análise sintática recebe a lista de tokens e constrói uma árvore sintática.
Use o algoritmo descendente recursivo. Para a árvore sintática, crie classes
como ExpAdd, ExpMul, ExpVar, ExpNum, etc. Se quiser pode usar ExpBin("+"
em vez do ExpAdd e por aí vai.

Crie uma classe Parser para o analisador sintático. O estado interno da
classe mantém uma representação do "próximo token" e de quanto o parser
já consumiu da entrada. Uma opção é armazenar a lista de tokens produzida
pela análise léxica, e um índice índice dizendo qual é o próximo token.

Para cada não terminal da gramática, crie um método parseX(). Por exemplo,
parseS(), parseE(), parseT(), parseF(), etc. Esses métodos consomem o quanto
da entrada for necessário e retornam um nó de árvore ou uma lista. Esses 
métodos tem um "if-elif" com um caso para cada produção da gramática.
"""
from syntax_analysis.grammar import (
    RootNode, ExpPrint, ExpIgual, ExpNum, ExpVar, ExpAdd, ExpSub, ExpMult, ExpDiv, ExpSqrt, ExpUnop
)
from syntax_analysis.lexer import (
    TOK_VARIAVEL, TOK_NUMERO, TOK_IGUAL, TOK_PARENTESES, TOK_MAIS, TOK_MENOS,
    TOK_MULTIPLICA, TOK_DIVIDE, TOK_SQRT, TOK_ARROBA, TOK_EOF
)

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
