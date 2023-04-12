const { actualizacionModel } = require("../../model/actualizacionModel");
const Actualizacion = require("../../class/actualizacion.class")

const crear_actualizacion = async (req, res)=>{
    try{
        let tipo_permiso = req.body.tipo_permiso
        let empleado = req.body.empleado
        let descripcion = req.body.descripcion
        let fecha = req.body.fecha
        let planificacion_id = req.body.planificacion_id
        let json = {}

        actualizacion_id = await actualizacionModel.guardar(planificacion_id,tipo_permiso, descripcion, empleado, fecha);

        json.tipo_permiso = tipo_permiso
        json.empleado = empleado
        json.descripcion = descripcion
        json.fecha = fecha
        json.planificacion_id = planificacion_id
        json.actualizacion_id = actualizacion_id
        
        let json_send = JSON.stringify(json);
        return res.send(json_send)
    }catch(error){
        return res.json({
            error: true,
            msg: ''+error
        });
    }

};

const eliminar_actualizacion = async (req,res) =>{
    try{
        let actualizacion_id = req.params.actualizacion_id;
        respuesta = await actualizacionModel.eliminar(actualizacion_id)
        return res.json({
            error: false,
            msg: "Actualización eliminada"
        });
    }catch(error){
        return res.json({
            error: true,
            msg: ''+error
        });
    }
}

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
    crear_actualizacion,
    eliminar_actualizacion,
    MostrarTipoActualizacion
}