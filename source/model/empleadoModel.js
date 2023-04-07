const conexion = require('../database');
const { validateRUT } = require('validar-rut');
const { empleadoHelper } = require('../helper/empleado.helper');
const Empleado = require('../class/empleado.class');


const Registrar = async(empleado, file)=>{
  nuevoEmpleado = new Empleado(empleado,file)
  if(!validateRUT(nuevoEmpleado.rut)){
    throw new TypeError("El RUT ingresado no es válido");
  }
  if(!await nuevoEmpleado.Buscar()){
    throw new TypeError("El usuario ya existe");
  }

  return await nuevoEmpleado.Registrar();
};

const MostrarAll = async() =>{
  const empleados = await Empleado.MostrarTodos();
  return await empleadoHelper.GenerandoListaEmpleado(empleados);
};


const Mostrar = async() =>{
  
};

/*
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
            empleado_rut,
            IF(DATEDIFF(fecha_vencimiento, CURDATE()) < 0, 1, fecha_vencimiento <= DATE_ADD(CURDATE(), INTERVAL 1 MONTH)) AS vence,
            DATEDIFF(fecha_vencimiento, CURDATE()) AS dias_restantes
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
*/
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
    
    await conexion.query(stringSQLCredencial);

    let stringSQLEmpleado = `
    DELETE FROM ${process.env.NOMBRE_BD}.empleado 
    WHERE rut = '${rut}'
    `;
    console.log(stringSQLEmpleado);
    return await conexion.query(stringSQLEmpleado);
};

const buscar = async (rut, tabla) => {
  let string_sql = `SELECT * FROM ${process.env.NOMBRE_BD}.${tabla} WHERE rut = '${rut}'`;
    console.log(string_sql);
    
  let respuesta = await conexion.query(string_sql);
  console.log(respuesta)
  if (respuesta.length == 0) return true;
  else return false;
};

const Modificar = async(empleado)=>{
  if (await empleadoHelper.buscar(empleado.rut,"empleado")) {
    throw new TypeError("El empleado no esta registrado en el sistema");
  }

  let sql_ModificarEmpleado = `
    UPDATE ${process.env.NOMBRE_BD}.empleado
    SET rut = "${empleado.rut}", 
    nombre_paterno = "${empleado.nombre_paterno}", 
    nombre_materno = "${empleado.nombre_materno}", 
    apellido_paterno = "${empleado.apellido_paterno}", 
    apellido_materno = "${empleado.apellido_materno}"
    WHERE ${process.env.NOMBRE_BD}.empleado.rut = "${empleado.rut}"
    `;

  return await conexion.query(sql_ModificarEmpleado);
}

module.exports.empleadoModel = {
  Registrar,
  mostrar,
  Modificar,
  eliminar,
  buscar,
  MostrarAll
};