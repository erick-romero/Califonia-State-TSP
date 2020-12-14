import Pkg
Pkg.add("JuMP")
Pkg.add("Cbc")
Pkg.add("Pandas")
using JuMP
using Cbc
using Pandas
model = Model(Cbc.Optimizer)
set_optimizer_attribute(model  "logLevel"  1)
df = read_csv("../../csv/matrizDistanciasCSV.csv")
