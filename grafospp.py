from enum import Flag
import re

numero=("[0-9]")
lsg=("([a-z]|( )|(-))")
nombreCalle=("[A-Z]("+lsg+"|"+numero+")*")
codigoID=("#"+"[A-Z]{2}"+numero+"{2}")
telefono=("\+[1-9][0-9]{5}")
rut=("([1-9]([0-9])*(\-)([0-9]|k))")
nombrePersona=("[A-Z]([a-z]|(\-)|( ))*")
apellidoPersona=("[A-Z]([a-z]|(\-)|( ))*")
persona=(nombrePersona+"((,)"+nombrePersona+")*(_)"+apellidoPersona+"((,)"+apellidoPersona+")*(_)"+telefono+"(_)"+rut)
personas=(persona+"((/)"+persona+")*")
calle=("("+nombreCalle+"."+codigoID+"."+personas+")+")
camino=("(\()*("+calle+"|"+codigoID+"):("+calle+"|"+codigoID+")\)((:("+calle+"|"+codigoID+"))\))*")

PID=("print "+codigoID)
PAL=("print_all")
PCM=("print_caminos "+codigoID)
PBN=("print_by_nombre "+nombrePersona)
PBR=("print_by_rut "+rut)
PBT=("print_by_telefono "+telefono)
PBA=("print_by_apellido "+apellidoPersona)
PVC=("valid_camino "+codigoID+" "+codigoID)
UPD=("update "+codigoID+" "+calle)

listaDeCalles=list()
listaDeCaminos=list()

file2=open("error.txt","w")
file1=open("input.txt","r")
x=file1.read()

x=x.split(";")
"""""
ImprimirCalle
_____________________
parametro 1:lista [0]:nombre calle
                 [1]:id calle
                 [2]:lista de personas en la calle
_____________________
imprime la calle segun el formato solicitado
"""""
def ImprimirCalle(calle):
    print("CALLE:")
    print(calle[0])
    print(calle[1])
    for persona in calle[2]:
        i=0
        aux=""
        while i!=len(persona[0]):
            if i>=1:
                aux=aux+","
            aux=aux+persona[0][i]
            i=i+1
            
        print(aux)
        aux=""
        i=0
        while i!=len(persona[1]):
            if i>=1:
                aux=aux+","
            aux=aux+persona[1][i]
            i=i+1
        print(aux)
        print(persona[2])
        print(persona[3])

"""""
imprimirCaminos
_____________________
parametro 1: str id 
parametro 2: lista donde el camino[0] es el id de la calle correspondiente (inicio)
                            camino[i] es el id de la calle a la cual se puede ir (fin)
_____________________
imprime los id a los cuales se pueden llegar desde el id inicial
"""""
def imprimirCaminos(id1,camino):
    i=1
    print("Caminos desde"+id1+":")
    while i!= len(camino):
        print(id1+"->"+camino[i])
        i=i+1

"""""
imprimirCalleBy
_____________________
parametro 1: lista calle con sus datos 
_____________________
imprime el nombre de la calle
"""""
def imprimirCalleBy(calle):
    print(calle[0])

"""""
verificarRut
_____________________
parametro 1: rut 
_____________________
toma el rut, lo divide y lo verifica 
"""""
def verificarRut (rut):
    x=rut
    y=re.split("-",x)
    lista=list(y[0])
    lista.reverse()
    i=2
    total=0
    for numero in lista:
        sumar=int(numero)*i
        if i==7:
            i=2
        else:
            i=i+1
        total=total+sumar

    resultado=11-(total%11)
    if resultado==11:
        resultado=0
    elif resultado==10:
        resultado="k"
    if y[1]==str(resultado):
        return True
    else:
        return False

