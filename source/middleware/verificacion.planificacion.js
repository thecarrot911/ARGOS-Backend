const conexion = require("../database")

const ExistenciaPlanificacion = async(req, res, next) =>{
      try{
            const meses=[     "Enero","Febrero","Marzo","Abril","Mayo",
                              "Junio","Julio","Agosto","Septiembre",
                              "Octubre","Noviembre","Diciembre"
                        ];

            const mesPlanificacion = meses[(req.body.mes) - 1];

            const sql_PlanificacionAnterior = `
            SELECT EXISTS(SELECT * FROM ${process.env.NOMBRE_BD}.planificacion 
            WHERE month = '${mesPlanificacion}' AND year = ${parseInt(req.body.anio)}) As existe;`;

            if((await conexion.query(sql_PlanificacionAnterior))[0].existe){
                  throw new TypeError(`Ya existe una planificación para el mes de ${mesPlanificacion} del año ${req.body.anio}`);
            }

            next();

      }catch(error){
            console.error(error)
            return res.status(400).json({
                  error: true,
                  msg: "" + error.message,
            });
      }
};



module.exports.verificadorPlanificacion = {
      ExistenciaPlanificacion
}