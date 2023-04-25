module.exports = (sequelize, Sequelize) => {
    return sequelize.define("device", {
        id:                             {type: Sequelize.UUID,         allowNull: false, primaryKey: true, defaultValue: Sequelize.UUIDV4},
        lastSnapshotReceivedAt:         {type: Sequelize.DATE,  allowNull: true}, //keep track last time received data from device

    });
};
