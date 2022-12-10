from numpy import array
from sklearn.utils import shuffle
import sys
import random
from calendar import monthrange
from ortools.sat.python import cp_model
import json

def GenerarPlanificacion(year,month,num_empleado,nuevo_itinerario):
    class SolutionPrinter(cp_model.CpSolverSolutionCallback):
        """Clase para imprimir la solución."""

        def __init__(self,lista_alarma_turno, lista_comodin_turno,solution_number,list_itinerario,mes,cont_semana,all_empleado,all_dias,cant_turno,solution_limit,meses_anio):
            cp_model.CpSolverSolutionCallback.__init__(self)
            self._lista_alarma_turno = lista_alarma_turno
            self._lista_comodin_turno = lista_comodin_turno
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
            #print(self._lista_comodin_turno)
            if(self._solution_count == self._solution_number):
                json_v = []
                #print(self._lista_alarma_turno)

                contador = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

                for num_semana in range(len(self._cont_semana)):
                    for i in range(self._cont_semana[num_semana]):
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
                                    contador[j][t+1] = contador[j][t+1] + 1 
                            if not is_working:
                                emp_turn["turno"] = 0
                                emp_turn["nombre"] = j+1
                                contador[j][0] = contador[j][0] + 1
                            empleados.append(emp_turn)
                        dia["empleados"] = empleados
                        
                        if(self._mes[num_semana][i][0] == self._meses_anio[month-1]):
                            itinerario_array = []
                            itinerario_var = 0
                            for k in range(len(self._lista_alarma_turno)):
                                if(self._mes[num_semana][i][1]==self._lista_alarma_turno[k][0]):
                                    itinerario_turno = {}
                                    itinerario_turno["turno_itinerario"] = self._lista_alarma_turno[k][1]
                                    itinerario_turno["falta"] = self._lista_alarma_turno[k][2]
                                    itinerario_array.append(itinerario_turno)
                                    itinerario_var = 1
                                
                            if(itinerario_var == 0):
                                dia["itinerario"] = itinerario_var
                            else:
                                dia["itinerario"] = itinerario_array
                            
                            comodin = 0
                            for c in range(len(self._lista_comodin_turno)):
                                if((self._mes[num_semana][i][1]==self._lista_comodin_turno[c][0])):
                                    comodin = self._lista_comodin_turno[c][1]
                            if(comodin != 0):
                                dia["comodin"] = comodin
                            else:
                                dia["comodin"] = 0
                        else:
                            dia["itinerario"]=0
                            dia["comodin"]=0

                        json_v.append(dia)
                print(json.dumps(json_v))
            if self._solution_count >= self._solution_limit:
                self.StopSearch()
        
        def solution_count(self):
            #print(self._solution_count)
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
    cant_turnos_totales = [0,0,0]
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

    # Cada empleado tiene 1 día libre por semana 
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
    #itinerario=[[1,1,3],[2,2,3]]
    #            [19,2,3],#2
    #            [19,3,3]]#2->1
    
    
    itinerario = nuevo_itinerario

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
    
    lista_comodin_turno = []
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
        control_five_turnos = True
        for i in range(cont_semana[indice]):
            if(mes[num_semana][i][0]==meses_anio[month-1]):
                list_index_itinerario = ItinerarioFunction(mes[num_semana][i][1],itinerario)
                if(i!=6):
                    if(len(list_index_itinerario)>1):
                        dia_work = [] 

                        acumulador = num_empleado - cant_turno

                        for j in range(cant_turno):
                            index_itinerario = list_index_itinerario[j]
                            if(index_itinerario != -1):
                                if((acumulador>=itinerario[index_itinerario][2]-1) and (work_extra>= itinerario[index_itinerario][2]-1) and (acumulador>0)):
                                    #TODO: Entra si esta dentro de lo permitido y lo asigna como preferencia
                                    acumulador = acumulador - (itinerario[index_itinerario][2])+1
                                    work_extra = work_extra - itinerario[index_itinerario][2]+1
                                    dia_work.append(
                                        model.NewIntVar(itinerario[index_itinerario][2], itinerario[index_itinerario][2],"turno %i" % (j+1))
                                    )
                                    cant_turnos_totales[j] = cant_turnos_totales[j] + itinerario[index_itinerario][2]
                                    
                                elif((acumulador<itinerario[index_itinerario][2]-1) and (acumulador>=0) and (work_extra>=itinerario[index_itinerario][2]-1)):
                                    #TODO: Entra si hay espacio pero no alcanza, por tanot, asigna un resto y lo demás a la lista
                                    for k in range(1, itinerario[index_itinerario][2]):
                                        if(acumulador-k==0):
                                            work_extra = work_extra - k
                                            break
                                    if(acumulador>0):
                                        acumulador = acumulador - k
                                        dia_work.append(#4-1
                                            model.NewIntVar(itinerario[index_itinerario][2]-(itinerario[index_itinerario][2]-k-1),itinerario[index_itinerario][2]-(itinerario[index_itinerario][2]-k-1),"turno %i" % (j+1))
                                        )
                                        
                                        cant_turnos_totales[j] = cant_turnos_totales[j] + itinerario[index_itinerario][2]-(itinerario[index_itinerario][2]-k-1)

                                        lista_alarma_turno.append([itinerario[index_itinerario][0],itinerario[index_itinerario][1],itinerario[index_itinerario][2]-k-1])


                                    elif(acumulador==0):
                                        dia_work.append(#4-0
                                            model.NewIntVar(itinerario[index_itinerario][2]-k,itinerario[index_itinerario][2]-k,"turno %i" % (j+1))
                                        )
                                        cant_turnos_totales[j] = cant_turnos_totales[j] + itinerario[index_itinerario][2]-k
                                        
                                        lista_alarma_turno.append([itinerario[index_itinerario][0],itinerario[index_itinerario][1],k])


                                elif((acumulador==0) and (work_extra<=itinerario[index_itinerario][2]-1)):
                                    #TODO: Entra si ya no hay más espacio para aasignar
                                    dia_work.append(
                                        model.NewIntVar(1,1,"turno %i" % (j+1))
                                    )
                                    cant_turnos_totales[j] = cant_turnos_totales[j] + 1
                                    lista_alarma_turno.append([itinerario[index_itinerario][0],itinerario[index_itinerario][1],itinerario[index_itinerario][2]-1,])
                            else:
                                dia_work.append(
                                    model.NewIntVar(1,1,"turno %i" % (j+1))
                                )
                                cant_turnos_totales[j] = cant_turnos_totales[j] + 1
                        semana_work.append(dia_work)
                    elif(len(list_index_itinerario)==1):
                        index_itinerario = list_index_itinerario[0]
                        dia_work = []
                        if((itinerario[index_itinerario][2]+cant_turno-1==num_empleado)and(work_extra>=itinerario[index_itinerario][2]-1)and(control_five_turnos==False)):
                            work_extra = work_extra+1 - itinerario[index_itinerario][2]
                            for t in range(cant_turno):
                                if(itinerario[index_itinerario][1]==(t+1)):
                                    dia_work.append(
                                        model.NewIntVar(itinerario[index_itinerario][2]-1,itinerario[index_itinerario][2]-1,"turno %i" % (t+1))
                                    )
                                    cant_turnos_totales[t] = cant_turnos_totales[t] + itinerario[index_itinerario][2]
                                else:
                                    dia_work.append(
                                        model.NewIntVar(1,num_empleado-itinerario[index_itinerario][2],"turno %i" % (t+1))
                                    )
                                    cant_turnos_totales[t] = cant_turnos_totales[t] + 1
                            lista_alarma_turno.append([itinerario[index_itinerario][0],itinerario[index_itinerario][1],1])
                            semana_work.append(dia_work)

                        elif((itinerario[index_itinerario][2]+cant_turno-1==num_empleado)and(work_extra>=itinerario[index_itinerario][2]-1)and(control_five_turnos==True)):
                            control_five_turnos = False
                            work_extra = work_extra+1 - itinerario[index_itinerario][2]
                            for t in range(cant_turno):
                                if(itinerario[index_itinerario][1]==(t+1)):
                                    dia_work.append(
                                        model.NewIntVar(itinerario[index_itinerario][2],itinerario[index_itinerario][2],"turno %i" % (t+1))
                                    )
                                    cant_turnos_totales[t] = cant_turnos_totales[t] + itinerario[index_itinerario][2]
                                else:
                                    dia_work.append(
                                        model.NewIntVar(1,num_empleado-itinerario[index_itinerario][2],"turno %i" % (t+1))
                                    )
                                    cant_turnos_totales[t] = cant_turnos_totales[t] + 1
                            semana_work.append(dia_work)
                        
                        elif((itinerario[index_itinerario][2]+cant_turno-1<num_empleado)and(work_extra>=itinerario[index_itinerario][2]-1)):
                            work_extra = work_extra+1 - itinerario[index_itinerario][2]
                            for t in range(cant_turno):
                                if(itinerario[index_itinerario][1]==(t+1)):
                                    dia_work.append(
                                        model.NewIntVar(itinerario[index_itinerario][2],itinerario[index_itinerario][2],"turno %i" % (t+1))
                                    )
                                    cant_turnos_totales[t] = cant_turnos_totales[t] + itinerario[index_itinerario][2]
                                else:
                                    dia_work.append(
                                        model.NewIntVar(1,num_empleado-itinerario[index_itinerario][2],"turno %i" % (t+1))
                                    )
                                    cant_turnos_totales[t] = cant_turnos_totales[t] + 1
                            
                            semana_work.append(dia_work)

                        elif((itinerario[index_itinerario][2]+cant_turno-1>num_empleado)and(work_extra>=itinerario[index_itinerario][2]-1)and(control_five_turnos==True)):
                            control_five_turnos = False
                            for t in range(cant_turno):
                                if(itinerario[index_itinerario][1]==(t+1)):
                                    for k in range(1,itinerario[index_itinerario][2]):
                                        if(k+cant_turno-1 == num_empleado):
                                            work_extra = work_extra - k+1
                                            break
                                    dia_work.append(
                                        model.NewIntVar(k,k,"turno %i" % (t+1))
                                    )
                                    cant_turnos_totales[t] = cant_turnos_totales[t] + k
                                else:
                                    dia_work.append(
                                        model.NewIntVar(1,1,"turno %i" % (t+1))
                                    )
                                    cant_turnos_totales[t] = cant_turnos_totales[t] + 1
                            semana_work.append(dia_work)
                            lista_alarma_turno.append([itinerario[index_itinerario][0],itinerario[index_itinerario][1], itinerario[index_itinerario][2]-k])
                        elif((itinerario[index_itinerario][2]+cant_turno-1>num_empleado)and(work_extra>=itinerario[index_itinerario][2]-1)and(control_five_turnos==False)):
                            for t in range(cant_turno):
                                if(itinerario[index_itinerario][1]==(t+1)):
                                    for k in range(1,itinerario[index_itinerario][2]):
                                        if(k+cant_turno-1 == num_empleado-1):
                                            work_extra = work_extra - k+1
                                            break
                                    dia_work.append(
                                        model.NewIntVar(k,k,"turno %i" % (t+1))
                                    )
                                    cant_turnos_totales[t] = cant_turnos_totales[t] + k
                                else:
                                    dia_work.append(
                                        model.NewIntVar(1,1,"turno %i" % (t+1))
                                    )
                                    cant_turnos_totales[t] = cant_turnos_totales[t] + 1
                            semana_work.append(dia_work)
                            lista_alarma_turno.append([itinerario[index_itinerario][0],itinerario[index_itinerario][1], itinerario[index_itinerario][2]-k])
                        elif((itinerario[index_itinerario][2]+cant_turno-1<=num_empleado) and (work_extra==0)):
                            semana_work.append([
                                model.NewIntVar(1,num_empleado-cant_turno+1,"turno 1"),
                                model.NewIntVar(1,num_empleado-cant_turno+1,"turno 2"),
                                model.NewIntVar(1,num_empleado-cant_turno+1,"turno 3")
                            ])
                            cant_turnos_totales[0] = cant_turnos_totales[0] + 1
                            cant_turnos_totales[1] = cant_turnos_totales[1] + 1
                            cant_turnos_totales[2] = cant_turnos_totales[2] + 1

                            lista_alarma_turno.append([itinerario[index_itinerario][0],itinerario[index_itinerario][1],itinerario[index_itinerario][2]-1])
                        elif(((itinerario[index_itinerario][2]+cant_turno-1<=num_empleado) and (work_extra>0) and (work_extra<itinerario[index_itinerario][2]-1))):
                            for t in range(cant_turno):
                                if(itinerario[index_itinerario][1]==(t+1)):
                                    for k in range(1,itinerario[index_itinerario][2]):
                                        if(work_extra-k==0):
                                            work_extra = work_extra - k+1
                                            break
                                    dia_work.append(
                                        model.NewIntVar(itinerario[index_itinerario][2]-k,itinerario[index_itinerario][2]-k,"turno %i" % (j+1))
                                    )
                                    cant_turnos_totales[t] = cant_turnos_totales[t] + itinerario[index_itinerario][2]-k
                                    lista_alarma_turno.append([itinerario[index_itinerario][0],itinerario[index_itinerario][1],k])
                                else:
                                    dia_work.append(
                                        model.NewIntVar(1,1,"turno %i" % (t+1))
                                    )
                                    cant_turnos_totales[t] = cant_turnos_totales[t] + 1
                            semana_work.append(dia_work)
                    else:
                        semana_work.append([
                            model.NewIntVar(1,num_empleado-cant_turno+1,"turno 1"),
                            model.NewIntVar(1,num_empleado-cant_turno+1,"turno 2"),
                            model.NewIntVar(1,num_empleado-cant_turno+1,"turno 3")
                        ])
                        cant_turnos_totales[0] = cant_turnos_totales[0] + 1
                        cant_turnos_totales[1] = cant_turnos_totales[1] + 1
                        cant_turnos_totales[2] = cant_turnos_totales[2] + 1
            else:
                semana_work.append([
                    model.NewIntVar(1,num_empleado-cant_turno+1,"turno 1"),
                    model.NewIntVar(1,num_empleado-cant_turno+1,"turno 2"),
                    model.NewIntVar(1,num_empleado-cant_turno+1,"turno 3")
                ])
                if(i!=6):
                    cant_turnos_totales[0] = cant_turnos_totales[0] + 1
                    cant_turnos_totales[1] = cant_turnos_totales[1] + 1
                    cant_turnos_totales[2] = cant_turnos_totales[2] + 1

        list_itinerario.append(semana_work)
        list_turno_extra.append(work_extra)
        indice = indice + 1

    # Turnos sobrantes por asignar en la mañana.
    indice = 0
    for num_semana in range(len(cont_semana)):
        work_extra = list_turno_extra[num_semana]


        if(work_extra>=1):
            for i in range(list_turno_extra[num_semana]):
                if(mes[num_semana][i][0]==meses_anio[month-1]):
                    list_index_itinerario = ItinerarioFunction(mes[num_semana][i][1], itinerario)
                    if((i<=5) and (work_extra>=1)): # ASIGNACIÓN EN LA MAÑANA
                        if(len(list_index_itinerario)==0):
                            model.Add(list_itinerario[num_semana][i][0]==2)
                            work_extra = work_extra - 1
                            cant_turnos_totales[0] = cant_turnos_totales[0] + 1

                        elif((len(list_index_itinerario)==1) and (itinerario[list_index_itinerario[0]][1]!=1) and (itinerario[list_index_itinerario[0]][2]+cant_turno-1<num_empleado)):
                            model.Add(list_itinerario[num_semana][i][0]==2)
                            work_extra = work_extra - 1
                            cant_turnos_totales[0] = cant_turnos_totales[0] + 1

                        elif((len(list_index_itinerario)==1 or len(list_index_itinerario)>=2) and (i<5)):
                            model.Add(list_itinerario[num_semana][i+1][0]==2)
                            work_extra = work_extra -1
                            cant_turnos_totales[0] = cant_turnos_totales[0] + 1

                        elif((len(list_index_itinerario)==1 or len(list_index_itinerario)>=2) and (itinerario[list_index_itinerario[0]][1]!=1) and i==5):
                            model.Add(list_itinerario[num_semana+1][0][1]==2)
                            work_extra = work_extra - 1
                            cant_turnos_totales[0] = cant_turnos_totales[0] + 1

                    elif((i==6) and (work_extra>=1)): # ASIGNACIÓN EN LA TARDE
                        for i in range(5):
                            if(len(list_index_itinerario)==0 and (work_extra>=1)):
                                model.Add(list_itinerario[num_semana][i][1]==2)
                                work_extra = work_extra - 1
                                cant_turnos_totales[1] = cant_turnos_totales[1] + 1

                            elif((len(list_index_itinerario)==1) and (itinerario[list_index_itinerario[0]][1]!=2) and (itinerario[list_index_itinerario[0]][2]+cant_turno-1<num_empleado) and (work_extra>=1)):
                                model.Add(list_itinerario[num_semana][i][1]==2)
                                work_extra = work_extra - 1
                                cant_turnos_totales[1] = cant_turnos_totales[1] + 1

                            elif((len(list_index_itinerario)==1 or len(list_index_itinerario)>=2) and (i<5) and (work_extra>=1)):
                                model.Add(list_itinerario[num_semana][i+1][1]==2)

                                work_extra = work_extra -1
                                cant_turnos_totales[1] = cant_turnos_totales[1] + 1

                else: 
                    if((i<=5) and (work_extra>=1)): # ASIGNACIÓN EN LA MAÑANA
                        if(len(list_index_itinerario)==0):
                            model.Add(list_itinerario[num_semana][i][0]==2)

                            work_extra = work_extra - 1
                            cant_turnos_totales[0] = cant_turnos_totales[0] + 1

                    elif((i==6) and (work_extra>=1)): # ASIGNACIÓN EN LA TARDE
                        for i in range(5):
                            if(len(list_index_itinerario)==0 and (work_extra>=1)):
                                model.Add(list_itinerario[num_semana][i][1]==2)
                                work_extra = work_extra - 1
                                cant_turnos_totales[1] = cant_turnos_totales[1] + 1


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
    
    list_complete_dom = [[1,1,1],[1,1,1]]
    list_incomplete_dom = [[1,1,0],[1,1,0]]
    list_complete = []

    if(len(domingos)==5):
        for num_semana in range(len(cont_semana)):
            for i in range(cont_semana[num_semana]):
                if(mes[num_semana][i][2]=="Domingo" and mes[num_semana][i][0] == meses_anio[month-1]):
                    cant_turnos_totales[0] = cant_turnos_totales[0] + 1
                    cant_turnos_totales[1] = cant_turnos_totales[1] + 1
                    cant_turnos_totales[2] = cant_turnos_totales[2] + 1
                    list_index_domingo = ItinerarioFunction(mes[num_semana][i][1],itinerario)
                    if(len(list_index_domingo)!=0):
                        for index_itinerario in list_index_domingo:
                            if(index_itinerario != -1):
                                lista_alarma_turno.append([itinerario[index_itinerario][0],itinerario[index_itinerario][1],itinerario[index_itinerario][2]-1])
                

    elif(len(domingos)==4):
        for num_semana in range(len(cont_semana)):
            for i in range(cont_semana[num_semana]):
                if(mes[num_semana][i][2]=="Domingo" and mes[num_semana][i][0] == meses_anio[month-1]):
                    list_index_domingo = ItinerarioFunction(mes[num_semana][i][1],itinerario)
                    if(len(list_index_domingo)!=0): # HAY ITINERARIO 
                        for index_itinerario in list_index_domingo:
                            if(index_itinerario != -1):
                                if(len(list_complete_dom)>0):
                                    list_complete.append(list_complete_dom.pop())
                                    lista_alarma_turno.append([itinerario[index_itinerario][0],itinerario[index_itinerario][1],itinerario[index_itinerario][2]-1])
                                    cant_turnos_totales[0] = cant_turnos_totales[0] + 1
                                    cant_turnos_totales[1] = cant_turnos_totales[1] + 1
                                    cant_turnos_totales[2] = cant_turnos_totales[2] + 1
                                    #print(cant_turnos_totales)

                                else:
                                    list_aux = list_incomplete_dom.pop()
                                    list_aux = shuffle(list_aux)
                                    indice_min = list_aux.index(min(list_aux))
                                    if(indice_min == itinerario[index_itinerario][1]-1):
                                        if(indice_min==2):
                                            list_aux.pop()
                                            list_aux.pop()
                                            list_aux.append(0)
                                            list_aux.append(1)
                                            lista_alarma_turno.append([itinerario[index_itinerario][0],itinerario[index_itinerario][1],itinerario[index_itinerario][2]-1])
                                            lista_comodin_turno.append([mes[num_semana][i][1],indice_min+1,1])
                                            cant_turnos_totales[0] = cant_turnos_totales[0] + 1
                                            cant_turnos_totales[2] = cant_turnos_totales[2] + 1
                                            #print(cant_turnos_totales)

                                        else: 
                                            list_aux.pop()
                                            list_aux.insert(indice_min,1)
                                            for t in range(cant_turno):
                                                if(indice_min != t):
                                                    cant_turnos_totales[t] = cant_turnos_totales[t] + 1
                                            lista_alarma_turno.append([itinerario[index_itinerario][0],itinerario[index_itinerario][1],itinerario[index_itinerario][2]-1])
                                            lista_comodin_turno.append([mes[num_semana][i][1],indice_min+1,1])
                                            #print(cant_turnos_totales)
                                    else: 
                                        for t in range(cant_turno):
                                            if(indice_min != t):
                                                cant_turnos_totales[t] = cant_turnos_totales[t] + 1
                                        lista_alarma_turno.append([itinerario[index_itinerario][0],itinerario[index_itinerario][1],itinerario[index_itinerario][2]-1])
                                        lista_comodin_turno.append([mes[num_semana][i][1],indice_min+1,1])
                                        #print(cant_turnos_totales)

                                        
                                    list_complete.append(list_aux)
                    else: # NO HAY ITINERARIO EN ESTE DOMINGO
                        if(len(list_incomplete_dom)>0):
                            list_aux = shuffle(list_incomplete_dom.pop())
                            list_complete.append(list_aux)
                            for t in range(cant_turno):
                                if(list_aux[t]==0):
                                    lista_comodin_turno.append([mes[num_semana][i][1],t+1,1])
                                else:
                                    cant_turnos_totales[t] = cant_turnos_totales[t] + 1
                            #print(cant_turnos_totales)

                        else:
                            list_complete.append(list_complete_dom.pop())
                            cant_turnos_totales[0] = cant_turnos_totales[0] + 1
                            cant_turnos_totales[1] = cant_turnos_totales[1] + 1
                            cant_turnos_totales[2] = cant_turnos_totales[2] + 1
                            #print(cant_turnos_totales)


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
                    model.Add(sum(mes[num_semana][i][3][e][0] for e in all_empleado)>=list_complete[num_semana][0])
                    model.Add(sum(mes[num_semana][i][3][e][1] for e in all_empleado)>=list_complete[num_semana][1])
                    model.Add(sum(mes[num_semana][i][3][e][2] for e in all_empleado)>=list_complete[num_semana][2])
                else:
                    model.Add(sum(mes[num_semana][i][3][e][0] for e in all_empleado)==list_itinerario[num_semana][i][0])
                    model.Add(sum(mes[num_semana][i][3][e][1] for e in all_empleado)==list_itinerario[num_semana][i][1])
                    model.Add(sum(mes[num_semana][i][3][e][2] for e in all_empleado)==list_itinerario[num_semana][i][2])
        indice = indice + 1
    
    #Distribuye los turno de maneraz uniforme para cada empleado
    # mínima cantidad de turnos de la mañana
    min_turno_manana =  cant_turnos_totales[0] // num_empleado
    # mínima cantidad de turnos de la tarde
    min_turno_tarde = cant_turnos_totales[1] // num_empleado
    # mínima cantidad de turnos de la noche
    min_turno_noche = cant_turnos_totales[2] // num_empleado

    # MANANA
    if(cant_turnos_totales[0] % num_empleado == 0):
        max_turno_manana = min_turno_manana
    else:
        max_turno_manana = min_turno_manana + 1
    # TARDE
    if(cant_turnos_totales[1] % num_empleado == 0):
        max_turno_tarde = min_turno_tarde
    else:
        max_turno_tarde = min_turno_tarde + 1
    # NOCHE
    if(cant_turnos_totales[2] % num_empleado == 0):
        max_turno_noche = min_turno_noche
    else:
        max_turno_noche = min_turno_noche + 1

    #print("%i + %i + %i = %i "  % (cant_turnos_totales[0],cant_turnos_totales[1],cant_turnos_totales[2],cant_turnos_totales[0]+cant_turnos_totales[1]+cant_turnos_totales[2]))
    # TURNOS TOTALES
    turno_totales = cant_turnos_totales[0] + cant_turnos_totales[1] + cant_turnos_totales[2]
    min_turno_totales = turno_totales // num_empleado
    
    if(turno_totales % num_empleado == 0):
        max_turno_totales = min_turno_totales
    else:
        max_turno_totales = min_turno_totales + 1


    # CANTIDAD DE TURNOS IGUALES = 28
    for e in all_empleado:
        turno_totales_emp = []
        manana = []
        tarde = []
        noche = []
        for num_semana in range(len(cont_semana)):
            for i in range(cont_semana[num_semana]):
                    for t in range(cant_turno):
                        if(t==0):
                            manana.append(mes[num_semana][i][3][e][0])
                        elif(t==1):
                            tarde.append(mes[num_semana][i][3][e][1])
                        else:
                            noche.append(mes[num_semana][i][3][e][2])
                        turno_totales_emp.append(mes[num_semana][i][3][e][t])
        model.Add(min_turno_manana <= sum(manana))
        #model.Add(sum(manana) <= max_turno_manana)
        
        model.Add(min_turno_tarde <= sum(tarde))
        #model.Add(sum(tarde) <= max_turno_tarde)
        
        model.Add(min_turno_noche <= sum(noche))
        #model.Add(sum(noche) <= max_turno_noche)

        model.Add(min_turno_totales <= sum(turno_totales_emp))
    
    #print([cant_turnos_totales[0],cant_turnos_totales[1],cant_turnos_totales[2]])
    #print(cant_turnos_totales[0]+cant_turnos_totales[1]+cant_turnos_totales[2])
    #print(lista_alarma_turno)
    #print("________")
    #print(lista_comodin_turno)
    # Crea el solver y la solución
    solver = cp_model.CpSolver()
    solver.parameters.linearization_level = 0

    # Enumera todas las soluciones encontradas
    solver.parameters.enumerate_all_solutions = True
    solution_limit = 10
    solution_number = random.randint(1,solution_limit)
    solution_printer = SolutionPrinter(lista_alarma_turno, lista_comodin_turno,solution_number,list_itinerario,mes,cont_semana,all_empleado,all_dias,cant_turno,solution_limit,meses_anio)
    solver.Solve(model, solution_printer)

    # Statistics.
    #print('\nStatistics')
    #print('  - conflicts      : %i' % solver.NumConflicts())
    #print('  - branches       : %i' % solver.NumBranches())
    #print('  - wall time      : %f s' % solver.WallTime())
    #print('  - solutions found: %i' % solution_printer.solution_count())

year = int(sys.argv[1]) 
month = int(sys.argv[2])
num_empleado = int(sys.argv[3])
itinerario = str(sys.argv[4])
if(itinerario != '0'):
    nuevo_itinerario=[]
    array = []
    cont = 0
    for caracter in itinerario.split(','):
        if(cont<2):
            array.append(int(caracter))
            cont = cont + 1
        elif(cont==2):
            array.append(int(caracter))
            nuevo_itinerario.append(array)
            cont = 0
            array = []
else: 
    nuevo_itinerario = []

GenerarPlanificacion(year,month,num_empleado, nuevo_itinerario)

