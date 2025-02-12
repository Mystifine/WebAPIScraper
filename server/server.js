//https://pokeapi.co/?ref=public_apis
const express = require('express');
const fs = require('fs');
const path = require("path");

const app = express();
const port = 5200;

// Serve static files from react app
app.use(express.static(path.join(__dirname,  'client/build')));

// When a client connects with the root of the server
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'client/build', 'index.html'))
});

// Start the server by listening to the port.
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
})