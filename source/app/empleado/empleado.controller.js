const { empleadoModel } = require("./empleado.model");

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
        const consulta = await empleadoModel.MostrarAll();
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

const PerfilEmpleado = async (req,res) =>{
    try{
        console.log("xD")
        const Perfil = await empleadoModel.Perfil(req.query.rut);
        return res.status(200).json({
            error:false,
            msg: 'Perfil del empleado',
            data: Perfil
        })
    }catch(error){
        console.error(error);
        return res.status(400).json({
            error: true,
            msg: ''+error.message
        });
    }
};
/*
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
};*/

const eliminar_empleado = async(req,res)=>{
    try{
        await empleadoModel.Eliminar(req.query.rut)
        return res.json({
            error: false,
            msg: "El empleado ha sido eliminado del sistema"
        })
    }catch(error){
        console.error(error)
        return res.json({
            error: true,
            msg: "" + error.message
        });
    }
};

module.exports.empleado_controller = {
    registrar_empleado,
    mostrar_todos_empleados,
    eliminar_empleado,
    PerfilEmpleado
};