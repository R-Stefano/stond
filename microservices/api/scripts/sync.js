const path = require('path')
const axios = require('axios')
configs = require('../configs.js')

if (process.argv.includes("production")) {
    configs.sql.host = "34.89.32.113"
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
    console.log(configs)
    await db.sequelize.sync({force: true})
}

run()
