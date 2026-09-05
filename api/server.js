require('dotenv').config();

// Dependencies 
const express = require('express'); 
const fs = require('fs');
const path = require('path');
const csv = require('csv-parser');

const app = express();
const PORT = process.env.PORT || 3000;
const DATA_PATH = path.join(__dirname, '../data/processed');

const cache = {};

const loadCSV = (filename) => {
    if (cache[filename]) return Promise.resolve(cache[filename]);

    return new Promise((resolve, reject) => {
        const rows = [];
        fs.createReadStream(path.join(DATA_PATH, filename), { encoding: 'utf-8' })
            .pipe(csv())
            .on('data', (row) => rows.push(row))
            .on('end', () => {
                cache[filename] = rows;
                resolve(rows);
            })
            .on('error', reject);
    });
};

app.use(express.json());

// Logging
app.use((req, res, next) => {
    console.log(`${req.method} ${req.url}`);
    next();
});

app.get('/', (req, res) => {
    res.json({ message: 'Welcome to Cue' });
});

app.get('/peliculas', async (req, res, next) => {
    try {
        const data = await loadCSV('tmdb_clean.csv');

        const page = Math.max(1, parseInt(req.query.page) || 1);
        const limit = Math.min(100, parseInt(req.query.limit) || 20);
        const start = (page - 1) * limit;

        res.json({
            total: data.length,
            page,
            limit,
            data: data.slice(start, start + limit)
        });
    } catch (err) {
        if (err.code === 'ENOENT') return res.status(404).json({ error: 'File not found' });
        next(err);
    }
});

app.get('/peliculas/:id', async (req, res, next) => {
    try {
        const data = await loadCSV('tmdb_clean.csv');
        const pelicula = data.find((p) => p.id === req.params.id);
        if (!pelicula) return res.status(404).json({ error: 'Movie not found' });
        res.json(pelicula);
    } catch (err) {
        next(err);
    }
});

app.get('/camaras', async (req, res, next) => {
    try {
        const data = await loadCSV('cinema_cameras_clean.csv');
        res.json({total: data.length, data});
    } catch (err) {
        if (err.code === 'ENOENT') return res.status(404).json({ error: 'File not found' });
        next(err);
    }
});

app.get('/generos', async (req, res, next) => {
    try {
        const data = await loadCSV('genre_counts.csv');
        res.json({total: data.length, data});
    } catch (err) {
        if (err.code === 'ENOENT') return res.status(404).json({ error: 'File not found' });
        next(err);
    }
});

app.use((req, res) => {
    res.status(404).json({ error: 'Route not found' });
});

app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({
        error: 'Internal server error',
        message: process.env.NODE_ENV === 'development' ? err.message : undefined
    });
});

app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});