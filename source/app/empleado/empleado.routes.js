const express = require("express");
const router = express.Router();
const { empleado_controller } = require("./empleado.controller");
const { middlewareIamgen } = require("../../middleware/verificacion.empleado");

router.get("", empleado_controller.mostrar_todos_empleados);
router.post("/registrar_empleado", [middlewareIamgen.Empleado.single("imagen")] , empleado_controller.registrar_empleado);

router.put("/modificar_empleado/:rut", empleado_controller.modificar_empleado);
router.delete("/eliminar_empleado/:rut", empleado_controller.eliminar_empleado);

module.exports = router;
