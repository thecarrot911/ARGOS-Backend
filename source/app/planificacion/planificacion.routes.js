const express = require("express");
const router = express.Router();
const { planificacion_controller } = require("./planificacion.controller");
const { verificadorPlanificacion } = require("../../middleware/verificacion.planificacion")


router.get("", planificacion_controller.MostrarUltimaPlanificacion);
router.post("/generar",[verificadorPlanificacion.ExistenciaPlanificacion],planificacion_controller.GenerarPlanificacionMensual);
router.get("/planificaciones_anuales", planificacion_controller.MostrarPlanificacionesAnuales);


//router.get("/planificacion_anual", planificacion_controller.MostrarPlanificacionAnual);



//router.get('/mostrar_planificacion_anual',planificacion_controller.planificacion_mostrar_todo);
//router.delete('/eliminar_planificacion/:planificacion_id', planificacion_controller.eliminarPlanificacion);

module.exports = router;