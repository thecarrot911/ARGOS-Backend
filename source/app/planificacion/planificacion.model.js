const Planificacion = require("../../class/planificacion.class");
const { planificacionHelper } = require("../../helper/planificacion.helper");

const GenerarPlanificacion = async(DatosPlanificacion) =>{
      
      const planificacion = new Planificacion(DatosPlanificacion);
      let planificacionAnterior = await planificacion.PlanificacionDelMesAnterior();
      planificacionAnterior = await planificacionHelper.GenerarListaPlanificacion(planificacionAnterior);
      
      if (planificacionAnterior.length != 0){
            const UltimaSemanaAnterior = await planificacionHelper.ObtenerUltimaSemanaDelMes(planificacionAnterior)
            const planificacionMensual =  await planificacion.GenerarPlanificacion(UltimaSemanaAnterior);
            return planificacionMensual;

      }else{
            // NO HAY PLANIFICACION ANTERIOR
            const planificacionMensual = await planificacion.GenerarPlanificacion(null);
            return planificacionMensual;

      }

      //Guardar Planificación
      //const planificacion_id = await planificacion.GuardarPlanificacion();
      //const dia_id = await planificacion.GuardarDia(planificacionMensual, planificacion_id);
      //const turno_id = await planificacion.GuardarTurno(planificacionMensual, dia_id);
      //await planificacion.GuardarTurnoDia(planificacionMensual, turno_id);

      //return planificacionMensual;
      return planificacionMensual;
};

const UltimaPlanificacion = async() =>{
      const DatosPlanificacion = await Planificacion.MostrarUltima();
      const ListaPlanificacion =  await planificacionHelper.GenerarListaPlanificacion(DatosPlanificacion);
      const ListaOrdenadaPlanificacion = await planificacionHelper.OrdenarLista(ListaPlanificacion)
      const data = [{
            "anio":DatosPlanificacion[DatosPlanificacion.length-1].year,
            "mes":DatosPlanificacion[DatosPlanificacion.length-1].month,
            "id": DatosPlanificacion[DatosPlanificacion.length-1].planificacion_id,
            "planificacion": ListaOrdenadaPlanificacion
      }]
      return data;
};

module.exports.planificacionModel = {
      GenerarPlanificacion,
      UltimaPlanificacion
}