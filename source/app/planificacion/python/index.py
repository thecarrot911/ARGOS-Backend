import json
import sys
import random
from ortools.sat.python import cp_model
from function.imprimirSolucion import SolutionPrinter
from function.restricciones import *
from function.itinerario import *
from function.distribucionUniforme import *
from function.definicionVariables import *

year = int(sys.argv[1]) 
month = int(sys.argv[2])
num_empleado = int(sys.argv[3])
itinerario = json.loads(sys.argv[4]) 
planificacionAnterior = json.loads(sys.argv[5])
comodin = sys.argv[6]
empPlan = sys.argv[7:]


for dia in itinerario:
    dia["turno"] = int(dia["turno"])
    
empleadoPlanificacionAnterior = []
if planificacionAnterior != None:
    for dia in planificacionAnterior:
        for empleado in dia:
            empleadoPlanificacionAnterior.append(empleado[1])
        break

empleadoPlanificacion = []

if empleadoPlanificacionAnterior:
    for empleado in empleadoPlanificacionAnterior:
        if empleado in empPlan:
            empleadoPlanificacion.append(empleado)
        else:
            empleadoPlanificacion.append(None)

    for empleado in empPlan:
        if empleado not in empleadoPlanificacion:
            empleadoPlanificacion.append(empleado)
else:
    empleadoPlanificacion = empPlan

# VARIABLES A UTILIZAR}

# Lista de los meses del anio
meses_anio = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre", "Diciembre"]

# Rango de empleados totales
all_empleado = range(len(empleadoPlanificacion)) # 0..num_empleado-1

# Rango de empleados totales de la planificación Anterior
all_empleadoAnterior = range(len(empleadoPlanificacionAnterior))

# Cantidad de empleados de la planificacion pasada
num_empleadoAnterior = len(empleadoPlanificacionAnterior)

# Variable que indica la cantidad de turnos
cant_turno = 3

# Lista de la cantidad de turnos total que hay en el mes
turnos_totales = [0] * cant_turno

# Lista de semanas del mes
cont_semana = []

# Lista de todos los domingos
domingos = []

# Turnos extras en una semana (30 - 5 - 18 = 7)
dias_libre_semana = num_empleado
turnos_extra = (6*num_empleado)-dias_libre_semana-(6*cant_turno) 
#print(turnos_extra)

# Lista alarma 
lista_alarma = []

# Lista comodin
lista_comodin = []

# Lista de asignación de empleados basado en el itinerario
lista_itinerario = []

# Lista de turnos sobrantes del itinerario
lista_turno_extra = []

## DEFINICIÓN DEL MODELO
modelo = cp_model.CpModel()

mes, all_dias, cont_semana, month_prev = DefiniendoVariable(modelo, empleadoPlanificacion, planificacionAnterior , empleadoPlanificacionAnterior, year, month, all_empleado, cant_turno , meses_anio, cont_semana)

# Restricciones

modelo, mes = EmpleadoTrabajoPorDia(all_empleado, cont_semana, modelo, mes, cant_turno,meses_anio,month,month_prev,all_empleadoAnterior)

modelo, mes = DiaLibrePorSemana(all_empleado,cont_semana, mes, cant_turno, modelo, meses_anio,month, all_empleadoAnterior,month_prev, empleadoPlanificacion)

modelo, domingos = DomingosLibres(modelo, domingos,cont_semana,mes, meses_anio,all_empleado,cant_turno,month)

modelo, mes = NoAdmitenTurnosSeguidos(all_empleado,all_empleadoAnterior , cont_semana, mes, modelo, meses_anio, month, month_prev)

modelo, mes, turnos_totales = CadaTurnoTieneAsignadoComoMinimoUnEmpleado(modelo, mes, cont_semana, cant_turno, turnos_totales,all_empleado, all_empleadoAnterior, meses_anio, month_prev,month)

modelo, lista_turno_extra, turnos_totales, lista_alarma = ListaEmpleadoParaCadaTurno(modelo,empleadoPlanificacionAnterior,planificacionAnterior , turnos_totales ,itinerario,lista_itinerario,lista_turno_extra,cant_turno,num_empleado,mes,cont_semana,turnos_extra,meses_anio,month,month_prev,lista_alarma, all_empleado)

modelo, turnos_totales, domingos_asignacion, lista_comodin = ContabilizandoTurnosDomingo(modelo,mes,domingos,all_empleado,cant_turno,turnos_totales, num_empleado, itinerario, lista_alarma) # Modificada sin itinerario

modelo, turnos_totales = ListaAsignacionTurnoSobrantes(modelo,mes,cont_semana,lista_turno_extra, meses_anio, month, month_prev, lista_itinerario, itinerario, turnos_totales, planificacionAnterior,lista_alarma, all_empleado, empleadoPlanificacionAnterior, cant_turno,num_empleado) #Modificada para 5 y 7 empleados

modelo = CalculoMinimaCantidadTurno(modelo,turnos_totales,mes, num_empleado,all_empleado, cont_semana, cant_turno, domingos,meses_anio, month, month_prev, all_empleadoAnterior, empleadoPlanificacion) 

# Crea el solver y la solución
solver = cp_model.CpSolver()
solver.parameters.linearization_level = 0

# Enumera todas las soluciones encontradas
solver.parameters.enumerate_all_solutions = True
solution_limit = 1
solution_number = random.randint(1,solution_limit)
solution_printer = SolutionPrinter(solution_number,solution_limit, mes, 
    all_empleado, cont_semana, meses_anio, month, cant_turno, month_prev, all_dias, empleadoPlanificacion, turnos_totales,all_empleadoAnterior, planificacionAnterior, lista_comodin, comodin,lista_alarma)
solver.Solve(modelo, solution_printer)

# Statistics.
#print('\nStatistics')
#print('  - conflicts      : %i' % solver.NumConflicts())
#print('  - branches       : %i' % solver.NumBranches())
#print('  - wall time      : %f s' % solver.WallTime())
#print('  - solutions found: %i' % solution_printer.solution_count())