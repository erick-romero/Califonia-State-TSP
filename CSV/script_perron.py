newf = ""
with open('estupidez.txt', 'r') as f:
    for line in f:
        newf += line.strip()+";\n"
    f.close()
with open('ojo.txt', 'w') as f:
    f.write(newf)
    f.close()
