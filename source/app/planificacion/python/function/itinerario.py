#mes[num_semana][i][0] -> Mes
#mes[num_semana][i][1] -> Dia del mes
#mes[num_semana][i][2] -> Dia de semana
#mes[num_semana][i][3] -> Array de Empleado

from statistics import mode
from ortools.sat.python import cp_model


def ListaEmpleadoParaCadaTurno(
      modelo: cp_model.CpModel, empleadoPlanificacionAnterior:list[list] ,planificacionAnterior: None ,turnos_totales: list[int], itinerario: list[object], lista_itinerario: list, lista_turno_extra: list , cant_turno: int, num_empleado: int,
      mes: list[list], cont_semana: list, turnos_extra: int, meses_anio: list[str], month:int, month_prev:int, lista_alarma: list):
      """
      Se genera una lista con la cantidad de empleados para cada turno.
      """
      #itinerario["dia"] - itineario["aviones"] - itineario["turno"]
      
      # Ordena el itineario por dia y Después por turno
      itinerario.sort(key=lambda itinerario: (itinerario["dia"], itinerario["turno"]))
      
      # Cantidad total de turno se le resta el turno del mismo empleado
      Domingo = 6

      # Lista de turnos no alcanzados
      lista_alarma = []

      for semana in range(len(cont_semana)):
            semana_trabajo = []
            trabajo_extra = turnos_extra

            for dia in range(cont_semana[semana]):
                  if mes[semana][dia][0] == meses_anio[month-1]: 
                        
                        # Corresponde al mes actual
                        itinerario_dia = [iti for iti in itinerario if iti["dia"] == mes[semana][dia][1] ]
                        if itinerario_dia:
                              if dia != Domingo:
                                    suma_itinerario = []
                                    dia_trabajo = []
                                    Lista_turnos = []
                                    acumulador = num_empleado - cant_turno
                                    for _itinerario in itinerario_dia:
                                          for turno in range(cant_turno):
                                                # Hay itinerario en este turno
                                                if _itinerario["turno"] == turno+1:
                                                      suma_itinerario.append(_itinerario["aviones"])

                                                      # Alcanza y hay empleados disponible
                                                      if sum(suma_itinerario) + cant_turno <= num_empleado and acumulador > 0 and trabajo_extra - _itinerario["aviones"] >= 0:
                                                            #print(1)
                                                            trabajo_extra = trabajo_extra - _itinerario["aviones"]
                                                            acumulador = acumulador - _itinerario["aviones"]
                                                            dia_trabajo.append(
                                                                  modelo.NewIntVar(1 + _itinerario["aviones"], 1 + _itinerario["aviones"],"turno %i" % (turno+1))
                                                            )
                                                            turnos_totales[turno] = turnos_totales[turno] + _itinerario["aviones"] + 1
                                                      # No Alcanza pero hay empleados disponible [SE REPARTE]
                                                      elif sum(suma_itinerario) + cant_turno > num_empleado and acumulador > 0 and trabajo_extra - _itinerario["aviones"] >= 0:
                                                            #print(2)
                                                            for numero in range(1,_itinerario["aviones"]):
                                                                  if num_empleado - cant_turno == numero:
                                                                        # RECORDAR QUE TRABAJO EXTRA YA INCLUSE EL 1 POR DEFECTO
                                                                        trabajo_extra = trabajo_extra - numero
                                                                        break
                                                            
                                                            dia_trabajo.append(
                                                                  modelo.NewIntVar(numero+1, numero+1,"turno %i" % (turno+1))
                                                            )
                                                            turnos_totales[turno] = turnos_totales[turno] + numero + 1
                                                            acumulador = acumulador - numero
                                                            lista_alarma.append([_itinerario["dia"],_itinerario["turno"],_itinerario["aviones"]-numero])
                                                            #print(turnos_totales)
                                                            #print(trabajo_extra)

                                                      # Alcanza y no hay empleados disponible [SE REPARTE LOS QUE ALCANZAN Y LOS QUE NO A LA LISTA?]
                                                      elif sum(suma_itinerario) + cant_turno <= num_empleado and acumulador > 0 and trabajo_extra - _itinerario["aviones"] < 0:
                                                            #print(3)
                                                            for numero in range(1,_itinerario["aviones"]):
                                                                  if (trabajo_extra - numero == 0) or (num_empleado - cant_turno == numero):
                                                                        trabajo_extra = trabajo_extra - numero
                                                                        break
                                                            
                                                            dia_trabajo.append(
                                                                  modelo.NewIntVar(numero+1, numero+1,"turno %i" % (turno+1))
                                                            )
                                                            turnos_totales[turno] = turnos_totales[turno] + numero + 1
                                                            lista_alarma.append([_itinerario["dia"],_itinerario["turno"],_itinerario["aviones"]-numero])
                                                            acumulador = acumulador - numero
                                                      
                                                      # No hay nada de nada xd
                                                      #elif sum(suma_itinerario) + cant_turno > num_empleado and trabajo_extra - _itinerario["aviones"] < 0:
                                                            #print(4)
                                                      
                                                      else: # No alacanza ?
                                                            dia_trabajo.append(
                                                                  modelo.NewIntVar(1,1,"turno %i" % (turno+1))
                                                            )
                                                            turnos_totales[turno] = turnos_totales[turno] + 1
                                                            lista_alarma.append([_itinerario["dia"],_itinerario["turno"],_itinerario["aviones"]])

                                                      
                                                      Lista_turnos.append(turno+1)
                                                      break
                                    #print(turnos_totales)
                                    if sum(Lista_turnos) != 6:
                                          for turno in range(cant_turno):
                                                if turno+1 not in Lista_turnos:
                                                      dia_trabajo.append(
                                                            modelo.NewIntVar(1,num_empleado - cant_turno +1,"turno %i" % (turno+1))
                                                      )
                                                      turnos_totales[turno] = turnos_totales[turno] + 1
                                    semana_trabajo.append(dia_trabajo)
                              else:
                                    semana_trabajo.append([
                                          modelo.NewIntVar(1, num_empleado - cant_turno + 1, "turno 1"),
                                          modelo.NewIntVar(1, num_empleado - cant_turno + 1, "turno 2"),
                                          modelo.NewIntVar(1, num_empleado - cant_turno + 1, "turno 3"),
                                    ])
                        
                        else: #En caso de que el día no tenga itinerario
                              semana_trabajo.append([
                                    modelo.NewIntVar(1, num_empleado - cant_turno + 1, "turno 1"),
                                    modelo.NewIntVar(1, num_empleado - cant_turno + 1, "turno 2"),
                                    modelo.NewIntVar(1, num_empleado - cant_turno + 1, "turno 3")
                              ])
                              if dia != Domingo: 
                                    AgregandoTurnosTotales(turnos_totales, cant_turno)
                                    #print(mes[semana][dia][1], mes[semana][dia][0])
                  
                  elif mes[semana][dia][0] == meses_anio[month_prev-1]: 
                        
                        # Corresponde al mes pasado
                        if planificacionAnterior != None:
                              contador = 0
                              for diaPlanificacion in planificacionAnterior[dia]:
                                    if diaPlanificacion[2] != 0:
                                          contador = contador + 1
                              trabajo_extra = trabajo_extra - contador + cant_turno

                        semana_trabajo.append([
                              modelo.NewIntVar(1, num_empleado - (cant_turno-1), "turno 1"),
                              modelo.NewIntVar(1, num_empleado - (cant_turno-1), "turno 2"),
                              modelo.NewIntVar(1, num_empleado - (cant_turno-1), "turno 3")
                        ])
                        
                        if dia != Domingo and planificacionAnterior == None: # Solo cuenta cuando no hay planificación anterior
                              AgregandoTurnosTotales(turnos_totales, cant_turno)
                              #print(mes[semana][dia][1], mes[semana][dia][0])

                  else: 
                        
                        # Corresponde al mes del futuro
                        #print((mes[semana][dia][0],mes[semana][dia][1]))
                        semana_trabajo.append([
                              modelo.NewIntVar(1, num_empleado - cant_turno + 1, "turno 1"),
                              modelo.NewIntVar(1, num_empleado - cant_turno + 1, "turno 2"),
                              modelo.NewIntVar(1, num_empleado - cant_turno + 1, "turno 3")
                        ])
                        #if i!=6: AgregandoTurnosTotales(turnos_totales, cant_turno)

            lista_itinerario.append(semana_trabajo)
            lista_turno_extra.append(trabajo_extra)
      return lista_itinerario, lista_turno_extra, modelo, itinerario, turnos_totales, lista_alarma

def AgregandoTurnosTotales(turnos_totales: list[int], cant_turno: int):
      """ """
      for t in range(cant_turno):
            turnos_totales[t] = turnos_totales[t] + 1
