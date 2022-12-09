const { json } = require("express/lib/response");
const { actualizacionModel } = require("../../model/actualizacionModel");

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
        console.log(req.body)
        let planificacion_id = req.body.planificacion_id
        let actualizacion_id = req.body.actualizacion_id
        
        await actualizacionModel.eliminar(planificacion_id, actualizacion_id)
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
}

module.exports.actualizacion_controller = {
    crear_actualizacion,
    eliminar_actualizacion
}