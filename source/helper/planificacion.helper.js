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
                  id: actual.id,
                  turno: actual.turno,
                  turno_id: actual.turno_id
            });
            return empleado;
      },[]);
      return Object.values(planificacion);
};

const GenerarPlanificacionesAnual = async(datosEstadisticasPlanificacion) => {
      let estadistica = datosEstadisticasPlanificacion.reduce((mes, actual) =>{
            mes[actual.month] = mes[actual.month] || {
                  month: actual.month,
                  empleados: []
            }

            mes[actual.month].empleados.push({
                  rut: actual.rut,
                  nombre_paterno: actual.nombre_paterno,
                  apellido_paterno: actual.apellido_paterno,
                  imagen: actual.imagen,
                  feriado: actual.feriado,
                  libre: actual.libre,
                  turno1: actual.turno1,
                  turno2: actual.turno2,
                  turno3: actual.turno3
            });
            return mes
      },[]);
      return Object.values(estadistica)
};

const AgregarItinerarioAnual = async (DatosItinerarioAnual, ListaPlanificacionAnual) => {
      let itinerario = DatosItinerarioAnual.reduce((mes, actual) => {
            mes[actual.month] = mes[actual.month] || {
                  mes: actual.month,
                  itinerario: []
            };
            
            mes[actual.month].itinerario.push({
                  dia_semana: actual.dia_semana,
                  dia_numero: actual.dia_numero,
                  turno: actual.turno,
                  falta: actual.empleado_faltante
            });
            return mes
      },[]);

      itinerario = Object.values(itinerario);

      for(const mes of ListaPlanificacionAnual){
            for(const iti of itinerario){
                  if(iti.mes == mes.mes){
                        for(const dia of mes.planificacion){
                              dia.itinerario = []
                              for(const diaIti of iti.itinerario){
                                    if(dia.dia_semana == diaIti.dia_semana && dia.dia_numero == diaIti.dia_numero){
                                          dia.itinerario.push({
                                                "turno": diaIti.turno,
                                                "falta": diaIti.falta
                                          });
                                    };
                              };
                        };
                  };
            };
      };

      return ListaPlanificacionAnual;
};

const GenerarPlanificacionesAnuales = async (datosPlanificacionesAnuales) => {
      let planificacion = datosPlanificacionesAnuales.reduce((anio, actual) => {
            anio[actual.year] = anio[actual.year] || {
                  year: actual.year,
                  months: [],
            };
            anio[actual.year].months.push({
                  month: actual.month,
                  id: actual.planificacion_id,
            });
            return anio;
      },[]);
      planificacion = Object.values(planificacion);
      return planificacion.sort((obj1, obj2) => obj2.year - obj1.year);
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
                  comodin: parseInt(actual.comodin),
                  dia_id: actual.dia_id,
                  turno: actual.turno,
                  turno_id: actual.turno_id,
                  rut: actual.rut,
                  nombre: actual.nombre_paterno,
                  apellido: actual.apellido_paterno

            });
            return mes;
      }, []);

      // Definir el orden de los meses
      const ordenMeses = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio',
                        'Agosto','Septiembre','Octubre','Noviembre','Diciembre'];

      // Ordenar por mes utilizando la función de comparación personalizada
      planificacionAnual.sort((a, b) => {
      const indexA = ordenMeses.findIndex((mes) => mes.toLowerCase() === a.mes.toLowerCase());
      const indexB = ordenMeses.findIndex((mes) => mes.toLowerCase() === b.mes.toLowerCase());
      return indexA - indexB;
      });

      Object.values(planificacionAnual).forEach((planificacion) => {
            const diasAgrupados = planificacion.planificacion.reduce((dias, actual) => {
                  dias[actual.dia_id] = dias[actual.dia_id] || {
                        dia_numero: actual.dia_numero,
                        dia_semana: actual.dia_semana,
                        feriado: actual.feriado,
                        dia_id: actual.dia_id,
                        comodin: actual.comodin,
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
      GenerarPlanificacionesAnuales,
      ObtenerMes,
      OrdenarLista,
      GenerarListaPlanificacionAnual,
      GenerarPlanificacionesAnual,
      AgregarItinerarioAnual
};