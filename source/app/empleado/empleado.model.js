const { empleadoHelper } = require("../../helper/empleado.helper");
const Empleado = require("../../class/empleado.class");
const conexion = require("../../database");

const Registrar = async (empleado, file) => {
      
      nuevoEmpleado = new Empleado(empleado, file);

      const { existe , BuscarEmpleado } = await nuevoEmpleado.Buscar();
      
      if(BuscarEmpleado.length != 0 && BuscarEmpleado[0].activo == 0){
            return await nuevoEmpleado.Reactivar();
      }else if(!existe && BuscarEmpleado[0].activo == 1){
            throw new TypeError("El usuario ya existe");
      }

      if (file == undefined || file.filename == null) {
            nuevoEmpleado.imagen = null;
      } else {
            nuevoEmpleado.imagen = `${process.env.HOST}/public/empleados/${file.filename}`;
      }
      
      return await nuevoEmpleado.Registrar();
};

const Modificar = async(empleado, file) =>{
      modificarEmpleado = new Empleado(empleado,file);

      if(empleado.imagenURL != undefined){
            modificarEmpleado.imagen = empleado.imagenURL;
      }else{
            if (file == undefined || file.filename == null) {
                  modificarEmpleado.imagen = null;
            } else {
                  modificarEmpleado.imagen = `${process.env.HOST}/public/empleados/${file.filename}`;
            }
      }
      return await modificarEmpleado.Modificar();
};

const MostrarAll = async () => {
      const empleados = await Empleado.MostrarTodos();
      const credenciales = await empleadoHelper.GenerandoListaEmpleado(empleados);
      return credenciales;
};

const Eliminar = async(rut) =>{
      const stringSQLEmpleado = `
      UPDATE empleado SET activo = 0 
      WHERE rut='${rut}';`;
      return await conexion.query(stringSQLEmpleado)
};


const Perfil = async() =>{
      const empleados = await Empleado.MostrarTodos();
      const credenciales = await empleadoHelper.GenerandoListaEmpleado(empleados);
      const datosPlanificacion = await Empleado.Perfil()
      const planificacion = await empleadoHelper.GenerandoListaPerfil(datosPlanificacion);

      const data = {
            "credencial": credenciales,
            "planificacion": planificacion
      }
      return data;
};

module.exports.empleadoModel = {
      Registrar,
      Modificar,
      MostrarAll,
      Eliminar,
      Perfil
}