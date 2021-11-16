const db = require('../libs/db')
const Op = require('sequelize').Op;
const configs = require('../configs')

exports.update = async (deviceId, statuses) => {
    // Save values to DB
    await Promise.all(statuses.map(actuatorStatus => db.actuator.update({status: actuatorStatus.status, isWorking: actuatorStatus.isWorking}, {where: {deviceId: deviceId, name: actuatorStatus.name}})))

    return Promise.resolve()
}

exports.get = async (deviceId) => {
    return db.actuator.findAll({where: {deviceId: deviceId}})
}
