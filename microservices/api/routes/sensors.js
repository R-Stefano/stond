const express = require('express');
const router = express.Router();
const logger=require('../libs/logger.js')
const service = require('../services/main')

router.post("/", function(req, response) {
    const {timestamp, env_temperature, env_humidity, cpu_temperature} = req.body

    Promise.all([
        service.sensors.add(timestamp, env_temperature, env_humidity, cpu_temperature)
    ])
    .then(results => {
        response.status(200).json("ok")
    })
    .catch((e) => {
        logger.warn(e.message)
        response.status(500).send(e.message);
    })
    return
})

module.exports = router;
