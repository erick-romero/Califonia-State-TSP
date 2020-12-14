import Pkg
Pkg.add("TravelingSalesmanHeuristics")
Pkg.add("Gadfly")
using LinearAlgebra
using TravelingSalesmanHeuristics
using Random
using Gadfly
function generate_instance(n)
	Random.seed!(47)
	pts = rand(2  n)
	distmat = [norm(pts[: i] - pts[: j]) for i in 1:n  j in 1:n]
	return pts  distmat
end
plot_instance(pts) = plot(x = pts[1 :]  y = pts[2 :]  Geom.point  Guide.xlabel(nothing)  Guide.ylabel(nothing))
function plot_solution(pts  path  extras = [])
	ptspath = pts[: path]
	plot(x = ptspath[1 :]  y = ptspath[2 :]  Geom.point  Geom.path  Guide.xlabel(nothing)  Guide.ylabel(nothing)  extras...)
end
pts  distmat = generate_instance(5)
distancia = Float64[0 10.1 23.4 15.1 17;9.8 0 16 8.1 19;23 16 0 16 34;14 8 17 0 35;16 20 35 36 0]
plot_instance(pts)
@time path  cost = solve_tsp(distancia; quality_factor = 5)
plot_solution(pts  path)
println("El costo total es: "  cost)
