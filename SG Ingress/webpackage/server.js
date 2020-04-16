const fs = require("fs");
const bodyParser = require("body-parser");
const express = require("express");
const { PythonShell } = require("python-shell");
const { spawn } = require('child_process');
const host = "127.0.0.1";
const port = 1337;

const app = express();
// Configuring body parser middleware
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());
app.use(express.static(__dirname + "/public")); //use static files in ROOT/public folder

let runPy = () => (
    new Promise((resolve, reject) => {
        // const python = spawn('python', [__dirname + '/sg_rule_addition.py']);
        const python = spawn('python', [__dirname + '/sample.py']);
        python.stdout.on('data', (data) => {
            console.log('Pipe data from python script...');
            console.log(data.toString());
        });

        python.stderr.on('data', (data) => {
            console.log('Found Error!');
            reject(data.toString());
        });

        // in close event we are sure that stream from child process is closed
        python.on('close', (code) => {
            console.log(`child process close all stdio with code ${code}`);
            // send data to browser
            resolve(code);
        });
    })
);


// Go to http://localhost:1337 directly. The file will be send
// No need to open index.html separately
app.get("/", (request, response) => {
    res.sendFile('index.html');
});

app.post("/save", async (request, response) => {
    let req = request.body;
    console.log('Request val', req);

    const jsonContent = JSON.stringify(req);

    // User relative path to save file
    // __dirname + '/params.json' saves file to current directory
    fs.writeFile(__dirname + '/params.json', jsonContent, 'utf8', (err) => {
        if (err) {
            console.log(err);
            response.json({ "status": "error" });
        }
        else {
            runPy().then((successMessage) => {
                response.json({ "status": "ok" });
            })
            .catch((err) => {
                console.log(err);
                response.json({"status": "error"});
            });
        }
    });
});

app.listen(port, host);
