const express = require('express');
const router = express.Router();
const service = require('../services/main')

router.get("/:sensorId", async (req, response, next) => {
    const sensorId = req.params.sensorId
    try {
        const results = await service.sensors.get(sensorId)
        response.status(200).json(results)
    } catch (e) {
        next(e)
    }

    return
})

router.get("/:sensorId/analytics", async (req, response, next) => {
    const sensorId = req.params.sensorId
    const params = req.query
    try {
        const results = await service.sensors.getAnalytics(sensorId, params)
        response.status(200).json(results)
    } catch (e) {
        next(e)
    }

    return
})

module.exports = router;
