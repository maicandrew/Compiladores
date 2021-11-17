# mpascal/checker.py
'''

*** No inicie este proyecto hasta que no haya completado el parser. ***

Visión general
--------------
En este proyecto necesitas realizar verificaciones semánticas
en tu programa.  Este problema es multifacético y complicado.
Para hacerlo un poco menos complicado, necesitas tomarlo lento
y en partes pequeñas.  La idea básica de lo que debe hacer es
la siguiente:

1.	Nombres y símbolos:

    Todos los identificadores deben definirse antes de ser
    utilizados. Esto incluye variables, constantes y nombres
    tipográficos. Por ejemplo, este tipo de código genera
    un error:

       a = 3; // Error. 'a' no definido.
       var a int;

2.	Tipos de literales y constantes.

    Todos los símbolos literales se escriben implícitamente
    y se les debe asignar un tipo "int", "float" o "char".
    Este tipo se utiliza para establecer el tipo de constantes.
    Por ejemplo:

       const a = 42; // Escribe "int"
       const b = 4.2; // Escribe "float"
       const c = 'a'; // Escribe "char"

3.	Comprobación del tipo de operador

    Los operadores binarios solo operan en operandos de un
    tipo compatible.  De lo contrario, obtendrá un error de
    tipo. Por ejemplo:

        var a int = 2;
        var b float = 3.14;

        var c int = a + 3; // OKAY
        var d int = a + b; // Error. int + float
        var e int = b + 4.5; // Error. int = float

    Además, debe asegurarse de que solo sea compatible
    Los operadores están permitidos. Por ejemplo:

        var a char = 'a'; // OKAY
        var b char = 'a' + 'b'; // Error (op + no soportada)

4.	Asignación.

    Los lados izquierdo y derecho de una operación de
    asignación deben estar declarado como el mismo tipo.

        var a int;
        a = 4 + 5; // OKAY
        a = 4.5; // Error. int = float

    Los valores solo se pueden asignar a declaraciones de
    variables, no a las constantes.

        var a int;
        const b = 42;

        a = 37; // OKAY
        b = 37; // Error. b es const

Estrategia de implementacion:
-----------------------------
Se va a usar la clase NodeVisitor definida en ast.py
para recorrer el árbol de parse. Se van a definir
varios métodos para diferentes tipos de nodos AST.
Por ejemplo, si tiene un nodo BinOp, escribirás un
método como este:

      def visit_BinOp (self, node):
          ...

Para comenzar, haga que cada método simplemente
imprima un mensaje:

      def visit_BinOp (self, node):
          imprimir ('visit_BinOp:', nodo)
          self.visit (node.left)
          self.visit (node.right)

Esto al menos te dirá que el método se está disparando.
Prueba ejemplos de código simple y asegúrese de que todos
sus métodos en realidad están corriendo cuando recorres
el árbol de análisis.

Pruebas
-------
Construya archicos que contengan diferentes elementos que
necesita para comprobar Las instrucciones específicas se
dan en cada archivo de prueba.

Pensamientos generales y consejos.
----------------------------------
Lo principal en lo que debe estar pensando con la verificación
es el programa exactitud. ¿Esta declaración u operación que
estás mirando? en el arbol de parse tiene sentido? Si no,
algún tipo de error necesita ser generado. Use sus propias
experiencias como programador como guía (piense sobre lo que
causaría un error en tu lenguaje de programación favorito).

Un desafío será la gestión de muchos detalles complicados.
Tienes que rastrear símbolos, tipos y diferentes tipos de
capacidades. No siempre está claro cómo organizar mejor
todo eso. Entonces, espera un poco al principio.
'''

from collections import ChainMap
from errors import error
from ast import *
from typesys import Type, RealType, IntType, CharType, BoolType

