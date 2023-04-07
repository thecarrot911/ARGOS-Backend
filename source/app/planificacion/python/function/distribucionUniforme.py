from ortools.sat.python import cp_model

def CalculoMinimaCantidadTurno(modelo: cp_model.CpModel,turnos_totales: list, mes: list[list], num_empleado: int, all_empleado: range, 
                              cont_semana: list, cant_turno: int, domingos: list):

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
                        #modelo.Add(sum(jornada[t]) < max_turno[t]+1)
            else: 
                  for t in range(cant_turno):
                        modelo.Add(min_turno[t] <= sum(jornada[t]))
                        #modelo.Add(sum(jornada[t]) < max_turno[t]+1)
            
            #modelo.Add(max_total+2 > sum(sum(jornada[t]) for t in range(cant_turno)))
      return modelo