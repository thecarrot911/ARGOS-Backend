const conexion = require("../database");

class Empleado{
      constructor({nombre_paterno, nombre_materno, apellido_paterno, apellido_materno, rut}, imagen){
            this.nombre_paterno = nombre_paterno.charAt(0).toUpperCase() + nombre_paterno.slice(1).toLowerCase(),
            this.nombre_materno = nombre_materno.charAt(0).toUpperCase() + nombre_materno.slice(1).toLowerCase()
            this.apellido_paterno = apellido_paterno.charAt(0).toUpperCase() + apellido_paterno.slice(1).toLowerCase()
            this.apellido_materno = apellido_materno.charAt(0).toUpperCase() + apellido_materno.slice(1).toLowerCase()
            this.rut = rut,
            this.activo = true,
            this.imagen = imagen
      };

      Registrar = async() =>{ 
            const sql_RegistrarEmpleado = `
            INSERT INTO empleado (rut, nombre_paterno, nombre_materno, apellido_paterno, apellido_materno, activo, imagen)
            VALUES ('${this.rut}', '${this.nombre_paterno}', '${this.nombre_materno}', '${this.apellido_paterno}', '${this.apellido_materno}', ${this.activo}, '${this.imagen}')
            `;
            return await conexion.query(sql_RegistrarEmpleado)
      };

      Buscar = async() =>{
            const sql_BuscarEmpleado = `
            SELECT * FROM empleado WHERE rut = '${this.rut}'`;
            const BuscarEmpleado = await conexion.query(sql_BuscarEmpleado);
            let existe = false
            if(BuscarEmpleado.length == 0) existe = true;
            return {existe, BuscarEmpleado}
      };

      Reactivar = async () =>{
            const stringSQLEmpleado = `
            UPDATE empleado 
                  SET   activo = 1,
                        nombre_paterno = '${this.nombre_paterno}',
                        nombre_materno = '${this.nombre_materno}',
                        apellido_paterno = '${this.apellido_paterno}',
                        apellido_materno = '${this.apellido_materno}'
            WHERE rut='${this.rut}';`;
            return await conexion.query(stringSQLEmpleado);
      }

      Modificar = async () =>{
            const sql = `
            UPDATE empleado
            SET   nombre_paterno = '${this.nombre_paterno}',
                  nombre_materno = '${this.nombre_materno}',
                  apellido_paterno = '${this.apellido_paterno}',
                  apellido_materno = '${this.apellido_materno}',
                  imagen = '${this.imagen}'
            WHERE rut = '${this.rut}'`;
            return await conexion.query(sql);
      };

      static Buscar = async(rut)=>{
            const sql = `SELECT * FROM empleado WHERE rut = '${rut}';`;
            const empleado = await conexion.query(sql);
            let existe = false;
            if(empleado.length == 0) existe = true;
            return {existe, empleado}
      }

      static MostrarTodos = async() =>{
            const sql_MostrarEmpleados = `
            SELECT
            e.rut,
            e.nombre_paterno,
            e.nombre_materno,
            e.apellido_paterno,
            e.apellido_materno,
            e.imagen,
            c.credencial_id,
            DATE_FORMAT(c.fecha_vencimiento, '%d-%m-%Y') fecha_vencimiento,
            c.tipo,
            c.numero,
            (SELECT 
            CASE
                  WHEN DATEDIFF(c.fecha_vencimiento, CURDATE()) < 0 THEN 1
                  WHEN c.fecha_vencimiento <= DATE_ADD(CURDATE(), INTERVAL 1 MONTH) THEN 1
                  ELSE 0
            END
            FROM credencial
            WHERE e.rut = empleado_rut
            LIMIT 1) AS vence
            FROM empleado e
            LEFT JOIN credencial c ON e.rut = c.empleado_rut
            WHERE e.activo = 1;
            `;
            return await conexion.query(sql_MostrarEmpleados);
      };

      static Perfil = async() =>{
            const sql = `
            SELECT empleado.rut, nombre_paterno, nombre_materno, apellido_paterno, apellido_materno,
                  activo, imagen, planificacion.planificacion_id, planificacion.month, planificacion.year,
                  SUM(CASE WHEN dia.feriado = 1 AND (turno.turno = 1 OR turno.turno = 2 OR turno.turno = 3) THEN 1 ELSE 0 END) AS feriado,
                  SUM(CASE WHEN turno.turno = 0 THEN 1 ELSE 0 END) AS libre,
                  SUM(CASE WHEN turno.turno = 1 THEN 1 ELSE 0 END) AS turno1,
                  SUM(CASE WHEN turno.turno = 2 THEN 1 ELSE 0 END) AS turno2,
                  SUM(CASE WHEN turno.turno = 3 THEN 1 ELSE 0 END) AS turno3,
                  horario.turno1 AS horario1,
                  horario.turno2 AS horario2,
                  horario.turno3 AS horario3
            FROM planificacion
                  INNER JOIN dia ON planificacion.planificacion_id = dia.planificacion_id
                  INNER JOIN horario ON horario.planificacion_id = planificacion.planificacion_id
                  INNER JOIN turno ON dia.id = turno.dia_id
                  INNER JOIN turno_dia ON turno.id = turno_dia.turno_id
                  INNER JOIN empleado ON turno_dia.empleado_rut = empleado.rut
            GROUP BY empleado.rut, nombre_paterno, nombre_materno, apellido_paterno, apellido_materno,
                  activo, imagen, planificacion.planificacion_id, planificacion.month, planificacion.year,
                  horario.turno1, horario.turno2, horario.turno3
            ORDER BY planificacion.year DESC,
                  CASE planificacion.month
                        WHEN 'enero' THEN 1
                        WHEN 'febrero' THEN 2
                        WHEN 'marzo' THEN 3
                        WHEN 'abril' THEN 4
                        WHEN 'mayo' THEN 5
                        WHEN 'junio' THEN 6
                        WHEN 'julio' THEN 7
                        WHEN 'agosto' THEN 8
                        WHEN 'septiembre' THEN 9
                        WHEN 'octubre' THEN 10
                        WHEN 'noviembre' THEN 11
                        WHEN 'diciembre' THEN 12
                  END ASC;
            `;
            return await conexion.query(sql);
      };
}

module.exports = Empleado;