const { spawn } = require("child_process");
const conexion = require("../database");
const { planificacionHelper } = require("../helper/planificacion.helper")

class Planificacion {
      constructor({ anio, mes, empleados, mes_planificacion, itinerario }) {
            this.anio = parseInt(anio),
            this.mes = parseInt(mes),
            this.cantidad_empleado = empleados.length,
            this.empleados = empleados,
            this.itinerario = JSON.stringify(itinerario)
      }

      PlanificacionDelMesAnterior = async() =>{
            let mesActual = await planificacionHelper.ObtenerMes(this.mes);
            let anioAnterior;
            let mesAnterior;
            
            if(mesActual == "Enero"){
                  anioAnterior = this.anio - 1; 
                  mesAnterior = "Diciembre";
            }
            else{
                  anioAnterior =  this.anio; 
                  mesAnterior = await planificacionHelper.ObtenerMes(this.mes-1)
            }
            const sql = `
            SELECT * FROM planificacion
            INNER JOIN dia ON planificacion.planificacion_id = (SELECT planificacion_id FROM planificacion WHERE planificacion.year = ${anioAnterior} and planificacion.month = '${mesAnterior}')
            INNER JOIN turno ON dia.id = turno.dia_id
            INNER JOIN turno_dia ON turno.id = turno_dia.turno_id
            INNER JOIN empleado ON turno_dia.empleado_rut = empleado.rut
            `;
            return await conexion.query(sql);
      };

      GenerarPlanificacion(planificacionAnterior) {
            return new Promise((resolve, reject) => {
                  let planificacionMensual = [];
                  const empleadosPlanificacion = this.empleados.map((emp) => emp.rut);
                  const command = spawn("python", [
                        "source/app/planificacion/python/index.py",
                        this.anio,
                        this.mes,
                        this.cantidad_empleado,
                        this.itinerario,
                        JSON.stringify(planificacionAnterior),
                        ...empleadosPlanificacion,
                  ]);

                  command.stdout.on("data", function (data) {
                        console.log("Child process ON");
                        planificacionMensual.push(data.toString().trim());
                  });
                  command.stderr.on("data", function (data) {
                        console.log("Print stderr data");
                        console.log(data.toString());
                  });
                  command.on("close", function (code) {
                        console.log("Child process CLOSE");
                        //let json = planificacionMensual[0]
                        const json = JSON.parse(planificacionMensual[0]);
                        resolve(json);
                  });
                  command.on("error", function (err) {
                        console.log("child process error");
                        console.log(err);
                        reject(err);
                  });
            });
      }

      GuardarTurnoDia = async (planificacion, turno_id) => {
            const turno_diaData = [];
            let i = 0
            for(const p of planificacion){
                  for(const d of p.empleados){
                        const turno_dia = [
                              d.nombre,
                              turno_id+i
                        ]
                        turno_diaData.push(turno_dia);
                        i++;
                  }
            }
            const sql_IngresarTurnoDia = `INSERT INTO turno_dia(empleado_rut, turno_id) VALUES ?`;
            const IngresarTurnoDia = await conexion.query(sql_IngresarTurnoDia,[turno_diaData])
            return IngresarTurnoDia.insertId;
      };
      
      GuardarTurno = async (planificacion,dia_id) => {
            const turnoData = []
            let j = 0
            for(const p of planificacion){
                  for (const d of p.empleados) {
                        const turno = [
                              dia_id+j,
                              d.turno
                        ];
                        turnoData.push(turno);
                  }
                  j++;
            }
            const sql_IngresarTurno = `INSERT INTO turno(dia_id, turno) VALUES ?`;
            const IngresarTurno = await conexion.query(sql_IngresarTurno,[turnoData]);
            return IngresarTurno.insertId;
      };

      GuardarDia = async (planificacion, planificacion_id) => {
            const diaData = [];
            for (const p of planificacion) {
                  const dia = [
                        planificacion_id,
                        p.dia_semana,
                        p.dia_numero,
                        p.feriado,
                        p.comodin,
                  ];
                  diaData.push(dia);
            }
            const sql_IngresarDia = `INSERT INTO dia(planificacion_id, dia_semana, dia_numero, feriado, comodin) VALUES ?`;
            const IngresarDia = await conexion.query(sql_IngresarDia, [diaData]);
            return IngresarDia.insertId;
      };

      GuardarPlanificacion = async () => {
            const sql = `INSERT INTO planificacion(month, year) VALUES('${await planificacionHelper.ObtenerMes(this.mes)}','${this.anio}');`;
            const IngresarPlanificacion = await conexion.query(sql);
            return IngresarPlanificacion.insertId;
      };

      static MostrarUltima = async() => {
            const sql = `
            SELECT * FROM planificacion
            INNER JOIN dia ON planificacion.planificacion_id = dia.planificacion_id
            INNER JOIN turno ON dia.id = turno.dia_id
            INNER JOIN turno_dia ON turno.id = turno_dia.turno_id
            INNER JOIN empleado ON turno_dia.empleado_rut = empleado.rut
            WHERE planificacion.planificacion_id = (SELECT MAX(planificacion_id) FROM planificacion);`;
            return await conexion.query(sql);
      };

      static Anual = async(year) =>{
            const sql = `
            SELECT * FROM planificacion
            INNER JOIN dia ON planificacion.planificacion_id = dia.planificacion_id
            INNER JOIN turno ON dia.id = turno.dia_id
            INNER JOIN turno_dia ON turno.id = turno_dia.turno_id
            INNER JOIN empleado ON turno_dia.empleado_rut = empleado.rut
            WHERE planificacion.year = ${year};
            `;
            return await conexion.query(sql)
      };

      static Anuales = async() =>{
            const sql = `SELECT * FROM planificacion`;
            return await conexion.query(sql);
      }

      static Estadistica = async() =>{
            const sql = `
            SELECT planificacion.month, empleado.rut, empleado.nombre_paterno, 
                  empleado.apellido_paterno, empleado.imagen,
                  SUM(CASE WHEN dia.feriado = 1 THEN 1 ELSE 0 END) feriado,
                  SUM(CASE WHEN turno.turno = 0 THEN 1 ELSE 0 END) libre,
                  SUM(CASE WHEN turno.turno = 1 THEN 1 ELSE 0 END) turno1,
                  SUM(CASE WHEN turno.turno = 2 THEN 1 ELSE 0 END) turno2,
                  SUM(CASE WHEN turno.turno = 3 THEN 1 ELSE 0 END) turno3
            FROM planificacion
                  INNER JOIN dia AS dia ON planificacion.planificacion_id = dia.planificacion_id
                  INNER JOIN turno AS turno ON dia.id = turno.dia_id
                  INNER JOIN turno_dia AS turno_dia ON turno.id = turno_dia.turno_id
                  INNER JOIN empleado AS empleado ON turno_dia.empleado_rut = empleado.rut
            WHERE planificacion.year = 2015
            GROUP BY empleado.rut, planificacion.planificacion_id
            ORDER BY year DESC,
            CASE month
                  WHEN 'enero' THEN 1
                  WHEN 'febrero' THEN 2
                  WHEN 'marzo' THEN 3
                  WHEN 'abril' THEN 4
                  WHEN 'mayo' THEN 5
                  WHEN 'junio' THEN 6
                  WHEN 'julio' THEN 7
                  WHEN 'agosto' THEN 8
                  WHEN 'septiembre' THEN 9
                  WHEN 'octubre' THEN 10
                  WHEN 'noviembre' THEN 11
                  WHEN 'diciembre' THEN 12
            END ASC;`;

            return await conexion.query(sql);
      }
}

module.exports = Planificacion;