const { response } = require("express");
const express = require("express");
const app = express();
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