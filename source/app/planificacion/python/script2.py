import sys
from numpy import append
from ortools.sat.python import cp_model
import random

# Sistema de turno operacionales
#
# Restricciones
#- 1    Cada trabajador durante la semana tiene 1 día libre. (Faltan las semanas iniciales y finales)
#       (Solucionarlo con agregar las semanas de los otro meses..)

#-[2]   Los trabajadores durante el mes de trabajo deben tener 2 domingos libres.
#       (Funciona pero solo para 1 empleado y no para 5)

#- 3    El turno abre con 2 personas(turno de la mañana).(Falta implementar)

#-[4]   Las personas no pueden tener 2 turnos seguidos.
#       (No olvidar consultar por la planifiación anterior para que no asigne de una planifiación a otro el mismo empleado en turnos seguidos)

#- 5.    En caso de que dos o más aviones de las líneas áreas SKY, LATAM y JETSMART lleguen a la misma hora o con una diferencia de menos de 20 minutos a reabastecerse de combustible, es necesario tener la misma cantidad de empleados que de aviones para ese turno.
#       _________________________
#      | Turno 1: 7:00 - 15:00;  |
#      | Turno 2: 15:00 - 23:00; | 
#      | Turno 3: 23:00 - 07:00; |
#      |_________________________|
#
#-[6].    En la empresa hay 5 empleados para la distribución de los turnos.
#- 7.    La carga de trabajo de los empleados debe ser equilibrada en base a la cantidad de turnos que tiene. (código listo, pero se debe terminar las demás restricciones para hacerlo)


# Restricciones incorporadas
#-6.   En la empresa hay 5 empleados para la distribución de los turnos.
#-7.   La carga de trabajo de los empleados debe ser equilibrada en base a: 
#-7.2.      Cantidad de turnos que tiene. 


def main():
    # Data.
    num_dias = int(sys.argv[1])
    num_employee = int(sys.argv[2])
    num_turno = 3
 
    all_employee = range(num_employee)
    all_turno = range(num_turno)
    all_dias = range(num_dias)

    #shift_requests = [  [[0, 0, 1], [0, 0, 1], [0, 0, 1]],
    #                    
    #                    [[LUNES , 0..3]], [1, 0, 0], [1, 0, 0]],
    #
    #                    [[0, 1, 0], [1, 0, 0], [1, 0, 0]],
    #                    
    #                    [[0, 1, 0], [0, 1, 0], [0, 1, 0]]]

    # CREACIÓN DEL MODELO.
    model = cp_model.CpModel()

    # Se crea las variables para el turno
    # shifts[(n, d, s)]: nurse 'n' works shift 's' on day 'd'.
    shifts = {}
    for n in all_employee:
        for d in all_dias:
            for s in all_turno:
                shifts[(n, d, s)] = model.NewBoolVar('shift_n%id%is%i' % (n, d, s))

    # Cada turno es asignado a solo un empleado por día.  
    # (Esta restricción debe depender según la cantidad de aviones que llegue a ese turno con al menos una diferencia de 20 minutos.)    
    for d in all_dias:
        model.Add(sum(shifts[(n, d, 0)] for n in all_employee)>=1)
        model.Add(sum(shifts[(n, d, 1)] for n in all_employee)>=1)
        model.Add(sum(shifts[(n, d, 2)] for n in all_employee)>=1)

    # Cada empleado trabaja como máximo un turno por día. (Puede ser 0 porque puede tener el día libre al ser solo 3 turnos)
    for n in all_employee:
        for d in all_dias:
            for s in all_turno:
                #print(shifts[(n,d,s)])
                model.AddAtMostOne(shifts[(n, d, s)] for s in all_turno)
        
    # Distribuye los turno de maneraz uniforme para cada empleado
    min_shifts_per_employee = ((num_turno) * num_dias) // num_employee
    if num_turno * num_dias % num_employee == 0:
        max_shifts_per_employee = min_shifts_per_employee
    else:
        max_shifts_per_employee = min_shifts_per_employee + 1
    for n in all_employee:
        num_turno_worked = []
        for d in all_dias:
            for s in all_turno:
                num_turno_worked.append(shifts[(n, d, s)])
        model.Add(min_shifts_per_employee <= sum(num_turno_worked))
        model.Add(sum(num_turno_worked) <= max_shifts_per_employee)

    #model.Maximize(
    #    sum(shift_requests[n][d][s] * shifts[(n, d, s)] for n in all_employee
    #        for d in all_dias for s in all_turno))

    
    # Crea el solver y la solución
    solver = cp_model.CpSolver()
    solver.parameters.linearization_level = 0

    # Enumera todas las soluciones encontradas
    solver.parameters.enumerate_all_solutions = True


    class NursesPartialSolutionPrinter(cp_model.CpSolverSolutionCallback):
        """Print intermediate solutions."""

        def __init__(self, number ,shifts, num_employee, num_dias, num_turno, limit):
            cp_model.CpSolverSolutionCallback.__init__(self)
            self._number = number
            self._shifts = shifts
            self._num_employee = num_employee
            self._num_dias = num_dias
            self._num_turno = num_turno
            self._solution_count = 0
            self._solution_limit = limit

        def on_solution_callback(self):
            self._solution_count += 1

            if(self._solution_count == self._number):
                array=[]
                json_grande={}
                json = {}
    
                for d in range(self._num_dias):
                    json={}
                    print("Día %i" % (d+1))
                    for n in range(self._num_employee):
                        is_working = False
                        for s in range(self._num_turno):
                            if self.Value(self._shifts[(n, d, s)]):
                                is_working = True
                                json["empleado_"+str(int(n)+1)] = s+1
                                print('  Nurse %i works shift %i' % (n, s))

                        if not is_working:
                            json["empleado_"+str(int(n)+1)] = 0
                            print('  Nurse {} does not work'.format(n))

                    array.append(json)
                
                json_grande = array
                #print(json_grande)
            
            if self._solution_count >= self._solution_limit:
                self.StopSearch()    

        def solution_count(self):
            return self._solution_count

    # Límite de cantidad de soluciones
    solution_limit = 100
    solution_number = random.randint(1,solution_limit)
    solution_printer = NursesPartialSolutionPrinter(solution_number,shifts, num_employee,
                                                    num_dias, num_turno,
                                                    solution_limit)

        

    solver.Solve(model, solution_printer)

    # Statistics.
    print('\nStatistics')
    print('  - conflicts      : %i' % solver.NumConflicts())
    print('  - branches       : %i' % solver.NumBranches())
    print('  - wall time      : %f s' % solver.WallTime())
    print('  - solutions found: %i' % solution_printer.solution_count())

main()