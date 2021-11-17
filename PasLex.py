from sly import Lexer

class PascalLexer(Lexer):
    #Set of keywords
    keywords = {'program', 'var', 'array', 'of',
                'procedure', 'begin', 'end', 'read',
                'write', 'if', 'then', 'else', 'while',
                'do', 'not', 'or', 'and', 'integer', 'float', 'boolean',
                'function', 'div'}

    # Set of token names.   This is always required
    tokens = {  *{kw.upper() for kw in keywords},
                ID, PLUS, MINUS, TIMES, DIVIDE, ASSIGN, EQ, LE, LT,
                GE, GT, NE, CONST_CHARACTER, CONST_INTEGER,CONST_BOOL, RANGE, REAL}

    literals = {'(', ')', '[', ']', '.', ',', ';', ':'}

    # String containing ignored characters between tokens
    ignore = ' \t'
    ignore_comment = r'\#.*|{([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*?}|\(\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*?\*\)'

    # Regular expression rules for tokens
    error_OCTAL = r'0[0-7]+'
    PLUS    = r'\+'
    MINUS   = r'-'
    TIMES   = r'\*'
    DIVIDE  = r'/'
    EQ = r'='
    ASSIGN  = r':='
    LE = r'<='
    NE = r'<>'
    LT = r'<'
    GE = r'>='
    GT = r'>'
    RANGE = r'\.\.'
    CONST_CHARACTER = r'\'[^\']*\''
    CONST_BOOL = r'"TRUE"|"FALSE"'

    @_(r'[-\+]?[0-9]*\.[0-9]+([eE][-\+]?[0-9]+)?')
    def REAL(self, p):
        return p

    @_(r'\d+')
    def CONST_INTEGER(self, p):
        return p

    # Special cases
    @_(r'[a-zA-Z][a-zA-Z0-9_]*')
    def ID (self,t):
        if t.value.lower() in self.keywords:
            t.type = t.value.upper()
        return t

    # Numero de linea
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print ("Linea %d: caracter incorrecto %r" % (self.lineno, t.value[0]))
        self.index += 1
    #Numeros en formato octal
    def error_OCTAL(self, t):
        print ("Linea %d: Formato de numero incorrecto" % (self.lineno))
        self.index += 1

if __name__ == '__main__':
    data = '''no hay nada que ver aqui'''
    lexer = PascalLexer()
    for tok in lexer.tokenize(data):
        print('type=%r, value=%r' % (tok.type, tok.value))
