const { empleadoModel } = require("../../model/empleadoModel");

const registrar_empleado = async(req,res)=>{
    try{
        const consulta_registrarEmpleado = await empleadoModel.Registrar(req.body, req.file)
        return res.status(200).json({
            error: false,
            msg: "Se ha registrado el empleado exitosamente",
            data: consulta_registrarEmpleado
        });
    }catch(error){
        console.error(error)
        return res.status(400).json({
            error: true,
            msg: "" + error.message,
        });
    }
};

const mostrar_todos_empleados = async(req,res)=>{
    try{
        consulta = await empleadoModel.MostrarAll();
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

const modificar_empleado = async(req,res)=>{
    try{
        await empleado_model.Modificar(req.body)
        return res.json({
            error: false,
            msg: "Los datos del empleado han sido modificado",
        });
    }catch(error){
        console.log(error);
            return res.json({
            error: true,
            msg: "" + error.message
        });
    }
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
    mostrar_todos_empleados
};