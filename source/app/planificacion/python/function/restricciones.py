import random
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

def DiaLibrePorSemana(all_empleado: range,cont_semana: list, mes: list[list], cant_turno: int, modelo: cp_model.CpModel, 
      meses_anio: list[str], month: int, all_empleadoAnterior: range, month_prev:int, empleadoPlanificacion: list[str]):
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
                  # Verificamos si el empleado participa en la planificación actual, si no participa, 
                  # entonces ya debería de tener un día libre, ya que solo se entra aquí, si el mes anterior
                  # termina en día que sea != sábado. Esto se debe al all_empleadoAnterior que hace esa verificación.
                  if mes[0][dia][3][empleadoAnterior][0].Name() in empleadoPlanificacion:
                        for dia in range(cont_semana[0]):
                              if mes[0][dia][0] == meses_anio[month-1] and mes[0][dia][2] != 'Domingo':
                                    for turno in range(cant_turno):
                                          lista_semana.append(mes[0][dia][3][empleadoAnterior][turno])
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
      meses_anio:list[str],month: int, month_prev: int):
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
                        if meses_anio[month_prev-1] == mes[0][dia][0]:
                              lista.append(mes[0][dia][3][empleadoAnterior][2]) # Último turno
                              if mes[0][dia+diaSiguiente][3][empleadoAnterior][0].Name() == '0': lista = []
                              else: lista.append(mes[0][dia+diaSiguiente][3][empleadoAnterior][0]) # Primer turno del dia siguiente
                        if lista: modelo.Add(sum(lista) <= 1)
            # Las demás semanas del mes
            for empleado in all_empleado:
                  for semana in range(len(cont_semana)):
                        for dia in range(cont_semana[semana]):
                              if mes[semana][dia][0] == meses_anio[month-1] and mes[semana][dia][3][empleado][0].Name() != '0':
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

def DomingosLibres(modelo: cp_model.CpModel,domingos: list , cont_semana: list, mes: list[list], 
      meses_anio: list[str], all_empleado: range, cant_turno: int, month: int):
      """
      Se identifican los dias que son domingos además, se hace la restricción
      de que los empleados tienen 2 domingos libres durante el mes.
      """

      for semana in range(len(cont_semana)):
            for dia in range(cont_semana[semana]):
                  if mes[semana][dia][2] == 'Domingo' and mes[semana][dia][0] == meses_anio[month-1]: 
                        domingos.append([dia, semana]) 
      
      DomingosLibresAlMes = 2

      for empleado in all_empleado:
            if mes[1][0][3][empleado][0].Name() != '0':
                  lista_domingo = []
                  for domingo, num_semana in domingos:
                        for turno in range(cant_turno):
                              lista_domingo.append(mes[num_semana][domingo][3][empleado][turno])
                  modelo.Add(sum(lista_domingo) == len(domingos) - DomingosLibresAlMes)

      return modelo, domingos

def CadaTurnoTieneAsignadoComoMinimoUnEmpleado(modelo: cp_model.CpModel,mes: list[list],cont_semana: list,
      cant_turno: int,turnos_totales, all_empleado: range,all_empleadoAnterior: range, meses_anio:list[str],
      month_prev: int, month: int):
      """
      Se aplica la restricción de que cada turno debe tener como mínimo un empleado.
      Se genera la lista "turnos totales"
      """
      Domingo = 6
      CantidadMinimaEmpleadoEnTurno = 1

      for semana in range(len(cont_semana)):
            for dia in range(cont_semana[semana]):
                  if dia != Domingo:
                        for turno in range(cant_turno):
                              lista = []
                              if all_empleadoAnterior == range(0):
                                    for empleado in all_empleado:
                                          lista.append(mes[semana][dia][3][empleado][turno])
                                    turnos_totales[turno]+=1
                              else:
                                    if mes[semana][dia][0] == meses_anio[month_prev-1]: 
                                          empleados = all_empleadoAnterior
                                    elif mes[semana][dia][0] == meses_anio[month-1]:
                                          turnos_totales[turno]+=1
                                          empleados = all_empleado
                                    else: 
                                          empleados = all_empleado
                                    for empleado in empleados:
                                          if mes[semana][dia][3][empleado][turno].Name() != '0':
                                                lista.append(mes[semana][dia][3][empleado][turno])
                              modelo.Add(sum(lista) >= CantidadMinimaEmpleadoEnTurno)

      return modelo, mes, turnos_totales






# Falta por optimizar.
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

