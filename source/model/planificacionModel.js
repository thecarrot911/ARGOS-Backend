const conexion = require("../database");

const asignar_turno_empleado = (obj, empleados)=>{
    let array_empleados = Object.values(empleados[0]);
    let turno = [':"Libre"',':"07:00 a 15:00"',':"15:00 a 23:00"',':"23:00 a 07:00"'];

    //Ordenamiento de turno al azar
    for (i = array_empleados.length;i; i-- ){
        j = Math.floor(Math.random()*i);
        k = array_empleados[i-1];;
        array_empleados[i-1]=array_empleados[j];
        array_empleados[j] = k;
    }

    //Asignación de turno
    for (i = 1;i<=array_empleados.length;i++){
        obj = obj.replaceAll('empleado_'+i,array_empleados[i-1]);
    }
    
    //Reemplazo de los numeros por horas
    for (i=0; i<=3;i++){
        obj = obj.replaceAll(": "+i+"",turno[i]);
    }
    return obj;
};


const guardar = async(nombre,planificacion)=>{ 
    let string_sql = "INSERT INTO mydb.planificacion(nombre) values('"+nombre+"');";
    //Inserción de la planificación
    let insert_planificacion = await conexion.query(string_sql);
    let id_planificacion = insert_planificacion.insertId;
    let id_dia = [];
    let id_turno = [];
    var k_indice = 0;
    //Inserción del día 
    for(i=1;i<=planificacion.length;i++){
        let string_sql_dia = "INSERT INTO mydb.dia(numero_dia,id_planificacion) values('"+i+"','"+id_planificacion+"');";
        let insert_dia = await conexion.query(string_sql_dia);   
        id_dia.push(insert_dia.insertId);
        
        //Inserción del turno
        rut_empleado = Object.keys(planificacion[i-1]);
        numero_turno = Object.values(planificacion[i-1]);

        for(j=0;j<numero_turno.length;j++){
            let string_sql_turno = "INSERT INTO mydb.turno(numero_turno,id_dia,id_planificacion) values('"+numero_turno[j]+"','"+id_dia[i-1]+"','"+id_planificacion+"');";

            let insert_turno = await conexion.query(string_sql_turno);
            id_turno.push(insert_turno.insertId);
            
            //Inserción empleado_turno
            let string_sql_empleado_turno = "INSERT INTO mydb.turno_empleado(id_turno, id_dia, id_planificacion, rut) values('"+id_turno[k_indice]+"','"+id_dia[i-1]+"','"+id_planificacion+"','"+rut_empleado[j]+"')";

            let insert_turno_empleado = await conexion.query(string_sql_empleado_turno);
            k_indice++;
        }
    }
    //Inserción empleado_turno
    /*var k = 0;
    for(i=0 ; i<id_dia.length ;i++){    
        for(j=0;j<rut_empleado.length; j++){
            let string_sql = "INSERT INTO mydb.turno_empleado(id_turno, id_dia, id_planificacion, rut) values('"+id_turno[k]+"','"+id_dia[i]+"','"+id_planificacion+"','"+rut_empleado[j]+"')";
            let insert_turno_empleado = await conexion.query(string_sql);
            k++;
        }
    }*/
    return id_planificacion;
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