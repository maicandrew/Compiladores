import argparse, os, PasLex, PasParser

parser1 = argparse.ArgumentParser()
parser1.add_argument("-v", "--verbose",
    help="Mostrar información de depuración", action = "store_true")
parser1.add_argument("-l", "--lexer", help = "Nombre de archivo a procesar")
parser1.add_argument("-s", "--syntax", help = "Analizador sintactico")
args = parser1.parse_args()

# Aquí procesamos lo que se tiene que hacer con cada argumento

if args.lexer:
    if os.path.isfile(args.lexer):
        data = open(args.lexer, "r").read()
        lexer = PasLex.PascalLexer()
        for tok in lexer.tokenize(data):
            print('type=%r, value=%r' % (tok.type, tok.value))
    else: print("Archivo no encontrado")

if args.verbose:
    def verboseprint(*args1):
        for arg in args1:
           print (arg)
    verboseprint(args)

if args.syntax:
    if os.path.isfile(args.syntax):
        text = open(args.syntax, "r").read()
        try:
            PasParser.mostrarArbol(text)
        except EOFError:
            print("end")
