const express = require('express');
const path = require('path');
const fs = require('fs');
const bodyParser = require('body-parser');
var busboy = require('connect-busboy');

const app = express();
app.use(bodyParser.urlencoded({extended:false})); //handle body requests
app.use(bodyParser.json()); // let's make JSON work too!
app.use(busboy());

// Serve static files from the React app
// app.use(express.static(path.join(__dirname, 'client/build')));

// Put all API endpoints under '/api'
app.get('/:name', (req, res) => {
	const hello = "hi ";
	var name = req.params.name;
	

	// Return them as json
  	res.json(hello+name);
  	console.log(`Sent ${hello} message to ${name}`);
	});

// Upload
app.post('/upload', (req, res, next) => {
	console.log("sending file???");
	if(req.busboy) {
        req.busboy.on("file", function(fieldName, fileStream, fileName, encoding, mimeType) {
            //Handle file stream here
            // console.log(mimeType);
            if (mimeType == "audio/mpeg") {
            	console.log("audio");
            } else if (mimeType == "text/plain") {
            	console.log("text")
            	fileStream.setEncoding('utf-8');
	            fileStream.on('data', function(data) {
	            	res.json(data);
	            });
            }
            
        });
        return req.pipe(req.busboy);
    }
    console.log("SOMETHING WENT WRONG")	
});

// The "catchall" handler: for any request that doesn't
// match one above, send back React's index.html file.
app.get('*',(req, res) => {
	console.log("You are a fool!! Error");
	res.json("error");
  // res.sendFile(path.join(__dirname+'/client/build/index.html'));
});

const port = process.env.PORT || 5000;
app.listen(port);

console.log(`lucie is listening on ${port}`);