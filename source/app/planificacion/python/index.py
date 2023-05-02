import re
import json
import sys
import random
from ortools.sat.python import cp_model
from function.definicionModelo import *
from function.imprimirSolucion import SolutionPrinter
from function.restricciones import *
from function.itinerario import *
from function.distribucionUniforme import *

year = int(sys.argv[1]) 
month = int(sys.argv[2])
num_empleado = int(sys.argv[3])
itinerario = json.loads(sys.argv[4]) # Si no hay devuevlve un []
planificacionAnterior = json.loads(sys.argv[5]) # Si no hay devuelve un None
empPlan = sys.argv[6:]


# Definir la función para extraer el número de RUT
def extraer_numero_rut(rut):
    numero_rut = re.sub("[^0-9]", "", rut)
    return int(numero_rut)

empleadoPlanificacionAnterior = []
if planificacionAnterior != None:
    for dia in planificacionAnterior:
        for empleado in dia:
            empleadoPlanificacionAnterior.append(empleado[1])
        break

# Ordenar la lista según el número de RUT extraído
empPlan = sorted(empPlan, key=extraer_numero_rut)
empleadoPlanificacionAnterior = sorted(empleadoPlanificacionAnterior, key=extraer_numero_rut)

empleadoPlanificacion = []

for empleado in empleadoPlanificacionAnterior:
    if empleado in empPlan:
        empleadoPlanificacion.append(empleado)
    else:
        empleadoPlanificacion.append(None)

for empleado in empPlan:
    if empleado not in empleadoPlanificacion:
        empleadoPlanificacion.append(empleado)

#print(empleadoPlanificacionAnterior) # PLANIFICACION PASADA
#print(empleadoPlanificacion) # PLANIFICACIÓN ACTUAL

# VARIABLES A UTILIZAR

# Lista de los meses del anio
meses_anio = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre", "Diciembre"]

# Rango de empleados totales
all_empleado = range(len(empleadoPlanificacion)) # 0..num_empleado-1

# Rango de empleados totales de la planificación Anterior
all_empleadoAnterior = range(len(empleadoPlanificacionAnterior))

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

mes, all_dias, cont_semana, month_prev = DefiniendoModelo(modelo, empleadoPlanificacion, planificacionAnterior , empleadoPlanificacionAnterior, year, month, all_empleado, cant_turno , meses_anio, cont_semana)

"""for dia in range(cont_semana[0]):
    for empleadoAnterior in all_empleadoAnterior:
        if mes[0][dia][0] == meses_anio[month_prev-1]:
            print(mes[0][dia][0],mes[0][dia][1], mes[0][dia][3][empleadoAnterior][0])
    
    for empleado in all_empleado:
        if mes[0][dia][0] == meses_anio[month-1]:
            print(mes[0][dia][0],mes[0][dia][1], mes[0][dia][3][empleado][0])"""

# Restricciones
modelo, mes = EmpleadoTrabajoPorDia(all_empleado, cont_semana, modelo, mes, cant_turno,meses_anio,month,month_prev,all_empleadoAnterior)
modelo, mes = DiaLibrePorSemana(all_empleado,cont_semana, mes, cant_turno, modelo, num_empleado, meses_anio,month, all_empleadoAnterior,month_prev, empleadoPlanificacion, empleadoPlanificacionAnterior)
modelo, domingos = DomingosLibres(modelo, domingos,cont_semana,mes, meses_anio,all_empleado,num_empleado,cant_turno,month)
modelo = CantidadMinimaDeEmpleadoDomingo(modelo, mes, all_empleado, domingos, num_empleado ,cant_turno) # Modificada
modelo = CantidadMaximaDeEmpleadoDomingo(modelo, mes, all_empleado, domingos, num_empleado ,cant_turno) # Modificada
lista_itinerario, lista_turno_extra, modelo, itinerario, turnos_totales = ListaEmpleadoParaCadaTurno(modelo,empleadoPlanificacionAnterior,planificacionAnterior , turnos_totales ,itinerario,lista_itinerario,lista_turno_extra,cant_turno,num_empleado,mes,cont_semana,turnos_extra,meses_anio,month,month_prev)

modelo, turnos_totales = ListaAsignacionTurnoSobrantes(modelo,mes,cont_semana,lista_turno_extra, meses_anio, month, month_prev, lista_itinerario, itinerario, turnos_totales) #Modificada para 5 y 7 empleados
turnos_totales, domingos_asignacion = ContabilizandoTurnosDomingo(mes,domingos,cant_turno,turnos_totales, num_empleado) # Modificada sin itinerario
modelo = CantidadEmpleadoTrabajandoXSemanaYDia(modelo,cont_semana,cant_turno,lista_itinerario, num_empleado) # Modificada?
modelo = AsignacionTurnos(modelo,mes,planificacionAnterior,empleadoPlanificacionAnterior, lista_itinerario,cont_semana,cant_turno,domingos,month,month_prev,meses_anio,all_empleado,domingos_asignacion) # Modificada

modelo = CalculoMinimaCantidadTurno(modelo,turnos_totales,mes, num_empleado,all_empleado, cont_semana, cant_turno, domingos,meses_anio, month, month_prev, all_empleadoAnterior, empleadoPlanificacion) # Modificada

#modelo, mes = NoAdmitenTurnosSeguidos(all_empleado, cont_semana, mes, modelo) # Modificar


# AGREGAR UNA FUNCIÓN QUE INDIQUE QUE EL ANTIGUO NO PUEDE ESTAR CON EL NUEVO

# Crea el solver y la solución
solver = cp_model.CpSolver()
solver.parameters.linearization_level = 0

# Enumera todas las soluciones encontradas
solver.parameters.enumerate_all_solutions = True
solution_limit = 1
solution_number = random.randint(1,solution_limit)
solution_printer = SolutionPrinter(solution_number,solution_limit, mes, 
    all_empleado, cont_semana, meses_anio, month, cant_turno, month_prev, all_dias, empleadoPlanificacion, turnos_totales,all_empleadoAnterior)
solver.Solve(modelo, solution_printer)

# Statistics.
#print('\nStatistics')
#print('  - conflicts      : %i' % solver.NumConflicts())
#print('  - branches       : %i' % solver.NumBranches())
#print('  - wall time      : %f s' % solver.WallTime())
#print('  - solutions found: %i' % solution_printer.solution_count())

