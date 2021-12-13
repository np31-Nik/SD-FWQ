const express = require("express");
const app = express();
// Se define el puerto
const port=3000;
app.get("/",(req, res) => {
res.json({message:'Página de inicio de aplicación de ejemplo de SD'})
});
// Ejecutar la aplicacion
app.listen(port, () => {
console.log(`Ejecutando la aplicación API REST de SD en el puerto
${port}`);
});