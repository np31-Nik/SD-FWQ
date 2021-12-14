const { response } = require("express");
const express = require("express");
const { use } = require("express/lib/application");
const req = require("express/lib/request");
const { jsonp } = require("express/lib/response");
const app = express();
const bodyParser=require('body-parser');
const jsonParser=bodyParser.json();
// Se define el puerto
const port=3002;
const sqlite3 = require('sqlite3').verbose();

// Ejecutar la aplicacion
app.listen(port, () => {
    console.log(`Ejecutando la aplicación API REST REGISTRY de SD en el puerto
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
    console.log("GET /")
  });

//usuarios GET
app.get("/usuarios",(req, response) => {
    connection.all(`SELECT * FROM usuarios`,[], (err, rows) => {
    if (err) {
        response.send(err.message);
        console.log("Error GET/usuarios")
    }
        console.log(rows)
        response.send(rows)
  });
  
});

//Añadir usuarios
app.post("/usuarios",jsonParser, (req, response) => {
    console.log("Añadiendo usuario");
    const id=req.body.id;
    const username=req.body.username;
    const password=req.body.password;
    
    const sql= ('Insert into usuarios (id,username,password) values(u'+id+','+username+','+password+')');
    connection.run(sql,error => {
      if(error) {
        console.log('Error: ', + error +' '+id+' '+username+ ' '+ password)
        response.send('Error: ', + error +' '+id+' '+username+ ' '+ password)
      }
      response.send('Usuario añadido');
    });
});

// // Añadir un nuevo usuario
// app.post("/usuarios",(request, response) => {
//   console.log('Añadir nuevo usuario');
//   const sql = 'INSERT INTO Usuarios SET ?';
//   console.log(request.body.id)

//   const usuarioObj = {
//     id: request.body.id,
//     username: request.body.username,
//     password: request.body.password
//   }
//   connection.query(sql,usuarioObj,error => {
//   if (error) throw error;
//   response.send('Usuario creado');
//   });
//  });

// app.post("/usuarios",jsonParser,(request, response) => {
//   console.log('Añadir nuevo usuario', request.body.nombre);
//   const sql = 'INSERT INTO Usuarios SET ?';
 
//   const usuarioObj = {
//     nombre: request.body.nombre,
//     ciudad: request.body.ciudad,
//     correo: request.body.correo
//   }
//   connection.run(sql,usuarioObj,error => {
//   if (error) throw error;
//   response.send('Usuario creado');
//   });
// });



// db.serialize(() => {
//   db.each(`SELECT *
//            FROM usuarios`, (err, row) => {
//     if (err) {
//       console.error(err.message);
//     }
//     console.log(row.id + "\t" + row.username);
//   });
// });

// db.close((err) => {
//   if (err) {
//     console.error(err.message);
//   }
//   console.log('Close the database connection.');
// });