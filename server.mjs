import { createServer } from 'node:http';
import admin from 'firebase-admin';
import * as path from 'path';

// Initialize Firebase Admin SDK
import serviceAccount from './serviceAccountKey.json' assert { type: "json" };

admin.initializeApp({
    credential: admin.credential.cert(serviceAccount)
});
const db = admin.firestore();

// Create the server
const server = createServer(async (req, res) => {
    const url = new URL(req.url, `http://${req.headers.host}`);

    if (url.pathname === '/home') {
        res.writeHead(200, { 'Content-Type': 'text/plain' });
        res.end('Welcome home!\n');
    } else if (url.pathname === '/task') {
        res.writeHead(200, { 'Content-Type': 'text/plain' });
        res.end('Do the task!\n');
    } else if (url.pathname.startsWith('/api/')) {
        const docId = url.pathname.substring('/api/'.length);
        try {
            const doc = await db.collection('results').doc(docId).get();

            if (!doc.exists) {
                res.writeHead(404, { 'Content-Type': 'text/plain' });
                res.end('Document not found\n');
                return;
            }

            const data = doc.data();
            const timestamp = data.time.toDate().toLocaleString('en-PH', { timeZone: 'Asia/Manila', dateStyle: 'full', timeStyle: 'long' }); // Format Firestore timestamp
            const result = data.result;
            const summary = data.summary;

            // Construct HTML to display the data
            let html = `
                <h1>Firestore Document Data</h1>
                <h3>Timestamp: ${timestamp}</h3>
                <pre>Summary: ${summary}</pre>
                <h4>Results:</h4>
                <ul>
            `;

            Object.entries(result).forEach(([domain, status]) => {
                html += `<li>${domain}: ${status}</li>`;
            });

            html += `</ul>`;

            res.writeHead(200, { 'Content-Type': 'text/html' });
            res.end(html);
        } catch (error) {
            res.writeHead(500, { 'Content-Type': 'text/plain' });
            res.end('Error retrieving document: ' + error.message);
        }
    } else {
        res.writeHead(200, { 'Content-Type': 'text/plain' });
        res.end('Test!\n');
    }
});

// Start the server on port 3000
server.listen(3000, 'replace with your own domain', () => {
    console.log('Server is running on yourdomain:3000');
});
