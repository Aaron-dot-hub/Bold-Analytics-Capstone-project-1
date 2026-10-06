const express = require('express');
const { Pool } = require('pg');
const cors = require('cors');
const dotenv = require('dotenv');

dotenv.config();

const app = express();

//  Global Middleware Configurations
app.use(cors());
app.use(express.json());
app.use(express.static('public')); // Hosts your frontend dashboard seamlessly

//  Initialize connection pool to PostgreSQL using our .env variables
const pool = new Pool({
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME,
    port: process.env.DB_PORT,
});

const PORT = process.env.PORT || 5000;

//  API Authentication Middleware with Deep Logging
const authenticateB2B = async (req, res, next) => {
    const apiKey = req.headers['x-api-key'];
    console.log(` Auth Attempt - Received API Key: "${apiKey}"`);
    
    if (!apiKey) {
        console.log(" Auth Failed: No API Key provided in headers.");
        return res.status(401).json({ error: 'Access Denied: Missing API Key inside x-api-key header.' });
    }

    try {
        const clientCheck = await pool.query('SELECT * FROM b2b_clients WHERE api_key = $1 AND is_active = true', [apiKey]);
        
        if (clientCheck.rows.length === 0) {
            console.log(` Auth Failed: Key "${apiKey}" does not exist or is inactive in DB.`);
            return res.status(403).json({ error: 'Unauthorized: Invalid API Key.' });
        }
        
        req.client = clientCheck.rows[0];
        console.log(` Auth Success: Welcome ${req.client.company_name}`);
        next();
    } catch (err) {
        console.error(" SYSTEM DATABASE ERROR INSIDE MIDDLEWARE:", err.message);
        return res.status(500).json({ error: 'Internal Security Authentication Fault.', details: err.message });
    }
};

//  Automated Traffic Analytics & Performance Logger Middleware
const logAPIMetrics = (req, res, next) => {
    // Capture the exact high-resolution start time of the incoming request
    const startTime = process.hrtime();

    // Intercept the response finish event to calculate query duration
    res.on('finish', async () => {
        // Skip logging if the request failed authentication or has no verified client attached
        if (!req.client) return;

        const diff = process.hrtime(startTime);
        // Convert high-resolution time array directly to milliseconds
        const responseTimeMs = Math.round((diff[0] * 1e3) + (diff[1] * 1e-6));

        try {
            await pool.query(
                `INSERT INTO api_logs (client_id, endpoint, response_time_ms, status_code) 
                 VALUES ($1, $2, $3, $4)`,
                [req.client.id, req.baseUrl + req.path, responseTimeMs, res.statusCode]
            );
            console.log(` Metrics Logged: ${req.baseUrl + req.path} took ${responseTimeMs}ms | Status: ${res.statusCode}`);
        } catch (err) {
            console.error("💥 Failed to write to telemetry logs:", err.message);
        }
    });

    next();
};

// --- B2B SAAS API ROUTES ---

// Get All States
app.get('/api/v1/locations/states', authenticateB2B, logAPIMetrics, async (req, res) => {
    console.log(" Incoming request received for /states from:", req.client.company_name);
    try {
        const result = await pool.query('SELECT id, state_name FROM states ORDER BY state_name ASC');
        res.json({ client: req.client.company_name, data: result.rows });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// Get Districts matching state_id
app.get('/api/v1/locations/districts/:state_id', authenticateB2B, logAPIMetrics, async (req, res) => {
    try {
        const result = await pool.query('SELECT id, district_name FROM districts WHERE state_id = $1 ORDER BY district_name ASC', [req.params.state_id]);
        res.json({ data: result.rows });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// Get Sub-Districts matching district_id
app.get('/api/v1/locations/subdistricts/:district_id', authenticateB2B, logAPIMetrics, async (req, res) => {
    try {
        const result = await pool.query('SELECT id, sub_district_name FROM sub_districts WHERE district_id = $1 ORDER BY sub_district_name ASC', [req.params.district_id]);
        res.json({ data: result.rows });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// Get Villages matching sub_district_id
app.get('/api/v1/locations/villages/:sub_district_id', authenticateB2B, logAPIMetrics, async (req, res) => {
    try {
        const result = await pool.query('SELECT id, village_name, pincode FROM villages WHERE sub_district_id = $1 ORDER BY village_name ASC LIMIT 500', [req.params.sub_district_id]);
        res.json({ data: result.rows });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

//  TEMPORARY BROWSER DIAGNOSTIC ROUTE
app.get('/api/v1/test-data', async (req, res) => {
    try {
        console.log(" Browser diagnostic route triggered!");
        const result = await pool.query('SELECT id, state_name FROM states ORDER BY state_name ASC LIMIT 10');
        res.json({ 
            success: true, 
            message: "Database connection is running perfectly!", 
            sample_states: result.rows 
        });
    } catch (err) {
        console.error(" Diagnostic Route Error:", err.message);
        res.status(500).json({ error: err.message });
    }
});


//  ADMIN METRICS DATA STREAMING ENDPOINT
app.get('/api/v1/admin/metrics', async (req, res) => {
    try {
        // Query 1: Calculate global aggregations
        const summaryRes = await pool.query(`
            SELECT 
                COUNT(*)::INT as total_requests,
                ROUND(AVG(response_time_ms))::INT as avg_latency
            FROM api_logs
        `);

        // Query 2: Aggregate hits grouped by specific endpoints
        const endpointRes = await pool.query(`
            SELECT 
                endpoint,
                COUNT(*)::INT as hits,
                ROUND(AVG(response_time_ms))::INT as avg_speed,
                MAX(status_code) as last_status
            FROM api_logs
            GROUP BY endpoint
            ORDER BY hits DESC
        `);

        res.json({
            summary: summaryRes.rows[0] || { total_requests: 0, avg_latency: 0 },
            breakdown: endpointRes.rows
        });
    } catch (err) {
        console.error(" Admin Metrics Collection Error:", err.message);
        res.status(500).json({ error: err.message });
    }
});


// Start up the core server engine
app.listen(PORT, () => {
    console.log(` Capstone Server operational on port ${PORT}`);
});