const conexion = require("../database");

const guardar = async(planificacion_id,tipo_permiso, descripcion, empleado, fecha)=>{
    let string_sql = "INSERT INTO "+process.env.NOMBRE_BD+".actualizacion(planificacion_id,tipo_permiso, descripcion, empleado, fecha) VALUES('"+planificacion_id+"','"+tipo_permiso+"','"+descripcion+"','"+empleado+"','"+fecha+"')";
    let insert_actualizacion = await conexion.query(string_sql);
    return insert_actualizacion.insertId;
};
/*
const eliminar = async(actualizacion_id)=>{
    let string_sql = `DELETE FROM ${process.env.NOMBRE_BD}.actualizacion actualizacion where actualizacion.actualizacion_id = ${actualizacion_id};`
    let delete_actualizacion = await conexion.query(string_sql);
    return delete_actualizacion.insertId;
}
const modificar = async(actualizacion)=>{
    let string_sql = 
    `UPDATE ${process.env.NOMBRE_BD}.actualizacion 
    SET tipo_permiso="${actualizacion.tipo_permiso}", 
    descripcion="${actualizacion.descripcion}", 
    empleado="${actualizacion.empleado}", 
    fecha="${actualizacion.fecha}" 
    WHERE ${process.env.NOMBRE_BD}.actualizacion.actualizacion_id = ${actualizacion.actualizacion_id};`

    let modificar_actualizacion = await conexion.query(string_sql);
    return modificar_actualizacion;
}
*/
module.exports.actualizacionModel = {
    guardar
}