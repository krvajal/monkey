from monkey import token


class Lexer:
    def __init__(self, input):
        self.input = input
        # current position in input
        self.position = 0
        # current reading position in input
        self.readPosition = 0
        # current char under exam
        self.ch = 0
        # read the first char
        self.read_char()

    def read_char(self):
        if self.readPosition >= len(self.input):
            self.ch = 0
        else:
            self.ch = self.input[self.readPosition]
        self.position = self.readPosition
        self.readPosition += 1

    def next_token(self):
        tok = None

        # eat all the whitespace
        self._skip_whitespace()

        if self.ch == '"':
            literal = self.read_string()
            tok = token.Token(token.STRING, literal)

        elif self.ch == '=':
            if self._peek_char() == "=":
                self.read_char()
                tok = token.Token(token.EQ, "==")
            else:
                tok = token.Token(token.ASSIGN, self.ch)
        elif self.ch == ';':
            tok = token.Token(token.SEMICOLON, self.ch)
        elif self.ch == '(':
            tok = token.Token(token.LPAREN, self.ch)
        elif self.ch == ')':
            tok = token.Token(token.RPAREN, self.ch)
        elif self.ch == ',':
            tok = token.Token(token.COMMA, self.ch)
        elif self.ch == 0:
            tok = token.Token(token.EOF, self.ch)
        elif self.ch == '{':
            tok = token.Token(token.LBRACE, self.ch)
        elif self.ch == '}':
            tok = token.Token(token.RBRACE, self.ch)
        elif self.ch == '+':
            tok = token.Token(token.PLUS, self.ch)
        elif self.ch == '-':
            tok = token.Token(token.MINUS, self.ch)
        elif self.ch == '!':
            if self._peek_char() == "=":
                self.read_char()
                tok = token.Token(token.NOT_EQ, "!=")
            else:
                tok = token.Token(token.BANG, self.ch)
        elif self.ch == '*':
            tok = token.Token(token.ASTERISK, self.ch)
        elif self.ch == '<':
            tok = token.Token(token.LT, self.ch)
        elif self.ch == '>':
            tok = token.Token(token.GT, self.ch)
        elif self.ch == '/':
            tok = token.Token(token.SLASH, self.ch)
        else:
            if self._is_letter(self.ch):
                literal = self._read_identifier()
                type = token.lookup_ident(literal)
                tok = token.Token(type, literal)
                # early exit needed here, to avoid the call for self.read_char
                return tok
            elif self._is_digit(self.ch):
                tok = token.Token(token.INT, self._read_number())
                return tok
            else:
                tok = token.Token(token.ILLEGAL, self.ch)

        self.read_char()

        return tok

    # returns True is a character is considered a letter
    def _is_letter(self, ch):
        if ch == 0:
            return False
        return ord('a') <= ord(ch) and ord(ch) <= ord('z') or ord('A') <= ord(ch) and ord(ch) <= ord('Z') or ch == '_'

    # returns True is the character is a digit, according to
    # the lang rules
    def _is_digit(self, ch):
        if ch == 0:
            return False
        return ord('0') <= ord(ch) and ord(ch) <= ord('9')

    def _read_identifier(self):
        position = self.position
        while self._is_letter(self.ch):
            self.read_char()
        return self.input[position:self.position]

    def _read_number(self):
        position = self.position
        while self._is_digit(self.ch):
            self.read_char()
        return self.input[position:self.position]

    def _skip_whitespace(self):
        while self.ch == ' ' or self.ch == '\n':
            self.read_char()

    def _peek_char(self):
        if self.readPosition >= len(self.input):
            return 0
        return self.input[self.readPosition]

    def read_string(self):
        position = self.position + 1
        while True:
            self.read_char()
            if self.ch == '"' or self.ch == 0:
                break
        return self.input[position:self.position]