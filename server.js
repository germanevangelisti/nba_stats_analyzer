const express = require('express');
const { exec } = require('child_process');
const path = require('path');
const fs = require('fs');
const app = express();
const port = process.env.PORT || 3000;

// Iniciar la aplicación Dash en segundo plano
const startDashApp = () => {
  return new Promise((resolve, reject) => {
    console.log('Iniciando aplicación Dash...');
    const dashProcess = exec('python app.py', (error, stdout, stderr) => {
      if (error) {
        console.error(`Error al ejecutar Dash: ${error}`);
        return reject(error);
      }
      console.log(`Salida de Dash: ${stdout}`);
      if (stderr) console.error(`Error de Dash: ${stderr}`);
    });

    // Dar tiempo para que Dash se inicie
    setTimeout(() => resolve(dashProcess), 5000);
  });
};

// Ruta principal que redirige a la aplicación Dash
app.get('/', (req, res) => {
  res.send(`
    <!DOCTYPE html>
    <html>
    <head>
      <title>NBA Stats Analyzer</title>
      <meta http-equiv="refresh" content="0;url=http://localhost:8050">
      <style>
        body {
          font-family: Arial, sans-serif;
          text-align: center;
          margin-top: 50px;
        }
      </style>
    </head>
    <body>
      <h1>Redirigiendo a NBA Stats Analyzer...</h1>
      <p>Si no eres redirigido automáticamente, <a href="http://localhost:8050">haz clic aquí</a>.</p>
    </body>
    </html>
  `);
});

// Iniciar el servidor
startDashApp()
  .then(() => {
    app.listen(port, () => {
      console.log(`Servidor proxy iniciado en http://localhost:${port}`);
      console.log('Redirigiendo a la aplicación Dash en http://localhost:8050');
    });
  })
  .catch(err => {
    console.error('Error al iniciar la aplicación:', err);
  }); 