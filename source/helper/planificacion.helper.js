const GenerarListaPlanificacion = async(datosPlanificacion) => {
      const planificacion = datosPlanificacion.reduce((empleado, actual)=>{
            empleado[actual.dia_id] = empleado[actual.dia_id] || {
                  dia_semana: actual.dia_semana,
                  dia_numero: actual.dia_numero,
                  dia_id: actual.dia_id,
                  feriado: actual.feriado,
                  empleados: []
            };
            empleado[actual.dia_id].empleados.push({
                  rut: actual.rut,
                  nombre: actual.nombre_paterno,
                  apellido: actual.apellido_paterno,
                  turno: actual.turno,
                  turno_id: actual.turno_id
            });
            return empleado;
      },[]);
      return Object.values(planificacion);
};

const GenerarListaPlanificacionAnual = async (datosPlanificacionAnual) => {
      const planificacionAnual = datosPlanificacionAnual.reduce((mes, actual) => {
            mes[actual.planificacion_id] = mes[actual.planificacion_id] || {
                  mes: actual.month,
                  planificacion_id: actual.planificacion_id,
                  anio: actual.year,
                  planificacion: []
            };
            mes[actual.planificacion_id].planificacion.push({
                  dia_numero: actual.dia_numero,
                  dia_semana: actual.dia_semana,
                  feriado: actual.feriado,
                  dia_id: actual.dia_id,
                  turno: actual.turno,
                  turno_id: actual.turno_id,
                  rut: actual.rut,
                  nombre: actual.nombre_paterno,
                  apellido: actual.apellido_paterno

            });
            return mes;
      }, []);

      Object.values(planificacionAnual).forEach((planificacion) => {
            const diasAgrupados = planificacion.planificacion.reduce((dias, actual) => {
                  dias[actual.dia_id] = dias[actual.dia_id] || {
                        dia_numero: actual.dia_numero,
                        dia_semana: actual.dia_semana,
                        feriado: actual.feriado,
                        dia_id: actual.dia_id,
                        empleados: []
                  };
                  dias[actual.dia_id].empleados.push({
                        rut: actual.rut,
                        nombre: actual.nombre,
                        apellido: actual.apellido,
                        turno: parseInt(actual.turno),
                        turno_id: actual.turno_id
                  });
                  dias[actual.dia_id].empleados.sort((a, b) => a.turno - b.turno);
                  return dias;
            }, {});

            planificacion.planificacion = Object.keys(diasAgrupados).map((dia_numero) => {
                  return diasAgrupados[dia_numero]
            });
      });

      return Object.values(planificacionAnual);
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

const ObtenerUltimaSemanaDelMes = async(planificacion) =>{
      const UltimaSemana = []
      for(let i=planificacion.length-1; i>=0; i--){
            for(let e=0;e<planificacion[i].empleados.length;e++){
                  UltimaSemana.push([
                        planificacion[i].dia_numero,
                        planificacion[i].empleados[e].rut,
                        parseInt(planificacion[i].empleados[e].turno),
                  ]);
            }
            if(planificacion[i].dia_semana == "Lunes") break;
      }
      
      const UltimaSemanaAgrupado = UltimaSemana.reduce((dia, elemento) => {
            const clave = elemento[0]
            if(!dia[clave]){
                  dia[clave] = []
            }
            dia[clave].push(elemento);
            return dia
      }, {});

      return Object.values(UltimaSemanaAgrupado);
};


module.exports.planificacionHelper = {
      GenerarListaPlanificacion,
      ObtenerUltimaSemanaDelMes,
      ObtenerMes,
      OrdenarLista,
      GenerarListaPlanificacionAnual
};