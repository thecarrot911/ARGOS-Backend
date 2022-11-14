const { spawn } = require("child_process");
const { planificacionModel } = require("../../model/planificacionModel");

const generarplanificacion = async (req, res)=>{
    try{
        //let mes = req.body.mes;
        //let anio = req.body.anio;
        //let empleados = req.body.empleados;
        //let cant_empleados = empleados.length
        let jsonsend;
        let obj;
        let dataToSend;
        const python = spawn('python', ['source/app/planificacion/python/script_constraint.py',dia,mes,cant_empleados]);
        python.stdout.on('data', function (data) {
            console.log('child process on');

            dataToSend = data.toString();
            //dataToSend =  JSON.stringify(data);
        });
        
        python.on("close", function (code) {
            console.log('child process off');
            //obj = dataToSend.replace(/'/g,"\"");  
            console.log(dataToSend)

            //turno_empleado = planificacionModel.asignar_turno_empleado(obj,empleados);
            //Convertir la variable obj en JSON
            //jsonsend = JSON.parse(dataToSend)
            //Se envía el JSON al front-end
            return await res.send("xd tabien");
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

