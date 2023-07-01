import numpy as np
import nltk
import json
import pprint
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer


stemmer = SnowballStemmer("english")
archivo = open("./stopwords.txt", "r", encoding="utf-8")
contenido = archivo.read()
stoplist = contenido.split()
noticias = []
filtro = []
for x in range(97, 123):
    filtro.append(chr(x))


def documento(nombre,articulos):
    file = open("archive/"+str(nombre), "r")
    archivo = file.read()
    lista = archivo.split("\n")
    articulos = []
    b = 0
    for linea in lista:
        temp = linea.split(",")
        art = ""
        for i in range(9,len(temp)):
            art += temp[i]
        articulos.append(art)



def preprocesamiento(texto):
    palabra =""
    prefijos ={}
    i = 0
    index = 0
  # tokenizar
    for noticia in texto:
        cant = 0
        for letra in noticia:
            letra = letra.lower()
            if letra != "":
                if letra in filtro:
                   palabra += letra 
                else:
                # filtrar stopwords
                    if len(palabra) >= 3:
                        if palabra not in stoplist and palabra!="":
                        # reducir palabras
                            palabra = stemmer.stem(palabra)
                            if palabra not in list(prefijos.keys()):
                                f = open("./keyword/"+str(i)+".txt","w")
                                f.write(palabra + ","+str(index))
                                f.close()
                                prefijos[palabra] = i
                                i += 1   
                                cant +=1      
                            else : 
                                f = open("./keyword/"+str(prefijos[palabra])+".txt","a")
                                f.write(","+str(index))
                                f.close()
                                cant +=1         
                    palabra = "" 
        f = open("./size.txt","a")
        f.write(str(index)+":"+str(cant)+"\n")
        f.close()
        print("Articulo: "+str(index))
        index += 1  
        


preprocesamiento(noticias)