def ContabilizandoTurnosDomingo(mes: list[list], domingos: list[list], cant_turno: int, turnos_totales: list, num_empleado: int, itinerario :list[object], lista_alarma: list[list]):
      CantidadDomingosLibre = 2 * num_empleado 
      CantidadTurnosMes = num_empleado * len(domingos) 
      #35 - 14 = 21 % 5 = 1
      cantidadMinimaDomingo = (CantidadTurnosMes - CantidadDomingosLibre) // len(domingos) 
      resto = (CantidadTurnosMes - CantidadDomingosLibre)%len(domingos)
      
      ArrayDeDomingo = [[0]*cant_turno for _ in range(len(domingos))]
      lista_comodin = []

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
            itinerario_dia = [iti for iti in itinerario if iti["dia"] == mes[num_semana][domingo][1] ]
            if itinerario_dia:
                  aux = ArrayDeDomingo.pop()
                  domingos_asignacion.append(aux)

                  for turno in range(cant_turno):
                        # Se busca si hay un itinerairo para el turno
                        _itinerario = [iti for iti in itinerario_dia if iti["turno"] == turno+1]

                        # Hay itinerario para el turno
                        if _itinerario:
                              # Alcanza los empleados para el itinerartio
                              if aux[turno] - 1 >= _itinerario[0]["aviones"]:
                                    turnos_totales[turno] = turnos_totales[turno] + aux[turno]
                              # No alcanzan los empleados para el itinerario
                              else:

                                    if aux[turno] == 0:

                                          lista_comodin.append([mes[num_semana][domingo][1],turno+1])
                                          empleadosFaltante = _itinerario[0]["aviones"]
                                          lista_alarma.append([_itinerario[0]["dia"],_itinerario[0]["turno"],empleadosFaltante])
                                          turnos_totales[turno] = turnos_totales[turno] + aux[turno]
                                    else:

                                          empleadosFaltante = _itinerario[0]["aviones"] - (aux[turno] - 1)
                                          lista_alarma.append([_itinerario[0]["dia"],_itinerario[0]["turno"],empleadosFaltante])
                                          turnos_totales[turno] = turnos_totales[turno] + aux[turno]

                        # No hay itinerario para el turno
                        else:
                              if aux[turno] == 0:
                                    lista_comodin.append([mes[num_semana][domingo][1],turno+1])
                                    turnos_totales[turno] = turnos_totales[turno] + aux[turno]
                              else:
                                    turnos_totales[turno] = turnos_totales[turno] + aux[turno]

            else: 
                  aux = ArrayDeDomingo.pop()
                  domingos_asignacion.append(aux)
                  for turno in range(cant_turno):
                        if aux[turno] == 0: lista_comodin.append([mes[num_semana][domingo][1],turno+1])
                        else: turnos_totales[turno] = turnos_totales[turno] + aux[turno]
      
      # Se cambia el orden de los elementos si son 5 empleados
      if num_empleado == 5 and len(domingos_asignacion) == 4:
            random.shuffle(domingos_asignacion)
            for domingo in domingos_asignacion:
                  random.shuffle(domingo)

      return turnos_totales, domingos_asignacion, lista_comodin

