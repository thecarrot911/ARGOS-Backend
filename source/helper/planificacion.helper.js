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
      OrdenarLista
};