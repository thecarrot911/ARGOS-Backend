require("dotenv").config({path:__dirname+'/../.env'});
const { promisify } = require("util");
const {createPool} = require('mysql2');

const pool = createPool({
    host: process.env.HOST_BD,
    user: process.env.USER_BD,
    password: process.env.PASSWORD_BD,
    port: process.env.PORT_BD,
    database: process.env.NOMBRE_BD
});

/**Connection Database */
pool.getConnection((err, con)=>{
    if(err){
      console.log(err)
    }
    if(con){
      con.release();
      console.log("base de datos conectada");
    }
});

pool.query = promisify(pool.query);

module.exports = pool;
