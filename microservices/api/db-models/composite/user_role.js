module.exports = (sequelize, Sequelize) => {
    return sequelize.define("user_role", {
        ID: {type: Sequelize.BIGINT,      allowNull: false, primaryKey: true, autoIncrement: true},
        roleID: {type: Sequelize.BIGINT, allowNull: false},
        userID: {type: Sequelize.BIGINT, allowNull: false}
    });
};
