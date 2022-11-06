from statistics import mode
import sys
import random
from calendar import monthrange
from ortools.sat.python import cp_model

def main():
    
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
                for num_semana in range(len(self._cont_semana)):
                    print("Semana %i"% (indice+1))
                    for i in range(self._cont_semana[indice]):
                        print("_____________________________")
                        print("Día n° %i - %s " % (self._mes[num_semana][i][0],self._mes[num_semana][i][1]))
                        #if(self._mes[num_semana][i][1]=="Domingo"):
                        for j in all_empleado:
                            is_working = False
                            for t in range(cant_turno):
                                if(self.Value(self._mes[num_semana][i][2][j][t])):
                                    is_working = True
                                    print('Empleado %i trabaja en el turno %i' % ((j+1), (t+1)))
                            if not is_working:
                                print('Empleado {} no trabaja en el turno'.format(j+1))
                    print("----------------------------------")                
                    indice = indice + 1
            if self._solution_count >= self._solution_limit:
                self.StopSearch()
        
        def solution_count(self):
            return self._solution_count

    year = int(sys.argv[1]) 
    month = int(sys.argv[2])
    num_empleado = int(sys.argv[3])

    #

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
    
    print("año: %i mes anterior: %i " % (year_prev, month_prev))
    print("año: %i mes actual: %i " % (year, month))
    print("año: %i mes siguiente: %i " % (year_next, month_next))
    

    dias_mes_prev = monthrange(year_prev, month_prev)
    dias_mes_actual  = monthrange(year,month)
    dias_mes_next = monthrange(year_next, month_next)
    
    indice_semana_prev = dias_mes_prev[0]
    cantidad_dias_prev = dias_mes_prev[1]

    indice_semana = dias_mes_actual[0]
    cantidad_dias = dias_mes_actual[1]

    indice_semana_next = dias_mes_next[0]
    cantidad_dias_next = dias_mes_next[1]


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
                semana.append([dia, dias_semana[indice_semana], array_empleado])
                mes.append(semana)
            else: 
                semana.append([dia, dias_semana[indice_semana], array_empleado])
        else: #TODO: SE TENDRÍAN QUE AGREGAR LOS DÍAS DEL MES PASADO (DATOS VIEJOS) Y LOS DEL MES NUEVO (A GENERAR)
            array_empleado = empleado_turno()
            if(dia == cantidad_dias):
                semana.append([dia, dias_semana[indice_semana], array_empleado])
                mes.append(semana)
            else:
                semana.append([dia, dias_semana[indice_semana], array_empleado])
        indice_semana = indice_semana + 1
        if(indice_semana == 7): indice_semana=0

    cont_semana = []
    # For para contar la cantidad de semanas
    for i in mes:
        cont_semana.append(len(i))
    
    indice = 0
    # For para imprimir
    """for num_semana in range(len(cont_semana)):
        print("semana n° %i" % num_semana)
        for i in range(cont_semana[indice]):
            print("dia n°: %i %s" % (mes[num_semana][i][0],mes[num_semana][i][1]))
        indice = indice + 1"""
    
     ## Restricciones
    # Cada empleado trabaja como máximo un turno por día. (Puede ser 0 porque puede tener el día libre al ser solo 3 turnos)
    for e in all_empleado:
        indice = 0
        for num_semana in range(len(cont_semana)):
            for i in range(cont_semana[indice]):
                model.AddAtMostOne(mes[num_semana][i][2][e][t] for t in range(cant_turno))
            indice = indice + 1

    # Cada turno es asignado a solo un empleado por día.
    # (Esta restricción debe depender según la cantidad de aviones que llegue a ese turno con al menos una diferencia de 20 minutos.)   
    indice = 0
    for num_semana in range(len(cont_semana)):
        for i in range(cont_semana[indice]):
                #El turno de la mañana tiene como mínimo 2 empleados.
                model.Add(sum(mes[num_semana][i][2][e][0] for e in all_empleado)>=1)
                #El turno de la tarde tiene como mínimo 1 empleado.
                model.Add(sum(mes[num_semana][i][2][e][1] for e in all_empleado)>=1)
                #El turno de la noche tiene comom mínimo 1 empleado.
                model.Add(sum(mes[num_semana][i][2][e][2] for e in all_empleado)>=1)

        indice = indice + 1
    # Cada empleado tiene 1 día libre por semana [PREGUNTAR] BD
    for e in all_empleado:
        indice = 0
        for num_semana in range(len(cont_semana)):
            #print("semana %i" % (indice+1))
            lista_semana = []
            if(cont_semana[num_semana]==7):
                for i in range(cont_semana[indice]):
                    #print("dia %i" % (i+1))
                    if mes[num_semana][i][1] != 'Domingo':
                        for t in range(cant_turno):
                            lista_semana.append(mes[num_semana][i][2][e][t])
                            #print(mes[num_semana][i][2][e][t])
                        #print(mes[num_semana][i][0])
                model.Add(sum(lista_semana) == 5)
            indice = indice + 1


    # Los empleados tienen 2 domingos libres durante el mes [FUNCIONA, PERO CON 5 SEMANAS CON 4 ES IMPOSIBLE]
    domingos = []
    indice = 0
    for num_semana in range(len(cont_semana)):
        for i in range(cont_semana[indice]):
            if mes[num_semana][i][1] == 'Domingo': 
                domingos.append([i, num_semana]) # i: índice del día (0..6) // num_semana: 0..cant_semana
        i +=1
        indice = indice + 1

    for e in all_empleado: #4
        lista_domingo_suma = []
        for domingo, num_semana in domingos:
            for t in range(cant_turno):
                lista_domingo_suma.append(mes[num_semana][domingo][2][e][t])
        model.Add(sum(lista_domingo_suma) == len(domingos) - 2)
            

    # Las personas no pueden tener 2 turnos seguidos [FALTA VER QUE NO SEA SEGUIDO EN LA SIGUIENTE PLANIFIACION]
    
    for e in all_empleado:
        indice = 0
        for num_semana in range(len(cont_semana)):
            for i in range(cont_semana[indice]):
                lista_turno = []
                if(i+1!=cont_semana[indice]):
                    lista_turno.append(mes[num_semana][i][2][e][2])
                    lista_turno.append(mes[num_semana][i+1][2][e][0])
                    #print("dia %i |----| dia %i" % (mes[num_semana][i][0],mes[num_semana][i+1][0]))
                    #print("%s , %s" % (mes[num_semana][i][2][e][2],mes[num_semana][i+1][2][e][0]))
                    model.Add(sum(lista_turno) <= 1)
            indice = indice + 1

    # Distribución de los turnos de manera uniforme para cada empleado
    # Recordar modificar la variable : cantidad_min_turno_empleado por la cantidad de turnos que hay en el sistema
    """cantidad_min_turno_empleado = ((cant_turno+2) * cantidad_dias) // num_empleado
    if cant_turno * cantidad_dias % num_empleado == 0:
        cantidad_max_turno_empleado = cantidad_min_turno_empleado
    else:
        cantidad_max_turno_empleado = cantidad_min_turno_empleado + 1
    for e in all_empleado:
        num_turno_trabajado = []
        indice = 0
        for num_semana in range(len(cont_semana)): 
            for i in range(cont_semana[indice]):
                num_turno_trabajado.append(mes[num_semana][i][2][e][0])
                num_turno_trabajado.append(mes[num_semana][i][2][e][1])
                num_turno_trabajado.append(mes[num_semana][i][2][e][2])
            indice = indice +1
        model.Add(cantidad_min_turno_empleado <= sum(num_turno_trabajado))
        model.Add(sum(num_turno_trabajado) <= cantidad_max_turno_empleado)"""
    # Crea el solver y la solución
    solver = cp_model.CpSolver()
    solver.parameters.linearization_level = 0

    # Enumera todas las soluciones encontradas
    solver.parameters.enumerate_all_solutions = True
    solution_limit = 100
    solution_number = random.randint(1,solution_limit)
    """solution_printer = SolutionPrinter(solution_number,mes,cont_semana,all_empleado,all_dias,cant_turno,solution_limit)
    solver.Solve(model, solution_printer)
    # Statistics.
    print('\nStatistics')
    print('  - conflicts      : %i' % solver.NumConflicts())
    print('  - branches       : %i' % solver.NumBranches())
    print('  - wall time      : %f s' % solver.WallTime())
    print('  - solutions found: %i' % solution_printer.solution_count())"""

main()