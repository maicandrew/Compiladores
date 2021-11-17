
from sly import Lexer

class Tokenizer(Lexer):
    
    
    keywords = {'program', 'if', 'then', 'else', 'of', 'while', 'do', 'begin',
                'end', 'read', 'write','var', 'array', 'procedure', 'writeln', 
                'or', 'and', 'readln'}
    
    literals = { '(' , ')', '[', ']', '.', ',', ';', ':', '<', '>', '=',}
    
    tokens = { 
            * {kw.upper() for kw in keywords},
            IDENTIFIER, CHARACTER_CONSTANT, 
            NOT, PLUS, TIMES, MINUS, ASSIGN, LOGIC_CONSTANT, REAL, 
            PREDEFINED_TYPE, DIV, MOD,  RANGE, DIV_REAL, DIFF, LE, GE, 
            INTEGER_CONSTANT, 
            }
    
   
    
    def __init__(self):
        self.hayError = False
        
    ignore = " \t"
    ignore_comment = r'\(\*(.|[\r\n])*?\*\)'
    ignore_coment2 = r'\{(.|[\r\n])*?\}'
    MINUS = r'-'
    PLUS = r'\+'
    TIMES = r'\*'
    DIV = r'[dD][iI][vV]'
    DIV_REAL = r'/'
    RANGE = r'\.\.'
    MOD = r'[mM][oO][dD]'
    ASSIGN = r':='
    DIFF = r'<>'
    LE = r'<='
    GE = r'>='
    NOT = r'[nN][oO][tT]'
    CHARACTER_CONSTANT = r"'[^']*'"
    #STRING = r"'.*?'"
    REAL = r'[0-9]+(\.[0-9]+)([eE][\+-]?[0-9]+)?|[0-9]+(\.[0-9]+)?([eE][\+-]?[0-9]+)'
    LOGIC_CONSTANT = r'[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]'
    
    @_(r'[0-9]+')
    def INTEGER_CONSTANT(self, t):
        if len(t.value) > 1 and t.value[0] == '0':
            print ("Error in line", self.lineno, 
                   ": integers cant start with '0'")
            self.hayError = True
        else:
            t.value = int(t.value)
            return t
        
    
    
    
    @_(r'[iI][nN][tT][eE][gG][eE][rR]', r'[rR][eE][aA][lL]',
       r'[cC][hH][aA][rR]', r'[bB][oO][oO][lL][eE][aA][nN]')  
    def PREDEFINED_TYPE(self, t):
        return t
        
    
    @_(r'[a-zA-Z][a-zA-Z0-9]*')
    def IDENTIFIER(self, t):
        if(t.value.lower() in self.keywords):
            t.type = t.value.upper()
        return t
    
    
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')
        
    
    def error(self, t):
        print ("ERROR: Ilegal character", t.value[0], "in line", self.lineno)
        if t.value[0] == '{':
            print ("Quizas queria cerrar un comentario que abrio en esta linea")
        self.hayError = True
        self.index += 1



class controlLexer:
    
    
    def __init__(self):
        self.lexer = Tokenizer()
    
    
    def showData(self, data):
        print ("\tAnalyzing: ")
        print (data)

    
    def showTokens(self, data):
        for tok in self.lexer.tokenize(data):
            print (tok)
        if not self.lexer.hayError:
            print("Compilacion exitosa!")
            
            
    def tokenizar(self, data):
        tokenized = self.lexer.tokenize(data)
        for tok in tokenized:
            pass
        if not self.lexer.hayError:
            print("Compilacion exitosa!")


if __name__ == "__main__":
    c = Tokenizer()
    
    print (c.tokens)
    print (type(c.tokens))
    