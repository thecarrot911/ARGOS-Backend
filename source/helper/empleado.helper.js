const conexion = require("../database");

const buscar = async (rut, tabla) => {
      let string_sql = `SELECT * FROM ${process.env.NOMBRE_BD}.${tabla} WHERE rut = '${rut}'`;
      let respuesta = await conexion.query(string_sql);
      if (respuesta.length == 0) return true;
      else return false;
};

module.exports.empleadoHelper = {
      buscar
}