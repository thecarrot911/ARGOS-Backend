const conexion = require("../database");

const guardar = async(planificacion_id,tipo_permiso, descripcion, empleado, fecha)=>{
    let string_sql = "INSERT INTO "+process.env.NOMBRE_BD+".actualizacion(planificacion_id,tipo_permiso, descripcion, empleado, fecha) VALUES('"+planificacion_id+"','"+tipo_permiso+"','"+descripcion+"','"+empleado+"','"+fecha+"')";

    let insert_actualizacion = await  conexion.query(string_sql);

    return insert_actualizacion.insertId;
};

module.exports.actualizacionModel = {
    guardar
}