class CheckProgramVisitor(NodeVisitor):
	'''
	Programa de comprobación de clase. Esta clase usa el patrón
	visitante como se describe en ast.py. Debe definir los métodos
	del formulario visit_NodeName() para cada tipo de nodo AST
	que desee procesar. Es posible que deba ajustar los nombres
	de los métodos aquí si ha seleccionado diferentes nombres
	de nodo AST.
	'''
	def __init__(self):
		# Inicialice la tabla de simbolos
		self.symbols = { }

		# Tabla de simbolos temporal para grabar los simbolos
		# globales cuando se compruebe una definicion de
		# funcion/procedimiento
		self.temp_symbols = { }

		# Aqui grabamos el tipo esperado de retorno cuando se
		# comprueba una funcion/procedimiento
		self.expected_ret_type = None

		# Y aquí guardamos el tipo de retorno observado al
		# verificar una funcion/procedimiento
		self.current_ret_type = None

		# Una tabla de definicion de funciones/procedimientos
		self.functions = { }

		# Ponga los nombres de tipo incorporados en la tabla de
		# símbolos  self.symbols.update(builtin_types)
		self.keywords = {t.name for t in Type.__subclasses__()}

	def visit_VarDeclaration(self, node):
		# Aquí debemos actualizar la tabla de símbolos con
		# el nuevo símbolo.
		node.type = None

		# Antes de nada, si estamos declarando una variable  con
		# un nombre que es un nombre de tipo, entonces debemos fallar
		if node.name in self.keywords:
			error(node.lineno, f"Nombre '{node.name}' no es un nombre legal para declaración de variable")
			return

		if node.name not in self.symbols:
			# Primero verifique que el nodo del tipo de datos sea correcto
			self.visit(node.datatype)

			if node.datatype.type:
				# Antes de terminar, esta declaración var puede tener una
				# expresión para inicializarla. Si es así, debemos visitar
				# el nodo, y verificar los errores de tipo.
				if node.value:
					self.visit(node.value)

					if node.value.type: # Si el valor no tiene ningún tipo, entonces hubo un error previo
						if node.value.type == node.datatype.type:
							# Genial, el tipo de valor coincide con la
							# declaración de tipo de variable
							node.type = node.datatype.type
							self.symbols[node.name] = node
						else:
							error(node.lineno,
							f"Declarando variable '{node.name}' de tipo '{node.datatype.type.name}' pero asignada expresion de tipo '{node.value.type.name}'")
				else:
					# No hay inicialización, así que tenemos todo lo necesario
					# para guardarlo en nuestra tabla de símbolos
					node.type = node.datatype.type
					self.symbols[node.name] = node
			else:
				error(node.lineno, f"Tipo desconocido '{node.datatype.name}'")
		else:
			prev_lineno = self.symbols[node.name].lineno
			error(node.lineno, f"Nombre '{node.name}' ya se ha definido en linea {prev_lineno}")

	def visit_ProgramStatement(self, node):
		self.visit(node.block)

	def visit_BlockStatement(self, node):
		for i in node.var_part:
			self.visit(i)
		for j in node.func_part:
			self.visit(j)
		for k in node.pro_part:
			self.visit(k)
		self.visit(node.stat_part)

	def visit_ArrayType(self, node):
		# Asocie un nombre de tipo como "int" con un objeto de tipo
		node.type = Type.get_by_name(node.datatype.name)
		if node.type is None:
			error(node.lineno, f"Tipo invalido '{node.name}'")

	def visit_VarDeclarationPascal(self, node):
		# Aquí debemos actualizar la tabla de símbolos con
		# el nuevo símbolo.
		node.type = None

		# Antes de nada, si estamos declarando una variable  con
		# un nombre que es un nombre de tipo, entonces debemos fallar
		if node.name in self.keywords:
			error(node.lineno, f"Nombre '{node.name}' no es un nombre legal para declaración de variable")
			return

		if node.name not in self.symbols:
			# Primero verifique que el nodo del tipo de datos sea correcto
			self.visit(node.datatype)

			if node.datatype.name:
				node.type = node.datatype.name
				self.symbols[node.name] = node
			else:
				error(node.lineno, f"Tipo desconocido '{node.datatype.name}'")
		else:
			prev_lineno = self.symbols[node.name].lineno
			error(node.lineno, f"Nombre '{node.name}' ya se ha definido en linea {prev_lineno}")

	def visit_ConstDeclaration(self, node):
		# Para una declaración, deberá verificar que no esté ya definida.
		# Colocarás la declaración en la tabla de símbolos para que
		# puedas consultarla más adelante.
		if node.name not in self.symbols:
			# Primer nodo de valor de visita para extraer su tipo
			self.visit(node.datatype)
		else:
			prev_lineno = self.symbols[node.name].lineno
			error(node.lineno, f"Nombre '{node.name}' ya se ha definido en linea {prev_lineno}")

	def visit_IntegerLiteral(self, node):
		# Para los literales, deberá asignar un tipo al nodo y permitir
		# que se propague. Este tipo funcionará a través de varios operadores.
		node.type = IntType

	def visit_RealLiteral(self, node):
		# Para los literales, deberá asignar un tipo al nodo y permitir
		# que se propague. Este tipo funcionará a través de varios operadores.
		node.type = RealType

	def visit_BoolLiteral(self, node):
		# Para los literales, deberá asignar un tipo al nodo y permitir
		# que se propague. Este tipo funcionará a través de varios operadores.
		node.type = BoolType

	def visit_CharLiteral(self, node):
		# Para los literales, deberá asignar un tipo al nodo y permitir
		# que se propague. Este tipo funcionará a través de varios operadores.
		node.type = CharType

	def visit_WriteStatement(self, node):
		self.visit(node.value)

	def visit_IfStatement(self, node):
		self.visit(node.condition)

		cond_type = node.condition.type
		if cond_type:
			if issubclass(node.condition.type, BoolType):
				self.visit(node.true_block)
			else:
				error(node.lineno, f"'Condicion debe ser de tipo 'bool' pero tiene tipo '{cond_type.name}'")

	def visit_IfElseStatement(self, node):
		self.visit(node.condition)
		cond_type = node.condition.type
		if cond_type:
			if issubclass(node.condition.type, BoolType):
				self.visit(node.true_block)
				self.visit(node.false_block)
			else:
				error(node.lineno, f"'Condicion debe ser de tipo 'bool' pero tiene tipo '{cond_type.name}'")


	def visit_WhileStatement(self, node):
		self.visit(node.condition)

		cond_type = node.condition.type
		if cond_type:
			if issubclass(node.condition.type, BoolType):
				self.visit(node.body)
			else:
				error(node.lineno, f"'Condición debe ser de tipo 'bool' pero tiene tipo '{cond_type.name}'")

	def visit_BinOp(self, node):
		# Para los operadores, debe visitar cada operando por separado.
		# A continuación, deberá asegurarse de que los tipos y el
		# operador sean todos compatibles.
		self.visit(node.left)
		self.visit(node.right)

		node.type = None
		# Realiza varios controles aquí
		if node.left.type and node.right.type:
			op_type = node.left.type.binop_type(node.op, node.right.type)
			if not op_type:
				left_tname = node.left.type.name
				right_tname = node.right.type.name
				error(node.lineno, f"Operacion binaria '{left_tname} {node.op} {right_tname}' no soportada")

			node.type = op_type

	def visit_UnaryOp(self, node):
		# Verificar y propagar el tipo del único operando.
		self.visit(node.right)

		node.type = None
		if node.right.type:
			op_type = node.right.type.unaryop_type(node.op)
			if not op_type:
				right_tname = node.right.type.name
				error(node.lineno, f"Operacion unaria '{node.op} {right_tname}' no soportada")

			node.type = op_type

	def visit_VariableAssign(self, node):
		# Primero visite la definición de ubicación para verificar
		# que sea una ubicación válida
		self.visit(node.location)
		# Visita el valor, para obtener también información de tipo.
		self.visit(node.value)

		node.type = None
		if node.location.type and node.value.type:
			loc_name = node.location.name

			if isinstance(self.symbols[loc_name], ConstDeclaration):
				# Básicamente, si escribimos en una ubicación que
				# se declaró como una constante, entonces esto es un error
				error(node.lineno, f"No se puede escribir a constante '{loc_name}'")
				return

			# Si ambos tienen información de tipo, entonces la verificación
			# de tipo funcionó en ambas ramas
			if node.location.type == node.value.type:
				# Propagar el tipo
				node.type = node.location.type
			else:
				error(node.lineno,
				f"No se puede asignar el tipo '{node.value.type.name}' a variable '{node.location.name}' de tipo '{node.location.type.name}'")

	def visit_ReadLocation(self, node):
		# Asocie un nombre de tipo como "int" con un objeto de tipo
		if node.name not in self.symbols:
			node.type = None
			error(node.lineno, f"Nombre '{node.name}' no esta definido")
		else:
			node.type = self.symbols[node.name].type

	def visit_SimpleLocation(self, node):
		if node.name in self.symbols:
			node.type = None
			error(node.lineno, f"Nombre '{node.name}' ya esta definido")
		else:
			node.type = self.symbols[node.name].type

	def visit_SimpleType(self, node):
		# Asocie un nombre de tipo como "int" con un objeto de tipo
		node.type = Type.get_by_name(node.name)
		if node.type is None:
			error(5 , f"Tipo invalido '{node.name}'")

	def visit_FuncParameter(self, node):
		self.visit(node.datatype)
		node.type = node.datatype.type

	def visit_ReturnStatement(self, node):
		self.visit(node.value)
		# Propagar el tipo de valor de retorno como una propiedad
		# especial ret_type, solo para revisarse en la verificación
		# de la declaración de la función
		if self.expected_ret_type:
			self.current_ret_type = node.value.type
			if node.value.type and node.value.type != self.expected_ret_type:
				error(node.lineno, f"Funcion retorna '{self.expected_ret_type.name}' pero el valor de la declaración de retorno es de tipo '{node.value.type.name}'")
		else:
			error(node.lineno, "Instrucción return debe de estar dentro de una funcion")

	def visit_FunctionDeclaration(self, node):
		if node.name in self.functions:
			prev_def = self.functions[node.name].lineno
			error(node.lineno, f"Funcion '{node.name}' esta definida en la linea {prev_def}")

		self.visit(node.params)

		param_types_ok = all((param.type is not None for param in node.params))
		param_names = [param.name for param in node.params]
		param_names_ok = len(param_names) == len(set(param_names))
		if not param_names_ok:
			error(node.lineno, "Nombre de parametros duplicados en definicion de funcion")

		self.visit(node.datatype)
		ret_type_ok = node.datatype.type is not None

		# Antes de visitar la función, cuerpo, debemos cambiar la tabla
		# de símbolos a una nueva.
		if self.temp_symbols:
			error(node.lineno, f"Declaración de función anidada ilegal '{node.name}'")
		else:
			self.temp_symbols = self.symbols
			self.symbols = ChainMap(
				{param.name: param for param in node.params},
				self.temp_symbols
			)
			# Establecer el valor de retorno esperado para observar
			self.expected_ret_type = node.datatype.type

			self.visit(node.body)

			if not self.current_ret_type:
				error(node.lineno, f"Funcion '{node.name}' no tiene instrucción return")
			elif self.current_ret_type == self.expected_ret_type:
				# Debemos agregar la declaración de función como
				# disponible para futuras llamadas.
				self.functions[node.name] = node

			self.symbols = self.temp_symbols
			self.temp_symbols = { }
			self.expected_ret_type = None
			self.current_ret_type = None

	def visit_ProcedureStatement(self, node):
		# Antes de visitar la función, cuerpo, debemos cambiar la tabla
		# de símbolos a una nueva.
		if self.temp_symbols:
			error(node.lineno, f"Declaración de función anidada ilegal '{node.name}'")
		else:
			self.temp_symbols = self.symbols
			self.symbols = ChainMap(
				{param.name: param for param in node.params},
				self.temp_symbols
			)

			self.visit(node.body)

			self.functions[node.name] = node

			self.symbols = self.temp_symbols
			self.temp_symbols = { }
			self.expected_ret_type = None
			self.current_ret_type = None

	def visit_FuncCall(self, node):
		if node.name not in self.functions:
			error(node.lineno, f"Function '{node.name}' no esta declarada")
			node.type = None
		else:
			# Debemos verificar que la lista de argumentos coincida con
			# la definición de parámetros de la función
			self.visit(node.arguments)

			arg_types = tuple([arg.type.name for arg in node.arguments])
			func = self.functions[node.name]
			expected_types = tuple([param.type.name for param in func.params])
			if arg_types != expected_types:
				error(node.lineno, f"Function '{node.name}' espera {expected_types}, pero fue llamada con {arg_types}")

			# El tipo de llamada a la función es el tipo de retorno de la función.
			node.type = func.datatype.type

	def visit_ReadLocationFactor(self, node):
		if node.name not in self.symbols:
			error(5, f"La variable'{node.name}' no está definida")
			node.type = None
		else:
			node.type = self.symbols[node.name].type

# ----------------------------------------------------------------------
#                       NO MODIFICAR NADA ABAJO
# ----------------------------------------------------------------------

def check_program(ast):
	'''
	Compruebe el programa suministrado (en forma de un AST)
	'''
	checker = CheckProgramVisitor()
	checker.visit(ast)

def main():
	'''
	Programa Main. Usado para testing
	'''
	import sys
	from PasParser import parse

	if len(sys.argv) < 2:
		sys.stderr.write('Uso: python -m mpascal.checker filename\n')
		raise SystemExit(1)

	ast = parse(open(sys.argv[1]).read())
	check_program(ast)
	if '--show-types' in sys.argv:
		for depth, node in flatten(ast):
			print('%s: %s%s type: %s' % (getattr(node, 'lineno', None), ' '*(4*depth), node,
			getattr(node, 'type', None)))

if __name__ == '__main__':
	main()

