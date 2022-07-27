module.exports = (sequelize, Sequelize) => {
    return sequelize.define("sensorReading", {
        Id:              {type: Sequelize.UUID,                 allowNull: false, primaryKey: true, defaultValue: Sequelize.UUIDV4},
        sensorId:        {type: Sequelize.UUID,                 allowNull: false},
        timestamp:       {type: Sequelize.DATE,                 allowNull: false},
        value:           {type: Sequelize.DECIMAL(6, 3),        allowNull: true},
        filename:        {type: Sequelize.STRING(100),          allowNull: true},
        isWorking:       {type: Sequelize.BOOLEAN,              allowNull: false},
    });
};
