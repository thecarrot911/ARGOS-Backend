const express = require("express");
const app = express();

app.use('/app/planificacion', require('./app/planificacion/planificacion.routes'));
app.use('/app/empleado', require('./app/empleado/empleado.routes'));
app.use('/app/actualizacion', require('./app/actualizacion/actualizacion.routes'))

module.exports = app;