from monkey import evaluator
from monkey.lexer import Lexer
from monkey.parser import Parser
from monkey import object
prompt = ">> "


def start():
  env = object.Environment()
  while True:
    line = input(prompt)
    l = Lexer(line)
    p = Parser(l)
    program = p.parse_program()
    val = evaluator.eval(program, env)
    print(val)