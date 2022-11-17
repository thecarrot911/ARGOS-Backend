a = 2
b = 3
c = 1

def OrdenarLista(a,b,c):
    lista = []
    if(a>b and b>c):
        lista.append([c,b,a])
        return lista
    elif(b>a and a>c):
        lista.append([c,a,b])
        return lista
    elif(c>a and a>b):
        lista.append([b,a,c])
        return lista
    elif(c>b and b>a):
        lista.append([a,b,c])
        return lista
    elif(a>c and c>b):
        lista.append([b,c,a])
        return lista
    elif(b>c and c>a):
        lista.append(a,c,b)
        return lista

print(OrdenarLista(a,b,c))