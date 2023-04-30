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
empleadoPlanificacion = sys.argv[6:]


empleadoPlanificacionAnterior = []
if planificacionAnterior != None:
    for dia in planificacionAnterior:
        for empleado in dia:
            empleadoPlanificacionAnterior.append(empleado[1])
        break


# VARIABLES A UTILIZAR

# Lista de los meses del anio
meses_anio = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre", "Diciembre"]

# Rango de empleados totales
all_empleado = range(num_empleado) # 0..num_empleado-1

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

# Restricciones
modelo, mes = EmpleadoTrabajoPorDia(all_empleado, cont_semana, modelo, mes, cant_turno)
modelo, mes = DiaLibrePorSemana(all_empleado,cont_semana, mes, cant_turno, modelo, num_empleado)
modelo, domingos = DomingosLibres(modelo, domingos,cont_semana,mes, meses_anio,all_empleado,num_empleado,cant_turno,month)
modelo = CantidadMinimaDeEmpleadoDomingo(modelo, mes, all_empleado, domingos, num_empleado ,cant_turno) # Modificada
modelo = CantidadMaximaDeEmpleadoDomingo(modelo, mes, all_empleado, domingos, num_empleado ,cant_turno) # Modificada
lista_itinerario, lista_turno_extra, modelo, itinerario, turnos_totales = ListaEmpleadoParaCadaTurno(modelo,empleadoPlanificacionAnterior,planificacionAnterior , turnos_totales ,itinerario,lista_itinerario,lista_turno_extra,cant_turno,num_empleado,mes,cont_semana,turnos_extra,meses_anio,month,month_prev)

modelo, turnos_totales = ListaAsignacionTurnoSobrantes(modelo,mes,cont_semana,lista_turno_extra, meses_anio, month, month_prev, lista_itinerario, itinerario, turnos_totales) #Modificada para 5 y 7 empleados
turnos_totales, domingos_asignacion = ContabilizandoTurnosDomingo(mes,domingos,cant_turno,turnos_totales, num_empleado) # Modificada sin itinerario
modelo = CantidadEmpleadoTrabajandoXSemanaYDia(modelo,cont_semana,cant_turno,lista_itinerario, num_empleado) # Modificada?
modelo = AsignacionTurnos(modelo,mes,planificacionAnterior,empleadoPlanificacionAnterior, lista_itinerario,cont_semana,cant_turno,domingos,month,month_prev,meses_anio,all_empleado,domingos_asignacion) # Modificada
modelo = CalculoMinimaCantidadTurno(modelo,turnos_totales,mes, num_empleado,all_empleado, cont_semana, cant_turno, domingos,meses_anio, month, month_prev) # Modificada

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
    all_empleado, cont_semana, meses_anio, month, cant_turno, month_prev, all_dias, empleadoPlanificacion, turnos_totales)
solver.Solve(modelo, solution_printer)

# Statistics.
#print('\nStatistics')
#print('  - conflicts      : %i' % solver.NumConflicts())
#print('  - branches       : %i' % solver.NumBranches())
#print('  - wall time      : %f s' % solver.WallTime())
#print('  - solutions found: %i' % solution_printer.solution_count())

