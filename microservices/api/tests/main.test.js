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

    it('Upload snapshot', function(done) {
        if (stubAPI) {
            sinon.stub(axios, "get").resolves(Promise.resolve({data: JSON.parse(fs.readFileSync('./tests/data/shopify/api_products.json', 'utf-8'))}));
        }

        axios.post('http://localhost:8080/api/sensors', {timestamp: new Date(), env_temperature: 23.56, env_humidity: 66.78, cpu_temperature: 23.56})
        .then((response) => {
            expect(response.status).to.equal(200)
            done();
        })
    }).timeout(60000);
})