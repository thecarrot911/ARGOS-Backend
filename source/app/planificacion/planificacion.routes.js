const express = require("express");
const router = express.Router();
const {planificacion_controller} = require("./planificacion.controller")

router.post('/generar_planificacion',planificacion_controller.generarplanificacion);
router.get('/mostrar_todo',planificacion_controller.planificacion_mostrar_todo);
router.get('/mostrar_ultima', planificacion_controller.planificacion_mostrar_ultima);


module.exports = router;