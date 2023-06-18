def NoAdmitenTurnosSeguidos(all_empleado: range,all_empleadoAnterior: range , cont_semana: list, mes: list[list], modelo: cp_model.CpModel,
      meses_anio:list[str],month: int, month_prev: int, empleadoPlanificacion: list[str]):
      """
      Los empleados no pueden tener turnos seguidos, es decir que un empleado que trabaje en la
      jornada de la noche, no puede trabajar el día siguiente en la jornada de la mañana.
      """

      #SE HICIERON VARIOS CAMBIOS EN EL IF XD DE LA PLANIFICAICÓN ANTERIOR
      diaSiguiente = 1

      # No hay planificación Anterior
      if all_empleadoAnterior == range(0):
            for empleado in all_empleado:
                  for semana in range(len(cont_semana)):
                        for dia in range(cont_semana[semana]):
                              #if meses_anio[month_prev-1] == mes[semana][dia][0] or meses_anio[month-1] == mes[semana][dia][0]:
                                    lista = []

                                    if dia + diaSiguiente != cont_semana[semana]:
                                          lista.append(mes[semana][dia][3][empleado][2]) # Último turno
                                          lista.append(mes[semana][dia+diaSiguiente][3][empleado][0]) # Primer turno del dia siguiente
                                    else:
                                          if (dia+diaSiguiente)*(semana+1) < len(mes[semana]) * len(mes):
                                                lista.append(mes[semana][dia][3][empleado][2])
                                                lista.append(mes[semana+1][0][3][empleado][0])
                                    modelo.Add(sum(lista) <= 1)

      
      # Hay planificación Anterior
      else:
            # Primera semana del mes
            for empleadoAnterior in all_empleadoAnterior:
                  for dia in range(cont_semana[0]):
                        lista = []

                        # Solo entra al if si hay una planificación anterior o si hay dias del mes anterior en la semana
                        if meses_anio[month_prev-1] == mes[0][dia][0]: 
                              lista.append(mes[0][dia][3][empleadoAnterior][2]) # Último turno
                              lista.append(mes[0][dia+diaSiguiente][3][empleadoAnterior][0]) # Primer turno del dia siguiente
                        
                        elif meses_anio[month-1] == mes[0][dia][0]:
                              if mes[0][dia][3][empleadoAnterior][0].Name() in empleadoPlanificacion:
                                    
                                    # Entra si el siguiente dia corresponde a un dia de la misma semana
                                    if dia + diaSiguiente != cont_semana[0]:
                                          lista.append(mes[0][dia][3][empleadoAnterior][2])
                                          lista.append(mes[0][dia+diaSiguiente][3][empleadoAnterior][0])

                                    # Entra si el siguiente dia corresponde a la siguiente semana
                                    else: 
                                          lista.append(mes[0][dia][3][empleadoAnterior][2]) # dia actual, ultimo turno
                                          lista.append(mes[1][0][3][empleadoAnterior][0]) # dia siguiente de la otra semana, primer turno

                        if lista: modelo.Add(sum(lista) <= 1)
            
            # Las demás semanas del mes
            for empleado in all_empleado:
                  for semana in range(1,len(cont_semana)):
                        for dia in range(cont_semana[semana]):
                              #if mes[semana][dia][0] == meses_anio[month-1] and mes[semana][dia][3][empleado][0].Name() != '0':
                              if mes[semana][dia][3][empleado][0].Name() != '0':
                                    lista = []

                                    if dia + diaSiguiente != cont_semana[semana]:
                                          lista.append(mes[semana][dia][3][empleado][2])
                                          lista.append(mes[semana][dia+diaSiguiente][3][empleado][0])
                                    else:
                                          if (dia+diaSiguiente)*(semana+1) < len(mes[semana]) * len(mes):
                                                lista.append(mes[semana][dia][3][empleado][2])
                                                lista.append(mes[semana+1][0][3][empleado][0])
                                    
                                    if lista: modelo.Add(sum(lista)<=1)

      return modelo, mes

