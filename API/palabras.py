

def tokenizar(lista):
    list_index = []
    for num in range(0,123503):
        archivo = open("/home/salvador/Documents/BD II/modulo2/Proyecto/keyword/"+str(num)+".txt", "r", encoding="utf-8")
        file = archivo.read()
        datos = file.split(",")
        if datos[0] in lista:
            list_index.append(num)
    return list_index

print(tokenizar(["content","run","speed","death"]))        