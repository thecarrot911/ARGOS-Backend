from operator import index
import random
from sklearn.utils import shuffle
import sys
from calendar import monthrange
from ortools.sat.python import cp_model

class SolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Clase para imprimir la solución."""

    def __init__(self,lista_alarma_turno,solution_number,mes,cont_semana,all_empleado,all_dias,cant_turno,solution_limit,list_itinerario):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._lista_alarma_turno = lista_alarma_turno
        self._solution_number = solution_number
        self._mes = mes
        self._cont_semana = cont_semana
        self._all_empleado = all_empleado
        self._all_dias = all_dias
        self._all_turno = cant_turno
        self._solution_count = 0
        self._solution_limit = solution_limit
        self._list_itinerario = list_itinerario

    def on_solution_callback(self):
        self._solution_count += 1
        if(self._solution_count == self._solution_number):
            indice = 0
            itinerario_final = []
            for num_semana in range(len(self._cont_semana)):
                print("Semana %i"% (num_semana+1))
                iti_week = []
                for i in range(self._cont_semana[indice]):
                    if(self._mes[num_semana][i][2]!="Domingo"):
                        #print("[%s]  Día n° %i - %s" % (self._mes[num_semana][i][0],self._mes[num_semana][i][1],self._mes[num_semana][i][2]))
                        a = self.Value(self._list_itinerario[num_semana][i][0])
                        b = self.Value(self._list_itinerario[num_semana][i][1])
                        c = self.Value(self._list_itinerario[num_semana][i][2])
                        #d = self._mes[num_semana][i][2]
                        e = self._mes[num_semana][i][1]
                        #f = self._mes[num_semana][i][0]

                        iti_week.append([a,b,c,e])
                        #print("%i %i %i" % (a,b,c))
                itinerario_final.append(iti_week)
                print(iti_week)
                indice = indice + 1
            print("_________________")
            print(lista_alarma_turno)
        if self._solution_count >= self._solution_limit:
            self.StopSearch()
    
    def solution_count(self):
        return self._solution_count

year = int(sys.argv[1]) 
month = int(sys.argv[2])
num_empleado = int(sys.argv[3])

if(month==12):
    month_next = 1
    year_next = year+1
    year_prev = year
    month_prev = month-1
elif(month==1):
    month_prev = 12
    year_prev = year-1
    year_next = year
    month_next = month+1
else:
    year_prev = year
    month_prev = month-1
    year_next = year
    month_next = month+1

dias_mes_prev = monthrange(year_prev, month_prev)
dias_mes_actual  = monthrange(year,month)
dias_mes_next = monthrange(year_next, month_next)

indice_semana_prev = dias_mes_prev[0]
cantidad_dias_prev = dias_mes_prev[1]

indice_semana = dias_mes_actual[0]
cantidad_dias = dias_mes_actual[1]

indice_semana_next = dias_mes_next[0]
cantidad_dias_next = dias_mes_next[1]

meses_anio = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre", "Diciembre"]
dias_semana = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
cant_turno = 3 

all_empleado = range(num_empleado) # 0..3
all_dias = range(1,cantidad_dias+1) # 1..cantidade_dias+1 #TODO: CAMBIAR PARA SIGUIENTES DÍAS DEL MES

# Modelo
model = cp_model.CpModel()

# Creación de las variables
mes = []
semana = []

def empleado_turno():
    array_empleado = []
    for empleado in all_empleado:
        turnos = []
        for t in range(cant_turno):
            turnos.append(
                model.NewBoolVar('Empleado n° %i con turno n°%i' % (empleado,(t+1)))
            )
        array_empleado.append(turnos)
    return array_empleado

for dia in all_dias:
    if(dias_semana[indice_semana] == "Lunes" and dia != 1):
        mes.append(semana)
        semana = []
        array_empleado = empleado_turno()
        if(dia == cantidad_dias): 
            semana.append([meses_anio[month-1],dia, dias_semana[indice_semana], array_empleado])
            mes.append(semana)
        else: 
            semana.append([meses_anio[month-1],dia, dias_semana[indice_semana], array_empleado])
    else: 
        array_empleado = empleado_turno()
        if(dia == cantidad_dias):
            semana.append([meses_anio[month-1],dia, dias_semana[indice_semana], array_empleado])
            mes.append(semana)
        else:
            semana.append([meses_anio[month-1],dia, dias_semana[indice_semana], array_empleado])
    indice_semana = indice_semana + 1
    if(indice_semana == 7): indice_semana=0

# Condición para agregar los dias faltantes de la última semana del mes
if(len(mes[len(mes)-1])!=7):
    indice_semana = dias_mes_actual[0]
    for k in range(7-indice_semana_next):
        array_empleado = empleado_turno()
        mes[len(mes)-1].insert(indice_semana_next,[meses_anio[month_next-1],k+1,dias_semana[indice_semana_next],array_empleado])
        indice_semana_next = indice_semana_next + 1
# Condición para gregar los dias faltantes de la primera semana del mes
if(len(mes[0])!=7):
    indice_semana = dias_mes_actual[0]
    for j in range(indice_semana):
        array_empleado = empleado_turno()
        mes[0].insert(0,[meses_anio[month_prev-1],cantidad_dias_prev,dias_semana[indice_semana-1],array_empleado])
        cantidad_dias_prev = cantidad_dias_prev-1
        indice_semana = indice_semana-1

# For para contar la cantidad de semanas
cont_semana = []
for i in mes:
    cont_semana.append(len(i))
indice = 0


# Restricción de Itinerario
# 5 DOMINGOS - 1 EMPLEADO PARA CADA TURNO. (3 EMPLEADO TRABAJANDO MÁXIMO)
# 4 DOMINGOS - 1 TURNO SIN OCUPAR. (2 EMPLEADO TRABAJANDO MÁXIMO)
# POR AHORA NOS E CONSDIERA 2 CHOQUES DE VUELO EN UN MISMO DIA :'V
#TURNOS:
#Turno 1: 07:00 – 15:00
#Turno 2: 15:00 – 23:00
#Turno 3: 23:00 – 07:00
            #dia,turno,empleado
"""itinerario=[[1,3,2],
            [5,3,2],
            [12,3,2],
            [12,1,2],
            [15,2,2],
            [19,3,3],
            [5,2,2],
            [26,2,2]]"""

itinerario=[[5,1,2],
            #[27,2,3],
            [5,3,3],
            [12,1,4],
            [19,2,2],
            [26,2,2]]

#itinerario=[]

def OrdenarLista(a,b,c,ind_a,ind_b,ind_c):
    lista = []
    if(a>b and b>c):
        lista.append(ind_c)
        lista.append(ind_b)
        lista.append(ind_a)
    elif(b>a and a>c):
        lista.append(ind_c)
        lista.append(ind_a)
        lista.append(ind_b)
    elif(c>a and a>b):
        lista.append(ind_b)
        lista.append(ind_a)
        lista.append(ind_c)
    elif(c>b and b>a):
        lista.append(ind_a)
        lista.append(ind_b)
        lista.append(ind_c)
    elif(a>c and c>b):
        lista.append(ind_b)
        lista.append(ind_c)
        lista.append(ind_a)
    elif(b>c and c>a):
        lista.append(ind_a)
        lista.append(ind_c)
        lista.append(ind_b)
    return lista


def ItinerarioFunction(dia,itinerario):
    lista = []
    for i in range(len(itinerario)):
        #print("%i|%i" % (d,itinerario[i][0]))
        if(itinerario[i][0]==dia):
            lista.append(i)
    if(len(lista)==2):
        a = itinerario[lista[0]][1]
        b = itinerario[lista[1]][1]
        c = 6-itinerario[lista[0]][1]-itinerario[lista[1]][1]
        #print(OrdenarLista(a,b,c,lista[0],lista[1],-1))
        return OrdenarLista(a,b,c,lista[0],lista[1],-1)
    elif(len(lista)==3):
        a = itinerario[lista[0]][1]
        b = itinerario[lista[1]][1]
        c = itinerario[lista[2]][1]
        return OrdenarLista(a,b,c,lista[0],lista[1],lista[2])
    else:
        return lista
                    #dia,turno,emp faltante
lista_alarma_turno = []
lista_comodin = []
dias_libre_semana = num_empleado
turnos_extra = 6*num_empleado-dias_libre_semana-6*cant_turno # 30-5-18 = 23 empleados

indice = 0
list_itinerario = []
list_turno_extra = []

# construir la lista con 1 nomás...
for num_semana in range(len(cont_semana)):
    semana_work = []
    work_extra = turnos_extra
    for i in range(cont_semana[indice]):
        if(mes[num_semana][i][0]==meses_anio[month-1]):
            list_index_itinerario = ItinerarioFunction(mes[num_semana][i][1],itinerario)
            if(i!=6):
                if(len(list_index_itinerario)>1): 
                    dia_work = []
                    acumulador = 2
                    for j in range(cant_turno):
                        index_iti = list_index_itinerario[j]
                        if(index_iti != -1):
                            if((acumulador>=itinerario[index_iti][2]-1)and(work_extra>=itinerario[index_iti][2]-1) and (acumulador>0)):
                                acumulador =  acumulador- (itinerario[index_iti][2]-1)
                                work_extra = work_extra+1 - itinerario[index_iti][2]
                                dia_work.append(
                                    model.NewIntVar(itinerario[index_iti][2],itinerario[index_iti][2],"turno %i" % (j+1))
                                )
                            elif((acumulador<itinerario[index_iti][2]-1) and (acumulador>0)):
                                for k in range(1,itinerario[index_iti][2]):
                                    if(acumulador-k==0):
                                        acumulador = acumulador - k
                                        break
                                work_extra = work_extra+1 - itinerario[index_iti][2]-k
                                dia_work.append(
                                    model.NewIntVar(itinerario[index_iti][2]-k,itinerario[index_iti][2]-k,"turno %i" % (j+1))
                                )
                                lista_alarma_turno.append([itinerario[index_iti][0],itinerario[index_iti][1],k])
                            elif((acumulador==0) or (work_extra<=itinerario[index_iti][2]-1)):
                                dia_work.append(
                                    model.NewIntVar(1,1,"turno %i" % (j+1))
                                )
                                lista_alarma_turno.append([itinerario[index_iti][0],itinerario[index_iti][1],itinerario[index_iti][2]-1,])
                            else:
                                print("wtff?")
                        else:
                            dia_work.append(
                                model.NewIntVar(1,1,"turno %i" % (j+1))
                            )
                    semana_work.append(dia_work)
                elif(len(list_index_itinerario)==1):
                    ind = list_index_itinerario[0]
                    dia_work = []
                    if((itinerario[ind][2]+cant_turno-1<=5)and(work_extra>=itinerario[ind][2])):
                        work_extra = work_extra+1 - itinerario[ind][2]
                        for t in range(cant_turno):
                            if(itinerario[ind][1]==(t+1)):
                                dia_work.append(
                                    model.NewIntVar(itinerario[ind][2],itinerario[ind][2],"turno %i" % (t+1))
                                )
                            else:
                                dia_work.append(
                                    model.NewIntVar(1,num_empleado-itinerario[ind][2],"turno %i" % (t+1))
                                )
                        print([mes[num_semana][i][1],dia_work])
                        semana_work.append(dia_work)
                    else:
                        number = 0
                        falta = 0
                        for num in range(1,itinerario[ind][2]+1):
                            if(num_empleado-cant_turno+1-num==0):
                                number=num
                                falta=itinerario[ind][2]-number
                                break
                        
                        for t in range(cant_turno):
                            if(itinerario[ind][1]==(t+1)):
                                dia_work.append(
                                    model.NewIntVar(number,number,"turno %i" % (t+1))
                                )
                            else:
                                dia_work.append(
                                    model.NewIntVar(1,1,"turno %i" % (t+1))
                                )
                        semana_work.append(dia_work)
                        lista_alarma_turno.append([itinerario[ind][0],itinerario[ind][1],falta])
                        print([mes[num_semana][i][1],dia_work])
                        # FALTA HACER LA LISTA EMERGENTE DE QUE NO ALCANZA A ENVIAR (LA WEA PAJA MANITO XD)
                else:
                    #print("NO HAY NADIE :d")
                    semana_work.append([
                        model.NewIntVar(1,num_empleado-cant_turno+1,"turno 1"),
                        model.NewIntVar(1,num_empleado-cant_turno+1,"turno 2"),
                        model.NewIntVar(1,num_empleado-cant_turno+1,"turno 3")
                    ])
        else:
            semana_work.append([
                model.NewIntVar(1,num_empleado-cant_turno+1,"turno 1"),
                model.NewIntVar(1,num_empleado-cant_turno+1,"turno 2"),
                model.NewIntVar(1,num_empleado-cant_turno+1,"turno 3")
            ])
    list_itinerario.append(semana_work)
    list_turno_extra.append(work_extra)
    indice = indice + 1

## Restricciones del itinerario

# Turnos sobrantes por asignar en la mañana.
indice = 0
for num_semana in range(len(cont_semana)):
    work_extra = list_turno_extra[num_semana]
    if(work_extra>=1):
        #print(list_turno_extra[indice])
        for i in range(list_turno_extra[num_semana]):
            if((i<=5) and (work_extra>=1)): # ASIGNA 2 PERSONA EN TURNO MAÑANA
                lista_index = ItinerarioFunction(mes[num_semana][i][1],itinerario)
                if(mes[num_semana][i][0]==meses_anio[month-1]):
                    if((len(lista_index)==0) and (work_extra>=1)):
                        model.Add(list_itinerario[num_semana][i][0]==2)
                        work_extra = work_extra - 1

                    elif((len(lista_index)==1) and (itinerario[lista_index[0]][1]!=1) and (itinerario[lista_index[0]][2]<=2) and (work_extra>=1)):
                        model.Add(list_itinerario[num_semana][i][0]==2)
                        work_extra = work_extra-1
                else:
                    if(work_extra>=1):
                        model.Add(list_itinerario[num_semana][i][0]==2)
                        work_extra = work_extra - 1
                        
            elif((i==6) and (work_extra>=1)):
                print(mes[num_semana][0][1])
                print("xdi")
                """for k in range(list_turno_extra[num_semana]):
                    if(k!=6): #ASIGNA 2 PERSONA EN TURNO TARDE
                        lista_index = ItinerarioFunction(mes[num_semana][k][1],itinerario)
                        if(mes[num_semana][k][0]==meses_anio[month-1]):
                            if((len(lista_index)==0) and (work_extra>=1)):
                                model.Add(list_itinerario[num_semana][k][1]==2)
                                work_extra = work_extra - 1
                            
                            elif((len(lista_index)==1) and (itinerario[lista_index[0]][1]!=2) and (itinerario[lista_index[0]][2]<num_empleado) and (work_extra>=1)):
                                model.Add(list_itinerario[num_semana][k][1]==2)
                                work_extra = work_extra -1
                        else:
                            if(work_extra>=1):
                                model.Add(list_itinerario[num_semana][k][1]==2)
                                work_extra = work_extra - 1"""
        indice = indice + 1


# Máxima cantidad de turnos trabajados en 1 semana por dia
indice = 0
for num_semana in range(len(cont_semana)):
    lista = []
    for i in range(cont_semana[indice]):
        if(i!=6):
            for t in range(cant_turno):
                lista.append(list_itinerario[num_semana][i][t])
    model.Add(sum(lista)==25)
    indice = indice + 1

# Mínima y máxima cantidad de turno en un día
indice = 0
for num_semana in range(len(cont_semana)):
    for i in range(cont_semana[indice]):
        if(i!=6):
            lista = []
            for t in range(cant_turno):
                lista.append(list_itinerario[num_semana][i][t])
            model.Add(sum(lista)<=5)
            model.Add(sum(lista)>=3)
    indice = indice + 1


# Crea el solver y la solución
solver = cp_model.CpSolver()
solver.parameters.linearization_level = 0

# Enumera todas las soluciones encontradas
solver.parameters.enumerate_all_solutions = True
solution_limit = 100
solution_number = random.randint(1,solution_limit)
solution_printer = SolutionPrinter(lista_alarma_turno,solution_number,mes,cont_semana,all_empleado,all_dias,cant_turno,solution_limit,list_itinerario)
solver.Solve(model, solution_printer)
# Statistics.
print('\nStatistics')
print('  - conflicts      : %i' % solver.NumConflicts())
print('  - branches       : %i' % solver.NumBranches())
print('  - wall time      : %f s' % solver.WallTime())
print('  - solutions found: %i' % solution_printer.solution_count())