const { response } = require("express");
const express = require("express");
const app = express();
const bodyParser = require('body-parser');
const jsonParser = bodyParser.json()
const fs = require('fs')

// Se define el puerto
const port=3003;
const sqlite3 = require('sqlite3').verbose();



// Add headers before the routes are defined
app.use(function (req, res, next) {

  // Website you wish to allow to connect
  res.setHeader('Access-Control-Allow-Origin', '*');

  // Request methods you wish to allow
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE');

  // Request headers you wish to allow
  res.setHeader('Access-Control-Allow-Headers', '*, Authorization');

  // Set to true if you need the website to include cookies in the requests sent
  // to the API (e.g. in case you use sessions)
  res.setHeader('Access-Control-Allow-Credentials', true);

  // Pass to next layer of middleware
  next();
});

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