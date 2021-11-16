module.exports = (sequelize, Sequelize) => {
    return sequelize.define("actuator", {
        Id:                      {type: Sequelize.UUID,                 allowNull: false, primaryKey: true, defaultValue: Sequelize.UUIDV4},
        name:                    {type: Sequelize.STRING(100),          allowNull: false},
        deviceId:                {type: Sequelize.UUID,                 allowNull: false},
        status:                  {type: Sequelize.STRING(10),              allowNull: true},
        statusChangedAt:         {type: Sequelize.DATE,                 allowNull: false},
        isWorking:               {type: Sequelize.BOOLEAN,              allowNull: false},
    });
};
