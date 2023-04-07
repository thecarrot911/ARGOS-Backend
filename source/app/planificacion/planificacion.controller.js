const { spawn } = require("child_process");
const { planificacionModel } = require("../../model/planificacionModel");
const Planificacion = require("../../class/planificacion.class");

const GenerarPlanificacionDeEmpleado = async(req, res) =>{
    try{
        const planificacion = new Planificacion(req.body);
        const planificacionMensual = await planificacion.GenerarPlanificacion();
        const planificacion_id = await planificacion.GuardarPlanificacion();
        const { insertId, affectedRows } = await planificacion.GuardarDia(planificacionMensual, planificacion_id);
        console.log(await insertId)
        console.log(await affectedRows)

      //const {} = await planificacion.GuardarTurno();
      //const {} = await planificacion.GuardarTurnoDia();

        return res.status(200).json({
            error: false,
            msg: `Se ha creado la Planificación de ${planificacion.mes_planificacion} del año ${planificacion.anio} correctamente`,
            data: planificacionMensual,
        });
    }catch(error){
        console.error(error);
        return res.status(400).json({
            error: true,
            msg: ''+error.message
        })
    }
}

const ggenerarplanificacion = async(req, res) =>{
    try{
        let anio = parseInt(req.body.anio);
        let mes = parseInt(req.body.mes);
        let empleados = req.body.empleados;
        let cant_empleados = empleados.length
        let itinerario_json = req.body.itinerario;
        // Variable que controla que las planificaciones no se repitan
        let planificacionMes = await planificacionModel.existe_planificacion(anio,mes);
        //let control = true;
        let control = planificacionMes.control;
        //let planificacion = planificacionMes.consulta_planificacion;

        if(control){
            if(itinerario_json[0].dia== '' || ( itinerario_json[0].aviones == null && itinerario_json[0].dia == null )){
                itinerario = 0
            }
            else if((itinerario_json[0].dia!='') || ( itinerario_json[0].aviones != null && itinerario_json[0].dia != null )){
                itinerario = new Array()
                for(i=0;i<itinerario_json.length;i++){
                    let itinerario_array = new Array()
                    if(itinerario_json[i].aviones>1){
                        itinerario_array.push(String(itinerario_json[i].dia))
                        itinerario_array.push(String(itinerario_json[i].turno))
                        itinerario_array.push(String(itinerario_json[i].aviones))
                        itinerario.push(itinerario_array)
                    }
                }
            }
            console.log(itinerario)

            let mesAnterior = await planificacionModel.existe_mes_anterior(anio,mes,cant_empleados);

            var planificacionAnterior = mesAnterior.planificacionAnterior
            var planificacionUltimaSemana;
            if(planificacionAnterior!=0){
                planificacionUltimaSemana = mesAnterior.copyPlanificacion
            }else{
                planificacionUltimaSemana = []
            }
            let command = await spawn('python', ['source/app/planificacion/python/script.py',anio,mes,cant_empleados,itinerario,planificacionAnterior])
            let planificacionMensual = new Array(); //verificador para que la variable sea disitnto de vacio y tenga una respuesta.
            
            command.stdout.on ('data', function (data){
                console.log("Child process on")
            
                //console.log(data.toString());
                planificacionMensual.push(data.toString());
                
                //planificacion.push(data.toString());
            });
            command.stderr.on ('data', function (data){
                console.log("stderr");
                console.log(data.toString());
            });
            command.on('close', async function(code){
                console.log("Child process close")
                //obj = planificacion[0].replace(/'/g,"\""); 
                turno_empleado = await planificacionModel.asignar_turno_empleado(planificacionMensual[0],empleados);
                jsonsend = JSON.parse(turno_empleado);
                if(planificacionUltimaSemana.length != 0){
                    jsonsend = await planificacionModel.asignar_nombre_ultima_semana(jsonsend,planificacionUltimaSemana,cant_empleados,empleados)
                }
                 ///*
                planificacion_id = await planificacionModel.guardar(mes, anio, jsonsend);
                let json = {}
                json.planificacion_id = planificacion_id;
                json.planificacion = jsonsend;
                let json_send = JSON.stringify(json)
                return res.send(json_send);
                 //*/
                //return res.json(jsonsend)
            });
            command.on('error', function(err){
                console.log('child process error')
                console.log(err);
                reject(err);
            });
        }
        else{
            meses_anio = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre", "Diciembre"]
            return res.json({
                error: true,
                msg: 'Ya existe una planificación para el mes de '+meses_anio[mes-1]
            });
        }
    }catch(e){
        return res.send(e)
    }

};
const planificacion_mostrar_todo = async(req,res) =>{
    try{
        let anio = req.query.anio;
        consulta_ultima_planificacion = await planificacionModel.mostrar_planificacion_anual(anio);
        return res.json({
            error: false,
            msg: "Planificaciones del año "+anio,
            data: consulta_ultima_planificacion
        });
    }catch(error){
        return res.json({
            error: true,
            msg: ''+error
        });
    }
};
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
};

const eliminarPlanificacion = async (req, res) =>{
    try{
        let planificacion_id = req.params.planificacion_id
        consulta_planificacion = await planificacionModel.eliminar(planificacion_id);
        return res.json({
            error: false,
            msg: "Planificación Eliminada"
        });
    }catch(error){
        return res.json({
            error: true,
            msg: ''+error
        });
    }
};

module.exports.planificacion_controller = {
    GenerarPlanificacionDeEmpleado,
    planificacion_mostrar_ultima,
    eliminarPlanificacion,
    planificacion_mostrar_todo,
};

