const express = require("express");
const router = express.Router();
const {planificacion_controller} = require("./planificacion.controller")

router.post('/generar_planificacion',planificacion_controller.generarplanificacion);
router.post('/guardar_planificacion',planificacion_controller.guardar_planificacion);
router.get('/mostrar_ultima_planificacion',planificacion_controller.mostrar_ultima_planificacion);


module.exports = router;