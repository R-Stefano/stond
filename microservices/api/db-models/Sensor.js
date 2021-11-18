module.exports = (sequelize, Sequelize) => {
    return sequelize.define("sensor", {
        Id:             {type: Sequelize.UUID,      allowNull: false, primaryKey: true, defaultValue: Sequelize.UUIDV4},
        name:           {type: Sequelize.STRING(100),          allowNull: false},
        deviceId:       {type: Sequelize.UUID,       allowNull: false},
        currentValue:   {type: Sequelize.DECIMAL(6, 3),    allowNull: true},
        isWorking:      {type: Sequelize.BOOLEAN,    allowNull: false},
    });
};
