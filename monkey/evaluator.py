from typing import List

from monkey import ast, object
from monkey.builtins import builtins


def eval(node: ast.Node, env: object.Environment):
    if type(node) is ast.Program:
        return eval_program(node.statements, env)
    elif type(node) is ast.ExpressionStatement:
        return eval(node.expression, env)
    elif type(node) is ast.LetStatement:
        val = eval(node.value, env)
        if is_error(val):
            return val
        env.set(node.name.value, val)
    elif type(node) is ast.Identifier:
        return eval_identifier(node, env)
    elif type(node) is ast.StringLiteral:
        return object.String(value=node.value)
    elif type(node) is ast.FunctionLiteral:
        parameters = node.parameters
        body = node.body
        return object.Function(parameters=parameters, body=body, env=env)
    elif type(node) is ast.CallExpression:
        fun = eval(node.function, env)
        if is_error(fun):
            return fun
        args = eval_expressions(node.arguments, env)
        if len(args) == 1 and is_error(args[0]):
            return args[0]
        return apply_function(fun, args)
    elif type(node) is ast.PrefixExpression:
        right = eval(node.right, env)
        if is_error(right):
            return right
        return eval_prefix_expression(node.operator, right)
    elif type(node) is ast.InfixExpression:
        left = eval(node.left, env)
        if is_error(left):
            return left
        right = eval(node.right, env)
        if is_error(right):
            return right
        return eval_infix_expression(node.operator, left, right)
    elif type(node) is ast.IntegerLiteral:
        return object.Integer(value=node.value)
    elif type(node) is ast.BlockStatement:
        return eval_block_statements(node.statements, env)
    elif type(node) is ast.IfExpression:
        return eval_if_expression(node, env)
    elif type(node) is ast.ReturnStatement:
        val = eval(node.return_value, env)
        return object.ReturnValue(value=val)
    elif type(node) is ast.Boolean:
        return object.TRUE if node.value is True else object.FALSE


def eval_block_statements(statements, env: object.Environment):
    result = None
    for statement in statements:
        result = eval(statement, env)
        if type(result) is object.ReturnValue or type(result) is object.Error:
            return result
    return result


def eval_program(statements, env: object.Environment):
    result = None
    for statement in statements:
        result = eval(statement, env)
        if type(result) is object.ReturnValue:
            return result.value
        elif type(result) is object.Error:
            return result
    return result


def eval_prefix_expression(operator, right):
    if operator is '!':
        return eval_bang_operator_expression(right)
    elif operator is '-':
        return eval_minus_prefix_operator_expression(right)
    else:
        return object.NULL


def eval_bang_operator_expression(right):
    if right == object.TRUE:
        return object.FALSE
    elif right == object.FALSE:
        return object.TRUE
    elif right == object.NULL:
        return object.TRUE
    else:
        return object.FALSE


def eval_minus_prefix_operator_expression(right):
    if type(right) is not object.Integer:
        return object.Error(message="unknown operator: {}{}".format("-", right.object_type))
    else:
        return object.Integer(value=-right.value)


def eval_string_infix_expression(operator, left, right):
    if operator is not "+":
        return object.Error("unknown operator: {} {} {}".format(left.object_type, operator, right.object_type))
        # use python string concat underneath
    return object.String(value=left.value + right.value)


def eval_infix_expression(operator, left, right):
    if type(left) is object.Integer and type(right) is object.Integer:
        return eval_integer_infix_expression(operator, left, right)
    if type(left) is object.String and type(right) is object.String:
        return eval_string_infix_expression(operator, left, right)
    elif operator == '==':
        return native_bool_to_boolean_object(left == right)
    elif operator == '!=':
        return native_bool_to_boolean_object(left != right)
    elif type(left) != type(right):
        return object.Error("type mismatch: {} {} {}".format(left.object_type, operator, right.object_type))
    else:
        return object.Error(message="unknown operator: {} {} {}".format(left.object_type, operator, right.object_type))


def eval_integer_infix_expression(operator, left, right):
    left_val = left.value
    right_val = right.value
    if operator == '+':
        return object.Integer(value=left_val + right_val)
    elif operator == '-':
        return object.Integer(value=left_val - right_val)
    elif operator == '*':
        return object.Integer(value=left_val * right_val)
    elif operator == '/':
        return object.Integer(value=left_val / right_val)
    elif operator == '<':
        return native_bool_to_boolean_object(left_val < right_val)
    elif operator == '>':
        return native_bool_to_boolean_object(left_val > right_val)
    elif operator == '==':
        return native_bool_to_boolean_object(left_val == right_val)
    elif operator == '!=':
        return native_bool_to_boolean_object(left_val != right_val)
    else:
        # an error
        return object.NULL


def eval_identifier(node: ast.Identifier, env: object.Environment):
    val = env.get(node.value)
    if val is not None:
        return val

    if node.value in builtins:
        return builtins[node.value]

    return object.Error("identifier not found: {}".format(node.token.literal))


def native_bool_to_boolean_object(val):
    return object.TRUE if val else object.FALSE


def eval_if_expression(exp: ast.IfExpression, env: object.Environment):
    condition = eval(exp.condition, env)
    if is_error(condition):
        return condition
    if is_truthy(condition):
        return eval(exp.consequence, env)
    elif exp.alternative is not None:
        return eval(exp.alternative, env)
    return object.NULL


def is_truthy(exp):
    if exp == object.NULL:
        return False
    elif exp == object.FALSE:
        return False
    return True


def is_error(maybe):
    return type(maybe) is object.Error


def eval_expressions(expressions: List[ast.Expression], env):
    result = []
    for expression in expressions:
        evaluated = eval(expression, env)
        if is_error(evaluated):
            return [evaluated]
        result.append(evaluated)
    return result


def apply_function(fun, arguments):
    if type(fun) is object.Function:
        extended_env = extend_function_env(fun, arguments)
        evaluated = eval(fun.body, extended_env)
        if type(evaluated) is object.ReturnValue:
            return evaluated.value
        return evaluated
    elif type(fun) is object.Builtin:
        return fun.fn(*arguments)
    return object.Error("not a function")


def extend_function_env(fun: object.Function, arguments: List[ast.Expression]):
    env = object.Environment(outer=fun.env)
    # what about "let x =10; let identity = fn(x){ return x}; fn();"
    # in the above example x should be NULL
    for idx, param in enumerate(fun.parameters):
        env.set(param.value, arguments[idx])
    return env
