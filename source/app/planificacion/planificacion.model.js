const Actualizacion = require("../../class/actualizacion.class");
const Planificacion = require("../../class/planificacion.class");
const { actualizacionHelper } = require("../../helper/actualizacion.helper");
const { planificacionHelper } = require("../../helper/planificacion.helper");

const GenerarPlanificacion = async(DatosPlanificacion) =>{
      const planificacion = new Planificacion(DatosPlanificacion);

      let planificacionAnterior = await planificacion.PlanificacionDelMesAnterior();

      planificacionAnterior = await planificacionHelper.GenerarListaPlanificacion(planificacionAnterior);

      let planificacionMensual

      if (planificacionAnterior.length != 0){
            const UltimaSemanaAnterior = await planificacionHelper.ObtenerUltimaSemanaDelMes(planificacionAnterior)
            planificacionMensual =  await planificacion.GenerarPlanificacion(UltimaSemanaAnterior);

      }else{
            // NO HAY PLANIFICACION ANTERIOR
            planificacionMensual = await planificacion.GenerarPlanificacion(null);
      }
      
      //Guardar Planificación
      const planificacion_id = await planificacion.GuardarPlanificacion();
      await planificacion.GuardarHorario(planificacion_id);
      const dia_id = await planificacion.GuardarDia(planificacionMensual, planificacion_id);
      const turno_id = await planificacion.GuardarTurno(planificacionMensual, dia_id);
      await planificacion.GuardarItinerario(planificacionMensual, dia_id);
      await planificacion.GuardarTurnoDia(planificacionMensual, turno_id);
      return planificacionMensual;
};

const UltimaPlanificacion = async() =>{
      const DatosPlanificacion = await Planificacion.MostrarUltima();
      const ListaPlanificacion =  await planificacionHelper.GenerarListaPlanificacion(DatosPlanificacion);
      const ListaOrdenadaPlanificacion = await planificacionHelper.OrdenarLista(ListaPlanificacion)
      const Actualizaciones = await Actualizacion.MostrarActualizacion(DatosPlanificacion[DatosPlanificacion.length-1].planificacion_id);
      const data = [{
            "anio":DatosPlanificacion[DatosPlanificacion.length-1].year,
            "mes":DatosPlanificacion[DatosPlanificacion.length-1].month,
            "id": DatosPlanificacion[DatosPlanificacion.length-1].planificacion_id,
            "planificacion": ListaOrdenadaPlanificacion,
            "actualizacion": Actualizaciones
      }]
      return data;
};

const MostrarPlanificaciones = async(year) =>{
      // Planificación
      const DatosPlanificacionAnual = await Planificacion.Anual(year);
      const ListaPlanificacionAnual = await planificacionHelper.GenerarListaPlanificacionAnual(DatosPlanificacionAnual);

      // Itinerario
      const DatosItinerarioAnual = await Planificacion.Itinerario(year);
      const ListaPlanificacionAnualItinerario = await planificacionHelper.AgregarItinerarioAnual(DatosItinerarioAnual, ListaPlanificacionAnual)

      // Estadistica
      const DatosEstadisticasPlanificacion = await Planificacion.Estadistica(year);
      const ListaEstadistica = await planificacionHelper.GenerarPlanificacionesAnual(DatosEstadisticasPlanificacion);

      //Actualización
      const DatosActualizacionAnual = await Actualizacion.MostrarActualizacionAnual(year);
      const ListaActualizacion = await actualizacionHelper.GenerarListaActualizacion(DatosActualizacionAnual);

      //Horario
      const DatosHorariosAnual = await Planificacion.Horario(year);

      for(let i=0;i<ListaPlanificacionAnualItinerario.length;i++){
            for(let j=0;j<ListaEstadistica.length;j++){
                  if(ListaEstadistica[j].month == ListaPlanificacionAnualItinerario[i].mes){
                        ListaPlanificacionAnualItinerario[i]["estadistica"] = ListaEstadistica[j]
                  }
            }
      }

      for(let i=0;i<ListaPlanificacionAnualItinerario.length;i++){
            for(let j=0;j<ListaActualizacion.length;j++){
                  if(ListaActualizacion[j].mes == ListaPlanificacionAnualItinerario[i].mes){

                        ListaPlanificacionAnualItinerario[i]["actualizacion"] = ListaActualizacion[j].actualizacion
                        let values = ListaActualizacion[j].actualizacion.filter( actualizacion => actualizacion.tipo != "Observación" )
                        if(values.length > 0){
                              for (const actualizacion of values){
                                    let cambioPlanificacion = await Actualizacion.ObtenerCambioTurno(actualizacion.id)
                                    for(const dia of ListaPlanificacionAnualItinerario[i]["planificacion"]){
                                          for (const cambio of cambioPlanificacion) {
                                                for (const empleado of dia.empleados) {
                                                      if(cambio.id_turno == empleado.turno_id){
                                                            for(const emp of ListaPlanificacionAnualItinerario[i]["estadistica"].empleados){
                                                                  if(emp.rut == empleado.rut){
                                                                        if(empleado.turno == 1){
                                                                              emp.turno1 = emp.turno1 - 1
                                                                        }else if(empleado.turno == 2){
                                                                              emp.turno2 = emp.turno2 - 1
                                                                        }else{
                                                                              emp.turno3 = emp.turno3 - 1
                                                                        }
                                                                  }
                                                            }
                                                            empleado.turno = cambio.turno
                                                      }
                                                }
                                          }
                                    }
                              }
                        }
                  }
            }
      }

      for(let i=0;i<ListaPlanificacionAnualItinerario.length;i++){
            for (let j = 0; j < DatosHorariosAnual.length; j++) {
                  if(ListaPlanificacionAnualItinerario[i].mes == DatosHorariosAnual[j].month){
                        ListaPlanificacionAnualItinerario[i]["horario"] = DatosHorariosAnual[j]
                  }
            }
      }

      return ListaPlanificacionAnualItinerario;
};

const AniosPlanificacion = async() =>{
      const DatosPlanificacionesAnuales = await Planificacion.Anuales();
      return await planificacionHelper.GenerarPlanificacionesAnuales(DatosPlanificacionesAnuales);
};

const EliminarPlanificacion = async(planificacion) =>{

      await Planificacion.EliminarActualizacion(planificacion.actualizacion)
      await Planificacion.EliminarHorario(planificacion.planificacion_id)
      return await Planificacion.EliminarPlanificacion(planificacion);
};

module.exports.planificacionModel = {
      GenerarPlanificacion,
      UltimaPlanificacion,
      MostrarPlanificaciones,
      AniosPlanificacion,
      EliminarPlanificacion
};