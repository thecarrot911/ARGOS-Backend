from ortools.sat.python import cp_model
import json

class SolutionPrinter(cp_model.CpSolverSolutionCallback):
      """Clase para imprimir la solución."""


      def __init__(self,solution_number: int, solution_limit: int, mes: list[list], all_empleado: range, 
            cont_semana: list, meses_anio: list[str], month: int, cant_turno: int,
            month_prev: int, all_dias: range, empleadoPlanificacion: list[str], turnos_totales, all_empleadoAnterior: range,planificacionAnterior: None, lista_comodin: list[list], comodin: object, lista_alarma:list[list]): 

            cp_model.CpSolverSolutionCallback.__init__(self)
            self._lista_alarma = lista_alarma  #lista_alarma_turno
            self._lista_comodin = lista_comodin
            self._solution_number = solution_number
            self._comodin = comodin
            self._list_itinerario = [] #list_itinerario
            self._mes = mes
            self._cont_semana = cont_semana
            self._all_empleado = all_empleado
            self._all_empleadoAnterior = all_empleadoAnterior
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
            self._planificacionAnterior = planificacionAnterior
      
      
      def on_solution_callback(self):
            self._solution_count += 1

            if(self._solution_count == self._solution_number):
                  json_v = []

                  #contador = [[0 for j in range(self._cant_turno)] for i in self._all_empleado]
                  for num_semana in range(len(self._cont_semana)):
                        for i in range(self._cont_semana[num_semana]):
                              #if self._mes[num_semana][i][2] == "Domingo":
                                    if self._mes[num_semana][i][0] == self._meses_anio[self._month_prev-1] and self._planificacionAnterior == None:
                                          dia = {}
                                          dia["comodin"] = 0
                                          dia["dia_semana"] = self._mes[num_semana][i][2]
                                          dia["dia_numero"] = self._mes[num_semana][i][1]
                                          dia["feriado"]    = self._mes[num_semana][i][4]
                                          empleados = []
                                          

                                          if self._all_empleadoAnterior == range(0):
                                                all_anterior = self._all_empleado
                                          else:
                                                all_anterior = self._all_empleadoAnterior

                                          for j in all_anterior:
                                                if self._mes[num_semana][i][3][j][0].Name() != '0':
                                                      emp_turn = {}
                                                      is_working = False
                                                      for t in range(self._cant_turno):
                                                            if(self.Value(self._mes[num_semana][i][3][j][t])):
                                                                  is_working = True
                                                                  emp_turn["turno"] = t+1
                                                                  emp_turn["nombre"] = self._mes[num_semana][i][3][j][t].Name()
                                                                  #if self._all_empleadoAnterior == range(0): contador[j][t] = contador[j][t] + 1 
                                                      if not is_working:
                                                            emp_turn["turno"] = 0
                                                            emp_turn["nombre"] = self._mes[num_semana][i][3][j][t].Name()
                                                      empleados.append(emp_turn)
                                          dia["empleados"] = empleados
                                          dia["itinerario"] = []
                                          json_v.append(dia)

                                    elif self._mes[num_semana][i][0] == self._meses_anio[self._month-1]:
                                          dia = {}
                                          dia["comodin"] = 0
                                          dia["dia_semana"] = self._mes[num_semana][i][2]
                                          dia["dia_numero"] = self._mes[num_semana][i][1]
                                          dia["feriado"]    = self._mes[num_semana][i][4]
                                          empleados = []
                                          for j in self._all_empleado:
                                                if self._mes[num_semana][i][3][j][0].Name() != '0':
                                                      emp_turn = {}
                                                      is_working = False
                                                      for t in range(self._cant_turno):
                                                            if(self.Value(self._mes[num_semana][i][3][j][t])):
                                                                  is_working = True
                                                                  emp_turn["turno"] = t+1
                                                                  emp_turn["nombre"] = self._mes[num_semana][i][3][j][t].Name()
                                                                  #contador[j][t] = contador[j][t] + 1 
                                                      if not is_working:
                                                            emp_turn["turno"] = 0
                                                            emp_turn["nombre"] = self._mes[num_semana][i][3][j][t].Name()
                                                      empleados.append(emp_turn)

                                          for lista in self._lista_comodin:
                                                domingo, turno = lista
                                                if self._mes[num_semana][i][1] == domingo:
                                                      dia["comodin"] = turno
                                                      emp = {}
                                                      emp["turno"] = turno
                                                      emp["nombre"] = self._comodin
                                                      empleados.append(emp)
                                                      break
                                          
                                          dia["empleados"] = empleados

                                          alarma = [alarma for alarma in self._lista_alarma if alarma[0] == self._mes[num_semana][i][1]]
                                          
                                          itinerario_array = []
                                          if alarma:
                                                for turno in alarma:
                                                      itinerario = {}
                                                      itinerario["turno"] = turno[1]
                                                      itinerario["falta"] = turno[2]
                                                      itinerario_array.append(itinerario)

                                          dia["itinerario"] = itinerario_array

                                          json_v.append(dia)
                  print(json.dumps(json_v))
            
            if self._solution_count >= self._solution_limit:
                  self.StopSearch()

      def solution_count(self):
            return self._solution_count



