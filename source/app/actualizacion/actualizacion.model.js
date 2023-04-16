const Actualizacion = require("../../class/actualizacion.class");
const Empleado = require("../../class/empleado.class")
const { empleadoHelper } = require("../../helper/empleado.helper");
const { planificacionHelper } = require("../../helper/planificacion.helper");

const Registrar = async(actualizacion) =>{
      nuevaActualizacion = new Actualizacion(actualizacion);
      const DatosPlanificacion = await nuevaActualizacion.ObtenerPlanificacion();
      const ListaPlanificacion = await planificacionHelper.GenerarListaPlanificacion(DatosPlanificacion);
      const ListaOrdenadaPlanificacion = await planificacionHelper.OrdenarLista(ListaPlanificacion)
      return ListaOrdenadaPlanificacion;
      //nuevaActualizacion.Registrar()
};

const MostrarFormulario = async() =>{
      const empleados = await Empleado.MostrarTodos();
      const ListaEmpleado = await empleadoHelper.GenerandoListaEmpleado(empleados);
      const TipoActualizacion = await Actualizacion.MostrarTipo();
      
      const data = {
            "actualizacion": TipoActualizacion,
            "empleados": ListaEmpleado
      }
      return data
};

module.exports.actualizacionModel = {
      Registrar,
      MostrarFormulario
}