"""""
Calle
_____________________
parametro 1: calle
_____________________
recibe la calle y la descompone en los datos requeridos para almacenarlos en una lista de listas (matriz) con la finalidad de simular ser un nodo del grafo
"""""
def Calle(dato):
    listaDeCalle=list()
    dato0=re.search(nombreCalle,dato).group()
    dato1=re.search(codigoID,dato).group()
    dato2=list()
    Auxdato2=re.search(personas,dato).group()
    Auxdato2=Auxdato2.split("/")
    for datoPersona in Auxdato2:
        y=re.split("_",datoPersona)

        if re.fullmatch(nombrePersona,y[0]):
            dato20=[y[0]]
        else:
            dato20=re.split(",",y[0])

        if re.fullmatch(apellidoPersona,y[1]):
            dato21=[y[1]]
        else:
            dato21=re.split(",",y[1])

        dato22=y[2]

        if verificarRut(y[3]):
            dato23=y[3]
        else:
            return True
        dato2.append((dato20,dato21,dato22,dato23))
        
    listaDeCalle.extend([dato0,dato1,dato2])
    listaDeCalles.append(listaDeCalle)
    return False

"""""
Camino
_____________________
parametro 1: camino
_____________________
recibe la calle y la descompone en los datos requeridos para almacenarlos en una lista de listas (matriz) con la finalidad de simular ser una lista de caminos tipo
[id0,id1,...] el id0 sera siempre el id inicial y los demas son los ids a las calles se pueden llegar apartir del id0
"""""
def Camino(dato):
    aux=re.split(":",dato)
    for datos in aux:
        if re.search(calle,datos):
            ids=re.search(calle,datos).group()
            Calle(ids)
    
    ids=re.findall(codigoID,dato)
    
    
    i1=1
    while i1!=len(ids):
        flag=True
        i2=0
        while i2!=len(listaDeCaminos):
            if ids[i1-1]==listaDeCaminos[i2][0]:
                if i1 !=len(ids):
                    listaDeCaminos[i2].append(ids[i1])
                flag=False
            i2=i2+1
        if flag:
            listaDeCaminos.append([ids[i1-1],ids[i1]])
        
        i1=i1+1

"""""
PRINTID
_____________________
parametro 1: id
_____________________
recibe el id y busca en la lista de calles la calle con ese id y la imprime 
"""""
def PRINTID(dato):
    flag=True
    for calle in listaDeCalles:
        if calle[1]==dato:
            flag=False
            ImprimirCalle(calle)
    if flag:
        print("no existen calles con ese id")

"""""
PRINTALL
_____________________

_____________________
recorre la lista de calles e imprime todas las calles 
"""""
def PRINTALL():
    for calle in listaDeCalles:
        ImprimirCalle(calle)

"""""
PRINTCAM
_____________________
parametro 1: id
_____________________
busca el id de la calle en la lista de caminos e imprime los caminos de esa calle
"""""
def PRINTCAM(dato):
    for caminos in listaDeCaminos:
        if caminos[0]==dato:
            imprimirCaminos(dato,caminos)

"""""
PRINTBN
_____________________
parametro 1: nombre persona
_____________________
busca el nombre de la persona en la lista de calles e imprime la calle en caso de tener a una persona con ese nombre dentro 
"""""
def PRINTBN(dato):
    print("CALLES CON PERSONAS DE NOMBRE ")
    print(dato+":")
    flag=True
    for calle in listaDeCalles:
        for persona in calle[2]:
            if persona[0][0]==dato:
                flag=False
                imprimirCalleBy(calle)
    if flag:
        print("no existe una calle con una persona con ese nombre")

"""""
PRINTBR
_____________________
parametro 1: rut
_____________________
busca el rut de la persona en la lista de calles e imprime la calle en caso de tener a una persona con ese rut dentro 
"""""  
def PRINTBR(dato):
    print("CALLES CON PERSONAS DE RUT ")
    print(dato+":")
    flag=True
    for calle in listaDeCalles:
        for persona in calle[2]:
            if persona[3]==dato:
                flag=False
                imprimirCalleBy(calle)
    if flag:
        print("no existe calle con persona con ese rut")

"""""
PRINTBT
_____________________
parametro 1: telefono
_____________________
busca el telefono de la persona en la lista de calles e imprime la calle en caso de tener a una persona con ese telefono dentro 
""""" 
def PRINTBT(dato):
    print("CALLES CON PERSONAS DE TELEFONO ")
    print(dato+":")
    flag=True
    for calle in listaDeCalles:
        for persona in calle[2]:
            if persona[2]==dato:
                flag=False
                imprimirCalleBy(calle)
    if flag:
        print("no existe calle con una persona con ese telefono")

