const express = require("express");
const router = express.Router();
const {credencial_controller} = require("./credencial.controller");

router.post('/registrar_credencial', credencial_controller.registrar_credencial);
router.delete("/eliminar_credencial/:credencial_id", credencial_controller.eliminar_credencial);
router.get("/mostrar_credencial",credencial_controller.mostrar_credencial);

// - - - - - - - - 
router.put('/renovar_credencial', credencial_controller.renovar_credencial);
router.put('/modificar_credencial', credencial_controller.modificar_credencial); // se puede eleimianr xd

module.exports = router;