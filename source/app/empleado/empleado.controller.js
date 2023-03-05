const { empleado_model } = require("../../model/empleadoModel");

const registrar_empleado = async(req,res)=>{
    try{
        if (await empleado_model.buscar(req.body.rut, "empleado")) {
            consulta_insercion = await empleado_model.registrarEmpleado(req.body);
            
            if(await empleado_model.buscar(req.body.rut, "empleado_planificacion")){
                await empleado_model.RegistrarPlanificacion(req.body);
            }

            return res.json({
                error: false,
                msg: "Empleado Registrado",
                data: consulta_insercion[0],
            });

        } else {
            return res.json({
                error: false,
                msg: "El empleado ya esta registrado",
            });
        }
    }catch(error){
        console.error(error)
        return res.json({
            error: true,
            msg: "" + error,
        });
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

const mostrar_perfil = async(req,res)=>{
    consulta_verificacion = await empleado_model.buscar(req.query.rut);
    if(consulta_verificacion != ""){
        try{
            let rut = req.query.rut;
            consulta_mostrar = await empleado_model.mostrar(rut);
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

const modificar_empleado = async(req,res)=>{
    let string_sql = "";
    console.log(req.body)
    //let consulta = await conexion.query(string_sql);
    return res.send(req.body);
};

const eliminar_empleado = async(req,res)=>{
    try{
        if(!await empleado_model.buscar(req.params.rut, "empleado")){
            await empleado_model.eliminar(req.params.rut);
            return res.json({
                error: false,
                msg: "El empleado ha sido eliminado del sistema"
            })
        }else{
            return res.json({
                error: false,
                msg: "El empleado no esta registrado en el sistema"
            })
        }
    }catch(error){
        return res.json({
            error: true,
            msg: "" + error
        });
    }
};

module.exports.empleado_controller = {
    registrar_empleado,
    modificar_empleado,
    eliminar_empleado,
    mostrar_todos_empleados,
    mostrar_perfil,
};