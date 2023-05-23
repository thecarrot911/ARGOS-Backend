const Actualizacion = require("../../class/actualizacion.class");
const Empleado = require("../../class/empleado.class");
const { empleadoHelper } = require("../../helper/empleado.helper");
const { planificacionHelper } = require("../../helper/planificacion.helper");

const Registrar = async(actualizacion) =>{
      nuevaActualizacion = new Actualizacion(actualizacion);
      const { existe, empleado } = await Empleado.Buscar(nuevaActualizacion.reemplazo);
      if(existe){
            //No hay empleado
            throw new TypeError("El usuario reemplazante no existe.")
      }else if(!existe && empleado[0].activo == 0){
            // Hay empleado pero esta desactivado
            throw new TypeError("El usuario fue eliminado")
      }else{
            // Hay empleado
            const DatosPlanificacion = await nuevaActualizacion.ObtenerPlanificacion();
            const ListaPlanificacion = await planificacionHelper.GenerarListaPlanificacion(DatosPlanificacion);
            let ListaOrdenadaPlanificacion = await planificacionHelper.OrdenarLista(ListaPlanificacion)
            
            const vacaciones = 4;
            const permiso = 5;
            const otro = 6

            // Permiso
            if(nuevaActualizacion.tipo_id == 1) return await nuevaActualizacion.Permiso(ListaOrdenadaPlanificacion,permiso)
            // Vacaciones
            else if(nuevaActualizacion.tipo_id == 2) return await nuevaActualizacion.Permiso(ListaOrdenadaPlanificacion,vacaciones)
            // Observación
            else if(nuevaActualizacion.tipo_id == 4) return await nuevaActualizacion.Observacion();
            // Otro
            else return await nuevaActualizacion.Permiso(ListaOrdenadaPlanificacion,otro)
      }
};

const MostrarFormulario = async(planificacion_id) =>{
      const empleados = await Empleado.MostrarTodos();
      const ListaEmpleado = await empleadoHelper.GenerandoListaEmpleado(empleados);

      const Solicitante = await Actualizacion.MostrarSolicitante(planificacion_id);
      const TipoActualizacion = await Actualizacion.MostrarTipo();
      
      const data = {
            "actualizacion": TipoActualizacion,
            "empleados": ListaEmpleado,
            "solicitante": Solicitante
      }
      return data;
};
      
const Eliminar = async(id, tipo) =>{

      if (tipo != "Observación") {
            const CambiosAnterior = await Actualizacion.MostrarCambioAnterior(id);
            await Actualizacion.RestablecerTurnoAnterior(CambiosAnterior);
            await Actualizacion.EliminarCambioTurno(CambiosAnterior);
      }
      await Actualizacion.Eliminar(id);
      return;
}

module.exports.actualizacionModel = {
      Registrar,
      MostrarFormulario,
      Eliminar
      
}