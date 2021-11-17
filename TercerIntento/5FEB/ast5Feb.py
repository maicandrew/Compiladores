# ast.py
'''
Objetos del AST (Abstract Syntax Tree).

Este archivo define clases para diferentes tipos de nodos de un Árbol
de sintaxis abstracto. Durante el análisis, creará estos nodos y los
conectará entre sí. En general, tendrá un nodo AST diferente para cada
tipo de regla de gramática. Se pueden encontrar algunos nodos AST de
muestra en la parte superior de este archivo. Tendrá que agregar más
por su cuenta.
'''

# NO MODIFIQUE
class AST(object):
	_nodes = { }

	@classmethod
	def __init_subclass__(cls):
		AST._nodes[cls.__name__] = cls

		if not hasattr(cls, '__annotations__'):
			return

		fields = list(cls.__annotations__.items())

		def __init__(self, *args, **kwargs):
			if len(args) != len(fields):
				raise TypeError(f'{len(fields)} argumentos esperados')
			for (name, ty), arg in zip(fields, args):
				if isinstance(ty, list):
					if not isinstance(arg, list):
						raise TypeError(f'{name} debe ser una lista')
					if not all(isinstance(item, ty[0]) for item in arg):
						raise TypeError(f'Todos los tipos de {name} deben ser {ty[0]}')
				elif not isinstance(arg, ty):
					raise TypeError(f'{name} debe ser {ty}')
				setattr(self, name, arg)

			for name, val in kwargs.items():
				setattr(self, name, val)

		cls.__init__ = __init__
		cls._fields = [name for name,_ in fields]

	def __repr__(self):
		vals = [ getattr(self, name) for name in self._fields ]
		argstr = ', '.join(f'{name}={type(val).__name__ if isinstance(val, AST) else repr(val)}'
		for name, val in zip(self._fields, vals))
		return f'{type(self).__name__}({argstr})'

# ----------------------------------------------------------------------
# Nodos espefificos del AST.
#
# Para cada uno de estos nodos, se debe agregar la especificacion
# apropiada de _fields = [] que especifique que campos seran guardados.
# Solo como ejemplo, para el operador binario, se debe guardar el
# operador, la expresion izquierda y la derecha como esto:
#
#    class Expression(AST):
#          pass
#
#    class BinOp(AST):
#          op: str
#          left: Expression
#          right: Expression
#
# En el archivo parser.py, se creara el nodo usando un codigo
# sililar a esto:
#
#    class PasParser(Parser):
#        ...
#        @_('expr "+" expr')
#        def expr(self, p):
#            return BinOp(p[1], p.expr0, p.expr1)
#
# ----------------------------------------------------------------------

# Nodos Abstract del AST
class Statement(AST):
	pass

class Expression(AST):
	pass

class Literal(Expression):
	'''
	Un valor literal como 2, 2.5, o "dos"
	'''
	pass

class DataType(AST):
	pass

class Location(AST):
	pass

# Nodos concretos del AST
class WriteStatement(Statement):
    value : [Expression]

class ReadStatement(Statement):
	'''
	read(expression) ;
	'''
	value : Expression

class IntegerLiteral(Literal):
	value : int

class RealLiteral(Literal):
	value : float

class CharLiteral(Literal):
	value : str

class BoolLiteral(Literal):
	value : str

class IfStatement(Statement):
	condition : Expression
	true_block : Statement
	false_block : Statement

#Mia
class IfStatementSolo(Statement):
	condition : Expression
	true_block : Statement


class WhileStatement(Statement):

	condition : Expression
	body : Statement

#Mi clase
class ProcedureStatement(Statement):
    name : str
    block : Statement


#Mi clase
class ListStatement(Statement):
    statements : [Statement]

#Mi clase
class BlockStatement(Statement):
    var_dec : [Statement]
    procedure_dec :  [Statement]
    statement_part : Statement

#Mi clase
class ProgramStatement(Statement):
    name : str
    block : Statement

#Mi clase
class ProcedureIdentifier(Statement):
    value : str

#Mi clase
class ExpressionLista(Expression): #Para que al retornar no sea una lista
    value : [Expression]


class BinOpListaIzq(Expression):
	'''
	Un operador binario como 2 + 3 o x * y
	'''
	op    : str
	#left  : [Expression]
	right : Expression

#Mi clase
class BinOpListas(Expression):
	'''
	Un operador binario como 2 + 3 o x * y
	'''
	op    : str
	left  : [Expression]
	right : [Expression]

