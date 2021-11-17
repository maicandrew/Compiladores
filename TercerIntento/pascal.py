# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 16:15:00 2018

@author: David
"""
import pasParser
import argparse
import paslex


def append(x, y):
    return x+y


if __name__ == '__main__':
    lexer = paslex.controlLexer()
    parser = argparse.ArgumentParser(description = "Analizador léxico para mini pascal")
    parser.add_argument("archivos", nargs = "+",  type = argparse.FileType('r'))
    parser.add_argument("-v", "--verbox", 
                        help = "Muestra linea por linea el codigo que se esta ejecutando", 
                        action = "store_true")
    parser.add_argument("-l", "--lex", 
                        help = "Muestra todos los simbolos del programa", action = "store_true")
    
    parser.add_argument("-s", "--sint", 
                        help = "Muestra el arbol de sintaxis abstracto", action = "store_true")
    args = parser.parse_args()
    #Cada archivo devuelve una lista de líneas, aqui se concatenan los renglones
    #para que sea un solo texto
    archivos = []
    for files in args.archivos:
        data_list = files.readlines()


        if len(data_list) > 0:
            data = data_list[0]
            for i in range(len(data_list) -1):
                data += data_list[i+1]
            archivos.append(data)
            
            
    if args.verbox and args.lex:
        for files in archivos:
            lexer = paslex.controlLexer()
            lexer.showData(files)
            lexer.showTokens(files)
    elif args.verbox:
        for files in archivos:
            lexer = paslex.controlLexer()
            lexer.showData(files)
            lexer.tokenizar(files)
    elif args.lex:
        for files in archivos:
            lexer = paslex.controlLexer()
            lexer.showTokens(files)
 
    
    else:
    
        for files in archivos:
            lexer = paslex.Tokenizer()
            parser = pasParser.PasParser()
            tokens = parser.parse(lexer.tokenize(files))
            #pasParser.mostrarArbol(files)
            if not lexer.hayError:
                print("Compilacion lexica exitosa!")
            if not parser.hayError:
                print("Compilacion sintactica exitosa!")
                
    if args.sint:
        for files in archivos:
            pasParser.mostrarArbol(files)
    