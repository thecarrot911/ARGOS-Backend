from re import I, S
from sklearn.utils import shuffle
from ortools.sat.python import cp_model
from function.itinerario import *
import itertools

#mes[num_semana][i][0] -> Mes
#mes[num_semana][i][1] -> Dia del mes
#mes[num_semana][i][2] -> Dia de semana
#mes[num_semana][i][3] -> Array de Empleado

def EmpleadoTrabajoPorDia(all_empleado: range, cont_semana: list, modelo:cp_model.CpModel, mes: list[list], cant_turno: int, meses_anio: list[str], month: int, month_prev:int, all_empleadoAnterior: range):
      """
      Cada empleado trabaja como máximo un turno por día.
      El resultado puede ser 0 porque puede tener el día libre.
      """
      # Restricción para el mes actual.
      for e in all_empleado:
            for num_semana in range(len(cont_semana)):
                  for i in range(cont_semana[num_semana]):
                        if meses_anio[month_prev-1] != mes[num_semana][i][0]: # Se cambio a distinto del mes pasado, para incluir futuro
                              modelo.AddAtMostOne(mes[num_semana][i][3][e][t] for t in range(cant_turno))
      
      # Restricción para el mes anterior (Asegurar)

      # Si no hay planificación anterior, entonces...
      if all_empleadoAnterior == range(0):
            all_anterior = all_empleado
      # Hay planificación anterior
      else:
            all_anterior = all_empleadoAnterior

      for e in all_anterior:
            for num_semana in range(len(cont_semana)):
                  for i in range(cont_semana[num_semana]):
                        if meses_anio[month_prev-1] == mes[num_semana][i][0]:
                              modelo.AddAtMostOne(mes[num_semana][i][3][e][t] for t in range(cant_turno))


      return modelo, mes

def DiaLibrePorSemana(all_empleado: range,cont_semana: list, mes: list[list], cant_turno: int, modelo: cp_model.CpModel, num_empleado: int, meses_anio: list[str], month: int, all_empleadoAnterior: range, month_prev:int, empleadoPlanificacion: list[str], empleadoPlanificacionAnterior: list[str]):
      """Cada empleado tiene 1 día libre por semana."""
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

def NoAdmitenTurnosSeguidos(all_empleado: range,all_empleadoAnterior: range , cont_semana: list, mes: list[list], modelo: cp_model.CpModel,
      meses_anio:list[str],month: int, month_prev: int, empleadoPlanificacion: list[str]):
      """
      Los empleados no pueden tener turnos seguidos, es decir que un empleado que trabaje en la
      jornada de la noche, no puede trabajar el día siguiente en la jornada de la mañana.
      """
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

def DomingosLibres(modelo: cp_model.CpModel,domingos: list , cont_semana: list, mes: list[list], meses_anio: list[str], all_empleado: range,num_empleado: int, cant_turno: int, month: int):
      """
      Se cuentan los dias que son domingos y además, se hace la restricción
      de que los empleados tienen 2 domingos libres durante el mes.
      """

      for num_semana in range(len(cont_semana)):
            for i in range(cont_semana[num_semana]):
                  if mes[num_semana][i][2] == 'Domingo' and mes[num_semana][i][0] == meses_anio[month-1]: 
                        domingos.append([i, num_semana]) 
      
      DomingosLibresAlMes = 2

      for empleado in all_empleado:
            if mes[1][0][3][empleado][0].Name() != '0':
                  lista_domingo = []
                  for domingo, num_semana in domingos:
                        for turno in range(cant_turno):
                              lista_domingo.append(mes[num_semana][domingo][3][empleado][turno])
                  modelo.Add(sum(lista_domingo) == len(domingos) - DomingosLibresAlMes)

      return modelo, domingos

def CantidadMaximaDeEmpleadoDomingo(modelo: cp_model.CpModel,mes: list[list], all_empleado: range, domingos: list[list], num_empleado: int , cant_turno: int):
      """Se límita la cantidad máxima de empleados que puede haber en los domningos del mes."""
      lista_domingos_empleados = []
      CantidadDomingosLibre = 2 * num_empleado
      CantidadTurnosMes = num_empleado * len(domingos)
      CantidadMaximaDomingo = CantidadTurnosMes - CantidadDomingosLibre
      for e in all_empleado: 
            for domingo, num_semana in domingos:
                  for t in range(cant_turno):
                        lista_domingos_empleados.append(mes[num_semana][domingo][3][e][t])
      modelo.Add(sum(lista_domingos_empleados) == CantidadMaximaDomingo)
      return modelo

