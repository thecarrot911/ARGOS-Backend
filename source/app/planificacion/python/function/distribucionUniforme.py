import json
from re import S, T
from ortools.sat.python import cp_model

def CalculoMinimaCantidadTurno(modelo: cp_model.CpModel,turnos_totales: list, mes: list[list], num_empleado: int, all_empleado: range, 
                              cont_semana: list, cant_turno: int, domingos: list, meses_anio: list[str], month: int, month_prev:int, all_empleadoAnterior: range,
                              empleadoPlanificacion: list[str]):

      # Mínima cantidad que los empleados deben tener por turno
      min_turno = [] 
      # Máxima cantidad que los empleados deben tener por turno
      max_turno = []

      # Se realiza el calculo de la máxima y mínima cantidad
      for turno in range(cant_turno):
            min_turno.append(turnos_totales[turno] // num_empleado)
            max_turno.append(min_turno[turno] + (turnos_totales[turno] % num_empleado != 0))

      #print(turnos_totales)
      #print(min_turno,max_turno)

      # Si no hay planificacion anterior entonces..
      if all_empleadoAnterior == range(0):
            
            for empleado in all_empleado:
                  jornada = [[] for _ in range(cant_turno)]
                  
                  for semana in range(len(cont_semana)):
                        for dia in range(cont_semana[semana]):
                              if mes[semana][dia][0] == meses_anio[month-1] or mes[semana][dia][0] == meses_anio[month_prev-1]:
                                    for turno in range(cant_turno):
                                          jornada[turno].append(mes[semana][dia][3][empleado][turno])

                  for turno in range(cant_turno):
                        modelo.Add(min_turno[turno] <= sum(jornada[turno]))
                        modelo.Add(sum(jornada[turno]) <= max_turno[turno])
      
      # Si hay planificación anterior entonces...
      else: 
            # Recordar que no se cuenta el mes pasado
            for empleado in all_empleado:

                  jornada = [[] for _ in range(cant_turno)]
                  for semana in range(len(cont_semana)):
                        for dia in range(cont_semana[semana]):
                              if mes[semana][dia][0] == meses_anio[month-1]:
                                    for turno in range(cant_turno):
                                          if mes[semana][dia][3][empleado][turno].Name() != '0' :
                                                jornada[turno].append(mes[semana][dia][3][empleado][turno])
                  
                  for turno in range(cant_turno):
                        if jornada[turno]:
                              modelo.Add(min_turno[turno] <= sum(jornada[turno]))
                              modelo.Add(sum(jornada[turno]) <= max_turno[turno])

      return modelo