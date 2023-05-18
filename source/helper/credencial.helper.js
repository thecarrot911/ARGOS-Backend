const conexion = require("../database");

const buscarTipo =  async (credencial) =>{

      let sql_buscarTipo = `
      SELECT * FROM credencial
      WHERE tipo = '${credencial.tipo}' and empleado_rut = '${credencial.rut}'`;
      let res_buscarTipo = await conexion.query(sql_buscarTipo);
      
      if(res_buscarTipo.length > 0) return true;
      else return false;
};

module.exports.crendecialHelper = {
      buscarTipo
}