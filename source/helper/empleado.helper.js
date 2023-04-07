const GenerandoListaEmpleado = async (empleados) => {
      const ListaEmpleado = empleados.reduce((empleado, actual) => {
            empleado[actual.rut] = empleado[actual.rut] || {
                  rut: actual.rut,
                  nombre_paterno: actual.nombre_paterno,
                  nombre_materno: actual.nombre_materno,
                  apellido_paterno: actual.apellido_paterno,
                  apellido_paterno: actual.apellido_materno,
                  imagen: actual.imagen,
                  credencial: []
                  
      };
            if (actual.credencial_id){
                  empleado[actual.rut].credencial.push({
                        credencial_id: actual.credencial_id,
                        fecha_emision: actual.fecha_emision,
                        fecha_vencimiento: actual.fecha_vencimiento,
                        tipo: actual.tipo,
                        numero: actual.numero
                  });
            }
            return empleado;
      }, []);
      return Object.values(ListaEmpleado);
};

module.exports.empleadoHelper = {
      GenerandoListaEmpleado
}