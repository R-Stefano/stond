const express = require('express');
const router = express.Router();
const service = require('../services/main')

router.get("/:Id/status", async (req, response, next) => {
    const deviceId = req.params.Id
    try {
        const sensors = await service.sensors.get(deviceId)
        const actuators = await service.actuators.get(deviceId)
        const data = {
            deviceId: deviceId,
            sensors: {},
            actuators: {}
        }

        sensors.map(sensor => data.sensors[sensor.name] = {
            value: sensor.currentValue,
            isWorking: sensor.isWorking
        })
        actuators.map(actuator => data.actuators[actuator.name] = {
            status: actuator.status,
            isWorking: actuator.isWorking
        })

        response.status(200).json(data)
    } catch (e) {
        next(e)
    }

    return
})

router.put("/:Id/status", async (req, response, next) => {
    const deviceId = req.params.Id

    try {
        await service.sensors.update(deviceId, req.body.sensors)
        await service.actuators.update(deviceId, req.body.actuators)
        response.status(200).json("ok")
    } catch (e) {
        next(e)
    }

    return
})

module.exports = router;
