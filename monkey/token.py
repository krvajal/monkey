EOF = "EOF"
ILLEGAL = "ILLEGAL"

# indentifier
IDENT = "IDENT"
# integer
INT = "INT"
# string
STRING = "STRING"

ASSIGN = "="
EQ = "=="
NOT_EQ = "!="
PLUS = "+"
MINUS = "-"
BANG = "!"
ASTERISK = "*"
SLASH = "/"

LT = "<"
GT = ">"
SEMICOLON = ";"
LPAREN = "("
RPAREN = ")"
COMMA = ","
PLUS = "+"
LBRACE = "{"
RBRACE = "}"

# keywords
FUNCTION = "FUNCTION"
LET = "LET"
TRUE = "TRUE"
FALSE = "FALSE"
IF = "IF"
ELSE = "ELSE"
RETURN = "RETURN"

keywords = {
    "fn": FUNCTION,
    "let": LET,
    "true": TRUE,
    "false": FALSE,
    "if": IF,
    "else": ELSE,
    "return": RETURN
}


def lookup_ident(ident):
    if ident in keywords:
        return keywords[ident]
    return IDENT


class Token:
    def __init__(self, token, literal):
        self.type = token
        self.literal = literal

    def __repr__(self):
        return "Token<type='{}', literal='{}'>".format(self.type, self.literal)


