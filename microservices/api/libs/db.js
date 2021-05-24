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
//db.user = require(dbModelsPath + "User.js")(sequelize, Sequelize)


//db.user.belongsToMany(db.role, {as: 'roles', through: 'user_role', foreignKey: 'userID', otherKey: 'roleID'})
//db.role.hasMany(db.permission, {as: 'permissions', sourceKey: 'ID', targetKey: 'roleID'})
//db.permission.belongsTo(db.resource, {as: 'resource', sourceKey: 'resourceID', targetKey: 'ID'})
module.exports = db
