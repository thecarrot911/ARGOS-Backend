const GenerandoListaEmpleado = async (empleados) => {
      const ListaEmpleado = empleados.reduce((empleado, actual) => {
            empleado[actual.rut] = empleado[actual.rut] || {
                  rut: actual.rut,
                  nombre_paterno: actual.nombre_paterno,
                  nombre_materno: actual.nombre_materno,
                  apellido_paterno: actual.apellido_paterno,
                  apellido_materno: actual.apellido_materno,
                  imagen: actual.imagen,
                  credencial: []
      };
            if (actual.credencial_id){
                  empleado[actual.rut].credencial.push({
                        credencial_id: actual.credencial_id,
                        fecha_emision: actual.fecha_emision,
                        fecha_vencimiento: actual.fecha_vencimiento,
                        tipo: actual.tipo,
                        numero: actual.numero,
                        vence: actual.vence
                  });
            }
            return empleado;
      }, []);
      return Object.values(ListaEmpleado);
};

const GenerandoListaPerfil = async(datosEmpleados) => {
      let perfil = datosEmpleados.reduce((anio, actual) =>{
            anio[actual.rut] = anio[actual.rut] || {
                  rut: actual.rut,
                  nombre_paterno: actual.nombre_paterno,
                  nombre_materno: actual.nombre_materno,
                  apellido_paterno: actual.apellido_paterno,
                  apellido_materno: actual.apellido_materno,
                  imagen: actual.imagen,
                  planificacion: []
            };
            anio[actual.rut].planificacion.push({
                  anio: actual.year,
                  mes: actual.month,
                  planificacion_id: actual.planificacion_id,
                  feriado: actual.feriado,
                  libre: actual.libre,
                  turno_1: actual.turno1,
                  turno_2: actual.turno2,
                  turno_3: actual.turno3,
                  horario1: actual.horario1,
                  horario2: actual.horario2,
                  horario3: actual.horario3
            })
            return anio
      },[]);

      perfil = Object.values(perfil).map((empleado) => {
            const planificacionPorAnio = empleado.planificacion.reduce((anios, planificacion) => {
                  const { anio, mes, planificacion_id, feriado, libre, turno_1, turno_2, turno_3, horario1, horario2, horario3 } = planificacion;
                  anios[anio] = anios[anio] || [];
                  anios[anio].push({ 
                        anio,
                        mes,
                        planificacion_id,
                        feriado,
                        libre,
                        turno_1,
                        turno_2,
                        turno_3,
                        horario1,
                        horario2,
                        horario3
                  });
            return anios;
      }, {});
      empleado.planificacion = Object.values(planificacionPorAnio);
      return empleado;
      });

      return Object.values(perfil)
};


module.exports.empleadoHelper = {
      GenerandoListaEmpleado,
      GenerandoListaPerfil,
}