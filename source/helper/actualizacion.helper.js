const GenerarListaActualizacion = async(DatosActualizacionAnual) =>{
      const ActualizacionAnual = DatosActualizacionAnual.reduce((mes, actual) =>{
            mes[actual.month] = mes[actual.month] || {
                  mes: actual.month,
                  actualizacion: []
            };

            mes[actual.month].actualizacion.push({
                  id: actual.id,
                  solicitante_rut: actual.solicitante_rut,
                  solicitante_nombre: actual.solicitante_nombre,
                  solicitante_apellido: actual.solicitante_apellido,
                  reemplazo_rut: actual.reemplazo_rut,
                  reemplazo_nombre: actual.reemplazo_nombre,
                  reemplazo_apellido: actual.reemplazo_apellido,
                  planificacion_id: actual.planificacion_id,
                  tipo: actual.tipo,
                  fecha: actual.fecha,
                  descripcion: actual.descripcion,
                  fecha_inicio: actual.fecha_inicio,
                  fecha_termino: actual.fecha_termino,
            });
            return mes
      },[]);
      return Object.values(ActualizacionAnual)
};

module.exports.actualizacionHelper = {
      GenerarListaActualizacion
}