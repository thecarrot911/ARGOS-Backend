const { actualizacionModel } = require("../actualizacion/actualizacion.model");

const RegistrarActualizacion = async (req, res)=>{
    try{
        const consulta_RegistrarActualizacion = await actualizacionModel.Registrar(req.body)
        return res.status(200).json({
            error: false,
            msg: 'Se ha registrado la nueva actualización',
            data:consulta_RegistrarActualizacion
        });
    }catch(error){
        console.error(error)
        return res.status(400).json({
            error: true,
            msg: ''+error.message
        });
    }

};

const FormularioActualizacion = async(req, res) =>{
    try{
        const consulta_FormularioActualizacion = await actualizacionModel.MostrarFormulario(req.query.planificacion_id);
        return res.status(200).json({
            error: false,
            msg: "Lista de todos los tipos de actualización que existen.",
            data: consulta_FormularioActualizacion
        });
    }catch(error){
        console.error(error)
        return res.status(400).json({
            error: true,
            msg: error.message
        });
    }
};

const EliminarActualizacion = async(req,res) => {
    try{
        const consulta_EliminarActualizacion = await actualizacionModel.Eliminar(req.query.id, req.query.tipo)
        return res.status(200).json({
            error: false,
            msg: "Se ha eliminado la actualización",
            data: consulta_EliminarActualizacion
        });
    }catch(error){
        console.error(error);
        return res.status(400).json({
            error: true,
            msg: error.message
        });
    }
};

module.exports.actualizacion_controller = {
    RegistrarActualizacion,
    FormularioActualizacion,
    EliminarActualizacion
}