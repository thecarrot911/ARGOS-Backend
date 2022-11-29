const { actualizacionModel } = require("../../model/actualizacionModel");

const crear_actualizacion = (req, res)=>{
    try{
        let permiso = req.body.tipo_permiso
        let empleado = req.body.empleado
        let descripcion = req.body.descripcion
        let fecha = req.body.fecha
        let planificacion_id = req.body.planificacion_id
        return res.send({"nice":"nice"})
    }catch(error){
        return res.json({
            error: true,
            msg: ''+error
        });
    }

};

module.exports.actualizacion_controller = {
    crear_actualizacion
}