const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');

// Fake database for support requests (in-memory)
let supportRequests = [];

const app = express();
const PORT = 3000;

app.use(cors());
app.use(bodyParser.json());

// Home route
app.get('/', (req, res) => {
    res.send('Cyber Guardians API is running!');
});

// Scan Endpoint (simulate scanning a URL or QR)
app.post('/api/scan', (req, res) => {
    const { input } = req.body;
    // Simulate detection logic
    if (!input) {
        return res.status(400).json({ status: 'error', message: 'No input provided' });
    }
    // Super simple: treat anything with "phish" as phishing
    const isPhishing = input.toLowerCase().includes('phish');
    res.json({
        status: 'success',
        result: isPhishing ? 'dangerous' : 'safe',
        reason: isPhishing ? 'Phishing detected!' : 'No threat detected.'
    });
});

// Support endpoint (collect support requests)
app.post('/api/support', (req, res) => {
    const { name, email, message } = req.body;
    if (!name || !email || !message) {
        return res.status(400).json({ status: 'error', message: 'All fields required' });
    }
    supportRequests.push({ name, email, message, date: new Date() });
    res.json({ status: 'success', message: 'Support request received! Our team will contact you soon.' });
});

// Get all support requests (for admin use)
app.get('/api/support', (req, res) => {
    res.json({ status: 'success', data: supportRequests });
});

app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});