const express = require('express');
const morgan = require('morgan');

require("dotenv").config({path:__dirname+'/../.env'});

/**Inicialización del servidor */
const app = express();

/**Configuraciones */
app.set("port", process.env.PORT_SERVER || 5000);

/**Middlewares */
app.use(morgan("dev")) 
app.use(express.json()); 

/**Rutas*/ 
app.use("/itinerario_de_vuelo", require("./routes/itinerario"));

/**Levantar el servidor */
app.listen(app.get("port"), () => {
    console.log("Sistema de gestion de turno");
    console.log("Escuchando el servidor desde el puerto: ", app.get("port"));
  });