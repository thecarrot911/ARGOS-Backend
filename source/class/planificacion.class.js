const { spawn } = require("child_process");

class Planificacion {
      constructor({anio, mes, empleados, mes_planificacion, itinerario}){
            this.anio = parseInt(anio),
            this.mes = parseInt(mes),
            this.cantidad_empleado = empleados.length,
            this.mes_planificacion = mes_planificacion,
            this.empleados = empleados,
            this.itinerario = JSON.stringify(itinerario)
      };

      GenerarPlanificacion(){
            return new Promise((resolve,reject) =>{
                  let planificacionMensual = []; 
                  //console.log(typeof(this.itinerario))
                  const empleadosPlanificacion = this.empleados.map(emp => emp.rut)
                  const command = spawn('python', ['source/app/planificacion/python/index.py',
                  this.anio,this.mes, this.cantidad_empleado, this.itinerario, 0, ...empleadosPlanificacion])


                  command.stdout.on('data', function(data){
                        console.log("Child process ON");
                        //console.log(data.toString())
                        planificacionMensual.push(data.toString().trim());
                  });
                  command.stderr.on("data", function (data) {
                        console.log("Print stderr data");
                        console.log(data.toString());
                  });
                  command.on("close", function (code) {
                        console.log("Child process CLOSE");
                        //console.log(planificacionMensual.toString());
                        //resolve(planificacionMensual[0]);

                        const json = JSON.parse(planificacionMensual[0])
                        resolve(json);
                  });
                  command.on("error", function (err) {
                        console.log("child process error");
                        console.log(err);
                        reject(err);
                  });
            });
      };
}

module.exports = Planificacion;