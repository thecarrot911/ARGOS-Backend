from re import I, S
from sklearn.utils import shuffle
from ortools.sat.python import cp_model
from function.itinerario import *

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
                        if meses_anio[month-1] == mes[num_semana][i][0]:
                              modelo.AddAtMostOne(mes[num_semana][i][3][e][t] for t in range(cant_turno))
      
      # Restricción para el mes anterior (Asegurar)
      for e in all_empleadoAnterior:
            for num_semana in range(len(cont_semana)):
                  for i in range(cont_semana[num_semana]):
                        if meses_anio[month_prev-1] == mes[num_semana][i][0]:
                              modelo.AddAtMostOne(mes[num_semana][i][3][e][t] for t in range(cant_turno))


      return modelo, mes

def DiaLibrePorSemana(all_empleado: range,cont_semana: list, mes: list[list], cant_turno: int, modelo: cp_model.CpModel, num_empleado: int, meses_anio: list[str], month: int, all_empleadoAnterior: range, month_prev:int, empleadoPlanificacion: list[str], empleadoPlanificacionAnterior: list[str]):
      """Cada empleado tiene 1 día libre por semana."""
      cantidadDiaSemana = 6 # Lunes a Sábado
      diasLibreCadaEmpleadoPorSemana = 1
      
      # Restricción para la primera semana
      for empleadoAnterior in all_empleadoAnterior:
            lista_semana = []
            for dia in range(cont_semana[0]):
                  if mes[0][dia][0] == meses_anio[month_prev-1] and mes[0][dia][2] != 'Domingo':
                        for turno in range(cant_turno):
                              lista_semana.append(mes[0][dia][3][empleadoAnterior][turno])

            if mes[0][dia][3][empleadoAnterior][0].Name() in empleadoPlanificacion:
                  for dia in range(cont_semana[0]):
                        if mes[0][dia][0] == meses_anio[month-1] and mes[0][dia][2] != 'Domingo':
                              for turno in range(cant_turno):
                                    lista_semana.append(mes[0][dia][3][empleadoAnterior][turno])
            if lista_semana and mes[0][dia][3][empleadoAnterior][0].Name() in empleadoPlanificacion:
                  modelo.Add(sum(lista_semana) == cantidadDiaSemana - diasLibreCadaEmpleadoPorSemana)


      # Restricción para las demás semanas
      for empleado in all_empleado:
            #print(mes[1][0][3][empleado][turno].Name())
            if mes[1][0][3][empleado][0].Name() != '0':
                  for semana in range(1,len(cont_semana)):
                        lista_semana = []
                        for dia in range(cont_semana[semana]):
                              if mes[semana][dia][2] != 'Domingo':
                                    for turno in range(cant_turno):
                                          lista_semana.append(mes[semana][dia][3][empleado][turno])
                        modelo.Add(sum(lista_semana) == cantidadDiaSemana - diasLibreCadaEmpleadoPorSemana)

      return modelo, mes

