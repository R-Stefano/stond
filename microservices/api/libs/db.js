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
db.component = require(dbModelsPath + "Component.js")(sequelize, Sequelize)
db.reading = require(dbModelsPath + "Reading.js")(sequelize, Sequelize)

db.device.hasMany(db.component, {as: 'components', sourceKey: 'id', targetKey: 'deviceId'})
db.component.hasMany(db.reading, {as: 'readings', sourceKey: 'id', targetKey: 'componentId'})

module.exports = db
