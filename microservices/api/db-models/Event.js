module.exports = (sequelize, Sequelize) => {
    return sequelize.define("event", {
        ID:                   {type: Sequelize.UUID,      allowNull: false, primaryKey: true, defaultValue: Sequelize.UUIDV4},
        type:                 {type: Sequelize.STRING(100),    allowNull: false},
        name:                 {type: Sequelize.STRING(100),    allowNull: false},
        value:                 {type: Sequelize.STRING(100),    allowNull: false},
    });
};
