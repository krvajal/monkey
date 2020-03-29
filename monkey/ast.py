from monkey.token import Token


class Node:
    token: Token = None

    def token_literal(self):
        return self.token.literal

    def __init__(self, token):
        self.token = token

    def __str__(self):
        return self.token_literal()


class Statement:
    def statement_node(self):
        pass


class Expression:
    def expression_node(self):
        pass


class Program:
    statements = None

    def __init__(self):
        self.statements = []

    def token_literal(self):
        if len(self.statements) > 0:
            return self.statements[0].token_literal()
        else:
            return ""

    def __str__(self):
        return "\n".join([str(stmt) for stmt in self.statements])


class Identifier(Node):
    value: str = None

    def __init__(self, token, value):
        super().__init__(token)
        self.value = value

    def __str__(self):
        return self.value


class IntegerLiteral(Node):
    value: int = None

    def __init__(self, token, value):
        super().__init__(token)
        self.value = value

    def __str__(self):
        return str(self.value)


class Boolean(Node):
    value = None


class LetStatement(Node, Statement):
    name: Identifier = None
    value: Expression = None

    def __str__(self):
        rep = self.token_literal() + " "
        rep += str(self.name)
        rep += " = "
        if self.value != None:
            rep += str(self.value)
        rep += ";"
        return rep


class ReturnStatement(Statement, Node):
    return_value: Expression = None

    def __str__(self):
        rep = str(self.token_literal()) + " "
        if self.return_value != None:
            rep += str(self.return_value)
        rep += ";"
        return rep


class ExpressionStatement(Node, Statement):
    expression: Expression = None

    def __str__(self):
        if self.expression != None:
            return str(self.expression) + ";"
        return ""


class PrefixExpression(Node):
    operator: str = None
    right: Expression = None

    def __init__(self, token, operator):
        super().__init__(token)
        self.operator = operator

    def __str__(self):
        rep = "("
        rep += self.operator
        rep += str(self.right)
        rep += ")"
        return rep


class InfixExpression(PrefixExpression):
    left: Expression = None

    def __str__(self):
        rep = "("
        rep += str(self.left)
        rep += " " + self.operator + " "
        rep += str(self.right)
        rep += ")"
        return rep


class BlockStatement(Node):
    statements = None

    def __init__(self, token):
        super().__init__(token)
        self.statements = []

    def __str__(self):
        rep = "{"
        for statement in self.statements:
            rep += str(statement)
        rep += "}"
        return rep


# if (<condition>) <consequence> else <alternative>
class IfExpression(Node):
    condition: Expression = None
    consequence: BlockStatement = None
    alternative: BlockStatement = None

    def __str__(self):
        rep = "if "
        rep += str(self.condition)
        rep += str(self.consequence)
        if self.alternative is not None:
            rep += " else "
            rep += str(self.alternative)
        return rep


#  fn <parameters> <block statement>
class FunctionLiteral(Node):
    parameters = None
    body: BlockStatement = None

    def __init__(self, token):
        super().__init__(token)
        self.parameters = []

    def __str__(self):
        rep = "fn "
        rep += "("
        rep += ", ".join([str(parameter) for parameter in self.parameters])
        rep += ")"
        rep += str(self.body)
        return rep


#  <expression>(<comma separated expressions>)
class CallExpression(Node):
    function: Expression = None
    arguments = None

    def __init__(self, token, function):
        super().__init__(token)
        self.function = function

    def __str__(self):
        args = ", ".join([str(arg) for arg in self.arguments])
        rep = str(self.function)
        rep += "("
        rep += args
        rep += ")"
        return rep
