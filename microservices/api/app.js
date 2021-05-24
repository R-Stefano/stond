var express = require('express')
const configs = require('./configs.js')
const logger = require('./libs/logger')
const cors = require('cors')
const jwt = require('jsonwebtoken');
const compression = require('compression');
var app = express()

app.use(express.json({limit: "50mb"}));
app.use(express.urlencoded({limit: "50mb", extended: true, parameterLimit:50000}));
app.use(compression());
app.use(cors())

/**
 * INTERNAL VARIABLES
 */
const port = configs.port

// Received HTTP request, check if JWT Valid
app.use(function (req, res, next) {
  logger.info(`Request: ${req.method} ${req.url}`)

  next()
  return
  /*

  // Get JWT Token in HTTP request header
  const token = req.headers['authorization'] ? req.headers['authorization'].split(" ")[1] : ''

  // Verify token
  jwt.verify(token, configs.jwt.secret, function(err, decoded) {
      if (err) {
          res.status(401).send({"error": {"message": err.message}});
      } else {
          req.headers.token_decoded = decoded
          next() //pass request to next middleware
      }
  });
  */
})


const sensors = require('./routes/sensors')

app.use('/api/sensors', sensors)

app.listen(port, function () {
  console.log('App listening on port 8080!')
})

module.exports = app; // for testing

