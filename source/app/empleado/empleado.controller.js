const {empleado_model} = require("../../model/empleadoModel");

const registrar_empleado = async(req,res)=>{
    consulta_verificacion = await empleado_model.buscar(req.body.rut);
    if(consulta_verificacion == ""){
        try{
            let nombre = req.body.nombre;
            let apellido = req.body.apellido;
            let rut = req.body.rut;
            consulta_insercion = await empleado_model.registrar(nombre,apellido,rut);
            console.log(consulta_insercion);
            return res.json({
                error: false,
                msg: "Empleado Registrado",
                data: consulta_insercion[0]
            });
        }catch(error){
            return res.json({
                error: true,
                msg: ''+error
            });
        }
    }
    else{
        try{
            return res.json({
                error: false,
                msg: "El empleado ya esta registrado",
                data: consulta_verificacion[0]
            });
        }catch(error){
            return res.json({
                error: true,
                msg: ''+error
            });
        }
    }
};

const mostrar_todos_empleados = async(req,res)=>{
    try{
        consulta = await empleado_model.mostrar_todos();
        return res.json({
            error:false,
            msg: 'Lista de empleados registrados',
            data: consulta
        });
    }catch(error){
        return res.json({
            error: true,
            msg: ''+error
        });
    }
};

const mostrar_un_empleado = async(req,res)=>{
    consulta_verificacion = await empleado_model.buscar(req.query.rut);
    if(consulta_verificacion != ""){
        try{
            let rut = req.query.rut;
            consulta_mostrar = await empleado_model.mostrar_uno(rut);
            return res.json({
                error: false,
                data: consulta_mostrar[0]
            });
        }catch(error){
            return res.json({
                error: true,
                msg: ''+error
            });
        }
    }else{
        try{
            return res.json({
                error: false,
                msg: "El empleado no esta registrado en el sistema"
            });
        }catch(error){
            return res.json({
                error: true,
                msg: ''+error
            });
        }
    }
};

//FALTA IMPLEMENTAR
const actualizar_empleado = async()=>{
    let string_sql = "";
    let consulta = await conexion.query(string_sql);
    return consulta;
};

const eliminar_empleado = async(req,res)=>{
    consulta_verificacion = await empleado_model.buscar(req.query.rut);
    if(consulta_verificacion != ""){
        try{
            let rut = req.query.rut;
            consulta = await empleado_model.eliminar(rut);
            return res.json({
                error: false,
                msg: "Empleado eliminado"
            });
        }catch(error){
            return res.json({
                error: true,
                msg: ''+error
            });
        }
    }else{
        try{
            return res.json({
                error: false,
                msg: "El empleado no esta registrado en el sistema"
            });
        }catch(error){
            return res.json({
                error: true,
                msg: ''+error
            });
        }
    }

};

module.exports.empleado_controller = {
    registrar_empleado, 
    actualizar_empleado,
    eliminar_empleado,
    mostrar_todos_empleados,
    mostrar_un_empleado
};