def NoAdmitenTurnosSeguidos(all_empleado: range, cont_semana: list, mes: list[list], modelo: cp_model.CpModel):
      """
      Los empleados no pueden tener turnos seguidos, es decir que un empleado que trabaje en la
      jornada de la noche, no puede trabajar el día siguiente en la jornada de la mañana.
      """
      for e in all_empleado:
            for num_semana in range(len(cont_semana)):
                  for i in range(cont_semana[num_semana]):
                        lista_turno = []
                        if(i+1!=cont_semana[num_semana]):
                              lista_turno.append(mes[num_semana][i][3][e][2])
                              lista_turno.append(mes[num_semana][i+1][3][e][0])

                              if mes[num_semana][i][3][e][2].Name() == mes[num_semana][i+1][3][e][0].Name():
                                    #print(str(mes[num_semana][i][1])+'|'+str(mes[num_semana][i+1][1]))
                                    #print(mes[num_semana][i][3][e][2].Name()+'|'+mes[num_semana][i+1][3][e][0].Name())
                                    modelo.Add(sum(lista_turno) <= 1)
                              else:
                                    modelo.Add(sum(lista_turno) <= 2)

                        else: 
                              if((i+1)*(num_semana+1)< len(mes[num_semana])*len(mes)):
                                    lista_turno.append(mes[num_semana][i][3][e][2])
                                    lista_turno.append(mes[num_semana+1][0][3][e][0])

                                    if mes[num_semana][i][3][e][2].Name() == mes[num_semana+1][0][3][e][0].Name():
                                          modelo.Add(sum(lista_turno) <= 1)
                                          #print(str(mes[num_semana][i][1])+'|'+str(mes[num_semana+1][i][1]))
                                          #print(mes[num_semana][i][3][e][2].Name()+'|'+mes[num_semana+1][0][3][e][0].Name())
                                    else:
                                          modelo.Add(sum(lista_turno) <= 2)

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
                  #print((CantidadTurnosMes - CantidadDomingosLibre) // len(domingos))
                  #print((CantidadTurnosMes - CantidadDomingosLibre) // len(domingos)+1)
                  modelo.Add(sum(lista_minima_emp_domingo) >= (CantidadTurnosMes - CantidadDomingosLibre) // len(domingos))
                  modelo.Add(sum(lista_minima_emp_domingo) <= (CantidadTurnosMes - CantidadDomingosLibre) // len(domingos)+1)

      #print((CantidadTurnosMes - CantidadDomingosLibre) // len(domingos))
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



def ListaAsignacionTurnoSobrantes(modelo: cp_model.CpModel, mes: list[list], cont_semana: list, lista_turno_extra: list, meses_anio: list[str], month: int, month_prev: int ,lista_itinerario: list, itinerario: list[object], turnos_totales: list):
      """ Se asigna a los empleados """
      for num_semana in range(len(cont_semana)):
            cantidad_turno_extra = lista_turno_extra[num_semana]
            for i in range(lista_turno_extra[num_semana]):
                  jornada = [False, False, False]
                  itinerario_dia = [dia for dia in itinerario if dia["dia"] == mes[num_semana][i][1] ]
                  if itinerario_dia and cantidad_turno_extra >= 1:
                        # Hay itinerario
                        print("")
                  elif cantidad_turno_extra>=1:
                        # No hay itinerario
                        if i <= 5: # ASIGNACIÓN EN LA MAÑANA PRIMERA VUELTA
                              modelo.Add(lista_itinerario[num_semana][i][0]>=2)
                              cantidad_turno_extra = cantidad_turno_extra - 1
                              if meses_anio[month-1] == mes[num_semana][i][0] or meses_anio[month_prev-1] == mes[num_semana][i][0]: 
                                    turnos_totales[0] = turnos_totales[0] + 1

                        elif i > 5: # ASIGNACIÓN DE LA MAÑANA, TARDE Y NOCHE
                              jornada[1] = True
                              vuelta = 1 # POSIBLE CALCULO PARA ASIGNAR MÁS..
                              dia = 0
                              for cantidad in range(cantidad_turno_extra):
                                    if dia + 1 == 7:
                                          dia = 0
                                          indice = jornada.index(True)
                                          if indice+1 == 3:
                                                jornada[0] = True
                                                jornada[indice] = False
                                          else:
                                                jornada[indice+1] = True
                                                jornada[indice] = False

                                    if jornada[1]: # Tarde
                                          modelo.Add(lista_itinerario[num_semana][dia][1] >= vuelta + 1)
                                          cantidad_turno_extra = cantidad_turno_extra - 1
                                          if meses_anio[month-1] == mes[num_semana][dia][0] or meses_anio[month_prev-1] == mes[num_semana][dia][0]: 
                                                turnos_totales[1] = turnos_totales[1] + 1

                                    elif jornada[2]: # Noche
                                          modelo.Add(lista_itinerario[num_semana][dia][2] >= vuelta + 1)
                                          cantidad_turno_extra = cantidad_turno_extra - 1
                                          if meses_anio[month-1] == mes[num_semana][dia][0] or meses_anio[month_prev-1] == mes[num_semana][dia][0]: 
                                                turnos_totales[2] = turnos_totales[2] + 1

                                    """elif jornada[0]: # Mañana
                                          modelo.Add(lista_itinerario[num_semana][dia][0] >= vuelta + 1)
                                          cantidad_turno_extra = cantidad_turno_extra - 1
                                          turnos_totales[0] = turnos_totales[0] + 1"""

                                    dia = dia + 1

      return modelo, turnos_totales



def CantidadEmpleadoTrabajandoXSemanaYDia(modelo: cp_model.CpModel, cont_semana: list, cant_turno: int, list_itinerario: list[list], num_empleado: int):
      """   [lista_semana] -> Máxima cantidad de turnos trabajados en 1 semana por dia
            [lista_dia] -> Máxima y mínima cantidad de empleados trabajando en un día.
      """
      for num_semana in range(len(cont_semana)):
            lista_semana = []
            for i in range(cont_semana[num_semana]):
                  if(i!=6):
                        lista_dia = []
                        for t in range(cant_turno):
                              lista_semana.append(list_itinerario[num_semana][i][t])
                              lista_dia.append(list_itinerario[num_semana][i][t])
                        modelo.Add(sum(lista_dia)<=num_empleado)
                        modelo.Add(sum(lista_dia)>=cant_turno)
            modelo.Add(sum(lista_semana)==(num_empleado*6)-num_empleado) # Esta bien, creo
      return modelo

def AsignacionTurnos(modelo: cp_model.CpModel, mes: list[list],planificacionAnterior: None ,empleadoPlanificacionAnterior: list[str] , lista_itinerario: list ,cont_semana: list, 
      cant_turno: int, domingos: list, month: int,month_prev:int, meses_anio: list[str], all_empleado: range, domingos_asignacion: list):
      
      """Se asigna los turnos a cada empleado durante el mes"""
      for semana in range(len(cont_semana)):
            for dia in range(cont_semana[semana]):
                  if mes[semana][dia][2] == "Domingo" and mes[semana][dia][0] == meses_anio[month-1]: #DOMINGO DE ESTE MES
                        for t in range(cant_turno):
                              modelo.Add(sum(mes[semana][dia][3][e][t] for e in all_empleado)==domingos_asignacion[semana][t])

                  elif mes[semana][dia][0] == meses_anio[month_prev-1] and planificacionAnterior != None: # MES ANTERIOR
                        for empleadoAnterior in empleadoPlanificacionAnterior:
                              for empleado in range(len(empleadoPlanificacionAnterior)):
                                    if empleadoAnterior == planificacionAnterior[dia][empleado][1]:
                                          for turno in range(cant_turno):
                                                if planificacionAnterior[dia][empleado][2] == turno+1:
                                                      modelo.Add(mes[semana][dia][3][empleado][turno]==1)
                                                else:
                                                      modelo.Add(mes[semana][dia][3][empleado][turno]==0)
                  else: # MES ACTUAL
                        for t in range(cant_turno):
                              modelo.Add(sum(mes[semana][dia][3][e][t] for e in all_empleado)==lista_itinerario[semana][dia][t])

      return modelo