from monkey import token
from monkey.lexer import Lexer
from monkey.parser import Parser


def test_parse_identifier():
    parser = Parser(Lexer("a"))
    p = parser.parse_program()
    assert len(p.statements) == 1
    assert p.statements[0].token.type == token.IDENT
    assert p.statements[0].token.literal == 'a'
