import random
from sklearn.utils import shuffle
import sys
from calendar import monthrange
from ortools.sat.python import cp_model

class SolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Clase para imprimir la solución."""

    def __init__(self,solution_number,mes,cont_semana,all_empleado,all_dias,cant_turno,solution_limit):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._solution_number = solution_number
        self._mes = mes
        self._cont_semana = cont_semana
        self._all_empleado = all_empleado
        self._all_dias = all_dias
        self._all_turno = cant_turno
        self._solution_count = 0
        self._solution_limit = solution_limit

    def on_solution_callback(self):
        self._solution_count += 1
        if(self._solution_count == self._solution_number):
            print("SOLUCIÓN N°%i" % self._solution_count)
            indice = 0
            # AGREGAR CONTADORES 
            for num_semana in range(len(self._cont_semana)):
                print("Semana %i"% (indice+1))
                print("_____________________________")
                for i in range(self._cont_semana[indice]):
                    print("[%s]  Día n° %i - %s" % (self._mes[num_semana][i][0],self._mes[num_semana][i][1],self._mes[num_semana][i][2]))
                    #if(self._mes[num_semana][i][1]=="Domingo"):
                    for j in all_empleado:
                        is_working = False
                        for t in range(cant_turno):
                            if(self.Value(self._mes[num_semana][i][3][j][t])):
                                is_working = True
                                print('Empleado %i trabaja en el turno %i' % ((j+1), (t+1)))
                        if not is_working:
                            print('Empleado {} no trabaja en el turno'.format(j+1))
                print("_____________________________")
                indice = indice + 1
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
"""itinerario=[[5,2,2],
            [12,1,3],
            [19,3,3],
            [26,2,2],
            [25,2,2]]"""

itinerario=[[3,2,2],
            [7,1,2],
            [12,2,3],
            [14,2,3],
            [15,2,2]]
    #son domingos
    #4
    #11
    #18
    #25
# SI HAY OTRO CHOQUE QUE MANDE ARREGLO IGUAL

def ItinerarioFunction(dia,itinerario):
    for i in range(len(itinerario)):
        #print("%i|%i" % (d,itinerario[i][0]))
        if(itinerario[i][0]==dia):
            return i
    return None

lista_alarma_turno = []
indice = 0
lista_domingos_four_week = [[1,1,0],[1,1,0],[1,1,1],[1,1,1]]

dias_libre_semana = num_empleado
turnos_extra = 6*num_empleado-dias_libre_semana-6*cant_turno # 30-5-18 = 23 empleados
lista_domingos_four_week[0] = shuffle(lista_domingos_four_week[0])
lista_domingos_four_week[1] = shuffle(lista_domingos_four_week[1])
lista_domingos_four_week = shuffle(lista_domingos_four_week)

indice = 0
list_itinerario = []
# construir la lista con 1 nomás...
for num_semana in range(len(cont_semana)):
    semana_work = []
    work_extra = turnos_extra
    for i in range(cont_semana[indice]):
        dia_work = [] 
        index_itinerario = ItinerarioFunction(mes[num_semana][i][1],itinerario) 
        if(i!=6):
            if(index_itinerario != None):
                if((itinerario[index_itinerario][2]+cant_turno-1<=5) and (work_extra>=itinerario[index_itinerario][2])): 
                    work_extra = work_extra+1 - itinerario[index_itinerario][2]
                    for t in range(cant_turno):
                        if(itinerario[index_itinerario][1]==(t+1)):
                            dia_work.append(itinerario[index_itinerario][2])
                        else:
                            dia_work.append(1)
                    semana_work.append(dia_work)
                else: # CONSDERAR PONER UN IF PARA AGREGAR DE A 1
                    print("no alcanza")
                    semana_work.append([1,1,1,"XD"])
            else:
                semana_work.append([1,1,1])
    if(work_extra>=1):
        for w_e in range(len(semana_work)):
            if((work_extra-1>=0) and (semana_work[w_e][0]==1) and (semana_work[w_e][0]+1+ semana_work[w_e][1]+semana_work[w_e][2]<=5)):
                
                semana_work[w_e][0]=semana_work[w_e][0]+1
                work_extra = work_extra-1
                #print("%i %i %i" % (semana_work[w_e][0],semana_work[w_e][1],semana_work[w_e][2]))
                #print("----")
            elif(work_extra-1>=0):
                work_extra = work_extra
            else:
                break
        if(work_extra-1==0): # hacer random :v
            dia_random = random.randint(0,5)
            semana_work[dia_random][1]=semana_work[dia_random][1]+1
            work_extra = work_extra-1

    list_itinerario.append(semana_work)
    print(semana_work)
    indice = indice + 1



"""
if((index_itinerario != None) and (mes[num_semana][i][0] == meses_anio[month-1])): # ITINERARIO
    num_empleado_turno = (cant_turno-1) + itinerario[index_itinerario][2]
    turno_semana = turno_semana - num_empleado_turno
    if(turno_semana//(6-i)>= cant_turno): # CONSEJO, CALCULAR DE ANTES CUANTOS TURNOS EN LA SEMANA HAY
        print(" alcanza %i" % mes[num_semana][i][1])
        for t in range(cant_turno):
            if(itinerario[index_itinerario][1]==(t+1)):
                model.Add(sum(mes[num_semana][i][3][e][t] for e in all_empleado)==itinerario[index_itinerario][2])
            else:
                model.Add(sum(mes[num_semana][i][3][e][t] for e in all_empleado)==1)
    else:
        print("no alcanza %i" % mes[num_semana][i][1])
        model.Add(sum(mes[num_semana][i][3][e][0] for e in all_empleado)>=1)
        model.Add(sum(mes[num_semana][i][3][e][1] for e in all_empleado)>=1)
        model.Add(sum(mes[num_semana][i][3][e][2] for e in all_empleado)>=1)
else: # NO ITINERARIO
    print("asignacion normal %i" % mes[num_semana][i][1])
    print(list_itinerario[num_semana][i])
    model.Add(sum(mes[num_semana][i][3][e][0] for e in all_empleado)>=1)
    model.Add(sum(mes[num_semana][i][3][e][1] for e in all_empleado)>=1)
    model.Add(sum(mes[num_semana][i][3][e][2] for e in all_empleado)>=1)
"""