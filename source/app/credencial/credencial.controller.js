const {credencial_model} = require("../../model/credencialModel");

const registrar_credencial = async (req,res) => {
    try{
        let consulta_insercion = await credencial_model.registrar(req.body);
        return res.json({
            error: false,
            msg: "Credencial Registrada",
            data: consulta_insercion
        });
    }catch(error){
        return res.json({
            error: true,
            msg: ''+error
        });
    }
};

const renovar_credencial = async (req, res) => {
    try{
        //let consulta_renovacion = await..
        return res.json({
            error: false,
            msg: "Credencial Renovada",
            data: consulta_renovacion
        });
    }catch(error){
        return res.json({
            error: true,
            msg: ''+error
        });
    }
};

const modificar_credencial = async(req,res) => {
    try{
        //let consulta_modificacion = await..
        return res.json({
            error: false,
            msg: "Credencial Modificada",
            data: consulta_renovacion
        });
    }catch(error){
        return res.json({
            error: true,
            msg: ''+error
        });
    }
};

const eliminar_credencial = async (req, res) => {
    try {
        console.log(req.params.credencial_id)
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
            msg: ''+error
        });
    }
};

module.exports.credencial_controller = {
    registrar_credencial,
    renovar_credencial,
    modificar_credencial,
    eliminar_credencial,
    mostrar_credencial

}