def DiaLibrePorSemana(all_empleado: range,cont_semana: list, mes: list[list], cant_turno: int, modelo: cp_model.CpModel, num_empleado: int, meses_anio: list[str], month: int, all_empleadoAnterior: range, month_prev:int, empleadoPlanificacion: list[str], empleadoPlanificacionAnterior: list[str]):
      """Cada empleado tiene 1 día libre por semana."""
      # Se cambio el If de la primera semana

      cantidadDiaSemana = 6 # Lunes a Sábado
      diasLibreCadaEmpleadoPorSemana = 1
      
      # No hay planificación anterior
      if all_empleadoAnterior == range(0):
            for empleado in all_empleado:
                  for semana in range(len(cont_semana)):
                        lista_semana = []
                        for dia in range(cont_semana[semana]):
                              if mes[semana][dia][2] != 'Domingo':
                                    for turno in range(cant_turno):
                                          lista_semana.append(mes[semana][dia][3][empleado][turno])
                        modelo.Add(sum(lista_semana) == cantidadDiaSemana - diasLibreCadaEmpleadoPorSemana)
      
      # Existe una planificación anterior
      else: 
            # Restricción para la primera semana 
            for empleadoAnterior in all_empleadoAnterior: 
                  lista_semana = []
                  for dia in range(cont_semana[0]):
                        if mes[0][dia][0] == meses_anio[month_prev-1] and mes[0][dia][2] != 'Domingo':
                              for turno in range(cant_turno):
                                    lista_semana.append(mes[0][dia][3][empleadoAnterior][turno])
                        else: break
                  # Verificamos si el empleado participa en la planificación actual, si no participa, 
                  # entonces ya debería de tener un día libre, ya que solo se entra aquí, si el mes anterior
                  # termina en día que sea != sábado. Esto se debe al all_empleadoAnterior que hace esa verificación.
                  if mes[0][dia][3][empleadoAnterior][0].Name() in empleadoPlanificacion:
                        for dia in range(cont_semana[0]):
                              if mes[0][dia][0] == meses_anio[month-1] and mes[0][dia][2] != 'Domingo':
                                    for turno in range(cant_turno):
                                          lista_semana.append(mes[0][dia][3][empleadoAnterior][turno])
                  if lista_semana and mes[0][dia][3][empleadoAnterior][0].Name() in empleadoPlanificacion:
                        modelo.Add(sum(lista_semana) == cantidadDiaSemana - diasLibreCadaEmpleadoPorSemana)
            
            # Restricción para las demás semanas
            for empleado in all_empleado:
                  if mes[1][0][3][empleado][0].Name() != '0':
                        for semana in range(1,len(cont_semana)):
                              lista_semana = []
                              for dia in range(cont_semana[semana]):
                                    if mes[semana][dia][2] != 'Domingo':
                                          for turno in range(cant_turno):
                                                lista_semana.append(mes[semana][dia][3][empleado][turno])
                              modelo.Add(sum(lista_semana) == cantidadDiaSemana - diasLibreCadaEmpleadoPorSemana)

      return modelo, mes
