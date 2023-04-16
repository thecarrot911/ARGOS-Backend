const express = require("express");
const router = express.Router();
const {actualizacion_controller } = require("./actualizacion.controller");



router.post("/registrar_actualizacion", actualizacion_controller.RegistrarActualizacion);
router.get("/formulario", actualizacion_controller.FormularioActualizacion);
//router.delete('/eliminar_actualizacion/:actualizacion_id',actualizacion_controller.eliminar_actualizacion);


module.exports = router;