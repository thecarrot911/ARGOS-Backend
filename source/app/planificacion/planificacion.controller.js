const { spawn } = require("child_process");
const { planificacionModel } = require("../planificacion/planificacion.model");

const GenerarPlanificacionMensual = async(req, res) =>{
    try{
        const planificacionMensual = await planificacionModel.GenerarPlanificacion(req.body);
        return res.status(200).json({
            error: false,
            msg: `Se ha creado la Planificación de ${req.body.mes} del año ${req.body.anio} correctamente`,
            data: planificacionMensual
        });
    }catch(error){
        console.error(error);
        return res.status(400).json({
            error: true,
            msg: ''+error.message
        })
    }
};

const MostrarUltimaPlanificacion = async(req, res) =>{
    try{
        const [planificacion] = await planificacionModel.UltimaPlanificacion();
        return res.status(200).json({
            error: true,
            msg: `La última planificación corresponde al mes de ${planificacion.mes} del año ${planificacion.anio}`,
            data: planificacion
        });
    }catch(error){
        console.error(error);
        return res.status(400).json({
            error: true,
            msg: ''+error.message
        })
    }
};

const MostrarAniosPlanificaciones = async(req,res) =>{
    try{
        const planificacionesAnuales = await planificacionModel.AniosPlanificacion();
        return res.status(200).json({
            error: true,
            msg: `Planificaciones del año`,
            data: planificacionesAnuales
        });
    }catch(error){
        console.error(error)
        return res.status(400).json({
            error: true,
            msg: ''+error
        })
    }
}

const MostrarPlanificaciones = async(req,res) =>{
    try{
        const planificacionesAnuales = await planificacionModel.MostrarPlanificaciones(req.query.anio);
        return res.status(200).json({
            error: true,
            msg: `Planificaciones del año ${req.query.anio}.`,
            data: planificacionesAnuales
        });
    }catch(error){
        console.error(error);
        return res.status(400).json({
            error: true,
            msg: "" + error,
        });
    }
}

const EliminarPlanificacion = async(req,res) =>{
    try{
        await planificacionModel.EliminarPlanificacion(req.body)
        return res.status(200).json({
            error: true,
            msg: `Se ha eliminado la planificación.`,
        });
    }catch(error){
        console.error(error);
        return res.status(400).json({
            error: true,
            msg: "" + error
        });
    }
};

module.exports.planificacion_controller = {
    GenerarPlanificacionMensual,
    MostrarUltimaPlanificacion,
    MostrarAniosPlanificaciones,
    MostrarPlanificaciones,
    EliminarPlanificacion
};