# itinerario
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
                        if planificacionAnterior != None and num_empleado < len(empleadoPlanificacionAnterior) and semana == 0:
                              diasRestante = 6 - len(planificacionAnterior)
                              nuevo_turno_extra = diasRestante * (num_empleado-cant_turno)
                              #print(nuevo_turno_extra)

                        # Corresponde al mes actual
                        itinerario_dia = [iti for iti in itinerario if iti["dia"] == mes[semana][dia][1] ]
                        
                        if itinerario_dia:
                              #print(trabajo_extra)
                              #print(itinerario_dia)
                              if dia != Domingo:
                                    suma_itinerario = []
                                    dia_trabajo = []
                                    Lista_turnos = []
                                    acumulador = num_empleado - cant_turno
                                    for _itinerario in itinerario_dia:
                                          for turno in range(cant_turno):
                                                # Hay itinerario en este turno
                                                if _itinerario["turno"] == (turno+1):
                                                      suma_itinerario.append(_itinerario["aviones"])
                                                      # Alcanza y hay empleados disponible
                                                      if sum(suma_itinerario) + cant_turno <= num_empleado and acumulador > 0 and trabajo_extra - _itinerario["aviones"] >= 0:
                                                            #print(1,'if')
                                                            trabajo_extra = trabajo_extra - _itinerario["aviones"]
                                                            acumulador = acumulador - _itinerario["aviones"]
                                                            dia_trabajo.append(
                                                                  modelo.NewIntVar(1 + _itinerario["aviones"], 1 + _itinerario["aviones"],"turno %i" % (turno+1))
                                                            )
                                                            turnos_totales[turno] = turnos_totales[turno] + _itinerario["aviones"] + 1
                                                      # No Alcanza pero hay empleados disponible [SE REPARTE]
                                                      elif sum(suma_itinerario) + cant_turno > num_empleado and acumulador > 0 and trabajo_extra - _itinerario["aviones"] >= 0:
                                                            #print(2,'if')
                                                            EnterFor = False

                                                            for numero in range(1,_itinerario["aviones"]):
                                                                  if num_empleado - cant_turno == numero:
                                                                        # RECORDAR QUE TRABAJO EXTRA YA INCLUSE EL 1 POR DEFECTO
                                                                        trabajo_extra = trabajo_extra - numero
                                                                        EnterFor = True
                                                                        break
                                                            
                                                            if not EnterFor:
                                                                  numero = 1
                                                                  dia_trabajo.append(
                                                                        modelo.NewIntVar(numero+1, numero+1,"turno %i" % (turno+1))
                                                                  )
                                                                  turnos_totales[turno] = turnos_totales[turno] + numero + 1 # Se suma el 1, obligatorio
                                                                  acumulador = acumulador - numero
                                                            else:
                                                                  dia_trabajo.append(
                                                                        modelo.NewIntVar(numero+1, numero+1,"turno %i" % (turno+1))
                                                                  )
                                                                  turnos_totales[turno] = turnos_totales[turno] + numero + 1 # Se suma el 1, obligatorio
                                                                  acumulador = acumulador - numero
                                                                  lista_alarma.append([_itinerario["dia"],_itinerario["turno"],_itinerario["aviones"]-numero])
                                                            
                                                            #print(t,'if'urnos_totales)
                                                            #print(t,'if'rabajo_extra)

                                                      # Alcanza y no hay empleados disponible [SE REPARTE LOS QUE ALCANZAN Y LOS QUE NO A LA LISTA?]
                                                      elif sum(suma_itinerario) + cant_turno <= num_empleado and acumulador > 0 and trabajo_extra < 0:
                                                            #print(3,'if')
                                                            for numero in range(1,_itinerario["aviones"]):
                                                                  if (trabajo_extra - numero == 0) or (num_empleado - cant_turno == numero):
                                                                        trabajo_extra = trabajo_extra - numero
                                                                        break
                                                            
                                                            dia_trabajo.append(
                                                                  modelo.NewIntVar(numero+1, numero+1,"turno %i" % (turno+1))
                                                            )
                                                            turnos_totales[turno] = turnos_totales[turno] + numero + 1
                                                            acumulador = acumulador - numero
                                                            lista_alarma.append([_itinerario["dia"],_itinerario["turno"],_itinerario["aviones"]-numero])
                                                      
                                                      else: # No alacanza ?
                                                            #print(4,'if')
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
                                                if (turno+1) not in Lista_turnos:
                                                      dia_trabajo.append(
                                                            modelo.NewIntVar(1,num_empleado - cant_turno +1,"turno %i" % (turno+1))
                                                      )
                                                      turnos_totales[turno] = turnos_totales[turno] + 1
                                    # Se ordena los turnos de 1 a 3
                                    dia_trabajo = sorted(dia_trabajo, key=ObtenerNumeroDeTurno)
                                    #print(dia_trabajo)
                                    semana_trabajo.append(dia_trabajo)
                              else:
                                    semana_trabajo.append([
                                          modelo.NewIntVar(1, num_empleado - cant_turno + 1, "turno 1"),
                                          modelo.NewIntVar(1, num_empleado - cant_turno + 1, "turno 2"),
                                          modelo.NewIntVar(1, num_empleado - cant_turno + 1, "turno 3"),
                                    ])
                        
                        else: #En caso de que el día no tenga itinerario
                              #if semana == 0: print(mes[semana][dia][2],mes[semana][dia][1],trabajo_extra)
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

