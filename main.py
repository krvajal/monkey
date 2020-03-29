from monkey import lexer, token, repl, parser

# def print_list(items):
#   for item in items:
#     print(item)
#   print("")

# def run_lexer(input):
#   print("running lexer for input: {}".format(input))
#   l = lexer.Lexer(input)
#   t = l.next_token()
#   tokens = [t]
#   while t.token != token.EOF:
#     t = l.next_token()
#     tokens.append(t)

#   return tokens

# print_list(run_lexer("=+(){},;let"))
# print('')
# print_list(run_lexer("""let five = 5; let ten = 10;

# let add = fn(x, y) { x + y; };

# let result = add(five, ten); !-/*5; 5
# """))
# print('')
# print_list(run_lexer("""
# let five = 5; let ten = 10;

# let add = fn(x, y) { x + y; };

# let result = add(five, ten); !-/*5; 5 < 10 > 5;

# if (5 < 10) { return true; } else {
#  return false;
# }
# """))

repl.start()

# str = """
# 5 + 5;
# -a + b;
# 5 - 5;
# 5 * 5;
# 5 / 5;
# -a + b;
# a + b * c;
# 5 == 5;
# 5 != 5;
# -a * b;
# !-a;
# a + b + c;
# a + b - c;
# a * b * c;
# a * b / c;
# a + b * c + d/e - f;
# 3 + 4; -5 * 5;
# 5 > 4 ==  3 < 4;
# 5 < 4 != 3 > 4;
# 3 + 4 * 5 == 3*1 + 4 * 5;
# true;
# false;
# let foobar = true;
# return false;
# return a + b;
# 1 + (2 + 3) + 4
# !2
# (5 + 5) * 2
# 2 * 5
# - ( - 5 + 5)
# - 3 + 10
# !(true == true)
# if(x<y) {10}
# """
# str = """if(x<y) {
#     10
#     return a + b;
# } else {
#     20;
#    return 2 + 4;
# }"""
#
# str = """
# a + add(b * c) + d;
# add(a, b, 1, 2 * 3, 4 + 5, add(6, 7 * 8));
# add(a + b + c * d / f + g)
# """
# p = parser.Parser(lexer.Lexer(str))
#
# program = p.parse_program()
#
# print(program)