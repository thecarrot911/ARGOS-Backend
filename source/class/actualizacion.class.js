const conexion = require("../database");

class Actualizacion{
      constructor({rut,planificacion_id,descripcion,fecha_inicio,fecha_termino,tipo_id, reemplazo}){
            (this.rut = rut),
            (this.planificacion_id = planificacion_id),
            (this.descripcion = descripcion),
            (this.fecha_inicio = fecha_inicio),
            (this.fecha_termino = fecha_termino),
            (this.tipo_id = parseInt(tipo_id)),
            (this.reemplazo = reemplazo);
      };

      Registrar = async() =>{
            const sql = `
            INSERT INTO actualizacion(rut, planificacion_id, descripcion, fecha_inicio, fecha_termino, tipo_id, reemplazo)
            VALUES ('${this.rut}',${this.planificacion_id},'${this.descripcion}','${this.fecha_inicio}','${this.fecha_termino}',${this.tipo_id},'${this.reemplazo}');
            `;
            return await conexion.query(sql);
      };

      ObtenerPlanificacion = async() =>{
            const sql = `
            SELECT * FROM planificacion
            INNER JOIN dia ON planificacion.planificacion_id =  dia.planificacion_id
            INNER JOIN turno ON dia.id = turno.dia_id
            INNER JOIN turno_dia ON turno.id = turno_dia.turno_id
            INNER JOIN empleado ON turno_dia.empleado_rut = empleado.rut
            WHERE planificacion.planificacion_id = ${this.planificacion_id};`;
            return await conexion.query(sql)
      };


      CambioTurno = async(planificacion, empleado) =>{
            let valuesTurnoDia = []
            planificacion.forEach(dia => {
                  const indice = dia.empleados.findIndex(emp => emp.rut == this.rut)
                  if(indice !== -1){
                        valuesTurnoDia.push([dia.empleados[indice].turno_id, empleado[0].rut ])
                  }
            });

            return valuesTurnoDia;
      };

      Permiso = async() =>{

      };

      ModificarPlanificacion = async(valuesTurnoDia)=>{
            const sql = `
                  UPDATE turno_dia
                  SET empleado_rut = CASE turno_id
                        ${valuesTurnoDia.map(([turno_id, empleado_rut])=> `WHEN ${turno_id} THEN '${empleado_rut}'`).join(' ')}
                        ELSE empleado_rut
                  END
                  WHERE turno_id IN (${valuesTurnoDia.map(([turno_id])=> turno_id).join(', ')})`;
            return await conexion.query(sql)
      }
      
      static MostrarTipo = async() =>{
            const sql_MostrarTipo = `SELECT * FROM tipo`;
            return await conexion.query(sql_MostrarTipo);
      };

      static MostrarActualizacion = async(planificacion_id) =>{
            const sql = `SELECT
            id,
            rut,
            planificacion_id,
            descripcion,
            DATE_FORMAT(fecha_inicio, '%Y-%m-%d') fecha_inicio,
            DATE_FORMAT(fecha_termino, '%Y-%m-%d') fecha_termino,
            tipo_id,
            reemplazo
            FROM actualizacion  WHERE planificacion_id = ${planificacion_id};`;
            return await conexion.query(sql);
      };

      static MostrarSolicitante = async(planificacion_id) =>{
            const sql = `
            SELECT 
            empleado_rut rut, 
            nombre_paterno, 
            nombre_materno, 
            apellido_paterno, 
            apellido_materno 
            FROM planificacion AS planificacion
                  INNER JOIN dia AS dia ON planificacion.planificacion_id =  dia.planificacion_id
                  INNER JOIN turno AS turno ON dia.id = turno.dia_id
                  INNER JOIN turno_dia AS turno_dia ON turno.id = turno_dia.turno_id
                  INNER JOIN empleado AS empleado ON turno_dia.empleado_rut = empleado.rut
            WHERE planificacion.planificacion_id = ${planificacion_id}
            GROUP BY empleado_rut;
            `;
            return await conexion.query(sql)
      }
}

module.exports = Actualizacion;