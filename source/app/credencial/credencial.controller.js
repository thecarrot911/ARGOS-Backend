const {credencial_model} = require("../../model/credencialModel");

const registrar_credencial = async (req,res) => {
    try{
        await credencial_model.registrar(req.body);
        return res.json({
            error: false,
            msg: "Credencial Registrada",
        });
    }catch(error){
        console.log(error.message);
        return res.json({
            error: true,
            msg: "" + error.message
        });
    }
};

const renovar_credencial = async (req, res) => {
    try{
        let consulta_renovacion = await credencial_model.renovar(req.body);
        return res.json({
            error: false,
            msg: "Credencial Renovada",
            data: consulta_renovacion
        });
    }catch(error){
        console.error(error);
        return res.json({
            error: true,
            msg: ''+error
        });
    }
};

const eliminar_credencial = async (req, res) => {
    try {
        let consulta_eliminacion = await credencial_model.eliminar(req.params.credencial_id);
        return res.json({
            error: false,
            msg: "Credencial Eliminada",
            data: consulta_eliminacion,
        });

    } catch (error) {
        return res.json({
            error: true,
            msg: "" + error,
        });
    }
};

const mostrar_credencial = async (req,res) => {
    try{
        let consulta_mostrar = await credencial_model.mostrar(req.query.rut);
        return res.json({
            error: false,
            msg: "Lista de Credenciales",
            data: consulta_mostrar
        });
    }catch(error){
        return res.json({
            error: true,
            msg: ''+error.message
        });
    }
};

const fecha_vencimiento = async(req, res)=>{
    try{
        let credencialPorVencer = await credencial_model.vencer();
        return res.json({
            error: false,
            msg: "Credenciales por vencer",
            data: credencialPorVencer
        });
    }catch(error){
        return res.json({
            error: true,
            msg: "" + error,
        });
    }
};

module.exports.credencial_controller = {
    registrar_credencial,
    renovar_credencial,
    eliminar_credencial,
    mostrar_credencial,
    fecha_vencimiento

}