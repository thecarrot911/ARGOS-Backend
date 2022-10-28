const conexion = require('../database');

const registrar = async(nombre,apellido,rut)=>{
    let string_sql = "INSERT INTO mydb.empleado (nombre, apellido, rut) values ('"+nombre+"', '"+apellido+"', '"+rut+"');"; 
    let consulta = await conexion.query(string_sql);
    return consulta;
};

const mostrar_todos = async()=>{
    let string_sql = "SELECT * FROM mydb.empleado;"
    let consulta = await conexion.query(string_sql);
    return consulta;
};

const mostrar_uno = async(rut)=>{
    let string_sql = "SELECT * FROM mydb.empleado WHERE rut = ('"+rut+"')";
    let consulta = await conexion.query(string_sql);
    return consulta;
};

const eliminar = async(rut)=>{
    let string_sql = "DELETE FROM mydb.empleado WHERE rut = ('"+rut+"')";
    let consulta = await conexion.query(string_sql);
    return consulta;
};

const buscar = async(rut)=>{
    let string_sql = "SELECT * FROM mydb.empleado WHERE rut = ('"+rut+"')";
    let consulta = await conexion.query(string_sql);
    return consulta
};

module.exports.empleado_model = {
    registrar,
    mostrar_todos,
    mostrar_uno,
    eliminar,
    buscar
};