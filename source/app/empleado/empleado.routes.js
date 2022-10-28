const express = require("express");
const router = express.Router();
const {empleado_controller} = require("./empleado.controller");

router.post('/registar_empleado',empleado_controller.registrar_empleado);
// Falta implementar
router.put('/actualizar_empleado',empleado_controller.actualizar_empleado);
//
router.get('/eliminar_empleado', empleado_controller.eliminar_empleado);
router.get('/mostrar_todos_empleados', empleado_controller.mostrar_todos_empleados);
router.get('/mostrar_un_empleado', empleado_controller.mostrar_un_empleado);

module.exports = router;