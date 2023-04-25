const db = require('../libs/db')
const Op = require('sequelize').Op;
const configs = require('../configs')
const moment = require('moment')
const service = require('./main')

exports.create = async (deviceId) => {
    const device = await db.device.create({
        id: deviceId
    })


    // register actuators and sensors
    const availableComponents = [
        {type: 'actuator', name: 'led',                isWorking: 0, status: null, value: null,        valueType: 'boolean'},
        {type: 'actuator', name: 'humidifier',         isWorking: 0, status: null, value: null,        valueType: 'boolean'},
        {type: 'actuator', name: 'hvac',               isWorking: 0, status: null, value: null,        valueType: 'string'},
        {type: 'actuator', name: 'fan_bottom',         isWorking: 0, status: null, value: null,        valueType: 'number'},
        {type: 'actuator', name: 'fan_top',            isWorking: 0, status: null, value: null,        valueType: 'number'},

        {type: 'sensor',   name: 'cpu_temperature',    isWorking: 0, status: null, value: null,        valueType: 'number'},
        {type: 'sensor',   name: 'camera',             isWorking: 0, status: null, value: null,        valueType: 'string'},
        {type: 'sensor',   name: 'env_temperature',    isWorking: 0, status: null, value: null,        valueType: 'number'},
        {type: 'sensor',   name: 'env_humidity',       isWorking: 0, status: null, value: null,        valueType: 'number'},
        {type: 'sensor',   name: 'water_temperature',  isWorking: 0, status: null, value: null,        valueType: 'number'},
        {type: 'sensor',   name: 'water_level',        isWorking: 0, status: null, value: null,        valueType: 'boolean'},
        {type: 'sensor',   name: 'water_ph',           isWorking: 0, status: null, value: null,        valueType: 'number'},
    ]

    await Promise.all(availableComponents.map(component => {
        component.deviceId = deviceId
        return db.component.create(component)
    }))

    return service.device.getById(deviceId)
}

exports.getById = async (deviceId) => {
    return db.device.findOne({
        where: {
            id: deviceId
        },
        include: [
            {model: db.component, as: 'components'}
        ]
    })
}


exports.uploadSnapshot = async (deviceId, data) => {
    /**
     * data: {
     *  deviceId:  string,
     *  readings: [{
     *      componentName: string,
     *      timestamp: isoDate
     *      isWorking: boolean
     *      status:    string
     *      value:     string
     *  }],
     * }
     * 
     *  since data may come in different orders due to connection problems
     *  1. Process images
     *  2. save all data received
     *  3. update the component state using the most recent reading
     *  4. set device.lastSnapshotReceivedAt with current timestamp to keep track of last time received data
     */
    // process images
    const cameraReadings = data.readings.filter(reading => reading.componentName == 'camera')
    for (var cameraReading of cameraReadings) {
        // save to google cloud if data available
        const filename = await service.gcloud.save(cameraReading.value, 'jpg')  

        //set the reading value as the filename
        const readingRef = data.readings.find(reading => (reading.componentName == 'camera' && reading.timestamp == cameraReading.timestamp))
        readingRef.value = filename
    }

    const deviceComponents = await db.component.findAll({where: {deviceId: deviceId}})

    //save all data received
    await Promise.all(data.readings.map(reading => {
        const component = deviceComponents.find(c => c.name == reading.componentName)
        return db.reading.create({
            componentId: component.id,
            timestamp: reading.timestamp,
            isWorking: reading.isWorking,
            status:    reading.status,
            value:     reading.value
        })
    }))

    //update the component state with the most recent
    const componentsUpdated = deviceComponents.filter(comp => data.readings.find(reading => reading.componentName == comp.name))
    const mostRecentReadings = await Promise.all(componentsUpdated.map(component => {
        return db.reading.findOne({
            where: {
                componentId: component.id
            },
            order: [
                ['timestamp', 'desc']
            ]
        })
    }))
    await Promise.all(mostRecentReadings.map(reading => db.component.update({
        isWorking: reading.isWorking,
        status:    reading.status,
        value:     reading.value
    }, {where: {id: reading.componentId}})))

    //update device lastSnapshotReceivedAt
    await db.device.update({lastSnapshotReceivedAt: moment()}, {where: {id: deviceId}})
}