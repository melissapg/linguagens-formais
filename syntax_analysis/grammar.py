"""
Árvores Sintáticas
   
   - Uma classe para cada produção da gramática.
     Por  exemplo, a produção "E -> n" tem uma classe ExpNum com um campo
     self.tag (nome da classe) e um campo self.value (o valor do número). 
   - Em geral, a classe tem um campo para cada não-terminal na produção
     e para cada token que tem um valor (por exemplo, números tem valor)
   - Pode criar classes separadas para o +-*/, ou criar uma classe só para
     todas as operações binárias. É questão de gosto.
"""
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
