module.exports = (sequelize, Sequelize) => {
    return sequelize.define("component", {
        id:                      {type: Sequelize.BIGINT,               allowNull: false, primaryKey: true, autoIncrement: true},
        deviceId:                {type: Sequelize.UUID,                 allowNull: false},
        type:                    {type: Sequelize.STRING(100),          allowNull: false},
        name:                    {type: Sequelize.STRING(100),          allowNull: false},
        isWorking:               {type: Sequelize.BOOLEAN,              allowNull: false},
        status:                  {type: Sequelize.STRING(10),           allowNull: true},// on, off or null if not working
        value:                   {type: Sequelize.STRING(100),           allowNull: true}, //anything: number, string etc.. or null if not working
        valueType:               {type: Sequelize.STRING(10),           allowNull: false}, //define the datatype of value string, float, boolean
    });
};
