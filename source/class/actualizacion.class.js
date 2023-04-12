const conexion = require("../database");

class Actualizacion{
      constructor({id, }){

      };

      static MostrarTipo = async() =>{
            const sql_MostrarTipo = `SELECT * FROM permiso`;
            return await conexion.query(sql_MostrarTipo);
      };
}

module.exports = Actualizacion;