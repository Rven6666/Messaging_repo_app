const https = require('https');
const fs = require('fs');
const express = require('express');
const app = express();

const certDirectory = './certs/';

const sslOptions = {
  key: fs.readFileSync(`${certDirectory}key.pem`),
  cert: fs.readFileSync(`${certDirectory}cert.pem`)
  };
  
  // Define the port to run the HTTPS server on
  const PORT = 5000;
  
  // Example route
  app.get('/', (req, res) => {
  res.send('Hello over HTTPS!');
  });
  
  // Create HTTPS server
  https.createServer(sslOptions, app)
  .listen(PORT, () => {
  console.log(`HTTPS server running on https://127.0.0.1:${PORT}`);
  });
