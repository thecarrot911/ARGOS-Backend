const express = require("express");
const router = express.Router();
const { empleado_controller } = require("./empleado.controller");
const { multerParse } = require("../../middleware/parseImagen");

router.get("", empleado_controller.mostrar_todos_empleados);
router.get("/perfil", empleado_controller.PerfilEmpleado);
router.post("/registrar_empleado",[multerParse.Empleado.single("imagen")], empleado_controller.registrar_empleado);
router.put("/modificar_empleado",[multerParse.Empleado.single("imagen")], empleado_controller.modificar_empleado); //CACHE DE IMÁGEN

router.put("/eliminar_empleado", empleado_controller.eliminar_empleado);

module.exports = router;
