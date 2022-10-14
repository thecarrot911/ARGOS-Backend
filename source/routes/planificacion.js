const express = require("express");
const router = express.Router();
const { spawn } = require("child_process");

router.get("/generar-planificacion-semanal", (req, res) => {
    var dataToSend;
    var dia=31
    var turno=3
    var empleado=5
    var jsonsend;
    var obj;
    
    const python = spawn('python', ['pipe/script.py',dia,turno,empleado]);    
    
    python.stdout.on('data', function (data) {
        dataToSend = data.toString();
    });
    
    python.on("close", (code) => {
        
        obj = dataToSend.replace(/'/g,"\"");
        
        //Convertir la variable obj en JSON
        jsonsend = JSON.parse(obj);
        
        //Se envía el JSON al front-end
        return res.send(jsonsend);
    });
});

module.exports = router;
