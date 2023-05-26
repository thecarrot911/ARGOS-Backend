const conexion = require('../database');
const { validateRUT } = require("validar-rut");
const { crendecialHelper } = require("../helper/credencial.helper");

const registrar = async(credencial)=>{
    let fecha_vencimiento = credencial.fecha_vencimiento;
    let tipo = credencial.tipo;
    let rut = credencial.rut;
    let numero = credencial.numero

    if (await crendecialHelper.buscarTipo(credencial)) {
        throw new TypeError("Ya existe ese tipo de credencial");
    }

    let string_sql = `
    INSERT INTO credencial(fecha_vencimiento, tipo, empleado_rut, numero)
    VALUES('${fecha_vencimiento}','${tipo}','${rut}','${numero}');
    `
    
    return await conexion.query(string_sql);
};

const eliminar = async(credencial_id)=>{
    let eliminarCredencial = `
    DELETE FROM credencial 
    WHERE credencial_id = '${credencial_id}';
    `
    let consulta = await conexion.query(eliminarCredencial);
    return consulta;
};

const mostrar = async (rut) => {
    let mostrarCredencial = `
    SELECT
    credencial_id,
    DATE_FORMAT(fecha_vencimiento, '%d-%m-%Y') fecha_vencimiento,
    tipo,
    numero,
    empleado_rut
    FROM credencial
    WHERE empleado_rut = '${rut}'
    `;
    let consulta = await conexion.query(mostrarCredencial);
    return consulta;
};


const renovar = async(credencial)=>{
    // Verificar el rut
    if (!validateRUT(credencial.rut)) {
        throw new TypeError("El RUT ingresado no es válido.");
    }

    let sql_RenovarCredencial = `
        UPDATE credencial
        SET empleado_rut = '${credencial.rut}',
        fecha_vencimiento = '${credencial.fecha_vencimiento}',
        tipo = '${credencial.tipo}',
        numero = ${credencial.numero}
        WHERE credencial_id = ${credencial.credencial_id}
        `;


    return await conexion.query(sql_RenovarCredencial);
};

const vencer = async() =>{

    let sql_CredencialVencer = `
    SELECT EXISTS (
    SELECT 1
    FROM credencial
    WHERE IF(DATEDIFF(fecha_vencimiento, CURDATE()) < 0, 1, fecha_vencimiento <= DATE_ADD(CURDATE(), INTERVAL 1 MONTH)) = 1
    ) AS vence;
    `;

    let credencialVencer = await conexion.query(sql_CredencialVencer)
    if (credencialVencer[0].vence) return true;
    else return false;

};

module.exports.credencial_model = {
    registrar,
    renovar,
    eliminar,
    mostrar,
    vencer
}