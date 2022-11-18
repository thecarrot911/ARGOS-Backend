from tkinter import N
from sklearn.utils import shuffle
import sys
import random
from calendar import monthrange
from ortools.sat.python import cp_model

def GenerarPlanificacion(year,month,num_empleado):
    class SolutionPrinter(cp_model.CpSolverSolutionCallback):
        """Clase para imprimir la solución."""

        def __init__(self,solution_number,list_itinerario,mes,cont_semana,all_empleado,all_dias,cant_turno,solution_limit,meses_anio):
            cp_model.CpSolverSolutionCallback.__init__(self)
            self._solution_number = solution_number
            self._list_itinerario = list_itinerario
            self._mes = mes
            self._cont_semana = cont_semana
            self._all_empleado = all_empleado
            self._all_dias = all_dias
            self._all_turno = cant_turno
            self._solution_count = 0
            self._solution_limit = solution_limit
            self._meses_anio = meses_anio

        def on_solution_callback(self):
            self._solution_count += 1
            if(self._solution_count == self._solution_number):
                json = []
                indice = 0
                itinerario_final = []

                # AGREGAR CONTADORES 
                for num_semana in range(len(self._cont_semana)):
                    #print("Semana %i"% (indice+1))
                    #print("_____________________________")
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
                    
                    """for i in range(self._cont_semana[indice]):

                        if(self._mes[num_semana][i][0] == self._meses_anio[month-1]):
                            dia = {}
                            dia["dia_semana"] = self._mes[num_semana][i][2]
                            dia["numero_dia"] = self._mes[num_semana][i][1]
                            empleados = []
                            for j in all_empleado:
                                emp_turn = {}
                                is_working = False
                                for t in range(cant_turno):
                                    if(self.Value(self._mes[num_semana][i][3][j][t])):
                                        is_working = True
                                        emp_turn["turno"] = t+1
                                        emp_turn["nombre"] = j+1
                                        #print('Empleado %i trabaja en el turno %i' % ((j+1), (t+1)))
                                if not is_working:
                                    emp_turn["turno"] = 0
                                    emp_turn["nombre"] = j+1
                                    #print('Empleado {} no trabaja en el turno'.format(j+1))
                                empleados.append(emp_turn)
                            dia["empleados"] = empleados
                            #print(dia)
                            json.append(dia)
                    indice = indice + 1"""
                #print(json)
            if self._solution_count >= self._solution_limit:
                self.StopSearch()
        
        def solution_count(self):
            return self._solution_count
        
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
    dias_semana = ["Lunes","Martes","Miercoles","Jueves","Viernes","Sabado","Domingo"]
    cant_turno = 3 

    all_empleado = range(num_empleado) # 0..3
    all_dias = range(1,cantidad_dias+1) 

    #Modelo
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

    #Restricciones
    #mes[num_semana][i][0] -> Mes
    #mes[num_semana][i][1] -> Dia del mes
    #mes[num_semana][i][2] -> Dia de semana
    #mes[num_semana][i][3] -> Array de Empleado

    # Cada empleado trabaja como máximo un turno por día. (Puede ser 0 porque puede tener el día libre al ser solo 3 turnos)
    for e in all_empleado:
        indice = 0
        for num_semana in range(len(cont_semana)):
            for i in range(cont_semana[indice]):
                model.AddAtMostOne(mes[num_semana][i][3][e][t] for t in range(cant_turno))
            indice = indice + 1

    # Cada empleado tiene 1 día libre por semana [AGREGAR LO DE BD]
    for e in all_empleado:
        indice = 0
        for num_semana in range(len(cont_semana)):
            lista_semana = []
            if(cont_semana[num_semana]==7):
                for i in range(cont_semana[indice]):
                    if mes[num_semana][i][2] != 'Domingo':
                        for t in range(cant_turno):
                            lista_semana.append(mes[num_semana][i][3][e][t])
                model.Add(sum(lista_semana) == 5)
            indice = indice + 1

    # Las personas no pueden tener 2 turnos seguidos 
    for e in all_empleado:
        indice = 0
        for num_semana in range(len(cont_semana)):
            for i in range(cont_semana[indice]):
                lista_turno = []
                if(i+1!=cont_semana[indice]):
                    lista_turno.append(mes[num_semana][i][3][e][2])
                    lista_turno.append(mes[num_semana][i+1][3][e][0])
                    model.Add(sum(lista_turno) <= 1)
            indice = indice + 1
    
    # Los empleados tienen 2 domingos libres durante el mes 
    domingos = []
    indice = 0
    for num_semana in range(len(cont_semana)):
        for i in range(cont_semana[indice]):
            if mes[num_semana][i][2] == 'Domingo' and mes[num_semana][i][0] == meses_anio[month-1]: 
                domingos.append([i, num_semana]) 
        indice = indice + 1

    if(len(domingos)==5):
        for e in all_empleado: 
            lista_domingo_suma = []
            for domingo, num_semana in domingos:
                for t in range(cant_turno):
                    lista_domingo_suma.append(mes[num_semana][domingo][3][e][t])
            model.Add(sum(lista_domingo_suma) == len(domingos) - (num_empleado-cant_turno))#2
    else:
        for e in all_empleado: 
            lista_domingo_suma = []
            for domingo, num_semana in domingos:
                for t in range(cant_turno):
                    lista_domingo_suma.append(mes[num_semana][domingo][3][e][t])
            model.Add(sum(lista_domingo_suma) == len(domingos) - (num_empleado-cant_turno))#2
    
                #dia,turno,empleado
    itinerario=[[5,2,2],
                [12,2,2],
                [19,2,3],
                [23,2,2],
                [9,2,3],
                [26,2,3]]
    
    def OrdenarLista(a,b,c,ind_a,ind_b,ind_c):
        lista = []
        if(a>b and b>c):
            lista.append(ind_c)
            lista.append(ind_b)
            lista.append(ind_a)
            return lista
        elif(b>a and a>c):
            lista.append(ind_c)
            lista.append(ind_a)
            lista.append(ind_b)
            return lista
        elif(c>a and a>b):
            lista.append(ind_b)
            lista.append(ind_a)
            lista.append(ind_c)
            return lista
        elif(c>b and b>a):
            lista.append(ind_a)
            lista.append(ind_b)
            lista.append(ind_c)
            return lista
        elif(a>c and c>b):
            lista.append(ind_b)
            lista.append(ind_c)
            lista.append(ind_a)
            return lista
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
            return OrdenarLista(a,b,c,lista[0],lista[1],-1)
        elif(len(lista)==3):
            a = itinerario[lista[0]][1]
            b = itinerario[lista[1]][1]
            c = itinerario[lista[2]][1]
            return OrdenarLista(a,b,c,lista[0],lista[1],lista[2])
        else:
            return lista
    

    lista_alarma_turno = []
    dias_libre_semana = num_empleado
    turnos_extra = 6*num_empleado-dias_libre_semana-6*cant_turno # 30-5-18 = 23 empleados
    list_itinerario = []
    list_turno_extra = []

    #Lista de cantidad de empleados de cada turno del dia
    indice=0
    for num_semana in range(len(cont_semana)):
        semana_work = []
        work_extra = turnos_extra
        for i in range(cont_semana[indice]):
            if(mes[num_semana][i][0]==meses_anio[month-1]):
                list_index_itinerario = ItinerarioFunction(mes[num_semana][i][1],itinerario)
                if(i!=6):
                    if(len(list_index_itinerario)>1):
                        dia_work = [] 
                        for j in range(3):
                            index_iti = list_index_itinerario[j]
                            if(index_iti != -1):
                                if((itinerario[index_iti][2]+cant_turno-1<=5)and(work_extra>=itinerario[index_iti][2])):
                                    work_extra = work_extra+1 - itinerario[index_iti][2]
                                    dia_work.append(
                                        model.NewIntVar(itinerario[index_iti][2],itinerario[index_iti][2],"turno %i" % (j+1))
                                    )
                                else:
                                    print("no alcanza")
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
                            semana_work.append(dia_work)
                        else:
                            print("No alcanza")
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

    # Turnos sobrantes por asignar en la mañana.
    indice = 0
    for num_semana in range(len(cont_semana)):
        work_extra = list_turno_extra[num_semana]
        if(work_extra>=1):
            #print(list_turno_extra[indice])
            for i in range(list_turno_extra[num_semana]):
                #print(mes[num_semana][i][1])
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
                    for k in range(list_turno_extra[num_semana]):
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
                                    work_extra = work_extra - 1
            indice = indice + 1
            #print("----")

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

    if(len(domingos)==5):
        for num_semana in range(len(cont_semana)):
            for i in range(cont_semana[num_semana]):
                if(mes[num_semana][i][2]=="Domingo" and mes[num_semana][i][0] == meses_anio[month-1]):
                    ind_domingo = ItinerarioFunction(mes[num_semana][i][1],itinerario)
                    if(ind_domingo != []):
                        falta = itinerario[ind_domingo[0]][2]-1
                        lista_alarma_turno.append([itinerario[ind_domingo[0]][0],itinerario[ind_domingo[0]][1],itinerario[ind_domingo[0]][2],falta])
    else:
        for domingo, num_semana in domingos:
            ind_domingo = ItinerarioFunction(num_semana,itinerario)
            lista_alarma_turno

            print(domingo)
            print(num_semana)
            print("______________")

    print(lista_alarma_turno)
    print("______________")

    list_four_mana = [[1,1,0],[1,1,0],[1,1,1],[1,1,1]]
    list_four_mana[0] = shuffle(list_four_mana[0])
    list_four_mana[1] = shuffle(list_four_mana[1])
    list_four_mana = shuffle(list_four_mana)
    indice = 0
    for num_semana in range(len(cont_semana)):
        for i in range(cont_semana[indice]):
            if(len(domingos)==5): # 5 DOMINGOS
                if(mes[num_semana][i][2]=="Domingo" and mes[num_semana][i][0] == meses_anio[month-1]):
                    model.Add(sum(mes[num_semana][i][3][e][0] for e in all_empleado)>=1)
                    model.Add(sum(mes[num_semana][i][3][e][1] for e in all_empleado)>=1)
                    model.Add(sum(mes[num_semana][i][3][e][2] for e in all_empleado)>=1)
                else:
                    model.Add(sum(mes[num_semana][i][3][e][0] for e in all_empleado)==list_itinerario[num_semana][i][0])
                    model.Add(sum(mes[num_semana][i][3][e][1] for e in all_empleado)==list_itinerario[num_semana][i][1])
                    model.Add(sum(mes[num_semana][i][3][e][2] for e in all_empleado)==list_itinerario[num_semana][i][2])
            else: # 4 DOMINGOS - ASIGNA LOS VALORES DE LIST FOUR PARA QUE HAYA COMO MÍNIMO 2 TRABAJADORES
                if(mes[num_semana][i][2]=="Domingo" and mes[num_semana][i][0] == meses_anio[month-1]):
                    model.Add(sum(mes[num_semana][i][3][e][0] for e in all_empleado)>=list_four_mana[num_semana][0])
                    model.Add(sum(mes[num_semana][i][3][e][1] for e in all_empleado)>=list_four_mana[num_semana][1])
                    model.Add(sum(mes[num_semana][i][3][e][2] for e in all_empleado)>=list_four_mana[num_semana][2])
                else:
                    model.Add(sum(mes[num_semana][i][3][e][0] for e in all_empleado)==list_itinerario[num_semana][i][0])
                    model.Add(sum(mes[num_semana][i][3][e][1] for e in all_empleado)==list_itinerario[num_semana][i][1])
                    model.Add(sum(mes[num_semana][i][3][e][2] for e in all_empleado)==list_itinerario[num_semana][i][2])
        indice = indice + 1
    
    # Crea el solver y la solución
    solver = cp_model.CpSolver()
    solver.parameters.linearization_level = 0

    # Enumera todas las soluciones encontradas
    solver.parameters.enumerate_all_solutions = True
    solution_limit = 100
    solution_number = random.randint(1,solution_limit)
    solution_printer = SolutionPrinter(solution_number,list_itinerario,mes,cont_semana,all_empleado,all_dias,cant_turno,solution_limit,meses_anio)
    solver.Solve(model, solution_printer)


year = int(sys.argv[1]) 
month = int(sys.argv[2])
num_empleado = int(sys.argv[3])
json = GenerarPlanificacion(year,month,num_empleado)


