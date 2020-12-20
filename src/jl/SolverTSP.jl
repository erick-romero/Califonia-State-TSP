#primero debemos importar Pkg, es el manejador de paquieres de Julia
import Pkg

#Debemos instalar 2 paquetes necesario para resolver el modelo
#JuMP es un paquete para trabajar con notacion simbolica y para modelar problemaas de optimizacion
Pkg.add("JuMP")
#Cbc es un paquete el cual contiene un solver de programacion entera basa en el metodo Branch and bound and cut y simplex
Pkg.add("Cbc")

#con esto se importan los paquetes al programa
#DelimitedFiles nos permite leer la informacion que se tiene almacenaad en los CSV
using JuMP,Cbc,DelimitedFiles

function Existen_subciclos(California, x)
    N=111
    #se guarda en un arreglo  los valores de las variables de decision de la iteracion actual
    Resultados_x = JuMP.value.(x)

    #creamos un arrego de ciclo actual y le agregamo el indice 1 que es la ciudad de los angeles
    ciclo_actual = Int[]
    push!(ciclo_actual, 1)

    #tenemos que encontrar a que ciudad esta conectada los angeles, esta se encuentra buscando en la fila 1 el valor de la variable de decision que sea 1
    while true
        y, fin_ciclo = findmax(Resultados_x[ciclo_actual[end],1:N])
        #si la ciudad del fin de ciclo es igual a la ciudad del inicio actual, entonces ya terminamos de encontar el ciclo actual
        if fin_ciclo == ciclo_actual[1]
            break
        #Se agrega al arreglo el ciclo actual, la siguiente ciudadd a la que esta conectada
        else
            push!(ciclo_actual,fin_ciclo)
        end
    end
    #Se imprime el ciclo actual y la lognitud del ciclo actual
    #es imporante notar que nuuestro subciclo actual tiene que tener una longitud de 111 para que se considere terminado el problema
    println("Ciclo actual: ", ciclo_actual)
    println("Longitud: ", length(ciclo_actual))
    #si la longitud del ciclo actual es menor a los 111 nodos que debemos tener entonces debemos agregar la restriccion para eliminar el subciclo que encontramos que pertenece a los angeles
    if length(ciclo_actual) < N
        @constraint(California, sum(x[ciclo_actual,ciclo_actual]) <= length(ciclo_actual)-1)
        #si existen subciclos se regresa false para volver terminar
        return false
    end
    #si no existen subciclos se regresa true para detener la solucion
    return true
end


#Se lee la informacion de nuestro archivo CSV
matriz = readdlm("../../CSV/matrizDistanciasCSV.csv", ',', Float64)
#N representa el numero de nodos en nuestro problema
N=111

#se instancia el modelo y se asigna el solver con el cual trabajaremos
California = Model(Cbc.Optimizer)
set_optimizer_attribute(California,  "logLevel" , 0)

#se crean las variables de decision para cada nodo  y se agregan al modelo, de tipo binario
@variable(California, x[1:N,1:N], Bin)
#Se agrega la funcion objetivo al modelo y se especifica que se debe minimizar
#min sumatoria CijXij
@objective(California, Min, sum(x[i,j]*matriz[i,j] for i=1:N,j=1:N))

#Se debe agregar la Restriccion de nodo de entrada a cada nodo
for i=1:N
    @constraint(California, sum(x[i,1:N]) == 1)
end
#se agrega la restriccion de salida a cada nodo
for j=1:N
    @constraint(California, sum(x[1:N,j]) == 1)
end
#Se agrega la restriccion para eliminar los subciclos de 2 nodos
for i=1:N, j=1:N
    @constraint(California, x[i,j]+x[j,i] <= 1)
end
#debido a que la distancia entre la misma ciudad es 0, se agrega una restriccion para que no se puedan conectar a si mismas
for i=1:N
    for j=1:N
        if matriz[i,j]==0
            @constraint(California, x[i,j] == 0)
        end
    end
end

#una vez se tiene todas las restricciones se llama el metodo optimizar el cual pasa el modelo de optimizacion
#al solver Cbc para resolver el problema
#el resultado devuelto es la solucion al modelo relajado que probablemente tenga subciclos
optimize!(California)

#debido a que el modelo relajado probablemente tenga subciclos debemos encontrar dicho subciclos y agregar las restricciones para eliminar los subciclos

while !Existen_subciclos(California,x)
    optimize!(California)
end
