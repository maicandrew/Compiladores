from sly import Parser
from PasLex import PascalLexer
from ast import *
from grafo import *

class PascalParser(Parser):

    debugfile = "parser.out"
    tokens = PascalLexer.tokens

    @_('PROGRAM ID ";" block "."')
    def program(self, p):
        return ProgramStatement(p[1], p[3])

    @_('variable_declaration_part function_declaration_part procedure_declaration_part statement_part')
    def block(self, p):
        return BlockStatement(p[0], p[1], p[2], p[3])

    @_('empty')
    def variable_declaration_part(self, p):
        return [VarDeclarationNull(p[0])]

    @_('VAR variable_declaration_list')
    def variable_declaration_part(self, p):
        return p[1]

    @_('variable_declaration ";"')
    def variable_declaration_list(self, p):
        return p[0]

    @_('variable_declaration_list variable_declaration ";"')
    def variable_declaration_list(self, p):
        p[0].extend(p[1])
        return p[0]

    @_('ID_list ":" type')
    def variable_declaration(self, p):
        list = []
        for i in p[0]:
            list.append(VarDeclarationPascal(i, p[2], p.lineno))
        return list

    @_('ID_list "," ID')
    def ID_list(self, p):
        p[0].append(SimpleLocation(p[2]))
        return p[0]

    @_('ID')
    def ID_list(self, p):
        return [SimpleLocation(p[0])]

    @_('simple_type')
    def type(self, p):
        return p[0]

    @_('array_type')
    def type(self, p):
        return p[0]

    @_('ARRAY "[" index_range "]" OF simple_type')
    def array_type(self, p):
        return ArrayType(p[2], p[5])

    @_('CONST_INTEGER RANGE CONST_INTEGER')
    def index_range(self, p):
        return [int(p[0]), int(p[2])]

    @_('type_identifier')
    def simple_type(self, p):
        return SimpleType(p[0])

    @_('ID')
    def type_identifier(self, p):
        return p[0]

    @_('predefined_type')
    def type_identifier(self, p):
        return p[0]

    @_('INTEGER')
    def predefined_type(self, p):
        return p[0]

    @_('BOOLEAN')
    def predefined_type(self, p):
        return p[0]

    @_('FLOAT')
    def predefined_type(self, p):
        return p[0]

    @_('empty')
    def procedure_declaration_part(self, p):
        return []

    @_('empty')
    def function_declaration_part(self, p):
        return []

    @_('function_declaration_part function_declaration ";"')
    def function_declaration_part(self, p):
        p[0].append(p[1])
        return p[0]

    @_('FUNCTION ID "(" variable_declaration_list_function ")" ":" type ";" block')
    def function_declaration(self, p):
        return FunctionDeclaration(p[1], p[3], p[6], p[8], p.lineno)

    @_('FUNCTION ID "(" ")" ":" type ";" block')
    def function_declaration(self, p):
        return FunctionDeclaration(p[1], [], p[5], p[7], p.lineno)

    @_('variable_declaration')
    def variable_declaration_list_function(self, p):
        return p[0]

    @_('variable_declaration_list_function ";" variable_declaration')
    def variable_declaration_list_function(self, p):
        for v in p[2]:
            p[0].append(v)
        return p[0]

    @_('procedure_declaration_part procedure_declaration ";"')
    def procedure_declaration_part(self, p):
        p[0].append(p[1])
        return p[0]

    @_('PROCEDURE ID ";" block')
    def procedure_declaration(self, p):
        return ProcedureStatement(p[1], p[3], p.lineno)

    @_('compound_statement')
    def statement_part(self, p):
        return p[0]

    @_('BEGIN statement_list END')
    def compound_statement(self, p):
        return StatementList(p[1])

    @_('statement')
    def statement_list(self, p):
        return [p[0]]

    @_('statement_list ";" statement')
    def statement_list(self, p):
        p[0].append(p[2])
        return p[0]

    @_('simple_statement')
    def statement(self, p):
        return p[0]

    @_('structured_statement')
    def statement(self, p):
        return p[0]

    @_('assignment_statement')
    def simple_statement(self, p):
        return p[0]

    @_('procedure_statement')
    def simple_statement(self, p):
        return p[0]

    @_('read_statement')
    def simple_statement(self, p):
        return p[0]

    @_('write_statement')
    def simple_statement(self, p):
        return p[0]

    @_('variable ASSIGN expression')
    def assignment_statement(self, p):
        return VariableAssign(WriteLocation(p[0]), p[2], p.lineno)

    @_('ID')
    def procedure_statement(self, p):
        return p[0]

    @_('READ "(" variable_list ")"')
    def read_statement(self, p):
        list = []
        for i in p.variable_list:
            list.append(WriteLocation(i.name))
        return ReadStatement(list, p.lineno)

    @_('variable')
    def variable_list(self, p):
        return [SimpleLocation(p[0])]

    @_('variable_list "," variable')
    def variable_list(self, p):
        p[0].append(SimpleLocation(p.variable))
        return p[0]

    @_('WRITE "(" expression_list ")"')
    def write_statement(self, p):
        return WriteStatement(p.expression_list, p.lineno)

    @_('expression')
    def expression_list(self, p):
        return [p[0]]

    @_('expression_list "," expression')
    def expression_list(self, p):
        p[0].append(p[2])
        return p[0]

    @_('statement_part')
    def structured_statement(self,p):
        return p[0]

    @_('if_statement', 'if_else_statement')
    def structured_statement(self,p):
        return p[0]

    @_('while_statement')
    def structured_statement(self,p):
        return p[0]

    @_('IF expression THEN statement')
    def if_statement(self,p):
        return IfStatement(p.expression, p[3], p.lineno)

    @_('IF expression THEN statement ELSE statement')
    def if_else_statement(self,p):
        return IfElseStatement(p.expression, p[3], p[5], p.lineno)

    @_('WHILE expression DO statement')
    def while_statement(self,p):
        return WhileStatement(p.expression, p.statement, p.lineno)

    @_('simple_expression')
    def expression(self,p):
        return ExpressionList(p[0])

    @_('simple_expression relational_operator simple_expression')
    def expression(self,p):
        return BinOp(p[1], p[0], p[2])

    @_('term')
    def simple_expression(self, p):
        return p[0]

    @_('sign term')
    def simple_expression(self,p):
        return UnaryOp(p[0], p[1])

    @_('simple_expression adding_operator term')
    def simple_expression(self,p):
        return BinOp(p[1], p[0], p[2])

    @_('factor')
    def term(self,p):
        return p.factor

    @_('term multiplying_operator factor')
    def term(self,p):
        return BinOp(p[1], p[0], p[2])

    @_('ID "(" expression_list ")"')
    def factor(self, p):
        return FuncCall(p[0], p[2], p.lineno)

    @_('variable')
    def factor(self,p):
        return ReadLocationFactor(p[0]) #Expression

    @_('constant')
    def factor(self,p):
        return FactorConstant(p[0])

    @_('"(" expression ")"')
    def factor(self,p):
        return p[1]

    @_('NOT factor')
    def factor(self,p):
        return p[1]

    @_('EQ')
    def relational_operator(self,p):
        return p[0]

    @_('NE')
    def relational_operator(self,p):
        return p[0]

    @_('LT')
    def relational_operator(self,p):
        return p[0]

    @_('LE')
    def relational_operator(self,p):
        return p[0]

    @_('GT')
    def relational_operator(self,p):
        return p[0]

    @_('GE')
    def relational_operator(self,p):
        return p[0]

    @_('PLUS')
    def sign(self,p):
        return str(p[0])

    @_('MINUS')
    def sign(self,p):
        return str(p[0])

    @_('PLUS')
    def adding_operator(self,p):
        return str(p[0])

    @_('MINUS')
    def adding_operator(self,p):
        return str(p[0])

    @_('OR')
    def adding_operator(self,p):
        return str(p[0])

    @_('TIMES')
    def multiplying_operator(self,p):
        return str(p[0])

    @_('DIVIDE')
    def multiplying_operator(self,p):
        return str(p[0])

    @_('DIV')
    def multiplying_operator(self,p):
        return str(p[0])

    @_('AND')
    def multiplying_operator(self,p):
        return str(p[0])

    @_('ID')
    def variable(self,p):
        return p[0] #str

    @_('indexed_variable')
    def variable(self,p):
        return p[0] #str

    @_('ID "[" expression "]"')
    def indexed_variable(self,p):
        retorno = p[0]
        return retorno #str

    @_('CONST_INTEGER')
    def constant(self,p):
        return IntegerLiteral(int(p[0]))

    @_('REAL')
    def constant(self,p):
        return RealLiteral(float(p.REAL))

    @_('CONST_CHARACTER')
    def constant(self,p):
        return CharLiteral(str(p.CONST_CHARACTER))

    @_('CONST_BOOL')
    def constant(self,p):
        return BoolLiteral(str(p[0]))

    @_('')
    def empty(self,p):
        pass


def parse(source):
    lexer = PascalLexer()
    parser = PascalParser()
    ast = parser.parse(lexer.tokenize(source))
    return ast

def mostrarArbol(file):
    ast = parse(file)
    for depth, node in flatten(ast):
        print('%s%s' % (' '*(4*depth), node))
    a = DotVisitor()
    a.visit(ast)
    print(a)

def main():
    file = open("P9.pas", "r")
    text = (file.read())
    mostrarArbol(text)

if __name__ == '__main__':
    main()
