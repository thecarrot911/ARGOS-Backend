const crear_actualizacion = (req, res)=>{
    console.log(req.body)

    return res.send("nice");
};

module.exports.actualizacion_controller = {
    crear_actualizacion
}