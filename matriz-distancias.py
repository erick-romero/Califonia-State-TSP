import requests
import json
import pandas as pd
import numpy

api_key= "gozMomO2h2ZYs5U8y3ySpy9Gh3QQVerq"

df = pd.read_csv("nombresCiudades.csv")
#print(df.head)
array = df.to_numpy()
#print(array)


distancias = numpy.zeros((191,191))

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


   

for i in range(25,26):
    for j in range(len(array)):
        if i!=j:
            r = calcularDistancia(array[i],array[j])
            distancias[i][j] = r

numpy.savetxt("distancias.csv", distancias, delimiter=",")        
             
    



   

