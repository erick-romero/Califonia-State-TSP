import Pkg
Pkg.add("JuMP")
Pkg.add("Cbc")
Pkg.add("TravelingSalesmanExact")
using TravelingSalesmanExact,Cbc
set_default_optimizer!(Cbc.Optimizer)
n = 50
cities = [ 100*rand(2) for _ in 1:n];
println(cities)
tour, cost = get_optimal_tour(cities; verbose = true)
plot_cities(cities[tour])
