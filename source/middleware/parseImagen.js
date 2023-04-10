const multer = require("multer");
const path = require("path");

const empleado = multer.diskStorage({
      destination: function (req, file, cb) {
            cb(null, path.join(__dirname, "../public", "empleados"));
      },
      filename: function (req, file , cb) {
            cb(null, file.originalname);
      }
});

const Empleado = multer({ storage: empleado});

module.exports.multerParse = {
      Empleado
}