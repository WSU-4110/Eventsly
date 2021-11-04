var findThis;
const { Pool } = require('pg');
const conn = new Pool({ connectionString: process.env.DATABASE_URL });

async function listEvents(req, res) {
    try {
        const db = await conn.connect();
        const result = await db.query('SELECT title FROM events order by title LIMIT 10');
        const results = { events: (result) ? result.rows : null};
        res.render('pages/search', results );
        document.getElementById("results").innerHTML = results;
        db.release();
    } catch (err) {
        console.error(err);
        res.send("Error " + err);
    }
}