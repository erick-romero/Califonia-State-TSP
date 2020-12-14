import Pkg
Pkg.add("JuMP")
Pkg.add("Cbc")
using JuMP
using Cbc
model = Model(Cbc.Optimizer)
set_optimizer_attribute(model, "logLevel", 1)
