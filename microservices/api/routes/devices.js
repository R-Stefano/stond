const express = require('express');
const router = express.Router();
const service = require('../services/main')

router.post("/", async (req, response, next) => {
    const deviceId = req.body.id

    try {
        const device = await service.device.create(deviceId)
        response.status(200).json(device)
    } catch (e) {
        next(e)
    }

    return
})

router.post("/:id/snapshot", async (req, response, next) => {
    try {
        await service.device.uploadSnapshot(req.params.id, req.body)
        response.status(200).json("ok")
    } catch (e) {
        next(e)
    }

    return
})

router.get("/:id/snapshot", async (req, response, next) => {
    const deviceId = req.params.id
    try {
        const data = {
            deviceId: deviceId,
            sensors: {},
            actuators: {}
        }

        response.status(200).json(data)
    } catch (e) {
        next(e)
    }

    return
})

module.exports = router;
