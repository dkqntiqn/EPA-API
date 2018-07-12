const express = require('express');
const path = require('path');

const app = express();

// Serve static files from the React app
app.use(express.static(path.join(__dirname, 'client/build')));

// Put all API endpoints under '/api'
app.get('/:name', (req, res) => {
	const hello = "hi ";
	var name = req.params.name;
	

	// Return them as json
  	res.json(hello+name);

  	console.log(`Sent ${hello} message to ${name}`);
	});

// The "catchall" handler: for any request that doesn't
// match one above, send back React's index.html file.
app.get('*', (req, res) => {
	console.log("You are a fool!! Error");
  // res.sendFile(path.join(__dirname+'/client/build/index.html'));
});

const port = process.env.PORT || 5000;
app.listen(port);

console.log(`lucie is listening on ${port}`);