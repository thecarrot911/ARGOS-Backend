const { validateRUT } = require("validar-rut");
const { empleadoHelper } = require("../../helper/empleado.helper");
const Empleado = require("../../class/empleado.class");
const conexion = require("../../database");


const Registrar = async (empleado, file) => {
      
      nuevoEmpleado = new Empleado(empleado, file);
      
      /*if (!validateRUT(nuevoEmpleado.rut)) {
            throw new TypeError("El RUT ingresado no es válido");
      }*/
      
      const { existe , BuscarEmpleado } = await nuevoEmpleado.Buscar();
      
      if(BuscarEmpleado.length != 0 && BuscarEmpleado[0].activo == 0){
            return await nuevoEmpleado.Reactivar();
      }else if(!existe && BuscarEmpleado[0].activo == 1){
            throw new TypeError("El usuario ya existe");
      }

      if (file == undefined) {
            nuevoEmpleado.imagen = "https://i.imgur.com/EBH7aDM.png";
      } else {
            nuevoEmpleado.imagen = `${process.env.HOST}/public/empleados/${file.filename}`;
      }
      
      return await nuevoEmpleado.Registrar();
};

const MostrarAll = async () => {
      const empleados = await Empleado.MostrarTodos();
      return await empleadoHelper.GenerandoListaEmpleado(empleados);
};

const Eliminar = async(rut) =>{
      const stringSQLEmpleado = `
      UPDATE empleado SET activo = 0 
      WHERE rut='${rut}';`;
      return await conexion.query(stringSQLEmpleado)
}

module.exports.empleadoModel = {
      Registrar,
      MostrarAll,
      Eliminar
}