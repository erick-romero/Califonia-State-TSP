import Pkg

Pkg.add("JuMP")
Pkg.add("Cbc")
Pkg.add("CSV")

using JuMP, CSV, Cbc
using DelimitedFiles

function is_tsp_solved(m, x)
    N = size(x)[1]
    x_val = JuMP.value.(x)

    # find cycle
    cycle_idx = Int[]
    push!(cycle_idx, 1)
    while true
        v, idx = findmax(x_val[cycle_idx[end],1:N])
        if idx == cycle_idx[1]
            break
        else
            push!(cycle_idx,idx)
        end
    end
    println("cycle_idx: ", cycle_idx)
    println("Length: ", length(cycle_idx))
    if length(cycle_idx) < N
        @constraint(m, sum(x[cycle_idx,cycle_idx]) <= length(cycle_idx)-1)
        return false
    end
    return true
end

m = Model(Cbc.Optimizer)
set_optimizer_attribute(m,  "logLevel" , 1)
matriz = readdlm("../../CSV/matrizDistanciasCSV.csv", ',', Float64)
#m = Matrix{Float64}(CSV.read("../../CSV/matrizDistanciasCSV.csv", header=0, delim=','))



N=111
@variable(m, x[1:N,1:N], Bin)
@objective(m, Min, sum(x[i,j]*matriz[i,j] for i=1:N,j=1:N))
for i=1:N
    @constraint(m, x[i,i] == 0)
    @constraint(m, sum(x[i,1:N]) == 1)
end
for j=1:N
    @constraint(m, sum(x[1:N,j]) == 1)
end
for f=1:N, t=1:N
    @constraint(m, x[f,t]+x[t,f] <= 1)
end

optimize!(m)

while !is_tsp_solved(m,x)
    optimize!(m)
end
