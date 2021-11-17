# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 14:25:32 2018

@author: utp
"""
from impGraphViz import DotVisitor
from sly import Parser
import errors
from paslex import Tokenizer
from ast import *

class PasParser(Parser):

    tokens = Tokenizer.tokens
    hayError = False
    debugfile = 'parser.out'

    precedence = precedence = (
       ('right', ASSIGN),
       ('left', '<', '>', GE, LE),
       ('left', PLUS, MINUS, OR),
       ('left', TIMES, DIV, AND),
       ('left', "(", ")")
    )
    def __init__(self):
        self.names = {}

    @_('PROGRAM IDENTIFIER ";" block "."')
    def programa(self, p):
            return ProgramStatement(p[1], p[3]) #Statement

    @_('variable_declaration_part procedure_declaration_part statement_part')
    def block(self, p):
        return BlockStatement(p[0], p[1], p[2]) #Statement

    @_('empty')
    def variable_declaration_part(self, p):
        return [VarDeclarationNull(p[0])]  #[Statement]

    @_('VAR variable_declaration_list')
    def variable_declaration_part(self, p):
        return p[1] #[Statement]

    @_('variable_declaration ";"')
    def variable_declaration_list(self, p):
        return [p[0]] #Statement
    
    @_('variable_declaration_list variable_declaration ";"')
    def variable_declaration_list(self, p):
        p[0].append(p[1])
        return p[0]#[Statement]
    
    @_('identifier_list ":" typee')
    def variable_declaration(self, p):
        return VarDeclarationPascal(p[0], p[2]) #Statement
    
    @_('IDENTIFIER')
    def identifier_list(self, p):
        return [SimpleLocation(p.IDENTIFIER)] #Location
    
    @_('identifier_list "," IDENTIFIER')
    def identifier_list(self, p):
        p.identifier_list.append(SimpleLocation(p[2])) #[Location]
        #print(p.identifier_list)
        return p.identifier_list
    
    @_('array_type', 'simple_type')
    def typee(self, p):
        return p[0] #DataType
    
    @_('ARRAY "[" index_range "]" OF simple_type')
    def array_type(self, p):
        return ArrayType(p.index_range, p.simple_type) #DataType
    
    @_('INTEGER_CONSTANT RANGE INTEGER_CONSTANT')
    def index_range(self, p):
        return [p[0], p[1], p[2]] #Una lista que tiene el rango
    
    @_('type_identifier')
    def simple_type(self, p):
        return SimpleType(p[0]) #Encapsulacion para que sea data type
    
    @_('PREDEFINED_TYPE', 'IDENTIFIER')
    def type_identifier(self, p):
        return p[0] #Aun no tiene clase en ast
    
    @_('empty')
    def procedure_declaration_part(self,  p):
        return [] #[]
        
    @_('procedure_declaration_part procedure_declaration ";"')
    def procedure_declaration_part(self,  p):
        p[0].append(p[1]) #[Statement]
        return p[0]
    
    @_('PROCEDURE IDENTIFIER ";" block')
    def procedure_declaration(self, p):
        return ProcedureStatement(p[1], p[3]) #Statement
    
    @_('compound_statement')
    def statement_part(self, p):
        return p[0] #Statement
    
    @_('BEGIN statement_list END')
    def compound_statement(self, p):
        return ListStatement(p[1]) #Statement
    
    @_('statement')
    def statement_list(self, p):
        return [p[0]] #Statement
    
    @_('statement_list ";" statement')
    def statement_list(self, p):
        p[0].append(p[2]) 
        return p[0] #[Statement]
    
    @_('structured_statement', 'simple_statement')
    def statement(self,  p):
        return p[0] #Statement
    
    @_('write_statement', 'read_statement', 'procedure_statement',
       'assignement_statement')
    def simple_statement(self, p):
        return p[0] #Todos son statement
    
    @_('variable ASSIGN expression')
    def assignement_statement(self, p):
        #print (str(p[0]) + " := " + str(p.expression))
        return VarAssign(p[0], p[2]) #Statement
    
    @_('procedure_identifier')
    def procedure_statement(self, p):
        return ProcedureIdentifier(p[0]) #Statement, encapsulado
    
    @_('IDENTIFIER')
    def procedure_identifier(self, p):
        return p[0] #No tiene clase
    
    @_('READ "(" variable_list ")"')
    def read_statement(self, p):
        return ReadLocationList(p[2]) #Statement, no he definido statement
    
    @_('READLN "(" variable_list ")"')
    def read_statement(self, p):
        return ReadLocationList(p[2]) #Statement, no he definido statement
    
    @_('input_variable')
    def variable_list(self, p):
        return [p[0]] #Expression
    
    @_('variable_list "," input_variable')
    def variable_list(self, p):
        p[0].append(p[2]) 
        return p[0] #[Expression]
    
    @_('variable')
    def input_variable(self, p):
        return ReadLocation(p[0]) #Expression, no he definido statement
    
    @_('WRITE "(" expression_list ")"')
    def write_statement(self, p):
        return WriteStatement(p[2]) #Statement, no he definido statement
    
    @_('WRITELN "(" expression_list ")"')
    def write_statement(self, p):
        return WriteStatement(p[2]) #Statement, no he definido statement
    
    
    @_('output_value')
    def expression_list(self, p):
        return [p[0]] #Expression
    
    @_('expression_list "," output_value')
    def expression_list(self, p):
        p[0].append(p[2]) 
        print(p[0])
        return p[0] #[Expression]
    
    @_('expression')
    def output_value(self, p):
        return p[0] #Expression

    @_('while_statement', 'if_statement', 'compound_statement')
    def structured_statement(self, p):
        return p[0] #No he definido el compound statement
    
    @_('IF expression THEN statement')
    def if_statement(self, p):
        return IfStatementSolo(p.expression, p[3]) #Statement, no he definido statement
    
    @_('IF expression THEN statement ELSE statement')
    def if_statement(self, p):
        return IfStatement(p.expression, p[3], p[5]) #Statement, no he definido statement
    
    @_('WHILE expression DO statement')
    def while_statement(self, p):
        return WhileStatement(p.expression, p.statement) #Statement, no he definido statement
    
    @_('simple_expression')
    def expression(self, p):
        return ExpressionLista(p[0]) #Expression
    
    @_('simple_expression relational_operator simple_expression')
    def expression(self, p):
        return BinOpListas(p[1], p[0], p[2]) #Expression
    
    @_('sign term')
    def simple_expression(self, p):
        return [UnaryOp(p[0], p[1])] #[Expression]
    
    #@_('empty')
    @_('simple_expression adding_operator term')
    def simple_expression(self, p):
        p[0].append(UnaryOp(p[1], p[2])) 
        return p[0]  #[Expression]
    
    
    '''
    Preguntar si esta bien
    '''
    
    @_('factor')
    def term(self, p):
        return [p.factor] #[Expression]

    @_('term multiplying_operator factor')
    def term(self, p):
        #print ("hola")
        #print(str(p[0]) +  '*' + str(p[2]))
        p[0].append(BinOpListaIzq(p[1], p[2])) #[Expression]
        '''
        Antes tambien en la clase guardaba el lado izquierdo, pero como el lado
        izquierdo es el indice-1 de la lista, es desperdicio guardarlo, esto 
        era lo que me daba el error de recursividad infinita
        '''
        return p[0]
    
    #Regla inventada por mi para que soporte el llamado a funciones en la asignacion
    @_('IDENTIFIER "(" expression_list ")"')
    def factor(self, p):
        return FuncCall(p[0], p[2]) #Expression

    @_('variable')
    def factor(self, p):
        return ReadLocation(p[0]) #Expression
    
    @_('constant')
    def factor(self, p):
        return FactorConstant(p[0]) #Expression con clase propia
      
    @_('"(" expression ")"')
    def factor(self, p):
        return p.expression #Expression
    
    @_('NOT factor')
    def factor(self, p):
        return p[1] #Aun  no tiene clase en ast
    
    @_('empty', 'MINUS', 'PLUS')
    def sign(self, p):
        return str(p[0]) #Aun no tienen clase ast, String

    @_('OR', 'MINUS', 'PLUS')
    def adding_operator(self, p):
        return str(p[0]) #Aun no tienen clase ast, String

    @_('AND', 'DIV', 'TIMES', 'MOD', 'DIV_REAL')
    def multiplying_operator(self, p):
        return p[0]  #Aun no tienen clase ast
    
    @_('entire_variable')
    def variable(self, p):
        return p[0]  #Location
    
    @_('indexed_variable')
    def variable(self, p):
        return p[0] #Location
    
    @_('array_variable "[" expression "]"')
    def indexed_variable(self, p):
        return LocationArray(p[0], p.expression) #Location
    
    @_('entire_variable')
    def array_variable(self, p):
        return p[0]   #Location
    
    @_('variable_identifier')
    def entire_variable(self, p):
        return p[0]    #Location
    
    @_('IDENTIFIER')
    def variable_identifier(self, p):
        return SimpleLocation(p[0]) #Location
    
    @_('INTEGER_CONSTANT')
    def constant(self, p):
        return IntegerLiteral(p[0]) #Literal
    
    @_('REAL')
    def constant(self, p):
        return RealLiteral(float(p[0])) #Literal
    
    @_('CHARACTER_CONSTANT')
    def constant(self, p):
        return CharLiteral(p[0]) #Literal
    
    @_('LOGIC_CONSTANT')
    def constant(self, p):
        return BoolLiteral(p[0]) #Literal
    
    @_('GE', 'LE', '">"', '"<"', 'DIFF', '"="')
    def relational_operator(self, p):
        return p[0] #Aun no tienen clase en ast
    
    @_('')
    def empty(self, p):
        pass


    def error(self, p):
        self.hayError = True
        print("Error en la linea", p.lineno)
        if p:
            errors.error(p.lineno, "Error de sintaxis en la entrada en el token '%s'" % p.value)
        else:
            error('EOF','Error de sintaxis. No mas entrada.')







def parse(source):
	'''
	Parser el código fuente en un AST. Devuelve la parte superior del árbol AST.
	'''
	lexer = Tokenizer()
	parser = PasParser()
	ast = parser.parse(lexer.tokenize(source))
	return ast
	

	

def mostrarArbol(file):
    
    # Parse y crea el AST
    ast = parse(file)
    # Genera el árbol de análisis sintáctico resultante
    #for depth, node in flatten(ast):
     #   print(' %s%s' % (' '*(4*depth), node))
    
    a = DotVisitor()
    a.visit(ast)
    print(a)
    



if __name__ == '__main__':
    file = open("comentario2.pas", "r")
    text = (file.read() )
    mostrarArbol(text)


"""
if __name__ == '__main__':
    lexer = Tokenizer()
    parser = PasParser()
    file = open("pruebaNegro.pas", "r")
    text = (file.read() )
    print(text)
    parser.parse(lexer.tokenize(text))
"""
