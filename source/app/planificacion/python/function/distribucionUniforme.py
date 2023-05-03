import json
from ortools.sat.python import cp_model

def CalculoMinimaCantidadTurno(modelo: cp_model.CpModel,turnos_totales: list, mes: list[list], num_empleado: int, all_empleado: range, 
                              cont_semana: list, cant_turno: int, domingos: list, meses_anio: list[str], month: int, month_prev:int, all_empleadoAnterior: range,
                              empleadoPlanificacion: list[str]):

      min_turno = []
      max_turno = []
      
      for t in range(cant_turno):
            min_turno.append(turnos_totales[t] // num_empleado)
            max_turno.append(min_turno[t] + (turnos_totales[t] % num_empleado != 0))


      # Restricción para la primera semana
      """for empleadoAnterior in all_empleadoAnterior:

            jornada = [[] for _ in range(cant_turno)]

            for dia in range(cont_semana[0]):
                  if meses_anio[month_prev-1] == mes[0][dia][0]:
                        for turno in range(cant_turno):
                              jornada[t].append(mes[0][dia][3][empleadoAnterior][turno])
            
            if mes[0][dia][3][empleadoAnterior][0].Name() in empleadoPlanificacion:
                  for dia in range(cont_semana[0]):
                        if mes[0][dia][0] == meses_anio[month-1]:
                              for turno in range(cant_turno):
                                    jornada[turno].append(mes[0][dia][3][empleadoAnterior][turno])

            if jornada[0] and mes[0][dia][3][empleadoAnterior][0].Name() in empleadoPlanificacion:
                  for turno in range(cant_turno):
                        modelo.Add(min_turno[turno] <= sum(jornada[turno]))
                        modelo.Add(sum(jornada[turno]) <= max_turno[turno])"""

      # CONTABILIZAR LA PRIMERA SEMANA Y LAS DEMÁS APARTE...

      # Restricción para las demás semanas

      for empleado in all_empleado:

            jornada = [[] for _ in range(cant_turno)]

            for semana in range(len(cont_semana)):
                  for dia in range(cont_semana[semana]):
                        if meses_anio[month-1] == mes[semana][dia][0]: 
                              for turno in range(cant_turno):
                                    jornada[turno].append(mes[semana][dia][3][empleado][turno])

            for turno in range(cant_turno):
                  modelo.Add(min_turno[turno] <= sum(jornada[turno]))
                  modelo.Add(sum(jornada[turno]) <= max_turno[turno])

      return modelo