module.exports = (sequelize, Sequelize) => {
    return sequelize.define("user", {
        ID: {type: Sequelize.BIGINT,      allowNull: false, primaryKey: true, autoIncrement: true},
        companyBranchID: {type: Sequelize.BIGINT, allowNull: false},
        email: {type: Sequelize.STRING(200), allowNull: false},
        name: {type: Sequelize.STRING(200), allowNull: false},
        surname: {type: Sequelize.STRING(200), allowNull: false},
        password: {type: Sequelize.STRING(200), allowNull: false},
        activatedAt:{type: Sequelize.DATE,   allowNull: true, defaultValue: null},
    });
};
