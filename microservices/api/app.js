var express = require('express')
const configs = require('./configs.js')
const logger = require('./libs/logger')
const cors = require('cors')
const jwt = require('jsonwebtoken');
const compression = require('compression');

const service = require('./services/main')
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

const server = app.listen(port, function () {
  console.log('App listening on port 8080!')
})

// Socket setup
const io = require("socket.io")(server, {
  cors: {
    origin: '*'
  }
})

io.on("connection", function (socket) {
  console.log("Made socket connection");

  socket.on("login", function (data) {
    console.log(`Device Login: ${data.deviceId}`)
    socket.deviceId = data.deviceId
    socket.join(data.deviceId);
  });

  socket.on("device:ventilation:put", async (data) => {
    console.log('device:ventilation:put')
    console.log(socket.deviceId, data)
    await service.device.ventilation(socket.deviceId, data.status)
    io.to(socket.deviceId).emit('event', {name: 'device/ventilation', data: {deviceId: socket.deviceId, value: data.status}});
  });

  socket.on("device:light:put", async (data) => {
    console.log('device:light:put')
    console.log(socket.deviceId, data)
    await service.device.light(socket.deviceId, data.status)
    io.to(socket.deviceId).emit('event', {name: 'device/light', data: {deviceId: socket.deviceId, value: data.status}});
  });

  socket.on("disconnect", () => {
    io.emit("user disconnected", socket.userId);
  });
});

module.exports = app; // for testing

