const db = require('../libs/db')
const Op = require('sequelize').Op;
const configs = require('../configs')

exports.ventilation = async (deviceId, status) => {

    console.log("Updating")
    await new Promise(resolve => setTimeout(resolve, 2000));
    console.log("returning")

    return Promise.resolve()
}

exports.light = async (deviceId, status) => {

    console.log("Updating")
    await new Promise(resolve => setTimeout(resolve, 2000));
    console.log("returning")

    return Promise.resolve()
}