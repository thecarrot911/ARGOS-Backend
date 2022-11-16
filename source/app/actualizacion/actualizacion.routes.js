const express = require("express");
const router = express.Router();
const {actualizacion_controller } = require("./actualizacion.controller");

router.post('/crear_actualizacion',actualizacion_controller.crear_actualizacion);

module.exports = router;