# mpascal/typesys.py
'''
Sistema de tipo mpascal
=======================
Este archivo implementa características básicas del sistema de tipos
Minipascal.  Ahi esta mucha flexibilidad es posible aquí, pero la
mejor estrategia podría ser no reconsiderar el problema. Al menos
no al principio. Aquí están los Requisitos básicos mínimos:

1. Los tipos tienen nombres (por ejemplo, 'int', 'real', 'string')
2. Los tipos deben ser comparables. (por ejemplo, int != real).
3. Los tipos admiten diferentes operadores (por ejemplo, +, -, *, /, etc.)

Para tratar todo esto inicialmente, recomiendo representar tipos
como simples string. Hacer tablas que representen las capacidades.
de diferentes tipos. Hacer algunas funciones de utilidad que
comprueban los operadores.

MANTENLO SIMPLE. REPETIR. SENCILLO.

'''

INT_ARITHM_BIN_OPS = ["+", "-", "*", "div"]
REAL_ARITHM_BIN_OPS = ["+", "-", "*", "/"]
ARITHM_UNARY_OPS = ["+", "-"]

REL_BIN_OPS = ["<", "<=", ">", ">=", "=", "<>"]

BOOL_BIN_OPS = ["and", "or", "=", "<>"]
BOOL_UNARY_OPS = ["not"]

class Type():
	'''
	Clase base para nuestro sistema de tipos
	'''

	@classmethod
	def binop_type(cls, op, right_type):
		'''
		Devuelve el tipo al aplicar el operador binario con el
		actual tipo y el tipo del operando derecho, o devuelve
		None si la operación no es válida
		'''
		return None

	@classmethod
	def unaryop_type(cls, op):
		'''
		Devuelve el tipo al aplicar el operador unario con el
		actual tipo
		'''
		return None

	@classmethod
	def get_by_name(cls, type_name):
		for type_cls in cls.__subclasses__():
			if type_cls.name == type_name:
				return type_cls

		return None

class RealType(Type):
	name = "REAL"

	@classmethod
	def binop_type(cls, op, right_type):
		if issubclass(right_type, RealType):
			if op in REAL_ARITHM_BIN_OPS:
				return RealType
			elif op in REL_BIN_OPS:
				return BoolType

		return None

	@classmethod
	def unaryop_type(cls, op):
		if op in ARITHM_UNARY_OPS:
			return FloatType

		return None

class IntType(Type):
	name = "INTEGER"

	@classmethod
	def binop_type(cls, op, right_type):
		if issubclass(right_type, IntType):
			if op in INT_ARITHM_BIN_OPS:
				return IntType
			elif op in REL_BIN_OPS:
				return BoolType

		return None

	@classmethod
	def unaryop_type(cls, op):
		if op in ARITHM_UNARY_OPS:
			return IntType

		return None

class CharType(Type):
	name = "CHAR"

	@classmethod
	def binop_type(cls, op, right_type):
		if issubclass(right_type, CharType):
			if op in REL_BIN_OPS:
				return BoolType

		return None


class BoolType(Type):
	name = "BOOL"

	@classmethod
	def binop_type(cls, op, right_type):
		if issubclass(right_type, BoolType) and op in BOOL_BIN_OPS:
			return BoolType

		return None

	@classmethod
	def unaryop_type(cls, op):
		if op in BOOL_UNARY_OPS:
			return BoolType

		return None
