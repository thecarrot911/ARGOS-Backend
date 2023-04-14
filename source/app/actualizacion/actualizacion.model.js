const Actualizacion = require("../../class/actualizacion.class");

const Registrar = async(actualizacion) =>{
      nuevaActualizacion = new Actualizacion(actualizacion);
      nuevaActualizacion.Registrar()
};

module.exports.actualizacionModel = {
      Registrar
}