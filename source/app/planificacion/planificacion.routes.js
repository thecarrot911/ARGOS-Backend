const express = require("express");
const router = express.Router();
const { planificacion_controller } = require("./planificacion.controller");

router.get("", planificacion_controller.MostrarUltimaPlanificacion);
router.post("/generar",planificacion_controller.GenerarPlanificacionMensual);


//router.get('/mostrar_planificacion_anual',planificacion_controller.planificacion_mostrar_todo);
//router.delete('/eliminar_planificacion/:planificacion_id', planificacion_controller.eliminarPlanificacion);

module.exports = router;