def ObtenerNumeroDeTurno(variable):
    return int(variable.Name().split()[1])

def ListaAsignacionTurnoSobrantes(modelo: cp_model.CpModel, mes: list[list], cont_semana: list, lista_turno_extra: list, meses_anio: list[str], month: int, month_prev: int ,lista_itinerario: list, itinerario: list[object], turnos_totales: list, planificacionAnterior: None, lista_alarma:list[list]):
      """ Se asigna a los empleados """
      LunesASabado = 5
      num_empleado = 5 #Ingresar como parametro de la funcion 
      cant_turno = 3 #Ingresar como parametro de la funcion

      for semana in range(len(cont_semana)):
            cantidad_turno_extra = lista_turno_extra[semana]
            #if semana == 0: print(cantidad_turno_extra)
            for diaSemana in range(cont_semana[semana]):
                  # Si no hay turno extra, se sale del for
                  if cantidad_turno_extra == 0: break
                  # Si hay turno extra, se sigue iterando    
                  else:
                        jornada = [False, False, False]
                        itinerario_dia = [dia for dia in itinerario if dia["dia"] == mes[semana][diaSemana][1] ]
                        if diaSemana <= LunesASabado:
                              
                              if meses_anio[month-1] == mes[semana][diaSemana][0]:

                                    _itinerario1 = [dia for dia in itinerario_dia if dia["turno"] == 1]
                                    _itinerario2 = [dia for dia in itinerario_dia if dia["turno"] == 2]
                                    _itinerario3 = [dia for dia in itinerario_dia if dia["turno"] == 3]
                                    
                                    if not _itinerario1 and (_itinerario2 or _itinerario3):

                                          if _itinerario2 and not _itinerario3:
                                                if _itinerario2[0]["aviones"] < num_empleado - cant_turno:
                                                      turnos_totales[0] = turnos_totales[0] + 1
                                                      cantidad_turno_extra = cantidad_turno_extra - 1
                                                      modelo.Add(lista_itinerario[semana][diaSemana][0] >= 2) # 2 Personas en la mañana
            
                                          elif _itinerario3 and not _itinerario2:
                                                if _itinerario3[0]["aviones"] < num_empleado - cant_turno:
                                                      turnos_totales[0] = turnos_totales[0] + 1
                                                      cantidad_turno_extra = cantidad_turno_extra - 1
                                                      modelo.Add(lista_itinerario[semana][diaSemana][0] >= 2)
                                          else:
                                                if _itinerario2[0]["aviones"] + _itinerario3[0]["aviones"] < num_empleado - cant_turno:
                                                      turnos_totales[0] = turnos_totales[0] + 1
                                                      cantidad_turno_extra = cantidad_turno_extra - 1
                                                      modelo.Add(lista_itinerario[semana][diaSemana][0] >= 2)
                                    
                                    else:
                                          #print(mes[semana][diaSemana][1],'manana')
                                          turnos_totales[0] = turnos_totales[0] + 1
                                          cantidad_turno_extra = cantidad_turno_extra - 1
                                          modelo.Add(lista_itinerario[semana][diaSemana][0] >= 2)

                              elif meses_anio[month_prev-1] == mes[semana][diaSemana][0]:
                                    if planificacionAnterior == None:
                                          turnos_totales[0] = turnos_totales[0] + 1
                                          cantidad_turno_extra = cantidad_turno_extra - 1
                                          modelo.Add(lista_itinerario[semana][diaSemana][0] >= 2) # 2 Personas en la mañana
                              
                              else: #Mes siguiente
                                    cantidad_turno_extra = cantidad_turno_extra - 1
                                    modelo.Add(lista_itinerario[semana][diaSemana][0] >= 2) # 2 Personas en la mañana


                        elif diaSemana > LunesASabado:
                              jornada[1] = True
                              vuelta = 1

                              for dia in itertools.cycle(range(cont_semana[semana])):
                                    itinerario_dia = [dias for dias in itinerario if dias["dia"] == mes[semana][dia][1] ]

                                    if cantidad_turno_extra == 0: break
                                    if jornada[0]: # Turno de la Mañana
                                          if dia <= LunesASabado:
                                                
                                                if meses_anio[month-1] == mes[semana][dia][0]:
                                                      
                                                      _itinerario1 = [dia for dia in itinerario_dia if dia["turno"] == 1]
                                                      _itinerario2 = [dia for dia in itinerario_dia if dia["turno"] == 2]
                                                      _itinerario3 = [dia for dia in itinerario_dia if dia["turno"] == 3]
                                                      
                                                      if not _itinerario1 and (_itinerario2 or _itinerario3):

                                                            if _itinerario2 and not _itinerario3:
                                                                  if _itinerario2[0]["aviones"] < num_empleado - cant_turno:
                                                                        turnos_totales[0] = turnos_totales[0] + 1
                                                                        cantidad_turno_extra = cantidad_turno_extra - 1
                                                                        modelo.Add(lista_itinerario[semana][dia][0] >= vuelta + 1) # 2 Personas en la mañana
                              
                                                            elif _itinerario3 and not _itinerario2:
                                                                  if _itinerario3[0]["aviones"] < num_empleado - cant_turno:
                                                                        turnos_totales[0] = turnos_totales[0] + 1
                                                                        cantidad_turno_extra = cantidad_turno_extra - 1
                                                                        modelo.Add(lista_itinerario[semana][dia][0] >= vuelta + 1)
                                                            else:
                                                                  if _itinerario2[0]["aviones"] + _itinerario3[0]["aviones"] < num_empleado - cant_turno:
                                                                        turnos_totales[0] = turnos_totales[0] + 1
                                                                        cantidad_turno_extra = cantidad_turno_extra - 1
                                                                        modelo.Add(lista_itinerario[semana][dia][0] >= vuelta + 1)
                                                      else:
                                                            turnos_totales[0] = turnos_totales[0] + 1
                                                            cantidad_turno_extra = cantidad_turno_extra - 1
                                                            modelo.Add(lista_itinerario[semana][dia][0] >= vuelta + 1)

                                                elif meses_anio[month_prev-1] == mes[semana][dia][0]:
                                                      if planificacionAnterior == None:
                                                            turnos_totales[0] = turnos_totales[0] + 1
                                                            cantidad_turno_extra = cantidad_turno_extra -1
                                                            modelo.Add(lista_itinerario[semana][dia][0] >= vuelta + 1)
                                                
                                                else:
                                                      #Mes siguiente al actual
                                                      cantidad_turno_extra = cantidad_turno_extra - 1
                                                      modelo.Add(lista_itinerario[semana][dia][0] >= vuelta + 1) # 2 Personas en la mañana

                                          else:
                                                jornada[0] = False
                                                jornada[1] = True
                                    
                                    elif jornada[1]: # Turno de la Tarde
                                          if dia <= LunesASabado:

                                                if meses_anio[month-1] == mes[semana][dia][0]:
                                                      _itinerario1 = [dia for dia in itinerario_dia if dia["turno"] == 1]
                                                      _itinerario2 = [dia for dia in itinerario_dia if dia["turno"] == 2]
                                                      _itinerario3 = [dia for dia in itinerario_dia if dia["turno"] == 3]

                                                      if not _itinerario2 and (_itinerario1 or _itinerario3):
                                                            if _itinerario1 and not _itinerario3:
                                                                  if _itinerario1[0]["aviones"] < num_empleado - cant_turno:
                                                                        turnos_totales[1] = turnos_totales[1] + 1
                                                                        cantidad_turno_extra = cantidad_turno_extra - 1
                                                                        modelo.Add(lista_itinerario[semana][dia][1] >= vuelta + 1) # 2 Personas en la mañana
                                                            elif _itinerario3 and not _itinerario1:
                                                                  if _itinerario3[0]["aviones"] < num_empleado - cant_turno:
                                                                        turnos_totales[1] = turnos_totales[1] + 1
                                                                        cantidad_turno_extra = cantidad_turno_extra - 1
                                                                        modelo.Add(lista_itinerario[semana][dia][1] >= vuelta + 1)
                                                            else:
                                                                  if _itinerario1[0]["aviones"] + _itinerario3[0]["aviones"] < num_empleado - cant_turno:
                                                                        turnos_totales[1] = turnos_totales[1] + 1
                                                                        cantidad_turno_extra = cantidad_turno_extra - 1
                                                                        modelo.Add(lista_itinerario[semana][dia][1] >= vuelta + 1)
                                                      
                                                      else:
                                                            #print(mes[semana][dia][1],'tarde')
                                                            turnos_totales[1] = turnos_totales[1] + 1
                                                            cantidad_turno_extra = cantidad_turno_extra - 1
                                                            modelo.Add(lista_itinerario[semana][dia][1] >= vuelta + 1)

                                                elif meses_anio[month_prev-1] == mes[semana][dia][0]:
                                                      if planificacionAnterior == None:
                                                            turnos_totales[1] = turnos_totales[1] + 1
                                                            cantidad_turno_extra = cantidad_turno_extra - 1
                                                            modelo.Add(lista_itinerario[semana][dia][1] >= vuelta + 1)
                                                else:
                                                      #Mes siguiente al actual
                                                      cantidad_turno_extra = cantidad_turno_extra - 1
                                                      modelo.Add(lista_itinerario[semana][dia][1] >= vuelta + 1) # 2 Personas en la mañana

                                          else:
                                                jornada[1] = False
                                                jornada[2] = True
                                    
                                    elif jornada[2]: # Turno de la Noche
                                          if dia <= LunesASabado:
                                                if meses_anio[month-1] == mes[semana][dia][0]:

                                                      _itinerario1 = [dia for dia in itinerario_dia if dia["turno"] == 1]
                                                      _itinerario2 = [dia for dia in itinerario_dia if dia["turno"] == 2]
                                                      _itinerario3 = [dia for dia in itinerario_dia if dia["turno"] == 3]

                                                      if not _itinerario1 and (_itinerario2 or _itinerario3):
                                                            if _itinerario2 and not _itinerario3:
                                                                  if _itinerario2[0]["aviones"] < num_empleado - cant_turno:
                                                                        turnos_totales[2] = turnos_totales[2] + 1
                                                                        cantidad_turno_extra = cantidad_turno_extra - 1
                                                                        modelo.Add(lista_itinerario[semana][dia][2] >= vuelta + 1) # 2 Personas en la mañana
                              
                                                            elif _itinerario3 and not _itinerario2:
                                                                  if _itinerario3[0]["aviones"] < num_empleado - cant_turno:
                                                                        turnos_totales[2] = turnos_totales[2] + 1
                                                                        cantidad_turno_extra = cantidad_turno_extra - 1
                                                                        modelo.Add(lista_itinerario[semana][dia][2] >= vuelta + 1)
                                                            else:
                                                                  if _itinerario2[0]["aviones"] + _itinerario3[0]["aviones"] < num_empleado - cant_turno:
                                                                        turnos_totales[2] = turnos_totales[2] + 1
                                                                        cantidad_turno_extra = cantidad_turno_extra - 1
                                                                        modelo.Add(lista_itinerario[semana][dia][2] >= vuelta + 1)
                                                      else:
                                                            turnos_totales[2] = turnos_totales[2] + 1
                                                            cantidad_turno_extra = cantidad_turno_extra - 1
                                                            modelo.Add(lista_itinerario[semana][dia][2] >= vuelta + 1)
                                                
                                                elif meses_anio[month_prev-1] == mes[semana][dia][0]:
                                                      if planificacionAnterior == None:
                                                            turnos_totales[2] = turnos_totales[2] + 1
                                                            cantidad_turno_extra = cantidad_turno_extra - 1
                                                            modelo.Add(lista_itinerario[semana][dia][2] >= vuelta + 1)
                                                else:
                                                      #Mes siguiente al actual
                                                      cantidad_turno_extra = cantidad_turno_extra - 1
                                                      modelo.Add(lista_itinerario[semana][dia][2] >= vuelta + 1)
                                          else:
                                                #print(cantidad_turno_extra,'noche')
                                                jornada[2] = False
                                                jornada[0] = True
                                                vuelta = vuelta + 1

      return modelo, turnos_totales, lista_itinerario