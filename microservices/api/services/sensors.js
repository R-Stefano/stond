const db = require('../libs/db')
const Op = require('sequelize').Op;
const configs = require('../configs')
const moment = require('moment')

exports.get = async (sensorId, params) => {
    const query = {
        where: {
            Id: sensorId
        },
    }

    return db.sensor.findOne(query)
}   

exports.getHistory = async (sensorId, params) => {
    const query = {
        where: {
            sensorId: sensorId
        },
        order: [
            ['timestamp', 'asc']
        ]
    }

    if (params.timestamp) {
        query.where['$timestamp$'] = {[Op.gte]: params.timestamp}
    }
    
    return db.sensorReading.findAll(query)
}

exports.update = async (deviceId, measurements) => {
    /**
     * deviceId: string
     * measurements: Measurement[]
     * 
     * Measurement: {
     *  name: string
     *  value: number
     *  isWORKING: boolean
     * }
     */

    // Save values to DB
    await Promise.all(measurements.map(measurement => db.sensor.update({currentValue: measurement.value, isWorking: measurement.isWorking}, {where: {deviceId: deviceId, name: measurement.name}})))

    // add to history data
    const sensors = await db.sensor.findAll({where: {deviceId: deviceId}})
    await Promise.all(measurements.map(measurement => {
        const sensor = sensors.find(sensor => sensor.name == measurement.name)
        return db.sensorReading.create({value: measurement.value, isWorking: measurement.isWorking, timestamp: moment(measurement.timestamp).set('second', 0), sensorId: sensor.Id})
    }))
    return Promise.resolve()
}
