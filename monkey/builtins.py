from monkey import object


def len_builtin(*args):
    if len(args) != 1:
        return object.Error('wrong number of arguments, got= {}, want = 1'.format(len(args)))
    if type(args[0]) is object.String:
        return object.Integer(value=len(args[0].value))
    else:
        return object.Error("argument to 'len' not supported, got {}".format(args[0].object_type))


builtins = {
    "len": object.Builtin(fn=len_builtin)
}
