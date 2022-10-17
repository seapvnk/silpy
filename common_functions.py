def replace_ast_with_args(scope, args_dict, ast):
    for index, node in enumerate(ast):
        if isinstance(node, list):
            ast[index] = replace_ast_with_args(scope, args_dict, node)
        else:
            if node in args_dict:
                ast[index] = args_dict[node]
                continue
            
            if node in scope.variables:
                ast[index] = scope.variables[node]
                continue
           
            if node in scope.operators or node in scope.scope_operators or str(node).isnumeric():
                ast[index] = node
            else:
                raise Exception(f'Undefined variable or function <{node}>')
    
    return ast


def create_function(scope, args, expression):
    '''create a function'''
    args_info = dict()
    arg_pos = 0

    for arg in args:
        args_info[arg_pos] = args[0]
        args = args[1:]
        arg_pos += 1

    def cfunction(fun_args):
        args_dict = args_info
        args_rep = dict()

        for index, argv in enumerate(fun_args):
            args_dict[args_dict[index]] = argv

        replaced_ast = replace_ast_with_args(scope, args_dict, expression)
        
        return scope.evaluate_node(expression)

    return cfunction

def define_variable(scope, args):
    '''define a variable'''
    name, value = args
    if name in scope.variables:
        raise Exception(f'Variable <{name} already defined')

    scope.variables[name] = value

def define_function(scope, args):
    '''define a function'''
    name, values, expression = args
    if name in scope.operators:
        raise Exception(f'Function <{name}> is already defined.')

    scope.operators[name] = create_function(scope, values, expression)
   
def reassign_variable(scope, args):
    name, value = args
    if not name in scope.variables:
        raise Exception(f'Variable <{name}> not defined')
    
    scope.variables[name] = value

scope_operators = {
    'let': define_variable,
    'fun': define_function,
    ':': reassign_variable,
}

def unfold(fn, args):
    for arg in args: 
        fn(arg)

def apply_operation(fn, numbers, acc=0):
    if len(numbers) == 1:
        return fn(acc, numbers[0])

    return apply_operation(fn, numbers[1:], fn(numbers[0], acc))

def flow_if(args):
    if (len(args) < 2):
        raise Exception('If expression requires at least two arguments')

    if (len(args) == 2):
        if (args[0]):
            return args[1]
    else:
        return args[1] if args[0] else args[2]

def flow_cond(args):
    for cond, expr in args:
        if cond:
            return expr

operators = {
    # aritmetic
    '+': lambda args: sum(args),
    '-': lambda args: apply_operation(lambda a, b: a - b, args),
    '/': lambda args: apply_operation(lambda a, b: a / b, args, 1),
    '*': lambda args: apply_operation(lambda a, b: a * b, args, 1),
    '**': lambda args: apply_operation(lambda a, b: a ** b, args, 1),
    
    # lang functions
    'print': lambda args: unfold(print, args),
    '~': lambda args: tuple(args),
    '#': lambda args: len(args[0]),

    # comparison
    '=': lambda args: args[0] == args[1],

    'neq': lambda args: not args[0] == args[1],
    '≠': lambda args: not args[0] == args[1],
    
    '|': lambda args: args[0] or args[1],
    '∨': lambda args: args[0] or args[1],

    '&': lambda args: args[0] and args[1],
    '∧': lambda args: args[0] and args[1],
    
    '>': lambda args: args[0] > args[1],
    '≥': lambda args: args[0] >= args[1],
    'moe': lambda args: args[0] >= args[1],

    '<': lambda args: args[0] < args[1],
    '≤': lambda args: args[0] <= args[1],
    'loe': lambda args: args[0] <= args[1],
    
    # flow control
    'if': flow_if,
    'cond': flow_cond
}

