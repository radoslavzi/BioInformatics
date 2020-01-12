var express = require('express'),
    app = express(),
    port = process.env.PORT || 3003,
    bodyParser = require('body-parser')
    // querystring = require('querystring');

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json())

var routes = require('./api/routes/router');
routes(app);

app.listen(port);

console.log(`sequence RESTful API server started on: http://www.localhost:${port}`);