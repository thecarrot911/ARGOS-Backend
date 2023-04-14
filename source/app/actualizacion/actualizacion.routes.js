const express = require("express");
const router = express.Router();
const {actualizacion_controller } = require("./actualizacion.controller");



router.get('/tipo', actualizacion_controller.MostrarTipoActualizacion);
router.post('     ',actualizacion_controller.RegistrarActualizacion);
//router.delete('/eliminar_actualizacion/:actualizacion_id',actualizacion_controller.eliminar_actualizacion);


module.exports = router;