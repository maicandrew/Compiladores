#
r'''
Proyecto 2: Escribir un analizador
==================================
En este proyecto, escribes el shell básico de un analizador para Pascal.
A continuación se incluye la forma BNF del lenguaje. Su tarea es escribir
las reglas de análisis y construir el AST para esta gramática usando SLY. 
La siguiente gramática es parcial. Se agregan más características en 
proyectos posteriores.

program : PROGRAM ID ';'
	declarations
	subprogram_declarations
	compound_statement 
	'.'

identifier_list : ID
	| identifier_list ',' ID

declarations : declarations VAR identifier_list ':' type ';'
	| empty

type : standard_type
	| ARRAY '[' NUM '..' NUM ']' OF statndard_type

standard_type : INTEGER
	| REAL

subprogram_declarations : subprogram_declarations subprogram_declaration ';'
	| empty

subprogram_declaration : subprogram_head declarations compound_statement

subprogram_head : FUNCTION ID arguments ':' standard_type ';'
	PROCEDURE ID arguments ';'

arguments : '(' parameter_list ')'
	| empty

parameter_list : identifier_list ':' type
	| parameter_list ';' identifier_list ':' type

compound_statement : BEGIN optional_statements END

optional_statements : statement_list
	| empty

statement_list : statement
	| statement_list ';' statement

statement : variable ASSIGNOP expression
	| procedure_statement
	| compound_statement
	| IF expression THEN statement ELSE statement
	| WHILE expression DO statement

variable : ID
	| ID '[' expression ']'

procedure_statement : ID
	| ID '(' expression_list ')'

expression_list : expression
	| expression_list ',' expression

expression : simple_expression
	| simple_expression RELOP simple_expression

simple_expression : term
	| sign term
	| simple_expression ADDOP term

term : factor
	| term MULOP factor

factor : ID
	| ID '(' expression_list ')'
	| NUM
	| '(' expression ')'
	| NOT factor

sign : '+' | '-'

lexical
=======

{ }, (* *) comments

letter : [a-zA-Z]
digit  : [0-9]
ID     : letter ( letter | digit )*

digits : digit digit*
optional_fraction : . digits | empty
optional_exponent :
	(E (+|-|empty) digits)
	| empty
NUM : digits optional_fraction optional_exponent

relop : =, <>, <, <=, >=, >
addop : +, -, or
mulop : *, /, div, mod, and
assignop : :=

Para hacer el proyecto, siga las instrucciones que siguen a continuación.
'''
# ----------------------------------------------------------------------
# Analizadores son definidos usando SLY.  Se hereda de la clase Parser
#
# vea http://sly.readthedocs.io/en/latest/
# ----------------------------------------------------------------------
from sly import Parser

# ----------------------------------------------------------------------
# El siguiente import carga la función error(lineno, msg) que se debe
# usar para informar todos los mensajes de error emitidos por su analizador. 
# Las pruebas unitarias y otras características del compilador se basarán 
# en esta función. Consulte el archivo errors.py para obtener más 
# documentación sobre el mecanismo de manejo de errores.
from errors import error

# ------------------------------------------------- ---------------------
# Importar la clase lexer. Su lista de tokens es necesaria para validar y 
# construir el objeto analizador.
from paslexer import PasLexer

# ----------------------------------------------------------------------
# Obtener los nodos AST.
# Lea las instrucciones en ast.py 
from ast import *

class PasParser(Parser):
	# El mismo conjunto de token definidos en lexer
	tokens = PasLexer.tokens

	# ----------------------------------------------------------------------
    # Tabla de precedencia de operadores. Los operadores deben seguir las 
	# mismas reglas de precedencia que en Python. Instrucciones que se darán 
	# en el proyecto.
    precedence = (
        ('left', 'AND', 'NOT'),
        ('nonassoc', 'LT', 'LE', 'GT', 'GE', 'EQ', 'NE'),
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UNARY')

	# ----------------------------------------------------------------------
	# SU TAREA. Traduzca el BNF en la secuencia siguiente a una colección
	# de funciones del analizador. Por ejemplo, una regla como:
	#
	# program : statements
	#
    # Se convirtió en un método de Python como este:
    #
    # @_ ('statements')
    # def programa (self, p):
    #     return Program(p.statements)
    #
    # Para símbolos como '(' o '+', deberás reemplazar con el nombre
    # del token correspondiente, como LPAREN o PLUS, si asi lo definió
	# en el lexer.
    #
    # En el cuerpo de cada regla, cree un nodo AST apropiado y devuélvalo
    # como se muestra arriba.
    #
    # Para fines del seguimiento del número de línea, debe asignar un número 
	# de línea a cada nodo AST según corresponda. Para hacer esto, sugiero 
	# enviar el número de línea de cualquier símbolo terminal cercano. 
	# Por ejemplo:
    #
    # @_('PRINT expr SEMI')
    # def print_statement(self, p):
    #     return PrintStatement(p.expr, lineno=p.lineno)

	@_("PROGRAM ID ';' declarations subprogram_declarations compound_statement '.'")
	def program(self, p):
		pass

	@_("ID")
	def identifier_list(self, p):
		pass

	@_("identifier_list ',' ID")
	def identifier_list(self, p):
		pass

	@_("declarations VAR identifier_list ':' type ';'")
	def declarations(self, p):
		pass

	@_("empty")
	def declarations(self, p):
		pass

	@_("standard_type")
	def type(self, p):
		pass

	@_("ARRAY '[' NUM '.' '.' NUM ']' OF statndard_type")
	def type(self, p):
		pass

	@_("INTEGER", "REAL")
	def standard_type(self, p):
		pass
		
    # ----------------------------------------------------------------------
    # NO MODIFIQUE
    #
    # manejo de errores catch-all. Se llama a la siguiente función en cualquier 
    # entrada incorrecta. p es el token ofensivo o None si el final de archivo (EOF).

    # catch-all error handling.   The following function gets called on any
    # bad input.  p is the offending token or None if end-of-file (EOF).
    def error(self, p):
        if p:
            error(p.lineno, "Error de sintaxis en la entrada en el token '%s'" % p.value)
        else:
            error('EOF','Error de sintaxis. No mas entrada.')

# ----------------------------------------------------------------------
#                  NO MODIFIQUE NADA A CONTINUACIÓN
# ----------------------------------------------------------------------

def parse(source):
    '''
	Parser el código fuente en un AST. Devuelve la parte superior del árbol AST.
	'''
    lexer = PasLexer()
    parser = PasParser()
    ast = parser.parse(lexer.tokenize(source))
    return ast

def main():
    '''
    Programa principal. Usado para probar.
    '''
    import sys

    if len(sys.argv) != 2:
        sys.stderr.write('Uso: python3 -m parser filename\n')
        raise SystemExit(1)

    # Parse y crea el AST
    ast = parse(open(sys.argv[1]).read())

    # Genera el árbol de análisis sintáctico resultante
    for depth, node in flatten(ast):
        print('%s: %s%s' % (getattr(node, 'lineno', None), ' '*(4*depth), node))

if __name__ == '__main__':
    main()