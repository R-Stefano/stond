const db = require('../libs/db')
const Op = require('sequelize').Op;
const configs = require('../configs')

exports.update = async (deviceId, measurements) => {
    // Save values to DB
    await Promise.all(measurements.map(measurement => db.sensor.update({currentValue: measurement.value, isWorking: measurement.isWorking}, {where: {deviceId: deviceId, name: measurement.name}})))

    return Promise.resolve()
}

exports.get = async (deviceId) => {
    return db.sensor.findAll({where: {deviceId: deviceId}})
}
