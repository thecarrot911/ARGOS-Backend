const express = require("express");
const app = express();

app.use('/app/planificacion', require('./app/planificacion/planificacion.routes'));
app.use('/app/empleado', require('./app/empleado/empleado.routes'));

module.exports = app;