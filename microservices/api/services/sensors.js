const db = require('../libs/db')
const Op = require('sequelize').Op;

exports.add = async (timestamp, env_temperature, env_humidity, cpu_temperature) => {
    // Save values to DB
    //await 

    await exports.checkValues(env_temperature, env_humidity)

    return Promise.resolve()
}

exports.checkValues = async (env_temperature, env_humidity) => {
    console.log(env_temperature, env_humidity)
    let messages = [] 
    if (env_temperature < 18 || env_temperature > 25) {
        messages.push(`Env Temperature at ${env_temperature}°C\n`)
    }

    if (env_humidity < 40 || env_humidity > 80) {
        messages.push(`Env Humidity at ${env_humidity} %\n`)
    }

    if (messages.length > 0) {
        console.log("SENDING MESSAGE:")
        let txt = "WARNING\n"
        txt = messages.reduce((fullTxt, message) => fullTxt += message, txt)
        console.log(txt)
    }

    return Promise.resolve()
}