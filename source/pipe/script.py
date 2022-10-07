import sys
from ortools.sat.python import cp_model

# Sistema de turno operacionales
#
# Restricciones
#-1.    Cada trabajador durante la semana tiene 1 día libre.
#-2.    Los trabajadores durante el mes de trabajo deben tener 2 domingos libres.
#-3.    En caso de que dos o más aviones de las líneas áreas SKY, LATAM y JETSMART lleguen a la misma hora o con una diferencia de menos de 20 minutos 
#       a reabastecerse de combustible, es necesario tener la misma cantidad de empleados que de aviones para ese turno.
#       _________________________
#      | Turno 1: 7:00 - 15:00;  |
#      | Turno 2: 15:00 - 23:00; | 
#      | Turno 3: 23:00 - 07:00; |
#      |_________________________|
#
#-4.    En la empresa hay 5 empleados para la distribución de los turnos.
#-5.    La carga de trabajo de los empleados debe ser equilibrada en base a: 
#-5.1.      Cantidad de aviones que atiende.  
#-5.2.      Cantidad de turnos que tiene. 

# Restricciones incorporadas
#-4.   En la empresa hay 5 empleados para la distribución de los turnos.
#-5.   La carga de trabajo de los empleados debe ser equilibrada en base a: 
#-5.2.      Cantidad de turnos que tiene. 


def main():
    # Data.
    num_dias = int(sys.argv[1])
    num_turno = int(sys.argv[2])
    num_employee = int(sys.argv[3])

    #num_freeday = 1 # On week
 
    all_employee = range(num_employee)
    all_turno = range(num_turno)
    all_dias = range(num_dias)

    # CREACIÓN DEL MODELO.
    model = cp_model.CpModel()

    # Se crea las variables para el turno
    # shifts[(n, d, s)]: nurse 'n' works shift 's' on day 'd'.
    shifts = {}
    for n in all_employee:
        for d in all_dias:
            for s in all_turno:
                shifts[(n, d,
                        s)] = model.NewBoolVar('shift_n%id%is%i' % (n, d, s))

    # Cada turno es asignado a solo un empleado por día.  
    # (Esta restricción debe depender según la cantidad de aviones que llegue a ese turno con al menos una diferencia de 20 minutos.)    
    for d in all_dias:
        for s in all_turno:
            model.AddExactlyOne(shifts[(n, d, s)] for n in all_employee)

    # Cada empleado trabaja como máximo un turno por día. (Puede ser 0 porque puede tener el día libre al ser solo 3 turnos)
    for n in all_employee:
        for d in all_dias:
            model.AddAtMostOne(shifts[(n, d, s)] for s in all_turno)
    
    
        
    
    # Distribuye los turno de maneraz uniforme para cada empleado
    min_shifts_per_employee = (num_turno * num_dias) // num_employee
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

    # Crea el solver y la solución
    solver = cp_model.CpSolver()
    solver.parameters.linearization_level = 0
    # Enumera todas las soluciones encontradas
    solver.parameters.enumerate_all_solutions = True


    class NursesPartialSolutionPrinter(cp_model.CpSolverSolutionCallback):
        """Print intermediate solutions."""

        def __init__(self, shifts, num_employee, num_dias, num_turno, limit):
            cp_model.CpSolverSolutionCallback.__init__(self)
            self._shifts = shifts
            self._num_employee = num_employee
            self._num_dias = num_dias
            self._num_turno = num_turno
            self._solution_count = 0
            self._solution_limit = limit

        def on_solution_callback(self):
            self._solution_count += 1
            print('Solution %i' % self._solution_count)
            for d in range(self._num_dias):
                print('Day %i' % d)
                for n in range(self._num_employee):
                    is_working = False
                    for s in range(self._num_turno):
                        if self.Value(self._shifts[(n, d, s)]):
                            is_working = True
                            print('  employee %i works shift %i' % (n, s))         
                    if not is_working:
                        print('  employee {} does not work'.format(n))
            if self._solution_count >= self._solution_limit:
                #print('Stop search after %i solutions' % self._solution_limit)
                self.StopSearch()

        def solution_count(self):
            return self._solution_count

    # Display the first five solutions.
    solution_limit = 1
    solution_printer = NursesPartialSolutionPrinter(shifts, num_employee,
                                                    num_dias, num_turno,
                                                    solution_limit)

    solver.Solve(model, solution_printer)

    # Statistics.
    #print('\nStatistics')
    #print('  - conflicts      : %i' % solver.NumConflicts())
    #print('  - branches       : %i' % solver.NumBranches())
    #print('  - wall time      : %f s' % solver.WallTime())
    #print('  - solutions found: %i' % solution_printer.solution_count())

main()