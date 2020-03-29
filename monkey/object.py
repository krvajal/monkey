from dataclasses import dataclass
from typing import List

from monkey import ast

INTEGER_OBJ = "INTEGER"
BOOLEAN_OBJ = "BOOLEAN"
NULL_OBJ = "NULL"
RETURN_VALUE_OBJ = "RETURN_VALUE"
ERROR_OBJ = "ERROR"
FUNCTION_OBJ = "FUNCTION"


class Obj:
    def __repr__(self):
        return self.object_type


@dataclass
class Integer(Obj):
    value: int = None
    object_type = INTEGER_OBJ


@dataclass
class Boolean(Obj):
    value: bool = None
    object_type = BOOLEAN_OBJ


class Null:
    object_type = NULL_OBJ


@dataclass
class ReturnValue:
    value: Null = None
    object_type = RETURN_VALUE_OBJ


TRUE = Boolean(value=True)
FALSE = Boolean(value=False)
NULL = Null()


@dataclass
class Error:
    message: str = None
    object_type = ERROR_OBJ


class Environment:
    store = None
    # outer environment
    outer = None

    def __init__(self, outer=None):
        self.store = {}
        self.outer = outer

    def get(self, identifier):
        val = self.store.get(identifier)
        if val is None and self.outer is not None:
            return self.outer.get(identifier)
        return val

    def set(self, identifier, value):
        self.store[identifier] = value
        return value


@dataclass
class Function:
    object_type = FUNCTION_OBJ
    parameters: List[ast.Identifier] = None
    body: ast.BlockStatement = None
    env: Environment = None
