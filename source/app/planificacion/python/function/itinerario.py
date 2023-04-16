#mes[num_semana][i][0] -> Mes
#mes[num_semana][i][1] -> Dia del mes
#mes[num_semana][i][2] -> Dia de semana
#mes[num_semana][i][3] -> Array de Empleado

from ortools.sat.python import cp_model


def ListaEmpleadoParaCadaTurno(
      modelo: cp_model.CpModel, empleadoPlanificacionAnterior:list[list] ,planificacionAnterior: None ,turnos_totales: list[int], itinerario: list[object], lista_itinerario: list, lista_turno_extra: list , cant_turno: int, num_empleado: int,
      mes: list[list], cont_semana: list, turnos_extra: int, meses_anio: list[str], month:int, month_prev:int):
      """
      Se genera una lista con la cantidad de empleados para cada turno.
      """
      #itinerario["dia"] - itineario["aviones"] - itineario["turno"]
      
      # Ordena el itineario por dia y Después por turno
      itinerario.sort(key=lambda itinerario: (itinerario["dia"], itinerario["turno"]))
      
      # Cantidad total de turno se le resta el turno del mismo empleado
      turno = cant_turno - 1

      for num_semana in range(len(cont_semana)):
            semana_trabajo = []
            trabajo_extra = turnos_extra
            for i in range(cont_semana[num_semana]):
                  if mes[num_semana][i][0] == meses_anio[month-1]: 
                        # Corresponde al mes actual
                        #print((mes[num_semana][i][0],mes[num_semana][i][1]))
                        itinerario_dia = [dia for dia in itinerario if dia["dia"] == mes[num_semana][i][1] ]
                        if itinerario_dia:
                              suma_itinerario = []
                              for _itinerario in itinerario_dia:

                                    suma_itinerario.append(_itinerario["aviones"])
                                    dia_trabajo = []

                                    if sum(suma_itinerario) + turno <= num_empleado and trabajo_extra - (_itinerario["aviones"] - 1) >= 0:
                                          Condicion_1(modelo, _itinerario, cant_turno, dia_trabajo, num_empleado, semana_trabajo)

                                    elif sum(suma_itinerario) + turno <= num_empleado and trabajo_extra - (_itinerario["aviones"] - 1) < 0:
                                          Condicion_2()

                                    elif sum(suma_itinerario) + turno > num_empleado or trabajo_extra - (_itinerario["aviones"]-1 < 0):
                                          Condicion_3()
                        
                        else: #En caso de que el día no tenga itinerario
                              #print((mes[num_semana][i][0],mes[num_semana][i][1]))
                              semana_trabajo.append([
                                    modelo.NewIntVar(1, num_empleado - cant_turno + 1, "turno 1"),
                                    modelo.NewIntVar(1, num_empleado - cant_turno + 1, "turno 2"),
                                    modelo.NewIntVar(1, num_empleado - cant_turno + 1, "turno 3")
                              ])
                              if i!=6: AgregandoTurnosTotales(turnos_totales, cant_turno)
                  
                  elif mes[num_semana][i][0] == meses_anio[month_prev-1]: 
                        
                        # Corresponde al mes pasado
                        #print((mes[num_semana][i][0],mes[num_semana][i][1]))
                        if planificacionAnterior!=None:
                              contador = 0
                              for dia in empleadoPlanificacionAnterior[i]:
                                    if dia[2] != 0:
                                          contador = contador + 1
                              trabajo_extra = trabajo_extra - contador + cant_turno

                        semana_trabajo.append([
                              modelo.NewIntVar(1, num_empleado - (cant_turno-1), "turno 1"),
                              modelo.NewIntVar(1, num_empleado - (cant_turno-1), "turno 2"),
                              modelo.NewIntVar(1, num_empleado - (cant_turno-1), "turno 3")
                        ])
                        if i!=6: AgregandoTurnosTotales(turnos_totales, cant_turno)

                  else: 
                        
                        # Corresponde al mes del futuro
                        #print((mes[num_semana][i][0],mes[num_semana][i][1]))

                        semana_trabajo.append([
                              modelo.NewIntVar(1, num_empleado - cant_turno + 1, "turno 1"),
                              modelo.NewIntVar(1, num_empleado - cant_turno + 1, "turno 2"),
                              modelo.NewIntVar(1, num_empleado - cant_turno + 1, "turno 3")
                        ])
                        #AgregandoTurnosTotales(turnos_totales, cant_turno)

            lista_itinerario.append(semana_trabajo)
            lista_turno_extra.append(trabajo_extra)
      return lista_itinerario, lista_turno_extra, modelo, itinerario, turnos_totales

def AgregandoTurnosTotales(turnos_totales: list[int], cant_turno: int):
      """ """
      for t in range(cant_turno):
            turnos_totales[t] = turnos_totales[t] + 1

def Condicion_1(modelo: cp_model.CpModel, _itinerario: object, cant_turno: int, dia_trabajo: list, num_empleado: int, semana_trabajo: list):
      """ Se controla que el [itinerario] más los [turnos] no pida más de los empleados que hay y
      que el [itinerario] no exceda los dias extras de la semana [trabajo extra]"""
      
      trabajo_extra = trabajo_extra + 1 - _itinerario["aviones"]

      for t in range(cant_turno):
            if _itinerario["turno"] == (t+1): 
                  dia_trabajo.append(modelo.NewIntVar(_itinerario["aviones"],_itinerario["aviones"],"turno %i" % (t+1)))
            else: 
                  dia_trabajo.append(modelo.NewIntVar(1,num_empleado - _itinerario["aviones"],"turno %i" % (t+1)))

      semana_trabajo.append(dia_trabajo)

def Condicion_2():
      """ Se agregan los que faltan en trabajo extra y el resto se va a la lista_faltante """
      print("2")

def Condicion_3():
      """ En caso de pedir más empleado de los disponibles en un día o pedir más de los que puedne trabajar en la semana."""
      print("3")
