const { response } = require("express");
const express = require("express");
const app = express();
const bodyParser = require('body-parser');
const jsonParser = bodyParser.json()
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
    connection.all(`SELECT * FROM usuarios`,[], (err, rows) => {
    if (err) {
        response.send(err.message);
        console.log("Error GET/usuarios")
    }
        console.log(rows)
        response.send(rows)
  });
});

//usuarios GET/id
app.get("/usuarios/:id",(req, response) => {
  connection.all(`SELECT * FROM usuarios WHERE id = ${id}`,[], (err, rows) => {
  if (err) {
      response.send(err.message);
      console.log("Error GET/usuarios/id")
  }
      console.log(rows)
      response.send(rows)
});
});

//usuarios POST
app.post("/usuarios",jsonParser,(req, response) => {
  console.log('Añadiendo usuario:',[req.body.id,req.body.username,req.body.password])
  try{
    connection.run(`INSERT INTO usuarios VALUES(?, ?, ?)`,[req.body.id,req.body.username,req.body.password], (err, rows) => {
    if (err) {
        response.send(err.message);
        console.log("Error POST/usuarios")
    }
        console.log("Usuario añadido.")
        response.send("Usuario añadido.")
    });
  }catch(e){} //comprobar
});

app.put("/usuarios/:id",jsonParser,(req, response) => {
    console.log('Modificando Usuario:',[req.body.id,req.body.username,req.body.password]);
    connection.run('Update usuarios set id=?,username=?, password=? where id=?',[req.body.id,req.body.username,req.body.password,req.body.id], (err, rows) => {
    if (err) console.log('Error modificando usuario');
    response.send('Usuario Modificado');

    });
});

app.delete("/usuarios/:id",jsonParser,(request, response) => {
    console.log('Borrar usuario');
    connection.run('DELETE FROM usuarios WHERE id= ?',[request.body.id], (err, rows) => {
    if (err) console.log('Error borrando usuario');
    else response.send('Usuario borrado');

    });
});