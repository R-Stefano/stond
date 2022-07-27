const db = require('../libs/db')
const Op = require('sequelize').Op;
const configs = require('../configs')
const moment = require('moment')
const service = require('./main')

exports.ventilation = async (deviceId, status) => {
    await new Promise(resolve => setTimeout(resolve, 2000));

    return Promise.resolve()
}

exports.light = async (deviceId, status) => {
    await new Promise(resolve => setTimeout(resolve, 2000));

    return Promise.resolve()
}

exports.getSensors = async (deviceId) => {
    return db.sensor.findAll({where: {deviceId: deviceId}})
}

exports.uploadSnapshot = async (deviceId, data) => {
    /**
     * data: {
     *  base64:    string
     *  isWorking: boolean
     *  timestamp: datetime
     * }
     */
    console.log(deviceId)
    console.log(data)
    
    // save to google cloud if data available
    const filename = data.base64 ? await service.gcloud.save(data.base64, 'jpg') : null  

    const sensors = await db.sensor.findAll({where: {deviceId: deviceId}})
    const sensor = sensors.find(sensor => sensor.name == 'camera')
    
    await db.sensor.update({currentFilename: filename, isWorking: data.isWorking}, {where: {id: sensor.Id}})
    return db.sensorReading.create({filename: filename, isWorking: data.isWorking, timestamp: moment(data.timestamp).set('second', 0), sensorId: sensor.Id})
}