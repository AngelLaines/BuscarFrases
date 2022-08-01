import csv
import Levenshtein
import argparse
import os

def carga_csv(archivo):
    lista = []
    try:
        with open(archivo,'r',encoding="UTF-8") as fh:
            lector_csv = csv.reader(fh)
            for linea in lector_csv:
                lista.append(linea)
    except IOError as e:
        print(os.getcwd())
        print(e)
    return lista

def filtrado(listado, limite, frase):
    distancias=[]
    peliculas=[]
    frases=[]
    for linea in listado:
        try:
            pelicula = linea[1]
            frase_lista = linea[0]
            año = linea[2]
            distancia = Levenshtein.ratio(frase_lista, frase)
            #if frase in frase1:
            if distancia >= limite:
                frases.append(frase_lista)
                res = ("Distancia: "+ str(round(distancia,2)),"Frase: "+ frase_lista,"Pelicula: "+ pelicula,"Año: "+ año)
                distancias.append(res)
                if pelicula not in peliculas:
                    peliculas.append(pelicula)
            
        except IndexError as v:
            print(linea)
            print(v)
    # print("-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-++-+-+-+-+-+-+-+-+-+-+-+-++-+-+-+-+-+-+-+-+-+-+-+-+-+-")
    # despliegue(distancias)
    # print("-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-++-+-+-+-+-+-+-+-+-+-+-+-++-+-+-+-+-+-+-+-+-+-+-+-+-+-")
    return distancias

def despliegue(listado):
    for elemento in listado:
        print(elemento)

def main(archivo,frase,limite):
    listado = carga_csv(archivo)
    max_dist = 0
    print("Frase a buscar: %s" % frase)
    if limite >= 10:
        limite=limite*.01
    elif limite >= 1:
        limite=limite*.1
    distancias=filtrado(listado,limite,frase)
    return distancias

def buscar_frases(archivo,frase,limite):
    distancias=main(archivo,frase,limite)
    return distancias

if __name__ == "__main__":
    parse =argparse.ArgumentParser()
    parse.add_argument("-a","--archivo", dest="archivo", required=False, default='./static/dicc_y_frases/frases_celebres.csv')
    parse.add_argument("-f", "--frase", dest="frase", required=False, default='todos estos momentos se perderan en el tiempo, como lagrimas bajo la lluvia')
    parse.add_argument("-l", "--limite", dest="limite", required=False, type=float,default=0.46)
    args = parse.parse_args()
    archivo = args.archivo
    frase = args.frase
    limite = args.limite
    main(archivo, frase, limite)