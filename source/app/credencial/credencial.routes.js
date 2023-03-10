const express = require("express");
const router = express.Router();
const {credencial_controller} = require("./credencial.controller");

router.get("/mostrar", credencial_controller.mostrar_credencial);
router.post("/registrar", credencial_controller.registrar_credencial);
router.delete("/eliminar/:credencial_id", credencial_controller.eliminar_credencial);
router.post("/renovar",credencial_controller.renovar_credencial);
router.get("/vencidas", credencial_controller.fecha_vencimiento);


module.exports = router;