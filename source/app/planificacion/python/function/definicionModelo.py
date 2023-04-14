from calendar import monthrange
from ortools.sat.python import cp_model
import holidays


def DefiniendoModelo(modelo: cp_model.CpModel ,year: int, month: int, 
      all_empleado: range, cant_turno: int , meses_anio: list[str], cont_semana: list):
      
      if(month==12):
            month_next = 1
            year_next = year+1
            year_prev = year
            month_prev = month-1
      elif(month==1):
            month_prev = 12
            year_prev = year-1
            year_next = year
            month_next = month+1
      else:
            year_prev = year
            month_prev = month-1
            year_next = year
            month_next = month+1

      dias_mes_prev = monthrange(year_prev, month_prev)
      dias_mes_actual  = monthrange(year,month)
      dias_mes_next = monthrange(year_next, month_next)

      indice_semana_prev = dias_mes_prev[0]
      cantidad_dias_prev = dias_mes_prev[1]

      indice_semana = dias_mes_actual[0]
      cantidad_dias = dias_mes_actual[1]

      indice_semana_next = dias_mes_next[0]
      cantidad_dias_next = dias_mes_next[1]

      all_dias = range(1,cantidad_dias+1) 

      dias_semana = ["Lunes","Martes","Miercoles","Jueves","Viernes","Sabado","Domingo"]

      # Creacion de las Variables
      mes = []
      semana = []

      # Definiendo Modelo [SOLO LOS DIAS DEL MES SOLICITADO]
      for dia in all_dias:
            if(dias_semana[indice_semana] == "Lunes" and dia != 1):
                  mes.append(semana)
                  semana = []
                  array_empleado = ModeloTurnoDeEmpleados(modelo, all_empleado, cant_turno)
                  if(dia == cantidad_dias): 
                        semana.append([meses_anio[month-1],dia, dias_semana[indice_semana], array_empleado, FeriadoMes(year,month,dia)])
                        mes.append(semana)
                  else: 
                        semana.append([meses_anio[month-1],dia, dias_semana[indice_semana], array_empleado, FeriadoMes(year,month,dia)])
            else: 
                  array_empleado = ModeloTurnoDeEmpleados(modelo, all_empleado, cant_turno)
                  if(dia == cantidad_dias):
                        semana.append([meses_anio[month-1],dia, dias_semana[indice_semana], array_empleado, FeriadoMes(year,month,dia)])
                        mes.append(semana)
                  else:
                        semana.append([meses_anio[month-1],dia, dias_semana[indice_semana], array_empleado, FeriadoMes(year,month,dia)])
            indice_semana = indice_semana + 1
            if(indice_semana == 7): indice_semana=0
      
      AgregandoDiasUltimmaSemana(mes,year_next ,meses_anio, month_next, dias_semana, indice_semana_next, modelo, all_empleado, cant_turno)
      AgregandoDiasPrimeraSemana(mes,year_prev ,dias_mes_actual, meses_anio, month_prev, dias_semana, modelo, all_empleado, cant_turno, cantidad_dias_prev)
      ContadorDeSemanas(mes, cont_semana)
      return mes, all_dias, cont_semana, month_prev

def FeriadoMes(anio: int, mes: int, dia: int):
      feriados_anio = holidays.Chile(years=anio)
            
      feriado = {}
      for fecha, nombre in feriados_anio.items():
            if fecha.month == mes and fecha.day == dia: 
                  feriado["dia"] = fecha.day
                  feriado["mes"] = fecha.month
                  feriado["anio"] = fecha.year
                  feriado["nombre"] = nombre
                  feriado["feriado"] = True
            
      if not bool(feriado):
            feriado["feriado"] = False

      return feriado["feriado"]


def ModeloTurnoDeEmpleados(modelo: cp_model.CpModel, all_empleado: range, cant_turno: int):
      
      array_empleado = []
      for empleado in all_empleado:
            turnos = []
            for t in range(cant_turno):
                  turnos.append(
                        modelo.NewBoolVar('Empleado n° %i con turno n°%i' % (empleado,(t+1)))
                  )
            array_empleado.append(turnos)
      return array_empleado

def AgregandoDiasUltimmaSemana(
      mes: list[list], year: int, meses_anio: list[str], month_next: int, dias_semana: int, 
      indice_semana_next: int, modelo: cp_model.CpModel, all_empleado: range, cant_turno: int):
      """
      Esta función agrega los ultimos dias faltantes de la última 
      semana del mes.
      """
      if(len(mes[len(mes)-1])!=7):
            for k in range(7-indice_semana_next):
                  array_empleado = ModeloTurnoDeEmpleados(modelo, all_empleado, cant_turno)
                  mes[len(mes)-1].insert(indice_semana_next,[meses_anio[month_next-1],k+1,dias_semana[indice_semana_next],array_empleado, FeriadoMes(year,month_next,k+1)])
                  indice_semana_next = indice_semana_next + 1

def AgregandoDiasPrimeraSemana(mes: list[list], year: int, dias_mes_actual: int, meses_anio: list[str], month_prev: int, 
      dias_semana: int, modelo: cp_model.CpModel, all_empleado: range, cant_turno: int, cantidad_dias_prev: int):
      """
      Esta función agrega los primeros dias faltantes de la primera 
      semana del mes.
      """
      if(len(mes[0])!=7):
            indice_semana = dias_mes_actual[0]
            for j in range(indice_semana):
                  array_empleado = ModeloTurnoDeEmpleados(modelo, all_empleado, cant_turno)
                  mes[0].insert(0,[meses_anio[month_prev-1],cantidad_dias_prev,dias_semana[indice_semana-1],array_empleado, FeriadoMes(year,month_prev,cantidad_dias_prev)])
                  cantidad_dias_prev = cantidad_dias_prev-1
                  indice_semana = indice_semana-1

def ContadorDeSemanas(mes: list, cont_semana: list):
      """Función que cuenta la cantidad de semanas del modelo."""
      for i in mes:
            cont_semana.append(len(i))
