const conexion = require("../../model/actualizacionModel");

const crear_actualizacion = async()=>{
    let string_sql ="";
    let consulta = await conexion.query(string_sql);
    return consulta;
};

const eliminar_actualizacion = async()=>{
    let string_sql ="";
    let consulta = await conexion.query(string_sql);
    return consulta;
};

const mostrar_actualizacion = async()=>{
    let string_sql ="";
    let consulta = await conexion.query(string_sql);
    return consulta;
};

module.exports.actualizacion_controller = {
    crear_actualizacion,
    eliminar_actualizacion,
    mostrar_actualizacion
}