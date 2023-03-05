const conexion = require('../database');
const { validateRUT, getCheckDigit, generateRandomRUT } = require('validar-rut')


const registrarEmpleado = async(empleado)=>{
    let nombre_materno = empleado.nombre_materno;
    let nombre_paterno = empleado.nombre_paterno;
    let apellido_materno = empleado.apellido_materno;
    let apellido_paterno = empleado.apellido_paterno;
    let rut = empleado.rut;
    
    if(!validateRUT(rut)){
        throw new TypeError('El RUT ingresado no es válido.')
    }

    let stringRegistrarEmpleado = 
    `
    INSERT INTO ${process.env.NOMBRE_BD}.empleado (rut, nombre_paterno, nombre_materno, apellido_paterno, apellido_materno)
    VALUES ('${rut}','${nombre_paterno}','${nombre_materno}','${apellido_paterno}','${apellido_materno}');
    `;

    let RegistroEmpleado = await conexion.query(stringRegistrarEmpleado);

    return RegistroEmpleado;
};

const RegistrarPlanificacion = async(empleado)=>{
    let nombre_materno = empleado.nombre_materno;
    let nombre_paterno = empleado.nombre_paterno;
    let apellido_materno = empleado.apellido_materno;
    let apellido_paterno = empleado.apellido_paterno;
    let rut = empleado.rut;

    let stringRegistrarEmpleadoPlanificacion = `
    INSERT INTO ${process.env.NOMBRE_BD}.empleado_planificacion (rut, nombre_paterno, nombre_materno, apellido_paterno, apellido_materno)
    VALUES ('${rut}','${nombre_paterno}','${nombre_materno}','${apellido_paterno}','${apellido_materno}');
    `;

    return await conexion.query(stringRegistrarEmpleadoPlanificacion);
}

const mostrar_todos = async()=>{
    let dataArray = new Array();

    let stringAllEmpleado = `
    SELECT * FROM ${process.env.NOMBRE_BD}.empleado;`;
    
    let allEmpleados = await conexion.query(stringAllEmpleado);
    for(let i = 0; i < allEmpleados.length; i++){
        
        let dataDiccionario = {}

        dataDiccionario.rut = allEmpleados[i].rut
        dataDiccionario.nombre_paterno = allEmpleados[i].nombre_paterno;
        dataDiccionario.nombre_materno = allEmpleados[i].nombre_materno;
        dataDiccionario.apellido_paterno = allEmpleados[i].apellido_paterno;
        dataDiccionario.apellido_materno = allEmpleados[i].apellido_materno;
        
        let stringEmpleadoCredencial = `
            SELECT 
            credencial_id,
            DATE_FORMAT(fecha_emision, '%Y-%m-%d') fecha_emision,
            DATE_FORMAT(fecha_vencimiento, '%Y-%m-%d') fecha_vencimiento,
            tipo,
            numero,
            empleado_rut
            FROM ${process.env.NOMBRE_BD}.credencial
            WHERE empleado_rut = '${allEmpleados[i].rut}'`;

        let empleadoCredencial = await conexion.query(stringEmpleadoCredencial);
        
        let credencial = new Array();

        for(let j = 0; j < empleadoCredencial.length; j++){
            credencial.push(empleadoCredencial[j])
        }
        dataDiccionario.credencial = credencial;

        dataArray.push(dataDiccionario)
    }
    
    return dataArray;
};

const mostrar = async(rut)=>{
    let string_sql = `
    SELECT rut, nombre_paterno, nombre_materno, apellido_paterno, apellido_materno, 
    DATE_FORMAT(fecha_emision, '%Y-%m-%d') fecha_emision, 
    DATE_FORMAT(fecha_vencimiento, '%Y-%m-%d') fecha_vencimiento, 
    tipo 
    FROM ${process.env.NOMBRE_BD}.empleado, ${process.env.NOMBRE_BD}.credencial
    WHERE rut='${rut}' and empleado_rut = '${rut}';
    `;
    let consulta = await conexion.query(string_sql);
    return consulta;
};

const eliminar = async(rut)=>{

    let stringSQLCredencial = 
    `DELETE FROM ${process.env.NOMBRE_BD}.credencial 
    WHERE empleado_rut = '${rut}'
    `
    
    conexion.query(stringSQLCredencial);

    let stringSQLEmpleado = `
    DELETE FROM ${process.env.NOMBRE_BD}.empleado 
    WHERE rut = '${rut}'
    `;
    
    return conexion.query(stringSQLEmpleado);
};

const buscar = async(rut, tabla)=>{
    let string_sql = `SELECT * FROM ${process.env.NOMBRE_BD}.${tabla} WHERE rut = '${rut}'`
    let respuesta = await conexion.query(string_sql);
    if(respuesta.length == 0) return true;
    else  return false;
};

module.exports.empleado_model = {
    registrarEmpleado,
    RegistrarPlanificacion,
    mostrar_todos,
    mostrar,
    eliminar,
    buscar,
};