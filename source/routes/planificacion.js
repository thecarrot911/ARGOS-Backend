const express = require("express");
const router = express.Router();
const { spawn } = require("child_process");
const { stringify } = require("querystring");

/*const {
    CalcularTurnoEmpleado,
} = require("../controllers/calcular-turno");
*/
//router provisional
//router.post("/crear",CalcularTurnoEmpleado);

router.post("/generar-planificacion-semanal", (req, res) => {
    var dataToSend;
    var dia=3
    var turno=3
    var empleado=5
    var jsonsend;
    var obj;
    const python = spawn('python', ['pipe/script.py',dia,turno,empleado]);    
    python.stdout.on('data', function (data) {
        //console.log("child process on");
        dataToSend = data.toString();
    });
    
    python.on("close", (code) => {
        //console.log('child process off');
        //console.log(dataToSend)
        obj = dataToSend.replace(/'/g,"\"");
        jsonsend = JSON.parse(obj);
        return res.send(jsonsend);

    });
});

module.exports = router;
