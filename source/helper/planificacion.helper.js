const GenerarListaPlanificacion = async(datosPlanificacion) => {
      const planificacion = datosPlanificacion.reduce((empleado, actual)=>{
            empleado[actual.dia_id] = empleado[actual.dia_id] || {
                  dia_semana: actual.dia_semana,
                  dia_numero: actual.dia_numero,
                  feriado: actual.feriado,
                  empleados: []
            };
            empleado[actual.dia_id].empleados.push({
                  rut: actual.rut,
                  nombre: actual.nombre_paterno,
                  apellido: actual.apellido_paterno,
                  turno: actual.turno
            });
            return empleado;
      },[]);
      return Object.values(planificacion);
};

const OrdenarLista = async(ListaPlanificacion) =>{
      ListaPlanificacion.forEach((dia) => {
            dia.empleados.sort((a, b) => a.turno - b.turno);
      });
      return ListaPlanificacion
};


const ObtenerMes = async(indice) =>{
      const meses=[   "Enero","Febrero","Marzo","Abril",
                        "Mayo","Junio","Julio","Agosto",
                        "Septiembre","Octubre","Noviembre","Diciembre"
                  ]
      return meses[indice - 1];
};

module.exports.planificacionHelper = {
      GenerarListaPlanificacion,
      ObtenerMes,
      OrdenarLista
};