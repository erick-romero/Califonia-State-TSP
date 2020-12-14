import requests
import json
import pandas as pd
import numpy


api_key= "YOUR-MAPQUEST-API-GOES-HERE"

#se importa el CSV del nombre de ciudades que quieres generar la matriz de distancias y se guarda en un pandas dataframe
df = pd.read_csv("nombresCiudades.csv")
#se pasa del dataframa a un array
array = df.to_numpy()
#se crea un array para ingresar las distancias entre las ciudades
distancias = numpy.zeros((190,190))

#esta funcion hace un request al API de mapquest y nos regrese la distancia de carretera entre 2 ciudades
def calcularDistancia(a,b):
    url = "http://www.mapquestapi.com/directions/v2/route?key="+api_key+"&from="+str(a)+",CA,USA&to="+str(b)+",CA,USA"
    response = requests.get(url)
    Jsonfile = response.json()
    z =Jsonfile["route"]
    x = z["distance"]
    print(a+" hacia "+b)
    print("distancia: "+ str(x))
    return x

#esto itera nuesto array de nombres de ciudades y lo guarda en forma de matriz en un array
for i in range(len(array)):
    for j in range(len(array)):
        if i!=j:
            r = calcularDistancia(array[i],array[j])
            distancias[i][j] = r

#se importa el array hacia un documento CSV            
numpy.savetxt("distancias.csv", distancias, delimiter=",")        
             
    



   