class SimpleLocationFactor(Expression):
	name : str

class UnaryOp(Expression):
	'''
	Un operador unario como -2 o +3
	'''
	op    : str
	right : [Expression]

class FuncCall(Expression):
	name      : str
	arguments : [Expression]

class ConstDeclaration(Statement):
	'''
	const name = value ;
	'''
	name  : str
	value : Expression

#Mia
class FactorConstant(Expression):
    value : Literal
#Mia
class VarAssign(Statement):
	'''
	const name = value ;
	'''
	name  : Location
	value : Expression

class FuncParameter(AST):
	name: str
	datatype: DataType

class FuncDeclaration(Statement):
	name  : str
	params : [FuncParameter]
	datatype: DataType
	body : [Statement]

class ReturnStatement(Statement):
	value: Expression

class SimpleType(DataType):
	name : str

class VarDeclaration(Statement):
	'''
	var name datatype [ = value ];
	'''
	name     : str
	datatype : DataType
	value    : (Expression, type(None))    # Optional

#Mi clase
class VarDeclarationPascal(Statement):

	id_list     : [Location] #Si lo encapsulo en parser seria una [Location], depende
	datatype : DataType

#Mi clase
class VarDeclarationNull(Statement):
    value : type(None)


#Mi clase
class LocationArray(Location):
    name : Location
    expression : Expression

#Mi clase
class ArrayType(DataType):
    index_range : [str]
    simple_type : str


class SimpleLocation(Location):
	name : str

#Mi clase
class ReadLocationList(Statement):
	location: [Location]

class ReadLocation(Location):
	location: str

class WriteLocation(Location):
	name : str

# ----------------------------------------------------------------------
#                NO MODIFIQUE NADA DE AQUI EN ADELANTE
# ----------------------------------------------------------------------

# Las siguientes clases para visitar y reescribir el AST se toman del
# módulo ast de Python.

# NO MODIFIQUE
class NodeVisitor(object):
	'''
	Clase para visitar los nodos del árbol de análisis sintáctico.
	Esto se modela después de una clase similar en la biblioteca estándar
	ast.NodeVisitor. Para cada nodo, el método de visit(node) llama a
	un método visit_NodeName(node) que debe implementarse en subclases.
	El método generic_visit() se llama para todos los nodos donde no hay
	ningún método de matching_NodeName() coincidente.

	Este es un ejemplo de un visitante que examina un operador binario:

	class VisitOps(NodeVisitor):
	visit_BinOp(self,node):
	print('Binary operator', node.op)
	self.visit(node.left)
	self.visit(node.right)
	visit_UnaryOp(self,node):
	print('Unary operator', node.op)
	self.visit(node.expr)

	tree = parse(txt)
	VisitOps().visit(tree)
	'''
	def visit(self, node):
		'''
		Enecuta un metodo de la forma visit_NodeName(node) donde
		NodeName es el nombre de la clase de un nodo particular.
		'''
		if isinstance(node, list):
			for item in node:
				self.visit(item)
		elif isinstance(node, AST):
			method = 'visit_' + node.__class__.__name__
			visitor = getattr(self, method, self.generic_visit)
			visitor(node)

	def generic_visit(self,node):
		'''
		Metodo ejecutado si no se encuentra el metodo visit_.
		Este examina el nodo para ver si tiene _fields, una lista,
		o puede ser atravesado.
		'''
		for field in getattr(node, '_fields'):
			value = getattr(node, field, None)
			self.visit(value)


	@classmethod
	def __init_subclass__(cls):
		'''
		Revision de sanidad. Se asegura que las clases visitor usen los
		nombres adecuados.
		'''
		for key in vars(cls):
			if key.startswith('visit_'):
				assert key[6:] in globals(), f"{key} no coincide con nodos AST"

# NO MODIFICAR
def flatten(top):
	'''
	Aplana todo el árbol de análisis sintáctico en una lista para
	depurar y probar.  Esto devuelve una lista de tuplas de la
	forma (depth, node) donde depth es un entero que representa
	la profundidad y node es el nodo AST asociado.
	'''
	class Flattener(NodeVisitor):
		def __init__(self):
			self.depth = 0
			self.nodes = []
		def generic_visit(self, node):
			self.nodes.append((self.depth, node))
			self.depth += 1
			NodeVisitor.generic_visit(self, node)
			self.depth -= 1

	d = Flattener()
	d.visit(top)
	return d.nodes
