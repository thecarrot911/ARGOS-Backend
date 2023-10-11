# ARGOS - BACKEND
Argos es un sistema web que se encarga de gestionar la información de los empleados de una empresa y de gestionar las planificaciones de turno que se vayan generando en el sistema a través del tiempo. 
El subsistema que se encarga de generar las planificaciones de turno utiliza el enfoque [Constraint Satisfaction Problem (CSP)](https://es.wikipedia.org/wiki/Problema_de_satisfacci%C3%B3n_de_restricciones) y para darle solución utiliza el solucionador [CP-SAT](https://developers.google.com/optimization/cp) de [OR-Tools](https://developers.google.com/optimization).

Este sistema fue desarrollado bajo el marco operativo de una empresa real que se encarga de suministrar combustible a los aviones, por lo tanto existen ciertas condiciones y restricciones que el sistema cumple para generar las planificaciones de turno, estas son:

**Condiciones:**
* Son 3 turnos al día.
* Son 5 empleados para distribución de los turnos.

**Restricciones:**
1. Cada empleado trabaja como máximo un turno al día.
2. Un empleado que sea asignado en el turno de las 23:00 a 07:00 no puede ser asignado al día siguiente en el turno 07:00 a 15:00.
3. Cada turno debe tener como mínimo un empleado al día.
4. Cada empleado tiene un día libre a la semana (la semana no incluye los domingos).
5. Cada empleado tiene dos domingos libres al mes.
6. Se debe asignar una cantidad determinada de empleados a un turno específico en un día, según lo que indique el itinerario.
7. Los empleados restantes que no hayan sido asignados a un turno (por la restricción 3 y 6) se distribuirán equitativamente desde el primer turno como prioridad seguido del segundo turno hasta el tercer turno.
8. Los meses que tengan cuatro domingos deben asignar a un empleado adicional (distinto de los cinco empleados) para trabajar en dos domingos en cualquier turno, a este último se le denominará como "comodín".
9. La carga de trabajo de los empleados debe ser distribuida lo más equitativamente posible para cada turno.



