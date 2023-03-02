const express = require("express");
const router = express.Router();
const { empleado_controller } = require("./empleado.controller");

router.get("", empleado_controller.mostrar_todos_empleados);
router.post("/registrar_empleado", empleado_controller.registrar_empleado);
router.put("/modificar_empleado",empleado_controller.modificar_empleado);
router.delete("/eliminar_empleado/:rut", empleado_controller.eliminar_empleado);
router.get("/perfil", empleado_controller.mostrar_perfil);

module.exports = router;
