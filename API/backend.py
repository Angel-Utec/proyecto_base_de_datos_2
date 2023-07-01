import numpy as np

def tokenizar(lista):
    list_index = []
    for num in range(0,123503):
        archivo = open("./keyword/"+str(num)+".txt", "r", encoding="utf-8")
        file = archivo.read()
        datos = file.split(",")
        if datos[0] in lista:
            list_index.append(num)
    return list_index

def size(index_noticia, k):
    with open("./size.txt", "r", encoding="utf-8") as archivo:
        datos = archivo.read().split("\n")
    result = datos[index_noticia+1].split(":")
    return int(result[1])

def cosine_sim(Q, Doc):
    normq = np.linalg.norm(Q)
    normdoc = np.linalg.norm(Doc)
    return np.dot(Q/normq, Doc/normdoc)

def calcular(matriz, index):
    resultados = {}
    for i1, q in enumerate(matriz):
        for i2, dic in enumerate(matriz):
            if i1 != i2:
                similarity = round(cosine_sim(q, dic), 3)
                if similarity not in resultados:
                    resultados[similarity] = [index[i1], index[i2]]
    return resultados

def matrizk(lista, k):
    index = {}
    indextemp = {}
    similitudcos = np.zeros((len(lista), len(lista)))  # Crear una matriz NumPy de ceros

    for index_lista, num in enumerate(lista):
        with open(f"./keyword/{num}.txt", "r", encoding="utf-8") as archivo:
            file = archivo.read()
            datos = file.split(",")
        
        tf = []
        temp = datos[1]
        frecuencia = 0
        df = 0

        for values in datos[1:]:
            if int(temp) < int(values):
                df += 1
                temp = values

        temp = datos[1]

        for values in datos[1:]:
            if int(temp) < int(values):
                tf_idf = round(np.log10(np.log10(50008/df) * (1 + np.log10(frecuencia))), 3)
                if temp not in indextemp or len(similitudcos) == 0:
                    index[index_lista] = temp
                    indextemp[temp] = index_lista
                    similitudcos[index_lista, index_lista] = tf_idf  # Asignar el valor en la diagonal principal
                else:
                    similitudcos[indextemp[temp], index_lista] = tf_idf
                    
                temp = values
            frecuencia += 1
    
    resultados = calcular(similitudcos, index)
    sorted_results = dict(sorted(resultados.items(), key=lambda item: item[1], reverse=True))
    
    index = []
    r = 0
    for x in sorted_results.keys():
        if r == k/2:

            break
        index.append(sorted_results[x][0])
        index.append(sorted_results[x][1])
        r += 1

    return index