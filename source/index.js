const express = require("express");
const morgan = require("morgan");
const cors = require("cors");
const bodyParser = require("body-parser");
const path = require("path");

require("dotenv").config({ path: __dirname + "/../.env" });

/**Inicialización del servidor */
const app = express();

/**Configuraciones */
app.set("port", process.env.PORT_SERVER || 5000);

/**Middlewares */
app.use(morgan("dev"));
app.use(cors());
app.use(express.json());
app.use(bodyParser.json({ limit: "2mb" }));
app.use(bodyParser.urlencoded({ limit: "2mb", extended: true }));
app.use("/public", express.static(path.join(__dirname, "public")));

/**Rutas*/
app.use(require("./routes"));

/**Levantar el servidor */
app.listen(app.get("port"), () => {
  console.log("Sistema de gestion de turno");
  console.log("Escuchando el servidor desde el puerto: ", app.get("port"));
});
