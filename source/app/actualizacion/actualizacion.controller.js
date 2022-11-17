const crear_actualizacion = (req, res)=>{
    try{
        console.log(req)
        return res.send({"nice":"nice"})
    }catch(e){
        return res.send(e);
    }

};

module.exports.actualizacion_controller = {
    crear_actualizacion
}