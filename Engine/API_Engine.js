const { response } = require("express");
const express = require("express");
const app = express();
const bodyParser = require('body-parser');
const jsonParser = bodyParser.json()
const fs = require('fs')

// Se define el puerto
const port=3000;
const sqlite3 = require('sqlite3').verbose();

// Ejecutar la aplicacion
app.listen(port,'0.0.0.0', () => {
    console.log(`Ejecutando la aplicación API REST de SD en el puerto
    ${port}`);
});

// open the database
let connection = new sqlite3.Database('../db.db', sqlite3.OPEN_READWRITE, (err) => {
    if (err) {
      console.error(err.message);
    }
    console.log('Connected to the database.');
  });

  app.get("/",(req,res) => {
    res.send("GET /")
  });

//usuarios GET
app.get("/usuarios",(req, response) => {
  console.log("Leyendo datos de fichero usuariosTemp.txt...");
    const datos = fs.readFile('usuariosTemp.txt','utf8',(err,data) =>{
      if(err){
        console.log(err);
        return;
      }else{
        console.log(data);
        response.send(data);
      }
    });
});


//mapa GET
app.get("/mapa",(req, response) => {
  console.log("Leyendo datos de fichero mapaTemp.txt...");
    const datos = fs.readFile('mapaTemp.txt','utf8',(err,data) =>{
      if(err){
        console.log(err);
        return;
      }else{
        console.log(data);
        response.send(data);
      }
    });
});
// db.close((err) => {
//   if (err) {
//     console.error(err.message);
//   }
//   console.log('Close the database connection.');
// });