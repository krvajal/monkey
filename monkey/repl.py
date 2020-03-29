from monkey.lexer import Lexer
from monkey.parser import Parser
from monkey.token import EOF
prompt = ">> "


def start():
  while True:
    line = input(prompt)
    l = Lexer(line)
    p = Parser(l)
    print(p.parse_program())