def CantidadMinimaDeEmpleadoDomingo(modelo: cp_model.CpModel,mes: list[list], all_empleado: range, domingos: list[list], num_empleado: int , cant_turno: int):
      """Se límita la cantidad mínima de empleados que puede haber en un día domingo."""
      CantidadDomingosLibre = 2 * num_empleado
      CantidadTurnosMes = num_empleado * len(domingos)
      
      for domingo, num_semana in domingos:
            lista_minima_emp_domingo = []
            for empleado in all_empleado:
                  for t in range(cant_turno):
                        lista_minima_emp_domingo.append(mes[num_semana][domingo][3][empleado][t])
            
            if (CantidadTurnosMes - CantidadDomingosLibre)%len(domingos) == 0:
                  modelo.Add(sum(lista_minima_emp_domingo) >= (CantidadTurnosMes - CantidadDomingosLibre) // len(domingos))
            else:
                  modelo.Add(sum(lista_minima_emp_domingo) >= (CantidadTurnosMes - CantidadDomingosLibre) // len(domingos))
                  modelo.Add(sum(lista_minima_emp_domingo) <= (CantidadTurnosMes - CantidadDomingosLibre) // len(domingos)+1)

      return modelo

def ContabilizandoTurnosDomingo(mes: list[list], domingos: list[list], cant_turno: int, turnos_totales: list, num_empleado: int):
      CantidadDomingosLibre = 2 * num_empleado # 14
      CantidadTurnosMes = num_empleado * len(domingos) #35 - 14 = 21 % 5 = 1

      cantidadMinimaDomingo = (CantidadTurnosMes - CantidadDomingosLibre) // len(domingos)
      resto = (CantidadTurnosMes - CantidadDomingosLibre)%len(domingos)
      
      ArrayDeDomingo = [[0]*cant_turno for _ in range(len(domingos))]

      for domingo in ArrayDeDomingo:
            indice = 0
            for _ in range(cantidadMinimaDomingo):
                  domingo[indice] = domingo[indice] + 1
                  indice = (indice + 1) % cant_turno # Circular indice

      if resto != 0:
            for domingo in ArrayDeDomingo:
                  indice = domingo.index(min(domingo))
                  resto = resto - 1
                  domingo[indice] = domingo[indice] + 1
                  if resto == 0: break

      domingos_asignacion = []

      for domingo, num_semana in domingos:
            aux = ArrayDeDomingo.pop()
            domingos_asignacion.append(aux)
            for t in range(cant_turno):
                  turnos_totales[t] = turnos_totales[t] + aux[t]

      """for domingo, num_semana in domingos:
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
                              else: turnos_totales[t] = turnos_totales[t] + 1"""

      return turnos_totales, domingos_asignacion



def ListaAsignacionTurnoSobrantes(modelo: cp_model.CpModel, mes: list[list], cont_semana: list, lista_turno_extra: list, meses_anio: list[str], month: int, month_prev: int ,lista_itinerario: list, itinerario: list[object], turnos_totales: list, planificacionAnterior: None):
      """ Se asigna a los empleados """
      LunesASabado = 5

      for semana in range(len(cont_semana)):
            cantidad_turno_extra = lista_turno_extra[semana]
            for diaSemana in range(cont_semana[semana]):
                  # Si no hay turno extra, se sale del for
                  if cantidad_turno_extra == 0: break
                  # Si hay turno extra, se sigue iterando
                  else:
                        jornada = [False, False, False]
                        itinerario_dia = [dia for dia in itinerario if dia["dia"] == mes[semana][diaSemana][1] ]
                        # Hay itinerario y turno extra
                        if itinerario_dia and cantidad_turno_extra >= 1:
                              # Hay itinerario
                              print("")
                        # No hay itinerario pero si turno extra
                        elif cantidad_turno_extra >= 1:
                              if diaSemana <= LunesASabado:

                                    #cantidad_turno_extra = cantidad_turno_extra - 1

                                    if meses_anio[month-1] == mes[semana][diaSemana][0]:
                                          turnos_totales[0] = turnos_totales[0] + 1
                                          cantidad_turno_extra = cantidad_turno_extra - 1
                                          modelo.Add(lista_itinerario[semana][diaSemana][0] >= 2) # 2 Personas en la mañana

                                    elif meses_anio[month_prev-1] == mes[semana][diaSemana][0]: 
                                          if planificacionAnterior == None:
                                                turnos_totales[0] = turnos_totales[0] + 1
                                                cantidad_turno_extra = cantidad_turno_extra - 1
                                                modelo.Add(lista_itinerario[semana][diaSemana][0] >= 2) # 2 Personas en la mañana
                                    
                                    else: #Mes siguiente
                                          cantidad_turno_extra = cantidad_turno_extra - 1
                                          modelo.Add(lista_itinerario[semana][diaSemana][0] >= 2) # 2 Personas en la mañana


                              elif diaSemana > LunesASabado:
                                    #print(cantidad_turno_extra,'fuera')
                                    jornada[1] = True
                                    vuelta = 1

                                    for dia in itertools.cycle(range(cont_semana[semana])):
                                          if cantidad_turno_extra == 0: break
                                          if jornada[0]: # Turno de la Mañana
                                                if dia <= LunesASabado:
                                                      
                                                      if meses_anio[month-1] == mes[semana][dia][0]:
                                                            turnos_totales[0] = turnos_totales[0] + 1
                                                            cantidad_turno_extra = cantidad_turno_extra - 1 # Se agrego
                                                            modelo.Add(lista_itinerario[semana][dia][0] >= vuelta + 1) # 2 Personas en la mañana


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
                                                            turnos_totales[1] = turnos_totales[1] + 1
                                                            cantidad_turno_extra = cantidad_turno_extra - 1
                                                            modelo.Add(lista_itinerario[semana][dia][1] >= vuelta + 1) # 2 Personas en la mañana


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
                                                      #print(cantidad_turno_extra,'tarde')
                                                      jornada[1] = False
                                                      jornada[2] = True
                                          
                                          elif jornada[2]: # Turno de la Noche
                                                if dia <= LunesASabado:
                                                      if meses_anio[month-1] == mes[semana][dia][0]:
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



def CantidadEmpleadoTrabajandoXSemanaYDia(modelo: cp_model.CpModel, mes: list[list], meses_anio: list[str], month_prev: int, month:int, cont_semana: list, cant_turno: int, list_itinerario: list[list], num_empleado: int, num_empleadoAnterior: int):
      """   [lista_semana] -> Máxima cantidad de turnos trabajados en 1 semana por dia
            [lista_dia] -> Máxima y mínima cantidad de empleados trabajando en un día.
      """
      Domingo = 6
      DiasSemanaSinDomingo = 6

      # No hay planificación Anterior
      if num_empleadoAnterior == 0: 
            for semana in range(len(cont_semana)):
                  lista_semana = []
                  for dia in range(cont_semana[semana]):
                        if dia != Domingo:
                              lista_dia = []
                              for turno in range(cant_turno):
                                    lista_semana.append(list_itinerario[semana][dia][turno])
                                    lista_dia.append(list_itinerario[semana][dia][turno])
                              modelo.Add(sum(lista_dia)<=num_empleado)
                              modelo.Add(sum(lista_dia)>=cant_turno)
                  modelo.Add(sum(lista_semana)==(num_empleado*DiasSemanaSinDomingo)-num_empleado)

      # Hay planificación Anterior
      else:

            for semana in range(1,len(cont_semana)):
                  lista_semana = []
                  for dia in range(cont_semana[semana]):
                        if dia != Domingo:
                              lista_dia = []
                              for turno in range(cant_turno):
                                    lista_semana.append(list_itinerario[semana][dia][turno])
                                    lista_dia.append(list_itinerario[semana][dia][turno])
                              modelo.Add(sum(lista_dia)<=num_empleado)
                              modelo.Add(sum(lista_dia)>=cant_turno)
                  
                  if lista_semana:
                        modelo.Add(sum(lista_semana)==(num_empleado*6)-num_empleado)
      return modelo

def AsignacionTurnos(modelo: cp_model.CpModel, mes: list[list],planificacionAnterior: None ,empleadoPlanificacionAnterior: list[str] , lista_itinerario: list ,cont_semana: list, 
      cant_turno: int, domingos: list, month: int,month_prev:int, meses_anio: list[str], all_empleado: range, domingos_asignacion: list):
      
      """Se asigna los turnos a cada empleado durante el mes"""
      for semana in range(len(cont_semana)):
            for dia in range(cont_semana[semana]):
                  if mes[semana][dia][2] == "Domingo" and mes[semana][dia][0] == meses_anio[month-1]: #DOMINGO DE ESTE MES
                        for t in range(cant_turno):
                              lista = []
                              for empleado in all_empleado:
                                    if mes[semana][dia][3][empleado][turno].Name() != '0':
                                          lista.append(mes[semana][dia][3][empleado][t])
                              modelo.Add(sum(lista)==domingos_asignacion[semana][t])

                  elif mes[semana][dia][0] == meses_anio[month_prev-1] and planificacionAnterior != None: # MES ANTERIOR
                        for empleadoAnterior in empleadoPlanificacionAnterior:
                              for empleado in range(len(empleadoPlanificacionAnterior)):
                                    if empleadoAnterior == planificacionAnterior[dia][empleado][1]:
                                          for turno in range(cant_turno):
                                                if planificacionAnterior[dia][empleado][2] == turno+1:
                                                      modelo.Add(mes[semana][dia][3][empleado][turno]==1)
                                                else:
                                                      modelo.Add(mes[semana][dia][3][empleado][turno]==0)

                  else: # MES ACTUAL y SI NO HAY PLANIFICACION ANTERIOR ENTRA EL MES PASADO Y FUTURO
                        for turno in range(cant_turno):
                              lista = []
                              for empleado in all_empleado:
                                    if mes[semana][dia][3][empleado][turno].Name() != '0':
                                          lista.append(mes[semana][dia][3][empleado][turno])
                              modelo.Add( sum(lista) == lista_itinerario[semana][dia][turno] )

      return modelo