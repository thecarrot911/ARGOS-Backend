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

      for e in all_empleado:

            jornada = [[] for _ in range(cant_turno)]

            for num_semana in range(1,len(cont_semana)):
                  for i in range(cont_semana[num_semana]):
                        if meses_anio[month-1] == mes[num_semana][i][0]: 
                              for t in range(cant_turno):
                                    jornada[t].append(mes[num_semana][i][3][e][t])

            for t in range(cant_turno):
                  modelo.Add(min_turno[t] <= sum(jornada[t]))
                  modelo.Add(sum(jornada[t]) <= max_turno[t])

      return modelo