"""""
PRINTBA
_____________________
parametro 1: apellido
_____________________
busca el apellido de la persona en la lista de calles e imprime la calle en caso de tener a una persona con ese apellido dentro 
""""" 
def PRINTBA(dato):
    print("CALLES CON PERSONAS DE NOMBRE ")
    print(dato+":")
    flag=True
    for calle in listaDeCalles:
        for persona in calle[2]:
            if persona[1][0]==dato:
                flag=False
                imprimirCalleBy(calle)    
    if flag:
        print("no existe calle con una persona con ese apellido")

"""""
VALID_CAMINO
_____________________
parametro 1: ids lista de ids id[0]id inicial id[1] id llegada
_____________________
busca en la lista de caminos si existe la relacion de camino entre los 2 ids
""""" 
def VALID_CAMINO(ids):
    flag1=False
    flag2=False
    for calle in listaDeCalles:
        if calle[1]==ids[0]:
            flag1=True
        if calle[1]==ids[1]:
            flag2=True
    if flag1 & flag2:
        for caminos in listaDeCaminos:
            if caminos[0]==ids[0]:
                for id in caminos:
                    if id==ids[1]:
                        print("Si se pudede")
                else: return 0
    elif flag1 ^ flag2:
        if flag1:
            print("no existe con "+ids[1]+"_calle_2")
        else: print("no existe con "+ids[0]+"_calle_1")
    else:
        print("no existe ni id1 ni id2")
        
"""""
FUPD
_____________________
parametro 1: id el id a actualizar
parametro 2: calle datos a actualizar
_____________________
busca la existencia de ese id en la lista de calles y luego borra el dato con el id de entrada y crea una calle con la nueva actualizacion y 
actualiza todos los caminos del id anterios y los reemplaza por el id nuevo
"""""
def FUPD (id, calle):
    i=0
    auxid=re.search(codigoID,calle).group()
    while i!=len(listaDeCalles):
        if listaDeCalles[i][1]==id:
            listaDeCalles[i].clear()
            listaDeCalles.remove(list())
            Calle(calle)
        i=i+1
    i1=0
    while i1!= len(listaDeCaminos):
        i2=0
        while i2!= len(listaDeCaminos[i1]):
            if listaDeCaminos[i1][i2]==id:
                listaDeCaminos[i1][i2]=auxid
            i2=i2+1
        i1=i1+1    

"""""
el programa recorre cada una de las posibles entradas y las analiza para saber de que tipo son y hace lo correspondiente segun cada tipo de entrada valido

"""""
for expresion in x :
    if re.fullmatch(calle,expresion):
        datoPuro=re.fullmatch(calle,expresion).group()
        aux=Calle(datoPuro)
        if aux:
            file2.write(expresion+"\n")
    elif re.fullmatch(camino,expresion):
        datoPuro=re.fullmatch(camino,expresion).group()
        Camino(datoPuro)
    elif re.fullmatch(PID,expresion):
        datoPuro=re.search(codigoID,expresion).group()
        PRINTID(datoPuro)
    elif re.fullmatch(PAL,expresion):
        PRINTALL()
    elif re. fullmatch(PCM,expresion):
        datoPuro=re.search(codigoID,expresion).group() 
        PRINTCAM(datoPuro)
    elif re.fullmatch(PBN,expresion):
        datoPuro=re.search(nombrePersona,expresion).group() 
        PRINTBN(datoPuro)
    elif re.fullmatch(PBR,expresion):
        datoPuro=re.search(rut,expresion).group() 
        PRINTBR(datoPuro)
    elif re.fullmatch(PBT,expresion):
        datoPuro=re.search(telefono,expresion).group() 
        PRINTBT(datoPuro)
    elif re.fullmatch(PBA,expresion):
        datoPuro=re.search(apellidoPersona,expresion).group()
        PRINTBA(datoPuro)
    elif re.fullmatch(PVC,expresion):
        datoPuro=re.findall(codigoID,expresion)
        VALID_CAMINO(datoPuro)
    elif re.fullmatch(UPD,expresion):
        datoPuro1=re.search(codigoID,expresion).group()
        datoPuro2=re.search(calle,expresion).group()
        FUPD(datoPuro1,datoPuro2)
    else:
        file2.write(expresion+"\n")

file1.close()
file2.close()