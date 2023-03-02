const conexion = require('../database');

const registrar = async(credencial)=>{
    let fecha_vencimiento = credencial.fecha_vencimiento;
    let fecha_emision = credencial.fecha_emision;
    let tipo = credencial.tipo;
    let rut = credencial.rut;
    let numero = credencial.numero

    let string_sql = `
    INSERT INTO ${process.env.NOMBRE_BD}.credencial(fecha_vencimiento, fecha_emision, tipo, empleado_rut, numero)
    VALUES('${fecha_vencimiento}','${fecha_emision}','${tipo}','${rut}','${numero}');
    `

    let consulta = await conexion.query(string_sql);
    return consulta;
};

const eliminar = async(credencial_id)=>{
    let eliminarCredencial = `
    DELETE FROM ${process.env.NOMBRE_BD}.credencial 
    WHERE credencial_id = '${credencial_id}';
    `
    let consulta = await conexion.query(eliminarCredencial);
    return consulta;
};

const mostrar = async (rut) => {
    let mostrarCredencial = `
    SELECT
    credencial_id,
    DATE_FORMAT(fecha_emision, '%Y-%m-%d') fecha_emision,
    DATE_FORMAT(fecha_vencimiento, '%Y-%m-%d') fecha_vencimiento,
    tipo,
    numero,
    empleado_rut
    FROM ${process.env.NOMBRE_BD}.credencial
    WHERE empleado_rut = '${rut}'
    `;
    let consulta = await conexion.query(mostrarCredencial);
    return consulta;
};


const renovar = async(credencial)=>{

};

const modificar = async(credencial)=>{

};


module.exports.credencial_model = {
    registrar,
    renovar,
    modificar,
    eliminar,
    mostrar
}