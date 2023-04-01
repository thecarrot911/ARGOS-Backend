from statistics import mode
from ortools.sat.python import cp_model

def CalculoMinimaCantidadTurno(modelo: cp_model.CpModel,turnos_totales: list, mes: list[list], num_empleado: int, all_empleado: range, 
                              cont_semana: list, cant_turno: int, domingos: list):

      """min_turno_m = turnos_totales[0] // num_empleado
      min_turno_t = turnos_totales[1] // num_empleado
      min_turno_n = turnos_totales[2] // num_empleado

      if turnos_totales[0] % num_empleado == 0:

            max_turno_m = min_turno_m
      else:
            max_turno_m = min_turno_m + 1
      
      if turnos_totales[1] % num_empleado == 0:

            max_turno_t = min_turno_t
      else:
            max_turno_t = min_turno_t + 1
      
      if turnos_totales[2] % num_empleado == 0:

            max_turno_n = min_turno_n
      else:
            max_turno_n = min_turno_n + 1
      
      ttotal = sum(turnos_totales)
      min_turno = ttotal // num_empleado
      
      if ttotal % num_empleado == 0:
            max_turno = min_turno
      else:
            max_turno = min_turno + 1

      for e in all_empleado:
            
            manana = []
            tarde = []
            noche = []
            for num_semana in range(len(cont_semana)):
                  for i in range(cont_semana[num_semana]):
                        manana.append(mes[num_semana][i][3][e][0])
                        tarde.append(mes[num_semana][i][3][e][1])
                        noche.append(mes[num_semana][i][3][e][2])

            if len(domingos) == 4:
                  modelo.Add(min_turno_m < sum(manana))
                  modelo.Add(max_turno_m+1 > sum(manana))

                  modelo.Add(min_turno_t < sum(tarde))
                  modelo.Add(max_turno_t+1 > sum(tarde))
                  
                  modelo.Add(min_turno_n < sum(noche))
                  modelo.Add(max_turno_n+1 > sum(noche))

                  modelo.Add(min_turno < sum(manana) + sum(tarde) + sum(noche))
            else: 
                  modelo.Add(min_turno_m <= sum(manana))
                  modelo.Add(min_turno_t <= sum(tarde))
                  modelo.Add(min_turno_n <= sum(noche))"""


      min_turno = []
      max_turno = []
      
      for t in range(cant_turno):
            min_turno.append(turnos_totales[t] // num_empleado)
            max_turno.append(min_turno[t] + (turnos_totales[t] % num_empleado != 0))
      
      total = sum(turnos_totales)
      min_total = total // num_empleado

      max_total = min_total + (total % num_empleado != 0)

      for e in all_empleado:

            jornada = [[] for _ in range(cant_turno)]

            for num_semana in range(len(cont_semana)):
                  for i in range(cont_semana[num_semana]):
                        for t in range(cant_turno):
                              jornada[t].append(mes[num_semana][i][3][e][t])

            if len(domingos) == 5:
                  for t in range(cant_turno):
                        modelo.Add(min_turno[t] <= sum(jornada[t]))
            else: 
                  for t in range(cant_turno):
                        modelo.Add(min_turno[t] < sum(jornada[t]))
                        modelo.Add(max_turno[t] + 1 > sum(jornada[t]))
      return modelo