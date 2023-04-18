const Actualizacion = require("../../class/actualizacion.class");
const Empleado = require("../../class/empleado.class")
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
            throw new TypeError("El usuario fue eliminando")
      }else{
            // Hay empleado
            const DatosPlanificacion = await nuevaActualizacion.ObtenerPlanificacion();
            const ListaPlanificacion = await planificacionHelper.GenerarListaPlanificacion(DatosPlanificacion);
            let ListaOrdenadaPlanificacion = await planificacionHelper.OrdenarLista(ListaPlanificacion)
            let valuesTurnoDia;
            let updatePlanificacion

            if(nuevaActualizacion.tipo_id == 1){
                  // Cambio de turno
                  valuesTurnoDia = await nuevaActualizacion.CambioTurno(ListaOrdenadaPlanificacion, empleado);
                  if(valuesTurnoDia.length == 0){
                        throw new TypeError("No hay cambios en la planificacion al realizar esta actualizacion.")
                  }     
                  updatePlanificacion = await nuevaActualizacion.ModificarPlanificacion(valuesTurnoDia);
                  await nuevaActualizacion.Registrar();

            }else if (nuevaActualizacion.tipo_id == 2){
                  // Permiso
            }else{
                  new TypeError("No existe este tipo de permiso")
            }
            return updatePlanificacion;
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

module.exports.actualizacionModel = {
      Registrar,
      MostrarFormulario
}