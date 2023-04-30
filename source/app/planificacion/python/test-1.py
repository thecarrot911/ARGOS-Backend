def ListaAsignacionTurnoSobrantes(modelo: cp_model.CpModel, mes: list[list], cont_semana: list, lista_turno_extra: list, meses_anio: list[str], month: int, month_prev: int ,lista_itinerario: list, itinerario: list[object], turnos_totales: list):
      """ Se asigna a los empleados """
      for num_semana in range(len(cont_semana)):
            cantidad_turno_extra = lista_turno_extra[num_semana]
            if cantidad_turno_extra >= 1:
                  for i in range(cantidad_turno_extra):
                        itinerario_dia = [dia for dia in itinerario if dia["dia"] == mes[num_semana][i][1] ]
                        if itinerario_dia and cantidad_turno_extra>=1:
                              # ITINERARIO
                              suma_itinerario = []
                              for _itinerario in itinerario_dia:
                                    suma_itinerario.append(_itinerario)
                                    if i<=5 and cantidad_turno_extra>=1: # Lunes a Sábado en la mañana.
                                          #Mes Actual
                                          if mes[num_semana][i][0] == meses_anio[month-1]: 
                                                print()
                                          #Mes pasado
                                          elif mes[num_semana][i][0] == meses_anio[month_prev-1]:
                                                print()
                                          #Mes Futuro
                                          else:
                                                print()
                                    elif i>5 and cantidad_turno_extra>=1: # Lunes a Sábado en la tarde.
                                          #Mes Actual
                                          if mes[num_semana][i][0] == meses_anio[month-1]: 
                                                print()
                                          #Mes pasado
                                          elif mes[num_semana][i][0] == meses_anio[month_prev-1]:
                                                print()
                                          #Mes Futuro
                                          else:
                                                print()
                        elif cantidad_turno_extra>=1: 
                              # NO ITINERARIO
                              if i<= 5: # Se asigna turno a la mañana si sobra
                                    modelo.Add(lista_itinerario[num_semana][i][0]==2) 
                                    cantidad_turno_extra = cantidad_turno_extra - 1
                                    if meses_anio[month-1] == mes[num_semana][i][0] or meses_anio[month_prev-1] == mes[num_semana][i][0]: 
                                          turnos_totales[0] = turnos_totales[0] + 1
                              elif i>5: # Se asigna en la tarde si sobra MODIFICAR DEBAJO DEL FOR...
                                    for i in range(cantidad_turno_extra):
                                          modelo.Add(lista_itinerario[num_semana][i][1]==2)
                                          cantidad_turno_extra = cantidad_turno_extra - 1
                                          if meses_anio[month-1] == mes[num_semana][i][0] or meses_anio[month_prev-1] == mes[num_semana][i][0]: 
                                                turnos_totales[1] = turnos_totales[1] + 1
      return modelo, turnos_totales


"""
      for domingo, num_semana in domingos:
            if len(domingos)==5:
                  AgregandoTurnosTotales(turnos_totales, cant_turno)
                  # Falta agregar el itinerario y los comodines xd
            else:
                  if len(domingos_completo)>0:
                        domingos_asignacion.append(domingos_completo.pop()) 
                        AgregandoTurnosTotales(turnos_totales, cant_turno)
                  else:
                        aux = shuffle(domingos_incompleto.pop())
                        domingos_asignacion.append(aux)
                        for t in range(cant_turno):
                              if aux[t] == 0: comodin.append([mes[num_semana][domingo][1],t+1,1])
                              else: turnos_totales[t] = turnos_totales[t] + 1
"""