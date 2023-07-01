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

def size(index_noticia,k):
    archivo = open("./size.txt", "r", encoding="utf-8")
    file = archivo.read()
    datos = file.split("\n")
    archivo.close()
    result = datos[index_noticia+1].split(":")
    return int(result[1])

def cosine_sim(Q, Doc):  
  # aplicar la similitud de coseno y construir la matriz
    normq= np.linalg.norm(Q)
    normdoc= np.linalg.norm(Doc)        
    return np.dot(Q/normq,Doc/normdoc)

    
def calcular(matriz, index):
    resultados ={}
    i1 = 0
    i2 = 0
    for q in matriz:
        for dic in matriz:
           if i1 != i2 and cosine_sim(q,dic) not in list(resultados.keys()):
            resultados[cosine_sim(q,dic)] = [index[i1],index[i2]]
           i2 +=1
        i1 +=1
        i2 = 0 
    return resultados

def matrizk(lista, k):
    similitudcos =[]
    index ={}
    indextemp = {}
    index_matriz=0
    index_lista = 0
    

    for num in lista:
        archivo = open("./keyword/"+str(num)+".txt", "r", encoding="utf-8")
        file = archivo.read()
        datos = file.split(",")
        archivo.close()
        tf = []
        temp = datos[1]
        frecuencia = 0
        df=0
        
        
        for values in datos[1:]:
            if int(temp) < int(values):
                df +=1
                temp = values

        temp = datos[1]
        
        for values in datos[1:]:
            if int(temp) < int(values):
                tf_idf =round(np.log10(np.log10(50008/df) * (1+ np.log10(frecuencia))),3)
               # print(tf_idf)
                if temp not in list(indextemp.keys()) or len(similitudcos) ==0:
                    index[index_matriz] = temp
                    indextemp[temp] = index_matriz
                    P=[0] * len(lista)
                    P[index_lista] = tf_idf
                    similitudcos.append(P)
                    index_matriz +=1
                else:
                    
                    similitudcos[indextemp[temp]][index_lista] = tf_idf
                    
                temp = values
            frecuencia += 1
        index_lista +=1
    
    calcular(similitudcos,index)
    sorted_desserts = dict(sorted(index.items(), key=lambda item:item[1], reverse=True))
    
    index = []
    r=0
    for x in list(sorted_desserts.keys()):
        if r== k/2:
            break
        index.append(sorted_desserts[x][0])
        index.append(sorted_desserts[x][1])
        r =+1

    return index

print(matrizk([514,549], 4))