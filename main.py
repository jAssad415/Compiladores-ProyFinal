from lexer import lexer
from parser import parser
import sys

with open("entrada.txt") as f:
    data = f.read()

parser.parse(data, lexer=lexer)
