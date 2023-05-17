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
            throw new TypeError("El usuario fue eliminando")
      }else{
            // Hay empleado
            const DatosPlanificacion = await nuevaActualizacion.ObtenerPlanificacion();
            const ListaPlanificacion = await planificacionHelper.GenerarListaPlanificacion(DatosPlanificacion);
            let ListaOrdenadaPlanificacion = await planificacionHelper.OrdenarLista(ListaPlanificacion)
            
            const fechaInicio = new Date(nuevaActualizacion.fecha_inicio);
            fechaInicio.setUTCHours(0, 0, 0, 0);
            const diaInicio = fechaInicio.getUTCDate();

            const fechaTermino = new Date(nuevaActualizacion.fecha_termino);
            fechaTermino.setUTCHours(0, 0, 0, 0);
            const diaTermino = fechaTermino.getUTCDate();


            console.log(diaInicio);
            console.log(diaTermino);
            /*if(nuevaActualizacion.tipo_id == 1) await nuevaActualizacion.Permiso(ListaOrdenadaPlanificacion,4)
            else if(nuevaActualizacion.tipo_id == 2) await nuevaActualizacion.Permiso(ListaOrdenadaPlanificacion,5)
            else await nuevaActualizacion.Permiso(ListaOrdenadaPlanificacion,6)

            return await nuevaActualizacion.Registrar() ;*/
            return;
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