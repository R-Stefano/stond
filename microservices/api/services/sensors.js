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

exports.getAnalytics = async (sensorId, params) => {
    const query = {
        where: {
            sensorId: sensorId
        },
        order: [
            ['timestamp', 'asc']
        ]
    }
    
    if (params.scale) {
        let startDate = moment().utc();
        switch (params.scale) {
            case '1H':
                startDate = startDate.subtract(1, "hours");
                query.where['$timestamp$'] = {[Op.gte]: startDate.format('YYYY-MM-DD HH:mm')}
                break;
            case '6H':
                startDate = startDate.subtract(6, "hours");
                query.where['$timestamp$'] = {[Op.gte]: startDate.format('YYYY-MM-DD HH:mm')}
                break;
            case '1D':
                startDate = startDate.subtract(24, "hours");
                query.where['$timestamp$'] = {[Op.gte]: startDate.format('YYYY-MM-DD HH:mm')}
                break;
            case '30D':
                startDate = startDate.subtract(24*30, "hours");
                query.where['$timestamp$'] = {[Op.gte]: startDate.format('YYYY-MM-DD HH:mm')}
                break;
        }
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
        return db.sensorReading.create({value: measurement.value, isWorking: measurement.isWorking, timestamp: moment().utc(), sensorId: sensor.Id})
    }))
    return Promise.resolve()
}
