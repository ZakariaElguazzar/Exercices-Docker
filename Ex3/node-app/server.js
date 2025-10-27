const express = require('express');
const app = express();
const port = 3000;

// Route d'accueil
app.get('/', (req, res) => {
    res.send('Bienvenue sur la page d’accueil !');
});

// Route health
app.get('/api/health', (req, res) => {
    res.json({ status: 'UP' });
});

// Route info
app.get('/api/info', (req, res) => {
    res.json({
        nodeVersion: process.version,
        platform: process.platform,
        memory: process.memoryUsage()
    });
});

// Route time
app.get('/api/time', (req, res) => {
    res.json({ time: new Date().toISOString() });
});

app.listen(port, () => {
    console.log(`Serveur lancé sur http://localhost:${port}`);
});

