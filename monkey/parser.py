from monkey.ast import Program, LetStatement, Identifier, ReturnStatement, ExpressionStatement, IntegerLiteral, \
    PrefixExpression, InfixExpression, Boolean, IfExpression, BlockStatement, FunctionLiteral, Expression, \
    CallExpression
from monkey import token


class Precedence:
    LOWEST = 1
    EQUALS = 2
    LESSGREATER = 3
    SUM = 4
    PRODUCT = 5
    PREFIX = 6
    CALL = 7


precedences = {
    token.EQ: Precedence.EQUALS,
    token.NOT_EQ: Precedence.EQUALS,
    token.LT: Precedence.LESSGREATER,
    token.GT: Precedence.LESSGREATER,
    token.PLUS: Precedence.SUM,
    token.MINUS: Precedence.SUM,
    token.SLASH: Precedence.PRODUCT,
    token.ASTERISK: Precedence.PRODUCT,
    token.LPAREN: Precedence.CALL
}


def parse_identifier(parser):
    return Identifier(parser.curr_token, parser.curr_token.literal)


def parse_integer_literal(parser):
    value = int(parser.curr_token.literal)
    lit = IntegerLiteral(parser.curr_token, value)
    return lit


def parse_prefix_expression(parser):
    expression = PrefixExpression(parser.curr_token, parser.curr_token.literal)
    parser.next_token()

    expression.right = parser.parse_expression(Precedence.PREFIX)
    return expression


def parse_infix_expression(parser, left):
    expression = InfixExpression(parser.curr_token, parser.curr_token.literal)
    expression.left = left
    precedence = parser.curr_precedence()
    parser.next_token()
    expression.right = parser.parse_expression(precedence)
    return expression


def parse_boolean(parser):
    expression = Boolean(parser.curr_token)
    expression.value = parser.curr_token_is(token.TRUE)
    return expression


def parse_grouped_expr(parser):
    parser.next_token()
    exp = parser.parse_expression(Precedence.LOWEST)
    if not parser.expect_peek(token.RPAREN):
        return None
    return exp


def parse_if_expr(parser):
    expression = IfExpression(parser.curr_token)

    if not parser.expect_peek(token.LPAREN):
        return None

    parser.next_token()

    expression.condition = parser.parse_expression(Precedence.LOWEST)

    if not parser.expect_peek(token.RPAREN):
        return None

    if not parser.expect_peek(token.LBRACE):
        return None

    expression.consequence = parser.parse_block_statement()

    if parser.peek_token_is(token.ELSE):
        parser.next_token()
        if not parser.expect_peek(token.LBRACE):
            return None
        expression.alternative = parser.parse_block_statement()

    return expression


def parse_fun_expr(parser):
    lit = FunctionLiteral(parser.curr_token)

    if not parser.expect_peek(token.LPAREN):
        return None

    lit.parameters = parser.parse_fun_params()

    if not parser.expect_peek(token.LBRACE):
        return None

    lit.body = parser.parse_block_statement()

    return lit


def parse_call_expression(parser, function: Expression):
    exp = CallExpression(parser.curr_token, function)
    exp.arguments = parser.parse_call_arguments()

    return exp

