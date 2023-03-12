module.exports = (sequelize, Sequelize) => {
    return sequelize.define("reading", {
        id:              {type: Sequelize.BIGINT,               allowNull: false, primaryKey: true, autoIncrement: true},
        componentId:     {type: Sequelize.BIGINT,                 allowNull: false},
        timestamp:       {type: Sequelize.DATE,                 allowNull: false},
        isWorking:       {type: Sequelize.BOOLEAN,              allowNull: false},
        status:          {type: Sequelize.STRING(10),           allowNull: true},// on, off or null if not working
        value:           {type: Sequelize.STRING(100),           allowNull: true}, //anything: number, string etc.. or null if not working
    });
};
