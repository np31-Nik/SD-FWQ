const { response } = require("express");
const express = require("express");
const app = express();
const bodyParser = require('body-parser');
const jsonParser = bodyParser.json()
// Se define el puerto
const port=3000;
const sqlite3 = require('sqlite3').verbose();


const crypto = require("crypto");
hash=crypto.getHashes();
cadena="Hola";
hashcadena=crypto.createHash('sha1').update(cadena).digest('hex');
console.log(hashcadena);


// Add headers before the routes are defined
app.use(function (req, res, next) {

  // Website you wish to allow to connect
  res.setHeader('Access-Control-Allow-Origin', 'null');

  // Request methods you wish to allow
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE');

  // Request headers you wish to allow
  res.setHeader('Access-Control-Allow-Headers', 'X-Requested-With,content-type');

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
    connection.all(`SELECT * FROM usuarios`,[], (err, resultado) => {
    if (err) {
      console.log("Error GET/usuarios");
        response.send(err.message);
    }
        console.log(resultado);
        response.status(200).send(resultado);
  });
});

//usuarios GET/id
app.get("/usuarios/:id",(req, response) => {
    console.log(req.params);
    const quote = "\'";
    connection.all('SELECT * FROM usuarios where id='+quote+Object.values(req.params)+quote, (err, rows) => {
    if (err) {
        response.send(err.message);
        console.log("Error GET/usuarios/id");
    }
    else{
        console.log(rows);
        response.write(rows);
        response.end();
        response.send(rows);
    }
});
});

app.get("/login",jsonParser,(req,response)=> {
  console.log("recibido")
  console.log(req.body);
  // response.writeHead(200,{'Content-Type':'text/plain'});
  // response.write('index.html');
  // response.end();
  response.write('hola');
  response.end();
    // connection.all('SELECT * FROM usuarios where username='+req.body.username+"' AND password='"+req.body.password+"'", (err, rows) => {
    // if (err) {
    //     response.send(err.message);
    //     console.log("Error GET/usuarios/id");
    // }
    // else{
    //   if (rows)
    //     console.log(rows);
    //     response.send(rows);
    // }  
//});
});

//usuarios POST
app.post("/usuarios",jsonParser,(req, response) => {
  console.log('Añadiendo usuario:',[req.body.id,req.body.username,req.body.password])

  //cifrado irreversible
  hash=crypto.getHashes();
  cadena=req.body.password;
  hashcadena=crypto.createHash('sha1').update(cadena).digest('hex');
  console.log(hashcadena);

  try{
    connection.run(`INSERT INTO usuarios VALUES(?, ?, ?)`,[req.body.id,req.body.username,hashcadena], (err, rows) => {
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

    //cifrado irreversible
    hash=crypto.getHashes();
    cadena=req.body.password;
    hashcadena=crypto.createHash('sha1').update(cadena).digest('hex');
    console.log(hashcadena);
    
    connection.run('Update usuarios set id=?,username=?, password=? where id=?',[req.body.id,req.body.username,hashcadena,req.body.id], (err, rows) => {
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