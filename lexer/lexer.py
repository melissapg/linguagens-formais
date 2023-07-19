import re

espacos = re.compile(r"\s+")
nome    = re.compile(r"[a-zA-Z_][a-zA-Z0-9_]*")  
numero  = re.compile(r"[0-9]+")
simbolo = re.compile(r">=|<=|>|<|==|!=|\+=|-=|\*=|\/=|%=|=|\+|-|\*\*|\*|\/|%|\(|\)|\[|\]|{|}|\.|,|:")
string_aspas_duplas  = re.compile(r'"(\\.|[^\\"])*"')   # string de aspas duplas
string_aspas_simples  = re.compile(r"'(\\.|[^\\'])*'")  # string de aspas simples
comentario = re.compile(r"#.+")

# abrindo o arquivo
with open('lexer.py', 'r', encoding='utf-8') as f:
    input = f.read()
i = 0

while i < len(input):
    # numeros
    m = numero.match(input, i)
    if m:
        print("NUMERO", m.group(0))
        i = m.end()
        continue

    # espaços
    m = espacos.match(input, i)
    if m:
        print("SPACE", m.group(0))
        i = m.end()
        continue

    # nomes
    m = nome.match(input, i)
    if m:
        print("NOME", m.group(0))
        i = m.end()
        continue

    # simbolos
    m = simbolo.match(input, i)
    if m:
        print("SIMBOLO", m.group(0))
        i = m.end()
        continue
    
    # strings
    m = string_aspas_duplas.match(input, i)
    if m:
        print("STRING", m.group(0))
        i = m.end()
        continue
    
    #strings
    m = string_aspas_simples.match(input, i)
    if m:
        print("STRING", m.group(0))
        i = m.end()
        continue

    # comentarios
    m = comentario.match(input, i)
    if m:
        print("COMENTARIO", m.group(0))
        i = m.end()
        continue
