const conexion = require("../database");

class Actualizacion{
      constructor({rut,planificacion_id,descripcion,fecha_inicio,fecha_termino,tipo_id, reemplazo}){
            this.rut = rut,
            this.planificacion_id = planificacion_id,
            this.descripcion = descripcion,
            this.fecha_inicio = fecha_inicio,
            this.fecha_termino = fecha_termino,
            this.tipo = tipo_id,
            this.reemplazo = reemplazo
      };

      Registrar = async() =>{
            console.log(this.rut)
            console.log(this.planificacion_id)
            console.log(this.descripcion)
            console.log(this.fecha_inicio)
            console.log(this.fecha_termino)
            console.log(this.tipo)
            console.log(this.reemplazo)
      };
      
      static MostrarTipo = async() =>{
            const sql_MostrarTipo = `SELECT * FROM tipo`;
            return await conexion.query(sql_MostrarTipo);
      };


}

module.exports = Actualizacion;