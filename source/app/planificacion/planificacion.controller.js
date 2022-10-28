const { spawn } = require("child_process");
const { planificacionModel } = require("../../model/planificacionModel");

const generarplanificacion = (req, res)=>{
    try{
        let mes = req.body.mes;
        let anio = req.body.anio;
        let empleados = req.body.empleados;
        let cant_empleados = Object.keys(empleados[0]).length
        let jsonsend;
        let obj;
        let dataToSend;

        const python = spawn('python', ['source/app/planificacion/python/test.py',anio,mes,cant_empleados]);    
        python.stdout.on('data', function (data) {
            dataToSend = data.toString();
        });
        
        python.on("close", (code) => {
            //obj = dataToSend.replace(/'/g,"\"");  
            //turno_empleado = planificacionModel.asignar_turno_empleado(obj,empleados);
            //Convertir la variable obj en JSON
            //jsonsend = JSON.parse(turno_empleado);
            //jsonsend = JSON.parse(dataToSend)
            //Se envía el JSON al front-end
            return res.send(dataToSend);
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

