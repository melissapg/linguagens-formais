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
