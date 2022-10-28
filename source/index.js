const express = require('express');
const morgan = require('morgan');
const cors = require('cors');

require("dotenv").config({path:__dirname+'/../.env'});

/**Inicialización del servidor */
const app = express();

/**Configuraciones */
app.set("port", process.env.PORT_SERVER || 5000);

/**Middlewares */
app.use(morgan("dev")) 
app.use(cors());
app.use(express.json()); 

/**Rutas*/ 
app.use(require("./routes"));

/**Levantar el servidor */
app.listen(app.get("port"), () => {
    console.log("Sistema de gestion de turno");
    console.log("Escuchando el servidor desde el puerto: ", app.get("port"));
  });