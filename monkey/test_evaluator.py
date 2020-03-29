from monkey import object, evaluator, parser, lexer


def test_eval_integer_expression():
    tests = [
        {"input": "5", "expected": 5},
        {"input": "10", "expected": 10},
        {"input": "-5", "expected": -5},
        {"input": "-10", "expected": -10},
        {"input": "2 * 2 * 2 * 2 * 2", "expected": 32},
        {"input": "-50 + 100 - 50", "expected": 0},
        {"input": "5 * 2 + 10", "expected": 20},
        {"input": "5 + 2 * 10", "expected": 25},
        {"input": "20 + 2 * -10", "expected": 0},
        {"input": "50 / 2 * 2 + 10", "expected": 60},
        {"input": " 2 * ( 5 + 10 )", "expected": 30},
        {"input": " 3 * 3 * 3  + 10", "expected": 37},
        {"input": "3 * ( 3 * 3 ) + 10", "expected": 37},
        {"input": "(5 + 10 * 2 + 15 / 3) * 2 + -10", "expected": 50},
    ]
    for test in tests:
        evaluated = eval_test(test.get("input"))
        integer_object_test(evaluated, test.get("expected"))


def test_str_literal():
    input = '"Hello World!"'
    evaluated = eval_test(input)
    assert type(evaluated) == object.String, "object is not String, got={}".format(evaluated.object_type)
    assert evaluated.value == "Hello World!"


def test_string_concatenation():
    input = '"Hello" + " "  + "World!"'
    evaluated = eval_test(input)
    assert type(evaluated) == object.String, "object is not String, got={}".format(evaluated.object_type)
    assert evaluated.value == "Hello World!"


def test_eval_boolean_expression():
    tests = [
        {"input": "true", "expected": True},
        {"input": "false", "expected": False},
        {"input": "1 < 2", "expected": True},
        {"input": "1 > 2", "expected": False},
        {"input": "1 == 1", "expected": True},
        {"input": "1 != 1", "expected": False},
        {"input": "1 == 2", "expected": False},
        {"input": "1 != 2", "expected": True},
        {"input": "true ==  true", "expected": True},
        {"input": "false ==  false", "expected": True},
        {"input": "true != false", "expected": True},
        {"input": "false != true", "expected": True},
        {"input": "(1 < 2) == true", "expected": True},
        {"input": "(1 < 2) == false", "expected": False},
        {"input": "(1 > 2) == true", "expected": False},
        {"input": "(1 > 2) == false", "expected": True},
    ]

    for test in tests:
        evaluated = eval_test(test.get("input"))
        bool_object_test(evaluated, test.get("expected"))


def test_bang_operator():
    tests = [
        {"input": "!true", "expected": False},
        {"input": "!false", "expected": True},
        {"input": "!5", "expected": False},
        {"input": "!!true", "expected": True},
        {"input": "!!false", "expected": False},
        {"input": "!!5", "expected": True},
        {"input": "!0", "expected": False}
    ]
    for test in tests:
        evaluated = eval_test(test.get("input"))
        bool_object_test(evaluated, test.get("expected"))


def test_if_else_expression():
    tests = [
        {"input": "if (true) { 10 }", "expected": 10},
        {"input": "if (false) { 10 }", "expected": None},
        {"input": "if (1) { 10 }", "expected": 10},
        {"input": "if (1 < 2) { 10 }", "expected": 10},
        {"input": "if (1 > 2) { 10 }", "expected": None},
        {"input": "if (1 > 2) { 10 } else { 20 }", "expected": 20},
        {"input": "if (1 < 2) { 10 } else { 20 }", "expected": 10}
    ]

    for test in tests:
        evaluated = eval_test(test.get("input"))
        expected = test.get('expected')
        if type(expected) is int:
            integer_object_test(evaluated, expected)
        else:
            assert evaluated == object.NULL, "object is not NULL, got={}"


