const { spawn } = require("child_process");
const { resolve } = require("path");
const { planificacionModel } = require("../../model/planificacionModel");

const generarplanificacion = async(req, res) =>{
    try{
        let anio = parseInt(req.body.anio);
        let mes = parseInt(req.body.mes);
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
        console.log(itinerario_json)
        //let ultimo_empleado = await planificacionModel.ultimo_empleado_planificacion_anterior()
        //console.log(ultimo_empleado)
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
            turno_empleado = await planificacionModel.asignar_turno_empleado(planificacion[0],empleados);
            jsonsend = JSON.parse(turno_empleado);
            planificacion_id = await planificacionModel.guardar(mes, anio, jsonsend);
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

const planificacion_mostrar_todo = async(req,res) =>{
    try{
        consulta_ultima_planificacion = await planificacionModel.mostrar_todo()
        return res.json({
            error: false,
            msg: "Mostrar planificación",
            data: consulta_ultima_planificacion
        });
    }catch(error){
        return res.json({
            error: true,
            msg: ''+error
        });
    }
}
const planificacion_mostrar_ultima = async(req,res)=>{
    try{
        consulta_ultima_planificacion = await planificacionModel.mostrar_ultima();
        return res.json({
            error: false,
            msg: "Última planificación",
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
    planificacion_mostrar_ultima,
    planificacion_mostrar_todo
}

