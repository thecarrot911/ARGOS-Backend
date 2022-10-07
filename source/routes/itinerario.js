const express = require("express");
const router = express.Router();
const { spawn } = require("child_process");

/*const {
    CalcularTurnoEmpleado,
} = require("../controllers/calcular-turno");
*/
//router provisional
//router.post("/crear",CalcularTurnoEmpleado);

router.post("/generar-planificacion-semanal", (req, res) => {
    var dataToSend;
    var dia=2
    var turno=3
    var empleado=5
    const python = spawn('python', ['pipe/script.py',dia,turno,empleado]);    
    python.stdout.on('data', function (data) {
        console.log("child process on");
        dataToSend = data.toString();
        console.log(dataToSend);
    });
    
    python.on("close", (code) => {
        console.log('child process off');
        return res.send(dataToSend);
    });
});

module.exports = router;