def test_return_statements():
    tests = [
        {"input": "return 10;", "expected": 10},
        {"input": "return 10; 9;", "expected": 10},
        {"input": "return 2 * 5; 9", "expected": 10},
        {"input": "9; return 2 * 5; 9;", "expected": 10},
        {"input": """
            if( 10 > 1) {
             if(10 > 1) {
                return 10
             }
             return 1;
            }
        """,
         "expected": 10}
    ]

    for test in tests:
        evaluated = eval_test(test.get("input"))
        integer_object_test(evaluated, test.get('expected'))


def test_builtin_functions():
    tests = [
        {"input": 'len("")', "expected": 0},
        {"input": 'len("four")', "expected": 4},
        {"input": 'len("hello world")', "expected": 11},
    ]

    for test in tests:
        evaluated = eval_test(test.get("input"))
        integer_object_test(evaluated, test.get('expected'))


def test_error_handling():
    tests = [
        {"input": "5 + true", "expected": "type mismatch: INTEGER + BOOLEAN"},
        {"input": "5 + true; 5", "expected": "type mismatch: INTEGER + BOOLEAN"},
        {"input": "-true", "expected": "unknown operator: -BOOLEAN"},
        {"input": "true  + false", "expected": "unknown operator: BOOLEAN + BOOLEAN"},
        {"input": "5; true  + false; 5", "expected": "unknown operator: BOOLEAN + BOOLEAN"},
        {"input": "if (10 > 1) { true + false; }", "expected": "unknown operator: BOOLEAN + BOOLEAN"},
        {"input": """
        if (10 > 1) {
          if (10 > 1) {
            return true + false;
          }
        return 1; }
        """,
         "expected": "unknown operator: BOOLEAN + BOOLEAN"},
        {
            "input": """
           if (10 > 1) {
             if (10 > 1) {
               true + false;
               2;
             }
           return 1; }
           """,
            "expected": "unknown operator: BOOLEAN + BOOLEAN",
        },
        {
            "input": '"Hello" - "World"',
            "expected": "unknown operator: STRING - STRING"
        }]

    for test in tests:
        evaluated = eval_test(test.get("input"))
    assert type(evaluated) is object.Error, "not error object returned"
    assert evaluated.message == test.get('expected'), "wrong error message"


def test_let_statement():
    tests = [
        {"input": "let a = 5; a;", "expected": 5},
        {"input": "let a = 5 * 5; a;", "expected": 25},
        {"input": "let a = 5; let b = a; b", "expected": 5},
        {"input": "let a = 5; let b = a; let c = a + b + 5; c", "expected": 15},
    ]

    for test in tests:
        evaluated = eval_test(test.get("input"))
        print("evaluated", evaluated)
        integer_object_test(evaluated, test.get("expected"))


def test_function_object():
    input = "fn(x){ x + 2};"
    evaluated = eval_test(input)
    assert type(evaluated) == object.Function, "object is not a function, got = {}".format(evaluated.object_type)
    assert len(evaluated.parameters) == 1, 'function has wrong parameters, parameters = {}'.format(evaluated.parameters)


def test_function_application():
    tests = [
        {"input": "let identity = fn(x) { x; }; identity(5);", "expected": 5},
        {"input": "let identity = fn(x) { return x; }; identity(5);", "expected": 5},
        {"input": "let double = fn(x) { x * 2; }; double(5);", "expected": 10},
        {"input": "let add = fn(x, y) { x + y; }; add(5, 5);", "expected": 10},
        {"input": "let add = fn(x, y) { x + y; }; add(5 + 5, add(5, 5));", "expected": 20},
        {"input": "fn(x) { x; }(5)", "expected": 5},
    ]

    for test in tests:
        evaluated = eval_test(test.get("input"))
        print("evaluated", evaluated)
        integer_object_test(evaluated, test.get("expected"))


def eval_test(input):
    l = lexer.Lexer(input)
    p = parser.Parser(l)
    program = p.parse_program()
    return evaluator.eval(program, object.Environment())


def integer_object_test(obj, expected):
    if type(obj) is object.Integer:
        assert obj.value == expected
    else:
        assert False, "object is not integer, got:  {}".format(obj.object_type)


def bool_object_test(obj, expected):
    if type(obj) is object.Boolean:
        assert obj.value == expected
    else:
        assert False, "object is not boolean"
