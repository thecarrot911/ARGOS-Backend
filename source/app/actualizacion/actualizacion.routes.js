const express = require("express");
const router = express.Router();
const {actualizacion_controller } = require("./actualizacion.controller");

router.post('/crear_actualizacion',actualizacion_controller.crear_actualizacion);
router.get('/eliminar_actualizacion',actualizacion_controller.eliminar_actualizacion);
router.get('/mostrar_actualizacion',actualizacion_controller.mostrar_actualizacion);

module.exports = router;