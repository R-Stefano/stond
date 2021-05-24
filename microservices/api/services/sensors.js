const db = require('../libs/db')
const Op = require('sequelize').Op;
const twilio = require('twilio')(configs.twilio.accoundSID, configs.twilio.authToken);
const configs = require('../configs')

exports.add = async (timestamp, env_temperature, env_humidity, cpu_temperature) => {
    console.log(timestamp, env_temperature, env_humidity, cpu_temperature)
    // Save values to DB
    //await 

    await exports.checkValues(env_temperature, env_humidity)

    return Promise.resolve()
}

exports.checkValues = async (env_temperature, env_humidity) => {
    const currentTimestamp = new Date()
    const currentHour = currentTimestamp.getHours() // 0 - 23

    let messages = [] 
    if (env_temperature < 18 && currentHour >= 12) {
        messages.push(`Env Temperature at ${env_temperature}°C\n`)
    }

    if (env_temperature > 30) {
        messages.push(`Env Temperature at ${env_temperature}°C\n`)
    }

    if (env_humidity < 60) {
        messages.push(`Env Humidity at ${env_humidity} %\n`)
    }

    if (messages.length > 0) {
        console.log("WARNING MESSAGE SENT")
        let txt = "WARNING\n"
        txt = messages.reduce((fullTxt, message) => fullTxt += message, txt)
        console.log(txt)
        await twilio.messages.create({
            from: configs.twilio.phoneNumber,
            to: '07522730390',
            body: txt
        })
    }

    return Promise.resolve()
}