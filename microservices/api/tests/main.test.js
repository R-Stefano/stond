const expect  = require('chai').expect;
const app = require('../app.js')
const sinon = require('sinon')
const axios = require('axios')
const fs = require('fs')

const stubAPI = false;

describe("Test Upload Sensors Data", function() {
    afterEach(function() {
        sinon.restore();
    })

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
})