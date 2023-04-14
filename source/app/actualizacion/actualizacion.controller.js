const Actualizacion = require("../../class/actualizacion.class");
const { actualizacionModel } = require("../actualizacion/actualizacion.model");

const RegistrarActualizacion = async (req, res)=>{
    try{
        const consulta_RegistrarActualizacion = await actualizacionModel.Registrar(req.body)
        return res.status(200).json({
            error: false,
            msg: ''+error,
            data: consulta_RegistrarActualizacion
        });
    }catch(error){
        return res.status(400).json({
            error: true,
            msg: ''+error
        });
    }

};

const MostrarTipoActualizacion = async(req, res) =>{
    try{
        const consulta_MostrarTipoActualizacion = await Actualizacion.MostrarTipo();
        return res.status(200).json({
            error: false,
            msg: "Lista de todos los tipos de actualización que existen.",
            data: consulta_MostrarTipoActualizacion
        });
    }catch(error){
        console.error(error)
        return res.status(400).json({
            error: true,
            msg: error.message
        });
    }
};

module.exports.actualizacion_controller = {
    RegistrarActualizacion,
    MostrarTipoActualizacion
}