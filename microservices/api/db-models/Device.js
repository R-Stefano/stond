module.exports = (sequelize, Sequelize) => {
    return sequelize.define("device", {
        ID:                   {type: Sequelize.UUID,      allowNull: false, primaryKey: true, defaultValue: Sequelize.UUIDV4},
        activatedAt:          {type: Sequelize.DATE,          allowNull: false},
        ventilationStatus:    {type: Sequelize.STRING(10),    allowNull: false},
    });
};