class Parser:
    peek_token = None
    curr_token = None
    errors = []

    prefix_parsing_fns = {}
    infix_parsing_fns = {}

    def __init__(self, lexer):
        self.lexer = lexer
        self.next_token()
        self.next_token()
        self.register_prefix(token.IDENT, parse_identifier)
        self.register_prefix(token.INT, parse_integer_literal)
        self.register_prefix(token.BANG, parse_prefix_expression)
        self.register_prefix(token.MINUS, parse_prefix_expression)
        self.register_prefix(token.TRUE, parse_boolean)
        self.register_prefix(token.FALSE, parse_boolean)
        self.register_prefix(token.LPAREN, parse_grouped_expr)
        self.register_prefix(token.IF, parse_if_expr)
        self.register_prefix(token.FUNCTION, parse_fun_expr)


        self.register_infix(token.PLUS, parse_infix_expression)
        self.register_infix(token.MINUS, parse_infix_expression)
        self.register_infix(token.SLASH, parse_infix_expression)
        self.register_infix(token.ASTERISK, parse_infix_expression)
        self.register_infix(token.EQ, parse_infix_expression)
        self.register_infix(token.NOT_EQ, parse_infix_expression)
        self.register_infix(token.LT, parse_infix_expression)
        self.register_infix(token.GT, parse_infix_expression)
        self.register_infix(token.LPAREN, parse_call_expression)

    def next_token(self):
        self.curr_token = self.peek_token
        self.peek_token = self.lexer.next_token()

    def parse_program(self):
        program = Program()

        while self.curr_token.type != token.EOF:
            stmt = self.parse_statement()
            if stmt is not None:
                program.statements.append(stmt)
            self.next_token()

        return program

    def parse_statement(self):
        if self.curr_token_is(token.LET):
            return self.parse_let_statement()
        elif self.curr_token_is(token.RETURN):
            return self.parse_return_statement()
        return self.parse_expression_statement()

    def parse_let_statement(self):
        stmt = LetStatement(self.curr_token)

        if not self.expect_peek(token.IDENT):
            return None

        stmt.name = Identifier(self.curr_token, self.curr_token.literal)

        if not self.expect_peek(token.ASSIGN):
            return None

        self.next_token()

        stmt.value = self.parse_expression(Precedence.LOWEST)
        if self.peek_token_is(token.SEMICOLON):
            self.next_token()

        return stmt

    def parse_expression_statement(self):
        stmt = ExpressionStatement(self.curr_token)
        stmt.expression = self.parse_expression(Precedence.LOWEST)

        if self.peek_token_is(token.SEMICOLON):
            self.next_token()

        return stmt

    def parse_return_statement(self):
        stmt = ReturnStatement(self.curr_token)

        self.next_token()
        stmt.return_value = self.parse_expression(Precedence.LOWEST)

        if self.peek_token_is(token.SEMICOLON):
            self.next_token()

        return stmt

    def parse_block_statement(self):
        block = BlockStatement(self.curr_token)
        self.next_token()

        while not self.curr_token_is(token.RBRACE) and not self.curr_token_is(token.EOF):
            stmt = self.parse_statement()
            if stmt is not None:
                block.statements.append(stmt)
            self.next_token()
        return block

    def parse_expression(self, precedence):
        if self.curr_token.type not in self.prefix_parsing_fns:
            print("No infix expression parser found for ", self.curr_token)
            raise ValueError()
        left_exp = self.prefix_parsing_fns[self.curr_token.type](self)

        while not self.peek_token_is(token.SEMICOLON) and (precedence < self.peek_precedence()):
            if self.peek_token.type in self.infix_parsing_fns:
                infix = self.infix_parsing_fns[self.peek_token.type]
                self.next_token()
                left_exp = infix(self, left_exp)
            else:
                return left_exp
        return left_exp

    def parse_fun_params(self):
        identifiers = []

        if self.peek_token_is(token.RPAREN):
            self.next_token()
            return identifiers

        self.next_token()

        identifiers.append(Identifier(self.curr_token, self.curr_token.literal))

        while self.peek_token_is(token.COMMA):
            self.next_token()
            self.next_token()
            identifiers.append(Identifier(self.curr_token, self.curr_token.literal))

        if not self.expect_peek(token.RPAREN):
            return None

        return identifiers

    def parse_call_arguments(self):
        arguments = []

        if self.peek_token_is(token.RPAREN):
            self.next_token()
            return arguments

        self.next_token()

        arguments.append(self.parse_expression(Precedence.LOWEST))

        while self.peek_token_is(token.COMMA):
            self.next_token()
            self.next_token()
            arguments.append(self.parse_expression(Precedence.LOWEST))

        if not self.expect_peek(token.RPAREN):
            return None

        return arguments


    def expect_peek(self, token_type):
        if self.peek_token_is(token_type):
            self.next_token()
            return True
        return False

    def peek_token_is(self, token_type):
        return self.peek_token.type == token_type

    def curr_token_is(self, token_type):
        return self.curr_token.type == token_type

    def register_prefix(self, token_type, prefix_fn):
        self.prefix_parsing_fns[token_type] = prefix_fn

    def register_infix(self, token_type, infix_fn):
        self.infix_parsing_fns[token_type] = infix_fn

    def peek_precedence(self):
        return precedences.get(self.peek_token.type, Precedence.LOWEST)

    def curr_precedence(self):
        return precedences.get(self.curr_token.type, Precedence.LOWEST)
