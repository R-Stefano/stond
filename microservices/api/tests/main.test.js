const expect  = require('chai').expect;
const app = require('../app.js')
const sinon = require('sinon')
const axios = require('axios')
const fs = require('fs')
const moment = require('moment')
const { v1: uuidv1 } = require('uuid');

const stubAPI = false;

describe("Test Upload Sensors Data", function() {
    afterEach(function() {
        sinon.restore();
    })

    it('Register Device', async (done) => {

        const resp = await axios.post('http://localhost:8080/api/devices', {
            id: uuidv1()
        })
        console.log(resp.data)
        expect(response.status).to.equal(200)
        //expect(response.data).to.equal(200)

        //done()
        return Promise.resolve()
    }).timeout(60000);

    it.only('Upload Snapshot', async (done) => {
        try {
            let resp = await axios.post('http://localhost:8080/api/devices', {
                id: uuidv1()
            })
            const device = resp.data

            resp = await axios.post(`http://localhost:8080/api/devices/${device.id}/snapshot`, {
                deviceId: device.id,
                readings: [
                    {'componentName': 'led',                'timestamp': moment().toISOString(), 'isWorking': 1,       'status': 'on', 'value': 1},
                    {'componentName': 'humidifier',         'timestamp': moment().toISOString(), 'isWorking': 1,       'status': 'on', 'value': 1},
                    {'componentName': 'hvac',               'timestamp': moment().toISOString(), 'isWorking': 1,       'status': 'on', 'value': 'heater'},
                    {'componentName': 'fan_bottom',         'timestamp': moment().toISOString(), 'isWorking': 1,       'status': 'on', 'value': 50}, 
                    {'componentName': 'fan_top',            'timestamp': moment().toISOString(), 'isWorking': 1,       'status': 'on', 'value': 100}, 
                    {'componentName': 'cpu_temperature',    'timestamp': moment().toISOString(), 'isWorking': 1,       'status': 'on', 'value': 30},
                    {'componentName': 'camera',             'timestamp': moment().toISOString(), 'isWorking': 1,       'status': 'on', 'value': 'imageBase64'},
                    {'componentName': 'env_temperature',    'timestamp': moment().toISOString(), 'isWorking': 1,       'status': 'on', 'value': 45},
                    {'componentName': 'env_humidity',       'timestamp': moment().toISOString(), 'isWorking': 1,       'status': 'on', 'value': 89},
                    {'componentName': 'water_temperature',  'timestamp': moment().toISOString(), 'isWorking': 1,       'status': 'on', 'value': 15},
                    {'componentName': 'water_level',        'timestamp': moment().toISOString(), 'isWorking': 1,       'status': 'on', 'value': 1},
                    {'componentName': 'water_ph',           'timestamp': moment().toISOString(), 'isWorking': 1,       'status': 'on', 'value': 7.89},
                ]
            })
        } catch (e) {
            console.log(e)
        }
        console.log(resp.data)
        expect(response.status).to.equal(200)
        //expect(response.data).to.equal(200)

        done()
        return Promise.all()
    }).timeout(60000);

    /*
    it('Upload snapshot', async (done) => {
        if (stubAPI) {
            sinon.stub(axios, "get").resolves(Promise.resolve({data: JSON.parse(fs.readFileSync('./tests/data/shopify/api_products.json', 'utf-8'))}));
        }

        const resp = await axios.put('http://localhost:8080/api/devices/e0db0991-5c15-4a98-bd05-7ed14cefbca5/status', {sensors: [
            {name: 'env_humidity', value: 0.00, isWorking: true},
            {name: 'water_temperature', value: 0.00, isWorking: true},
            {name: 'env_temperature', value: 0.00, isWorking: true},
            {name: 'water_ph', value: 0.00, isWorking: true},
            {name: 'water_level', value: 0.00, isWorking: true}
        ]})
        console.log(resp)

        //.then((response) => {
        //    expect(response.status).to.equal(200)
        //    done();
        //})

        return Promise.all()
    }).timeout(60000);

    it.only('Get Sensor Details', async () => {
        if (stubAPI) {
            sinon.stub(axios, "get").resolves(Promise.resolve({data: JSON.parse(fs.readFileSync('./tests/data/shopify/api_products.json', 'utf-8'))}));
        }

        const resp = await axios.get('http://localhost:8080/api/devices/e0db0991-5c15-4a98-bd05-7ed14cefbca5/sensors/2c7ffa6e-0163-4284-a3dd-10e0f123b523')
        console.log(resp.data.readings)

        return Promise.resolve()
        //.then((response) => {
        //    expect(response.status).to.equal(200)
        //    done();
        //})

        return Promise.all()
    }).timeout(60000);
    */
})