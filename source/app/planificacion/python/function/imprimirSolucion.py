from ortools.sat.python import cp_model
import json

class SolutionPrinter(cp_model.CpSolverSolutionCallback):
      """Clase para imprimir la solución."""


      def __init__(self,solution_number: int, solution_limit: int, mes: list[list], all_empleado: range, 
            cont_semana: list, meses_anio: list[str], month: int, cant_turno: int,
            month_prev: int, all_dias: range, empleadoPlanificacion: list[str], turnos_totales): 

            cp_model.CpSolverSolutionCallback.__init__(self)
            self._lista_alarma_turno = []  #lista_alarma_turno
            self._lista_comodin_turno = [] #lista_comodin_turno
            self._solution_number = solution_number
            self._list_itinerario = [] #list_itinerario
            self._mes = mes
            self._cont_semana = cont_semana
            self._all_empleado = all_empleado
            self._all_dias = all_dias
            self._solution_count = 0
            self._solution_limit = solution_limit
            self._meses_anio = meses_anio
            self._month = month
            self._month_prev = month_prev
            self._month = month
            self._cant_turno = cant_turno
            self._empleadoPlanificacion = empleadoPlanificacion
            self._turnos_totales = turnos_totales
      
      
      def on_solution_callback(self):
            self._solution_count += 1

            if(self._solution_count == self._solution_number):
                  json_v = []

                  contador = [[0 for j in range(self._cant_turno+1)] for i in self._all_empleado]

                  for num_semana in range(len(self._cont_semana)):
                        for i in range(self._cont_semana[num_semana]):
                              if self._mes[num_semana][i][0] == self._meses_anio[self._month-1] or self._mes[num_semana][i][0] == self._meses_anio[self._month_prev-1]:
                                    dia = {}
                                    dia["comodin"] = 0
                                    dia["dia_semana"] = self._mes[num_semana][i][2]
                                    dia["dia_numero"] = self._mes[num_semana][i][1]
                                    dia["feriado"]    = self._mes[num_semana][i][4]
                                    empleados = []
                                    for j in self._all_empleado:
                                          emp_turn = {}
                                          is_working = False
                                          for t in range(self._cant_turno):
                                                if(self.Value(self._mes[num_semana][i][3][j][t])):
                                                      is_working = True
                                                      emp_turn["turno"] = t+1
                                                      emp_turn["nombre"] = self._empleadoPlanificacion[j]
                                                      if self._mes[num_semana][i][4]: contador[j][3] = contador[j][3] + 1
                                                      contador[j][t] = contador[j][t] + 1 
                                          if not is_working:
                                                emp_turn["turno"] = 0
                                                emp_turn["nombre"] = self._empleadoPlanificacion[j]
                                                #contador[j][0] = contador[j][0] + 1
                                          empleados.append(emp_turn)
                                    dia["empleados"] = empleados
                                    if i == self._cont_semana[num_semana]-1 or self._mes[num_semana][i+1][0] == self._meses_anio[self._month]:
                                          result = {}
                                          #result["turno_0"] = sum([contador[e][0] for e in self._all_empleado])
                                          #result["turno_1"] = sum([contador[e][1] for e in self._all_empleado])
                                          #result["turno_2"] = sum([contador[e][2] for e in self._all_empleado])
                                          #result["turno_3"] = sum([contador[e][3] for e in self._all_empleado])
                                          #result["total"] = sum([contador[e][t] for t in range(1,self._cant_turno+1) for e in self._all_empleado])
                                          result["total_mes"] = self._turnos_totales
                                          result["emp_1"] = contador[0]
                                          result["emp_2"] = contador[1]
                                          result["emp_3"] = contador[2]
                                          result["emp_4"] = contador[3]
                                          result["emp_5"] = contador[4]
                                          result["feriado_1"] = contador[0][3]
                                          result["feriado_2"] = contador[1][3]
                                          result["feriado_3"] = contador[2][3]
                                          result["feriado_4"] = contador[3][3]
                                          result["feriado_5"] = contador[4][3]

                                          #dia["resultado"] = result
                                    json_v.append(dia)
                  print(json.dumps(json_v))
            if self._solution_count >= self._solution_limit:
                  self.StopSearch()

      def solution_count(self):
            return self._solution_count


