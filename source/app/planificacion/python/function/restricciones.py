from re import A
from statistics import mode
from sklearn.utils import shuffle
from ortools.sat.python import cp_model
from function.itinerario import *

#mes[num_semana][i][0] -> Mes
#mes[num_semana][i][1] -> Dia del mes
#mes[num_semana][i][2] -> Dia de semana
#mes[num_semana][i][3] -> Array de Empleado

def EmpleadoTrabajoPorDia(all_empleado: range, cont_semana: list, modelo:cp_model.CpModel, mes: list[list], cant_turno: int):
      """
      Cada empleado trabaja como máximo un turno por día.
      El resultado puede ser 0 porque puede tener el día libre.
      """
      for e in all_empleado:
            for num_semana in range(len(cont_semana)):
                  for i in range(cont_semana[num_semana]):
                        modelo.AddAtMostOne(mes[num_semana][i][3][e][t] for t in range(cant_turno))
      return modelo, mes

def DiaLibrePorSemana(all_empleado: range, cont_semana: list, mes: list[list], cant_turno: int, modelo: cp_model.CpModel, num_empleado: int):
      """Cada empleado tiene 1 día libre por semana."""
      for e in all_empleado:
            for num_semana in range(len(cont_semana)):
                  lista_semana = []
                  if(cont_semana[num_semana]==7):
                        for i in range(cont_semana[num_semana]):
                              if mes[num_semana][i][2] != 'Domingo':
                                    for t in range(cant_turno):
                                          lista_semana.append(mes[num_semana][i][3][e][t])
                        modelo.Add(sum(lista_semana) == num_empleado)
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
      Los empleados tienen 2 domingos libres durante el mes. Además, se límita
      la cantidad de empleados en los domingos.
      """
      #CantidadDomingosLibres = 2

      for num_semana in range(len(cont_semana)):
            for i in range(cont_semana[num_semana]):
                  if mes[num_semana][i][2] == 'Domingo' and mes[num_semana][i][0] == meses_anio[month-1]: 
                        domingos.append([i, num_semana]) 

      #for e in all_empleado: 
      #      lista_domingo_suma = []
      #      for domingo, num_semana in domingos:
      #            for t in range(cant_turno):
      #                  lista_domingo_suma.append(mes[num_semana][domingo][3][e][t])
      #      modelo.Add(sum(lista_domingo_suma) == CantidadDomingosLibres)

      return domingos

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
            for e in all_empleado: 
                  for t in range(cant_turno):
                        lista_minima_emp_domingo.append(mes[num_semana][domingo][3][e][t])

            if (CantidadTurnosMes - CantidadDomingosLibre)%len(domingos) == 0:
                  modelo.Add(sum(lista_minima_emp_domingo) >= (CantidadTurnosMes - CantidadDomingosLibre) // len(domingos))
            else:
                  modelo.Add(sum(lista_minima_emp_domingo) >= (CantidadTurnosMes - CantidadDomingosLibre) // len(domingos))
                  modelo.Add(sum(lista_minima_emp_domingo) <= (CantidadTurnosMes - CantidadDomingosLibre) // len(domingos)+1)

      #print((CantidadTurnosMes - CantidadDomingosLibre) // len(domingos))
      return modelo

def ContabilizandoTurnosDomingo(mes: list[list], domingos: list[list], cant_turno: int, turnos_totales: list):
      domingos_completo = [[1,1,1],[1,1,1]]
      domingos_incompleto = [[1,1,0],[1,1,0]]
      domingos_asignacion = []
      comodin = []

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
      return turnos_totales, domingos_asignacion



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
                              if i<= 5:
                                    modelo.Add(lista_itinerario[num_semana][i][0]==2)
                                    cantidad_turno_extra = cantidad_turno_extra - 1
                                    if meses_anio[month-1] == mes[num_semana][i][0] or meses_anio[month_prev-1] == mes[num_semana][i][0]: 
                                          turnos_totales[0] = turnos_totales[0] + 1
                              elif i>5:
                                    for i in range(cantidad_turno_extra):
                                          modelo.Add(lista_itinerario[num_semana][i][1]==2)
                                          cantidad_turno_extra = cantidad_turno_extra - 1
                                          if meses_anio[month-1] == mes[num_semana][i][0] or meses_anio[month_prev-1] == mes[num_semana][i][0]: 
                                                turnos_totales[1] = turnos_totales[1] + 1
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
            modelo.Add(sum(lista_semana)==(num_empleado*6)-num_empleado) # MODIFICAR
      return modelo

def AsignacionTurnos(modelo: cp_model.CpModel, mes: list[list],planificacionAnterior: None ,empleadoPlanificacionAnterior: list[str] , lista_itinerario: list ,cont_semana: list, 
      cant_turno: int, domingos: list, month: int,month_prev:int, meses_anio: list[str], all_empleado: range, domingos_asignacion: list):
      
      """Se asigna los turnos a cada empleado durante el mes"""
      
      for num_semana in range(len(cont_semana)):
            for i in range(cont_semana[num_semana]):
                  if(len(domingos)==5):
                        if mes[num_semana][i][2] == "Domingo" and mes[num_semana][i][0] == meses_anio[month-1]:
                              for t in range(cant_turno):
                                    modelo.Add(sum(mes[num_semana][i][3][e][t] for e in all_empleado)>=1)
                        
                        elif mes[num_semana][i][0] == meses_anio[month_prev-1] and planificacionAnterior != None:
                              for empleado in empleadoPlanificacionAnterior:
                                    for e in all_empleado: 
                                          if empleado == planificacionAnterior[i][e][1]:
                                                for t in range(cant_turno):
                                                      if planificacionAnterior[i][e][2] == t+1:
                                                            modelo.Add(mes[num_semana][i][3][e][t]==1)
                                                      else:
                                                            modelo.Add(mes[num_semana][i][3][e][t]==0)
                        else: 
                              for t in range(cant_turno):
                                    modelo.Add(sum(mes[num_semana][i][3][e][t] for e in all_empleado)==lista_itinerario[num_semana][i][t])

                  elif(len(domingos)==4):
                        if mes[num_semana][i][2] == "Domingo" and mes[num_semana][i][0] == meses_anio[month-1]:
                              for t in range(cant_turno):
                                    modelo.Add(sum(mes[num_semana][i][3][e][t] for e in all_empleado)==domingos_asignacion[num_semana][t])

                        elif mes[num_semana][i][0] == meses_anio[month_prev-1] and planificacionAnterior != None:
                              for empleado in empleadoPlanificacionAnterior:
                                    for e in all_empleado: 
                                          if empleado == planificacionAnterior[i][e][1]:
                                                for t in range(cant_turno):
                                                      if planificacionAnterior[i][e][2] == t+1:
                                                            modelo.Add(mes[num_semana][i][3][e][t]==1)
                                                      else:
                                                            modelo.Add(mes[num_semana][i][3][e][t]==0)
                        else:
                              for t in range(cant_turno):
                                    modelo.Add(sum(mes[num_semana][i][3][e][t] for e in all_empleado)==lista_itinerario[num_semana][i][t])

      return modelo