const { actualizacionModel } = require("../actualizacion/actualizacion.model");

const RegistrarActualizacion = async (req, res)=>{
    try{
        const consulta_RegistrarActualizacion = await actualizacionModel.Registrar(req.body)
        await actualizacionModel.Registrar(req.body);
        return res.status(200).json({
            error: false,
            msg: 'Se ha registrado la nueva actualización',
            data:consulta_RegistrarActualizacion
        });
    }catch(error){
        console.error(error)
        return res.status(400).json({
            error: true,
            msg: ''+error
        });
    }

};

const FormularioActualizacion = async(req, res) =>{
    try{
        const consulta_FormularioActualizacion = await actualizacionModel.MostrarFormulario();
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

module.exports.actualizacion_controller = {
    RegistrarActualizacion,
    FormularioActualizacion
}