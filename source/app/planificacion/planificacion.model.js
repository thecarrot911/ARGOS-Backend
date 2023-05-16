const Actualizacion = require("../../class/actualizacion.class");
const Planificacion = require("../../class/planificacion.class");
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

      for(let i=0;i<ListaPlanificacionAnualItinerario.length;i++){
            for(let j=0;j<ListaEstadistica.length;j++){
                  if(ListaEstadistica[j].month == ListaPlanificacionAnualItinerario[i].mes){
                        ListaPlanificacionAnualItinerario[i]["estadistica"] = ListaEstadistica[j]
                  }
            }
      }

      return ListaPlanificacionAnualItinerario;
};

const AniosPlanificacion = async() =>{
      const DatosPlanificacionesAnuales = await Planificacion.Anuales();
      return await planificacionHelper.GenerarPlanificacionesAnuales(DatosPlanificacionesAnuales);
};

module.exports.planificacionModel = {
      GenerarPlanificacion,
      UltimaPlanificacion,
      MostrarPlanificaciones,
      AniosPlanificacion
};