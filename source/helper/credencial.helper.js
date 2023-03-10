const conexion = require("../database");

const buscarId = async (rut, credencial_id) =>{
};

const buscarTipo =  async (credencial) =>{

      let sql_buscarTipo = `
      SELECT * FROM ${process.env.NOMBRE_BD}.credencial
      WHERE credencial.tipo = '${credencial.tipo}'`;

      let res_buscarTipo = await conexion.query(sql_buscarTipo);
      console.log(res_buscarTipo.length);
      if(res_buscarTipo.length > 0){
            return true;
      }
      return false;
};

module.exports.crendecialHelper = {
      buscarId,
      buscarTipo
};
