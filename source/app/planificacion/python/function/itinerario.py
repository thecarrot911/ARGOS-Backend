#mes[num_semana][i][0] -> Mes
#mes[num_semana][i][1] -> Dia del mes
#mes[num_semana][i][2] -> Dia de semana
#mes[num_semana][i][3] -> Array de Empleado

from statistics import mode
from ortools.sat.python import cp_model


def ListaEmpleadoParaCadaTurno(
      modelo: cp_model.CpModel, empleadoPlanificacionAnterior:list[list] ,planificacionAnterior: None ,turnos_totales: list[int], itinerario: list[object], lista_itinerario: list, lista_turno_extra: list , cant_turno: int, num_empleado: int,
      mes: list[list], cont_semana: list, turnos_extra: int, meses_anio: list[str], month:int, month_prev:int, lista_alarma: list, all_empleado: range):
      """
      Asignación de itinerario y Generación de las listas: 
      turnos extras (asignar empleado sobrantes), 
      lista_alarma (si puede o no asignar), 
      turno_totales (distirbuir) -> Solo aplica para itinerairo
      """
      # Ordena el itineario por dia y Después por turno
      itinerario.sort(key=lambda itinerario: (itinerario["dia"], itinerario["turno"]))
      
      # Cantidad total de turno se le resta el turno del mismo empleado
      Domingo = 6

      # Lista de turnos no alcanzados
      lista_alarma = []

      for semana in range(len(cont_semana)):
            trabajo_extra = turnos_extra
            for dia in range(cont_semana[semana]):
                  if mes[semana][dia][0] == meses_anio[month-1]:
                        itinerario_dia = [_itinerario for _itinerario in itinerario if _itinerario["dia"] == mes[semana][dia][1] ]
                        if itinerario_dia and dia != Domingo:
                              suma_itinerario = [] 
                              acumulador = num_empleado - cant_turno
                              for _itinerario in itinerario_dia:
                                    for turno in range(cant_turno):
                                          if _itinerario["turno"] == (turno+1):
                                                suma_itinerario.append(_itinerario["aviones"])
                                                # Alcanza y asigna esa cantidad a los empleados
                                                if sum(suma_itinerario) + cant_turno <= num_empleado and acumulador > 0 and trabajo_extra >= _itinerario["aviones"]:
                                                      trabajo_extra -= _itinerario["aviones"]
                                                      acumulador -= _itinerario["aviones"]
                                                      turnos_totales[turno] += _itinerario["aviones"]
                                                      lista = []
                                                      for empleado in all_empleado:
                                                            if(mes[semana][dia][3][empleado][turno].Name()!='0'):
                                                                  lista.append(mes[semana][dia][3][empleado][turno])
                                                      if lista: modelo.Add( sum(lista) >= _itinerario["aviones"] + 1)
                                                # No alcanza pero es posible asignar algunos empleados al turno
                                                elif sum(suma_itinerario) + cant_turno > num_empleado and acumulador > 0 and trabajo_extra >= _itinerario["aviones"]:
                                                      for cantidad in range(_itinerario["aviones"]):
                                                            if (num_empleado - cant_turno == cantidad) or (trabajo_extra == cantidad):
                                                                  trabajo_extra-=cantidad
                                                                  break
                                                      acumulador-=cantidad
                                                      turnos_totales[turno]+=cantidad
                                                      lista = []
                                                      for empleado in all_empleado:
                                                            if(mes[semana][dia][3][empleado][turno].Name()!='0'):
                                                                  lista.append(mes[semana][dia][3][empleado][turno])
                                                      if lista: modelo.Add( sum(lista) >= cantidad + 1)
                                                      lista_alarma.append([_itinerario["dia"],_itinerario["turno"],_itinerario["aviones"]-cantidad])
                                                # No alcanza y los manda como alarma
                                                else:
                                                      lista_alarma.append([_itinerario["dia"],_itinerario["turno"],_itinerario["aviones"]])

                  elif mes[semana][dia][0] == meses_anio[month_prev-1] and planificacionAnterior != None:
                        contador = 0
                        for diaPlanificacion in planificacionAnterior[dia]:
                              if diaPlanificacion[2] != 0:  
                                    contador = contador + 1
                        trabajo_extra = trabajo_extra - contador + cant_turno
            lista_turno_extra.append(trabajo_extra)
      return modelo, lista_turno_extra, turnos_totales, lista_alarma
