const conexion = require("../database");

class Actualizacion{
      constructor({rut,planificacion_id,descripcion,fecha,fecha_inicio,fecha_termino,tipo_id, reemplazo}){
            (this.rut = rut),
            (this.planificacion_id = planificacion_id),
            (this.descripcion = descripcion),
            (this.fecha = fecha),
            (this.fecha_inicio = fecha_inicio),
            (this.fecha_termino = fecha_termino),
            (this.tipo_id = parseInt(tipo_id)),
            (this.reemplazo = reemplazo);
      };

      Registrar = async() =>{
            const sql = `
            INSERT INTO actualizacion(rut, planificacion_id, descripcion, fecha, fecha_inicio, fecha_termino, tipo_id, reemplazo)
            VALUES ('${this.rut}',${this.planificacion_id},'${this.descripcion}','${this.fecha}','${this.fecha_inicio}','${this.fecha_termino}',${this.tipo_id},'${this.reemplazo}');
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

      Permiso = async(planificacion, id) =>{

            const fechaInicio = new Date(this.fecha_inicio);
            fechaInicio.setUTCHours(0, 0, 0, 0);
            const diaInicio = fechaInicio.getUTCDate();


            const fechaTermino = new Date(this.fecha_termino);
            fechaTermino.setUTCHours(0, 0, 0, 0);
            const diaTermino = fechaTermino.getUTCDate();

            const indiceFilter = planificacion.filter( dia => dia.dia_numero == parseInt(diaInicio))
            const indiceInicio = planificacion.indexOf(indiceFilter[0]);

            let CambiosPlanificacion = []

            // Acumulando los dias para modificar
            for(let i = indiceInicio; i<planificacion.length; i++){
                  CambiosPlanificacion.push(planificacion[i].empleados.filter(empleado => this.rut == empleado.rut)[0])
                  if(planificacion[i].dia_numero == parseInt(diaTermino)) break;
            }
            
            const registrarActualizacion = await this.Registrar();
            const actualizacionId = registrarActualizacion.insertId
            
           
            // Ingresando la planificación anterior
            const values = CambiosPlanificacion.map(dia => [dia.id, dia.turno, actualizacionId]);
            const sql = `INSERT INTO cambioturno(id_turno, turno, actualizacion_id) VALUES ?`;
            await conexion.query(sql, [values])

            // Cambiando al tipo de actualización
            for(const turno of CambiosPlanificacion) turno.turno=id;

            // Actualización de la planificación
            for(const dia of CambiosPlanificacion){
                  const sql = `UPDATE turno SET turno = ? WHERE id = ?`;
                  await conexion.query(sql, [dia.turno, dia.id]);
            }
            return;
      };

      static MostrarActualizacionAnual = async(year) =>{
            const sql = `
            SELECT
                  planificacion.month,
                  actualizacion.id id,
                  solicitante.rut solicitante_rut,
                  solicitante.nombre_paterno solicitante_nombre,
                  solicitante.apellido_paterno solicitante_apellido,
                  reemplazo.rut reemplazo_rut,
                  reemplazo.nombre_paterno reemplazo_nombre,
                  reemplazo.apellido_paterno reemplazo_apellido,
                  actualizacion.planificacion_id planificacion_id,
                  tipo.nombre tipo,
                  actualizacion.descripcion descripcion,
                  DATE_FORMAT(actualizacion.fecha, '%d-%m-%Y') fecha,
                  DATE_FORMAT(actualizacion.fecha_inicio, '%d-%m-%Y') fecha_inicio,
                  DATE_FORMAT(actualizacion.fecha_termino, '%d-%m-%Y') fecha_termino
            FROM actualizacion
                  INNER JOIN planificacion ON planificacion.planificacion_id = actualizacion.planificacion_id
                  INNER JOIN tipo ON tipo.id = actualizacion.tipo_id
                  INNER JOIN empleado AS solicitante ON solicitante.rut = actualizacion.rut 
                  INNER JOIN empleado AS reemplazo ON reemplazo.rut = actualizacion.reemplazo
            WHERE planificacion.year = ${year}
            UNION
            SELECT
                  planificacion.month,
                  actualizacion.id id,
                  solicitante.rut solicitante_rut,
                  solicitante.nombre_paterno solicitante_nombre,
                  solicitante.apellido_paterno solicitante_apellido,
                  NULL AS reemplazo_rut,
                  NULL AS reemplazo_nombre,
                  NULL AS reemplazo_apellido,
                  actualizacion.planificacion_id AS planificacion_id,
                  tipo.nombre tipo,
                  actualizacion.descripcion descripcion,
                  DATE_FORMAT(actualizacion.fecha, '%d-%m-%Y') fecha,
                  NULL AS fecha_inicio,
                  NULL AS fecha_termino
            FROM actualizacion 
            INNER JOIN planificacion ON planificacion.planificacion_id = actualizacion.planificacion_id
            INNER JOIN tipo ON tipo.id = actualizacion.tipo_id
            INNER JOIN empleado AS solicitante ON solicitante.rut = actualizacion.rut 
            WHERE planificacion.year = ${year} and actualizacion.tipo_id = ${4}
            ORDER BY id DESC;`;
            return await conexion.query(sql)
      };

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
            DATE_FORMAT(fecha_inicio, '%d-%m-%Y') fecha_inicio,
            DATE_FORMAT(fecha_termino, '%d-%m-%Y') fecha_termino,
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

      static MostrarCambioAnterior = async(id) =>{
            const sql = `SELECT * FROM cambioturno WHERE actualizacion_id = ${id}`;
            return await conexion.query(sql)
      };

      static RestablecerTurnoAnterior = async(CambiosAnterior) =>{
            for(const dia of CambiosAnterior){
                  const sql = `UPDATE turno SET turno = ? WHERE id = ?;`;
                  await conexion.query(sql, [dia.turno, dia.id_turno]);
            }
            return;
      };

      static EliminarCambioTurno = async(CambiosAnterior) =>{
            for(const dia of CambiosAnterior){
                  const sql = `DELETE FROM cambioturno WHERE id = ${dia.id}`;
                  await conexion.query(sql)
            }
            return;
      };

      static Eliminar = async(id) =>{
            const sql = `DELETE FROM actualizacion WHERE id = ${id}`;
            return await conexion.query(sql);
      };

      Observacion = async()=>{
            const sql = `
            INSERT INTO actualizacion(rut, planificacion_id, tipo_id, descripcion, fecha)
            VALUES('${this.reemplazo}',${this.planificacion_id},${this.tipo_id},'${this.descripcion}','${this.fecha}');`;
            return await conexion.query(sql);
      };
}

module.exports = Actualizacion;