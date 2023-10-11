# ARGOS - BACKEND
Argos es un sistema web que se encarga de gestionar la información de los empleados de una empresa y de gestionar las planificaciones de turno que se vayan generando en el sistema a través del tiempo. 
El subsistema que se encarga de generar las planificaciones de turno utiliza el enfoque [Constraint Satisfaction Problem (CSP)](https://es.wikipedia.org/wiki/Problema_de_satisfacci%C3%B3n_de_restricciones) y para dar solución a este problema utiliza el Solver [CP-SAT](https://developers.google.com/optimization/cp) de [OR-Tools](https://developers.google.com/optimization).
Este sistema fue desarrollado bajo el marco operativo de una empresa real que se encarga de suministrar combustible a los aviones, por lo tanto existen ciertas condiciones y restricciones que el sistema debe cumplir para generar las planificaciones de turno, estas son:

### Condiciones

### Restricciones

