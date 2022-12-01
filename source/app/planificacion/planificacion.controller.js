const { spawn } = require("child_process");
const { resolve } = require("path");
const { planificacionModel } = require("../../model/planificacionModel");

const generarplanificacion = async(req, res) =>{
    try{
        let anio = req.body.anio;
        let mes = req.body.mes;
        let empleados = req.body.empleados;
        let cant_empleados = empleados.length
        let itinerario_json = req.body.itinerario;
        if((itinerario_json[0].dia=='')){
            itinerario = 0
        }
        else if((itinerario_json[0].dia!='')){
            itinerario = new Array()
            for(i=0;i<itinerario_json.length;i++){
                let itinerario_array = new Array()
                itinerario_array.push(itinerario_json[i].dia)
                itinerario_array.push(itinerario_json[i].aviones)
                itinerario_array.push(itinerario_json[i].turno)
                itinerario.push(itinerario_array)
            }
        }
        let command = await spawn('python', ['source/app/planificacion/python/script_dev.py',anio,mes,cant_empleados,itinerario])
        let planificacion = new Array(); //verificador para que la variable sea disitnto de vacio y tenga una respuesta.
        
        command.stdout.on ('data', function (data){
            console.log("Child process on")
            planificacion.push(data.toString());
            
        });
        command.stderr.on ('data', function (data){
            planificacion = data.toString();
        });
        command.on('close', async function(code){
            console.log("Child process close")
            obj = planificacion[0].replace(/'/g,"\""); 
            turno_empleado = await planificacionModel.asignar_turno_empleado(obj,empleados);
            jsonsend = JSON.parse(turno_empleado);
            planificacion_id = await planificacionModel.guardar(mes, anio, jsonsend);
            console.log(jsonsend);
            let json = {}
            json.planificacion_id = planificacion_id;
            json.planificacion = jsonsend;
            let json_send = JSON.stringify(json)
            return res.send(json_send);
        });
        command.on('error', function(err){
            console.log('child process error')
            console.log(err);
            reject(err);
        });
    }catch(e){
        return res.send(e)
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