def ListaAsignacionTurnoSobrantes(modelo: cp_model.CpModel, mes: list[list],domingos_asignacion: list ,cont_semana: list, lista_turno_extra: list, meses_anio: list[str], month: int, month_prev: int ,lista_itinerario: list, itinerario: list[object], 
      turnos_totales: list, planificacionAnterior: None, lista_alarma:list[list], all_empleado: range, empleadoPlanificacionAnterior: list[str], cant_turno: int):
      """ Se asigna a los empleados """
      LunesASabado = 5
      empleadoRequerido = 1
      Domingo = 6

      for semana in range(len(cont_semana)):
            cantidad_turno_extra = lista_turno_extra[semana]
            turnoAsignar = 0 # 0->Mañana, 1->Tarde, 2->Noche
            empleadoAdicionales = 1
            for dia in itertools.cycle(range(cont_semana[semana])):
                  if cantidad_turno_extra == 0: break
                  itinerario_dia = [_itinerario for _itinerario in itinerario if _itinerario["dia"] == mes[semana][dia][1] ]
                  if dia <= LunesASabado:
                        # Mes actual
                        if meses_anio[month-1] == mes[semana][dia][0]:
                              # ARREGLAR
                              _itinerario1 = [dia for dia in itinerario_dia if dia["turno"] == 1]
                              _itinerario2 = [dia for dia in itinerario_dia if dia["turno"] == 2]
                              _itinerario3 = [dia for dia in itinerario_dia if dia["turno"] == 3]

                              if not _itinerario1 and (_itinerario2 or _itinerario3):
                                    print("No entrar")
                              else:
                                    turnos_totales[turnoAsignar]+=1
                                    cantidad_turno_extra-=1
                                    lista = []
                                    for empleado in all_empleado:
                                          if mes[semana][dia][3][empleado][turnoAsignar].Name() != '0':
                                                lista.append(mes[semana][dia][3][empleado][turnoAsignar])
                                    if lista: modelo.Add(sum(lista) >= empleadoRequerido + empleadoAdicionales)
                        elif meses_anio[month_prev-1] == mes[semana][dia][0]:  
                              if planificacionAnterior == None:
                                    turnos_totales[turnoAsignar]+=1
                                    cantidad_turno_extra-=1
                                    lista = []
                                    for empleado in all_empleado:
                                          if mes[semana][dia][3][empleado][turnoAsignar].Name() != '0':
                                                lista.append(mes[semana][dia][3][empleado][turnoAsignar])
                                    if lista: modelo.Add(sum(lista) >= empleadoRequerido + empleadoAdicionales)
                              else: # Asignación de la planificación pasada
                                    for empleadoAnterior in empleadoPlanificacionAnterior:
                                          for empleado in range(len(empleadoPlanificacionAnterior)):
                                                if empleadoAnterior == planificacionAnterior[dia][empleado][1]:
                                                      for turno in range(cant_turno):
                                                            if planificacionAnterior[dia][empleado][2] == turno+1:
                                                                  modelo.Add(mes[semana][dia][3][empleado][turno]==1)
                                                            else:
                                                                  modelo.Add(mes[semana][dia][3][empleado][turno]==0)
                        else:
                              cantidad_turno_extra-=1
                              lista = []
                              for empleado in all_empleado:
                                    if mes[semana][dia][3][empleado][turnoAsignar].Name() != '0':
                                          lista.append(mes[semana][dia][3][empleado][turnoAsignar])
                              if lista: modelo.Add(sum(lista) >= empleadoRequerido + empleadoAdicionales)
                  else:
                        if (turnoAsignar) == 2: 
                              turnoAsignar = 0
                              empleadoAdicionales+=1
                        else: 
                              turnoAsignar+=1
                  if mes[semana][dia][2] == 'Domingo' and meses_anio[month-1] == mes[semana][dia][1]:
                        for turno in range(cant_turno):
                              lista = []
                              for empleado in all_empleado:
                                    if mes[semana][dia][3][empleado][turno].Name() != '0':
                                          lista.append(mes[semana][dia][3][empleado][turno])
                              modelo.Add(sum(lista) == domingos_asignacion[semana][turno])
      return modelo, turnos_totales

def CantidadEmpleadoTrabajandoXSemanaYDia(modelo: cp_model.CpModel, mes: list[list], meses_anio: list[str], month_prev: int, month:int, cont_semana: list, cant_turno: int, list_itinerario: list[list], num_empleado: int, num_empleadoAnterior: int, lista_turno_extra: list[int], turnos_extra: int):
      """   [lista_semana] -> Máxima cantidad de turnos trabajados en 1 semana por dia
            [lista_dia] -> Máxima y mínima cantidad de empleados trabajando en un día.
      """
      Domingo = 6
      DiasSemanaSinDomingo = 6
      cantidadDiasPrimeraSemana = 0 # Se cuentan desde el lunes hasta el domingo

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
            lista_primera_semana = []

            for dia in range(cont_semana[0]):
                  if dia != Domingo and mes[0][dia][0] == meses_anio[month-1]:
                        lista_dia = []
                        for turno in range(cant_turno):
                              lista_primera_semana.append(list_itinerario[0][dia][turno])
                              lista_dia.append(list_itinerario[0][dia][turno])
                        modelo.Add(sum(lista_dia) <= num_empleado)
                        modelo.Add(sum(lista_dia) >= cant_turno)
                        cantidadDiasPrimeraSemana = cantidadDiasPrimeraSemana + 1
                        #print(mes[0][dia][0],mes[0][dia][2],mes[0][dia][1],cantidadDiasPrimeraSemana)
            #if lista_primera_semana:
                  #print(cantidadDiasPrimeraSemana,(cant_turno*cantidadDiasPrimeraSemana)+lista_turno_extra[0])
                  #print(cant_turno,cantidadDiasPrimeraSemana, lista_turno_extra[0])
                  #modelo.Add(sum(lista_primera_semana)== (cant_turno*cantidadDiasPrimeraSemana)+(lista_turno_extra[0]))  #16 

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
                                    if mes[semana][dia][3][empleado][t].Name() != '0':
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