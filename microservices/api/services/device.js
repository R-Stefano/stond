const db = require('../libs/db')
const Op = require('sequelize').Op;
const configs = require('../configs')

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