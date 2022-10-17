from common_functions import scope_operators, operators

class Lisp:
    '''Generate abstract syntax tree and evaluate languages expressions'''
    
    def __init__(self, code, is_path=False):
        self.code = code
        if is_path:
            self.load_from_file()

        self.code = self.normalize_str(self.code)
        self.ast = self.get_ast(self.code)
        self.operators = operators
        self.scope_operators = scope_operators
        self.variables = dict()

    def load_from_file(self):
        '''load code from file'''
        path = self.code
        code_file = open(path)
        self.code = code_file.read()
        code_file.close()

    def normalize_str(self, string):
        '''normalize string input'''
        str_norm = []
        last_c = None
        comment = False

        for c in string:
            if c == ';':
                comment = True

            if c == '\n' and comment:
                comment = False

            if comment:
                continue

            if c.isalnum():
                if last_c.isalnum():
                    str_norm[-1] += c
                else:
                    str_norm.append(c)
            elif not c.isspace():
                str_norm.append(c)
            last_c = c

        return str_norm

    def get_ast(self, input_norm):
        '''Generate abstract syntax tree from normalized input'''
        ast = []
        i = 0

        while i < len(input_norm):
            symbol = input_norm[i]
            
            if symbol == '(':
                list_content = []
                match_ctr = 1
                while match_ctr != 0:
                    i += 1
                    if i >= len(input_norm):
                        raise ValueError("Invalid input: Unmatched open parenthesis.")
                    symbol = input_norm[i]
                    if symbol == '(':
                        match_ctr += 1
                    elif symbol == ')':
                        match_ctr -= 1
                    if match_ctr != 0:
                        list_content.append(symbol)             
                ast.append(self.get_ast(list_content))
            elif symbol == ')':
                    raise ValueError("Invalid input: Unmatched close parenthesis.")
            else:
                try:
                    ast.append(int(symbol))
                except ValueError:
                    ast.append(symbol)
            i += 1
        
        return ast

    def evaluate(self):
        for node in self.ast:
            self.evaluate_node(node)

    def evaluate_node(self, node):
       '''evaluate a node of type <operator> <expr>...<expr-n>'''
       operator = node[0]
       node = node[1:]

       if operator == 'fun':
           return self.scope_operators[operator](self, node)

       if not operator in self.operators and not operator in self.scope_operators:
           node.insert(0, operator)
           return tuple(node)

       for index, expr in enumerate(node):
           if isinstance(expr, list):
               node[index] = self.evaluate_node(expr)

           if isinstance(expr, str) and expr in self.variables and operator != ':':
               node[index] = self.variables[expr]

       if operator in self.operators:
           operator = self.operators[operator]
       
       if operator in self.scope_operators:
           operator = self.scope_operators[operator]
           return operator(self, node)

       
       return operator(node)


l2 = Lisp('./example3.lsp', True)
l2.evaluate()

