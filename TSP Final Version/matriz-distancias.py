import requests
import json
import pandas as pd
import numpy

api_key= "yLspcOFXBaxprTwHqPIurBz2wCkRDJy5"

#print(df.head)
df = pd.read_csv("csv/nombresCiudades.csv")
array = df.to_numpy()
#print(array)


distancias = numpy.zeros((111,111))

#print(distancias)


def calcularDistancia(a,b):
    url = "http://www.mapquestapi.com/directions/v2/route?key="+api_key+"&from="+str(a)+",CA,USA&to="+str(b)+",CA,USA"
    response = requests.get(url)
    Jsonfile = response.json()
    z =Jsonfile["route"]
    x = z["distance"]
    print(a+" hacia "+b)
    print("distancia: "+ str(x))
    return x


   

for i in range(105,111):
    for j in range(len(array)):
        if i!=j:
            r = calcularDistancia(array[i],array[j])
            distancias[i][j] = r
            numpy.savetxt("distancias.csv", distancias, delimiter=",")

        
             
    



   

