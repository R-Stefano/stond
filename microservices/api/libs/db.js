const Sequelize = require('sequelize')
const configs = require('../configs')

const dbModelsPath = "../db-models/"
const compositeModel = "composite/"

const sequelize = new Sequelize(configs.sql.database, configs.sql.username, configs.sql.password, {
    host: configs.sql.host,
    dialect: 'mysql',
    define: {
        freezeTableName: true
    },
    logging: false,
    dialectOptions: { 
        socketPath: configs.sql.connection_name,
      }
});

const db = {};

db.Sequelize = Sequelize;
db.sequelize = sequelize;

/*
 * COMPOSITE
 */

//db.user_role = require(dbModelsPath + compositeModel + "user_role.js")(sequelize, Sequelize);

/* STANDARD MODELS */
db.device = require(dbModelsPath + "Device.js")(sequelize, Sequelize)
db.sensor = require(dbModelsPath + "Sensor.js")(sequelize, Sequelize)
db.sensorReading = require(dbModelsPath + "SensorReading.js")(sequelize, Sequelize)
db.actuator = require(dbModelsPath + "Actuator.js")(sequelize, Sequelize)

//db.device.belongsToMany(db.role, {as: 'roles', through: 'user_role', foreignKey: 'userID', otherKey: 'roleID'})
db.sensor.hasMany(db.sensorReading, {as: 'readings', sourceKey: 'Id', targetKey: 'sensorId'})
//db.permission.belongsTo(db.resource, {as: 'resource', sourceKey: 'resourceID', targetKey: 'ID'})
module.exports = db
