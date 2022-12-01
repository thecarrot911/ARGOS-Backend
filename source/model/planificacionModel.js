const conexion = require("../database");

const asignar_turno_empleado = (obj, empleados)=>{
    let turno = ['"Libre"','"07:00 a 15:00"','"15:00 a 23:00"','"23:00 a 07:00"'];
    let array_empleados = new Array(5);
    array_empleados[0] = empleados[0].nombre 
    array_empleados[1] = empleados[1].nombre
    array_empleados[2] = empleados[2].nombre
    array_empleados[3] = empleados[3].nombre
    array_empleados[4] = empleados[4].nombre 

    array_empleados = array_empleados.sort(function() {return Math.random() - 0.5});
    
    //Asignación de turno
    for (i = 1;i<=array_empleados.length;i++){
        obj = obj.replaceAll('"nombre": '+i,'"nombre": "'+array_empleados[i-1]+'"');
    }
    
    //Reemplazo de los numeros por horas
    for (i=0; i<=3;i++){
        obj = obj.replaceAll('"turno": '+i,'"turno": '+turno[i]);
    }
    return obj;
};

const guardar = async(month, year, planificacion)=>{
    let string_sql = "INSERT INTO "+process.env.NOMBRE_BD+".planificacion(month, year) VALUES('"+month+"','"+year+"');";
    //Inserción de la planificación
    let insert_planificacion = await conexion.query(string_sql);
    let planificacion_id = insert_planificacion.insertId;
    let dia_semana;
    let numero_dia;
    let comodin;

    // Inserción del día 
    for(i=0;i<planificacion.length;i++){
        dia_semana = planificacion[i].dia_semana
        numero_dia = planificacion[i].numero_dia
        comodin = planificacion[i].comodin
        let string_sql_dia = "INSERT INTO "+process.env.NOMBRE_BD+".dia(planificacion_id, dia_semana, dia_numero, comodin) VALUES('"+planificacion_id+"','"+dia_semana+"','"+numero_dia+"','"+comodin+"')";

        let insert_dia = await conexion.query(string_sql_dia);
        dia_id = insert_dia.insertId

        // Inserción de empleados
        for(j=0;j<planificacion[i].empleados.length;j++){
            let nombre = planificacion[i].empleados[j].nombre
            let turno = planificacion[i].empleados[j].turno
            let string_sql_empleado = "INSERT INTO "+process.env.NOMBRE_BD+".empleado(dia_id, nombre, turno) VALUES('"+dia_id+"','"+nombre+"','"+turno+"')";
            await conexion.query(string_sql_empleado);
        }
        // Inserción de itinerario
        if(planificacion[i].itinerario !=0)
        {
            for(k=0;k<planificacion[i].itinerario.length;k++){
                turno = planificacion[i].itinerario[k].turno_itinerario
                empleado_faltante = planificacion[i].itinerario[k].falta
                let string_sql_itinerario = "INSERT INTO "+process.env.NOMBRE_BD+".itinerario(dia_id, turno, empleado_faltante) VALUES('"+dia_id+"','"+turno+"','"+empleado_faltante+"')";
                await conexion.query(string_sql_itinerario)
            }
        }
    }
    return planificacion_id;
};
const mostrar_todas = async()=>{

};
const mostrar_ultima = async(id_planificacion)=>{
    let string_sql = "SELECT * FROM mydb.turno_empleado WHERE id_planificacion = ('"+id_planificacion+"')";
    let consulta = await conexion.query(string_sql);
    return consulta;
};
const mostrar = async(id_planificacion)=>{

};

module.exports.planificacionModel = {
    asignar_turno_empleado,
    guardar,
    mostrar_ultima,
    mostrar_todas,
    mostrar
};