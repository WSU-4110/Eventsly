const { Pool } = require('pg');
const conn = new Pool({ connectionString: process.env.DATABASE_URL });

async function listEvents(req, res) {
    try {
        const db = await conn.connect()
        const result = await db.query('SELECT * FROM events');
        const results = { users: (result) ? result.rows : null};
        res.render('pages/index', results );
        db.release();
    } catch (err) {
        console.error(err);
        res.send("Error " + err);
    }
}