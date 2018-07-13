const express = require('express');
const path = require('path');
const fs = require('fs');
const bodyParser = require('body-parser');
var exec = require('child_process').exec;


const app = express();
app.use(bodyParser.urlencoded({extended:false})); //handle body requests
app.use(bodyParser.json()); // let's make JSON work too!


// Serve static files from the React app
// app.use(express.static(path.join(__dirname, 'client/build')));

// Put all API endpoints under '/api'
app.get('/', (req, res) => {
	var command = "python pythonexample.py"
	var child = exec(command,
		function (error, stdout, stderr){
			console.log('Output -> ' + stdout);
			if(error !== null){
				console.log("Error -> "+error);
			}
	});
  	console.log(`running the python file...`);
	});

app.post('/upload', (req, res) => {
		console.log("recognizing");
		var folder = req.body.folder;
		res.send(folder);
		var command = "java -jar epa.recognizer.jar " + folder + " " + folder;
		// var command = ;
		var child = exec(command,
		  function (error, stdout, stderr){
		    console.log('Output -> ' + stdout);
		    if(error !== null){
		      console.log("Error -> "+error);
		    }
		});

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
