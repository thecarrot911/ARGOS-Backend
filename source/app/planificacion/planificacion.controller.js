const { spawn } = require("child_process");
const { planificacionModel } = require("../../model/planificacionModel");

const generarplanificacion = async(req, res) =>{
    try{
        let anio = req.body.anio;
        let mes = req.body.mes;
        let empleados = req.body.empleados;
        let cant_empleados = empleados.length
        
        let spawn = require('child_process').spawn;
        let command = spawn('python', ['source/app/planificacion/python/script_integrado.py',anio,mes,cant_empleados])
        let dataToSend;
        let obj;
        
        command.stdout.on ('data', function (data){
            console.log('child process on');
            dataToSend = data.toString();
        });
        command.stderr.on ('data', function (data){
            console.log('child process on');
            dataToSend = data.toString();
        });
        command.on('close', function(code){
            console.log('child process close')
            obj = dataToSend.replace(/'/g,"\""); 
            turno_empleado = planificacionModel.asignar_turno_empleado(obj,empleados);
            jsonsend = JSON.parse(turno_empleado);
            //jsonsend = JSON.parse(obj)
            return res.send(jsonsend)
        });
        command.on('error', function(err){
            console.log('child process error')
            console.log(err);
            reject(err);
        });
    }catch(e){
        return res.send("error - xd")
    }

};

const guardar_planificacion = async(req, res)=>{
    try{
        let nombre = req.body[0].nombre;
        let planificacion = req.body[0].planificacion
        consulta_insercion = await planificacionModel.guardar(nombre,planificacion);
        return res.json({
            error: false,
            msg: "Planificación guardada"
        });
    }catch(error){
        return res.json({
            error: true,
            msg: ''+error
        });
    }
};

const mostrar_ultima_planificacion = async(req,res)=>{
    try{
        let id_planificacion = req.query.id_planificacion;
        consulta_ultima_planificacion = await planificacionModel.mostrar_ultima(id_planificacion);
        return res.json({
            error: false,
            msg: "Planificación guardada",
            data: consulta_ultima_planificacion
        });
    }catch(error){
        return res.json({
            error: true,
            msg: ''+error
        });
    }
}

module.exports.planificacion_controller={
    generarplanificacion, 
    guardar_planificacion, 
    mostrar_ultima_planificacion
}

