const conexion = require("../database");

const imgAuxiliar = "https://i.imgur.com/EBH7aDM.png";

class Empleado{
      constructor({nombre_paterno, nombre_materno, apellido_paterno, apellido_materno, rut}, imagen){
            this.nombre_paterno = nombre_paterno.charAt(0).toUpperCase() + nombre_paterno.slice(1).toLowerCase(),
            this.nombre_materno = nombre_materno.charAt(0).toUpperCase() + nombre_materno.slice(1).toLowerCase()
            this.apellido_paterno = apellido_paterno.charAt(0).toUpperCase() + apellido_paterno.slice(1).toLowerCase()
            this.apellido_materno = apellido_materno.charAt(0).toUpperCase() + apellido_materno.slice(1).toLowerCase()
            this.rut = rut,
            this.activo = true,
            this.imagen = imagen !== undefined ? `${process.env.HOST}/public/empleados/${imagen.filename}` : imgAuxiliar;
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
            if(BuscarEmpleado.length == 0) return true;
            else return false;
      };

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
                  DATE_FORMAT(c.fecha_emision, '%Y-%m-%d') fecha_emision,
                  DATE_FORMAT(c.fecha_vencimiento, '%Y-%m-%d') fecha_vencimiento,
                  c.tipo,
                  c.numero
            FROM empleado e
            LEFT JOIN credencial c ON e.rut = c.empleado_rut;
            `;
            return await conexion.query(sql_MostrarEmpleados);
      };
}

module.exports = Empleado;