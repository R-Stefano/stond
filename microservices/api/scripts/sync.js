const path = require('path')
const axios = require('axios')
configs = require('../configs.js')

if (process.argv.includes("production")) {
    configs.sql.host = "35.189.95.166"
    configs.sql.database = "stond"
    configs.sql.username = "root"
    configs.sql.password = "root"
} else if (process.argv.includes("staging")) {
    configs.sql.host = "35.189.121.159"
    configs.sql.database = ""
    configs.sql.username = "root"
    configs.sql.password = "root"
    configs.cloud.bucket_name = ""
} else {
    console.log("Syncing Local DB")
}

const db = require('../libs/db')
const { Op } = require("sequelize");

/*
const {Storage} = require('@google-cloud/storage');
const storage = new Storage({keyFilename: path.resolve(__dirname, '../../' + configs.cloud.bucket_auths)});
const GCBucket = storage.bucket(configs.cloud.bucket_name);
*/


async function run() {
    await db.sequelize.sync({force: true})

    const sensors = [
        {name: 'env_temperature',   deviceId: 'e0db0991-5c15-4a98-bd05-7ed14cefbca5', currentValue: null, isWorking: 1},
        {name: 'env_humidity',      deviceId: 'e0db0991-5c15-4a98-bd05-7ed14cefbca5', currentValue: null, isWorking: 1},
        {name: 'water_temperature', deviceId: 'e0db0991-5c15-4a98-bd05-7ed14cefbca5', currentValue: null, isWorking: 1},
        {name: 'water_level',       deviceId: 'e0db0991-5c15-4a98-bd05-7ed14cefbca5', currentValue: null, isWorking: 1},
        {name: 'water_ph',          deviceId: 'e0db0991-5c15-4a98-bd05-7ed14cefbca5', currentValue: null, isWorking: 1},
    ]

    await Promise.all(sensors.map(sensor => db.sensor.findOrCreate({where: {name: sensor.name, deviceId: sensor.deviceId}, defaults: {name: sensor.name, deviceId: sensor.deviceId, currentValue: null, isWorking: sensor.isWorking}})))

    const actuators = [
        {name: 'ventilation',          deviceId: 'e0db0991-5c15-4a98-bd05-7ed14cefbca5', status: 'OFF', isWorking: 1, statusChangedAt: new Date()},
        {name: 'LED',                  deviceId: 'e0db0991-5c15-4a98-bd05-7ed14cefbca5', status: 'OFF', isWorking: 1, statusChangedAt: new Date()},

    ]
    await Promise.all(actuators.map(actuator => db.actuator.findOrCreate({where: {name: actuator.name, deviceId: actuator.deviceId}, defaults: {name: actuator.name, deviceId: actuator.deviceId, status: null, isWorking: actuator.isWorking, statusChangedAt: actuator.statusChangedAt}})))

    console.log("DONE!")
}

run()
